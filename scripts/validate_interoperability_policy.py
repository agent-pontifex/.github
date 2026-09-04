#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


required_files = [
    "AGENTS.md",
    "agents.md",
    "architecture/INTEROPERABILITY_CONTRACT.md",
    "architecture/REPOSITORY_RELATIONSHIPS.md",
    "architecture/repository-relationships.json",
    "architecture/repository-relationships.schema.json",
]
missing = [path for path in required_files if not (ROOT / path).is_file()]
if missing:
    fail("missing interoperability files: " + ", ".join(missing))

agents = (ROOT / "agents.md").read_text(encoding="utf-8")
if agents != (ROOT / "AGENTS.md").read_text(encoding="utf-8"):
    fail("AGENTS.md compatibility mirror differs from canonical agents.md")
for phrase in [
    "avoid git rebase in favor of git merge",
    "env/enc/*.env.enc",
    "env/dec/*.env",
    "outside the Nix store",
]:
    if phrase not in agents:
        fail(f"organization policy is missing interoperability phrase: {phrase!r}")

tracked = subprocess.run(
    ["git", "ls-files", "-z"],
    cwd=ROOT,
    check=True,
    stdout=subprocess.PIPE,
).stdout.split(b"\0")
for raw_path in tracked:
    if not raw_path:
        continue
    relative = Path(raw_path.decode("utf-8"))
    parts = relative.parts
    if len(parts) >= 3 and parts[0:2] == ("env", "dec") and relative.name.endswith(".env"):
        fail(f"decrypted environment file is tracked: {relative}")
    if len(parts) >= 3 and parts[0:2] == ("env", "enc"):
        if not relative.name.endswith(".env.enc"):
            fail(f"non-ciphertext file is tracked under env/enc: {relative}")
        contents = (ROOT / relative).read_text(encoding="utf-8")
        if "ENC[" not in contents or "sops_" not in contents:
            fail(f"environment ciphertext lacks SOPS markers: {relative}")

registry = json.loads(
    (ROOT / "architecture/repository-relationships.json").read_text(encoding="utf-8")
)
policy = registry.get("interoperability_policy")
if not isinstance(policy, dict):
    fail("repository registry lacks interoperability_policy")

expected_authorities = {
    "contract": "architecture/INTEROPERABILITY_CONTRACT.md",
    "protocol_authority": "agent-pontifex/agent-sdk.rs",
    "repository_write_authority": "platform://fiducia-cloud",
    "human_identity_authority": "platform://shared-auth",
    "machine_identity_authority": "platform://fiducia-cloud",
    "package_and_artifact_authority": "platform://zed-pkg",
    "secret_encryption_authority": "platform://sops",
}
for field, expected in expected_authorities.items():
    if policy.get(field) != expected:
        fail(f"invalid interoperability authority {field}: {policy.get(field)!r}")

human = policy.get("human_identity_constraints", {})
if human.get("authorization_owner") != "product-local":
    fail("human authorization must remain product-local")
if human.get("caller_bearer_as_downstream_authorization") != "forbidden":
    fail("caller bearer must not become downstream authorization")
if human.get("jwt_verification") != "local verification with pinned issuer, audience, and JWKS policy":
    fail("Shared Auth JWT verification policy is not local and fail closed")
introspection = human.get("introspection", {})
if introspection.get("raw_token_role") != "inspected-data-only":
    fail("Shared Auth introspection must treat the caller token as inspected data only")
if introspection.get("service_credential") != "required-and-separate":
    fail("Shared Auth introspection must use a separate service credential")

machine = policy.get("machine_credential_policy", {})
for field in ["audience_bound", "least_privilege", "short_lived"]:
    if machine.get(field) is not True:
        fail(f"machine credential policy must require {field}")
if machine.get("scope") != "selected-agent-and-tool":
    fail("machine credentials must be scoped to the selected agent and tool")

write = policy.get("repository_write_constraints", {})
if write.get("canonical_repository_format") != "owner/repo":
    fail("repository writes must use canonical owner/repo scope")
if write.get("lease_scope") != "complete-atomic-normalized-path-set":
    fail("repository write leases must cover the complete atomic path set")
fencing = write.get("fencing_token", {})
if fencing != {
    "maximum": 9_007_199_254_740_991,
    "minimum": 1,
    "required_on_protected_write": True,
}:
    fail("repository write fencing-token policy is not JSON-safe and fail closed")
required_failures = {
    "missing-authority",
    "partial-scope",
    "stale-token",
    "expired-lease",
    "mismatched-holder-or-scope",
}
if set(write.get("fail_closed_on", [])) != required_failures:
    fail("repository write failure set is incomplete")

secret = policy.get("secret_materialization_policy", {})
if secret.get("encrypted_files") != "only SOPS-encrypted env/enc/*.env.enc files may be tracked":
    fail("encrypted environment path policy is invalid")
if secret.get("decrypted_files") != "env/dec/*.env must be ignored and untracked":
    fail("decrypted environment path policy is invalid")
if secret.get("nix_store_plaintext") != "forbidden":
    fail("plaintext environment material must not enter the Nix store")
if secret.get("plaintext_tokens") != "forbidden":
    fail("plaintext token policy must fail closed")

schema = json.loads(
    (ROOT / "architecture/repository-relationships.schema.json").read_text(encoding="utf-8")
)
if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
    fail("relationship schema must use JSON Schema Draft 2020-12")
if "interoperability_policy" not in schema.get("required", []):
    fail("relationship schema does not require interoperability_policy")

edges = {
    (edge.get("from"), edge.get("kind"), edge.get("to"))
    for edge in registry.get("relationships", [])
}
required_edges = {
    ("agent-pontifex/agent-sdk.rs", "protocol_authority_for", "agent-pontifex/ai-agent-bridge.rs"),
    ("agent-pontifex/agent-sdk.rs", "protocol_authority_for", "agent-pontifex/ai-agent-coordinator.rs"),
    ("organization://agent-pontifex", "repository_writes_fenced_by", "platform://fiducia-cloud"),
    ("organization://agent-pontifex", "human_identity_via", "platform://shared-auth"),
    ("organization://agent-pontifex", "workload_identity_via", "platform://fiducia-cloud"),
    ("organization://agent-pontifex", "packaged_via", "platform://zed-pkg"),
    ("organization://agent-pontifex", "environment_secrets_encrypted_via", "platform://sops"),
}
missing_edges = required_edges - edges
if missing_edges:
    fail(f"missing interoperability edges: {sorted(missing_edges)}")

markdown = (ROOT / "architecture/REPOSITORY_RELATIONSHIPS.md").read_text(encoding="utf-8")
expected_count = f'- Relationship edges: **{len(registry.get("relationships", []))}**'
if expected_count not in markdown:
    fail("relationship documentation edge count differs from JSON")

contract = (ROOT / "architecture/INTEROPERABILITY_CONTRACT.md").read_text(encoding="utf-8")
for phrase in [
    "Status: **normative**",
    "A `tool_request`",
    "positive fencing token",
    "Never propagate the caller's raw bearer token",
    "env/enc/*.env.enc",
]:
    if phrase not in contract:
        fail(f"interoperability contract is missing required invariant: {phrase!r}")

print(f"PASS: validated Agent Pontifex interoperability policy in {ROOT}")
