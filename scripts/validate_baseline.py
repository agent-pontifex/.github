#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
REQUIRED = [
    'README.md', 'profile/README.md', 'ORG_CONTEXT.md', 'agents.md', 'AGENTS.md',
    'CONTRIBUTING.md', 'SECURITY.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md',
    'GOVERNANCE.md', '.github/pull_request_template.md',
    '.github/copilot-instructions.md', '.github/dependabot.yml',
    '.github/ISSUE_TEMPLATE/bug_report.yml',
    '.github/ISSUE_TEMPLATE/feature_request.yml',
    '.github/ISSUE_TEMPLATE/config.yml',
    '.github/workflows/baseline-policy.yml',
    '.github/workflows/reusable-policy.yml',
    '.github/workflows/repository-relationships.yml',
    'repository-relationships.json',
    'repository-relationships.manual.json',
    'repository-relationships.schema.json',
    'repository-relationships.manual.schema.json',
    'docs/REPOSITORY_RELATIONSHIPS.md',
    'scripts/repository_relationships_lib.py',
    'scripts/validate_repository_relationships.py',
    'architecture/INTEROPERABILITY_CONTRACT.md',
    'architecture/REPOSITORY_RELATIONSHIPS.md',
    'architecture/repository-relationships.json',
    'architecture/repository-relationships.schema.json',
]
PHRASES = [
    'avoid git rebase in favor of git merge',
    'git stash', 'git reset', 'git clean', 'git filter-repo',
    '3–10 relevant commits', 'Never report',
]
SECRET_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'(?i)authorization:\s*bearer\s+[A-Za-z0-9._-]{16,}'),
]


def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)


def environment_tree(path: Path) -> str | None:
    parts = path.parts
    for index in range(len(parts) - 1):
        if parts[index:index + 2] == ('env', 'enc'):
            return 'enc'
        if parts[index:index + 2] == ('env', 'dec'):
            return 'dec'
    return None


def environment_file_error(path: Path, contents: str) -> str | None:
    tree = environment_tree(path)
    if tree == 'dec' and path.name.endswith('.env'):
        return f'decrypted environment file is tracked: {path}'
    if tree != 'enc':
        return None
    if not path.name.endswith('.env.enc'):
        return f'non-ciphertext file is tracked under env/enc: {path}'
    if 'ENC[' not in contents or 'sops_' not in contents:
        return f'environment ciphertext lacks SOPS markers: {path}'
    return None


missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
if missing:
    fail('missing required files: ' + ', '.join(missing))

agents = (ROOT / 'agents.md').read_text(encoding='utf-8')
if agents != (ROOT / 'AGENTS.md').read_text(encoding='utf-8'):
    fail('AGENTS.md compatibility mirror differs from agents.md')
for phrase in PHRASES:
    if phrase not in agents:
        fail(f'agents.md missing required phrase: {phrase!r}')

for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    if re.search(r'\{\{[A-Z][A-Z0-9_]*\}\}', text):
        fail(f'unrendered placeholder in {path.relative_to(ROOT)}')
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f'possible credential in {path.relative_to(ROOT)}')
    if text and not text.endswith('\n'):
        fail(f'missing final newline: {path.relative_to(ROOT)}')

tracked = subprocess.run(
    ['git', 'ls-files', '-z'],
    cwd=ROOT,
    check=True,
    stdout=subprocess.PIPE,
).stdout.split(b'\0')
for raw_path in tracked:
    if not raw_path:
        continue
    relative = Path(raw_path.decode())
    contents = ''
    if environment_tree(relative) == 'enc':
        contents = (ROOT / relative).read_text(encoding='utf-8')
    if error := environment_file_error(relative, contents):
        fail(error)

architecture_registry = json.loads(
    (ROOT / 'architecture/repository-relationships.json').read_text(encoding='utf-8')
)
interoperability = architecture_registry.get('interoperability_policy', {})
if interoperability.get('contract') != 'architecture/INTEROPERABILITY_CONTRACT.md':
    fail('architecture interoperability policy points to the wrong contract')
expected_authorities = {
    'protocol_authority': 'agent-pontifex/agent-sdk.rs',
    'repository_write_authority': 'platform://fiducia-cloud',
    'human_identity_authority': 'platform://shared-auth',
    'machine_identity_authority': 'platform://fiducia-cloud',
    'package_and_artifact_authority': 'platform://zed-pkg',
    'secret_encryption_authority': 'platform://sops',
}
for field, expected in expected_authorities.items():
    if interoperability.get(field) != expected:
        fail(f'architecture interoperability policy has invalid {field}')

human_policy = interoperability.get('human_identity_constraints', {})
if human_policy.get('authorization_owner') != 'product-local':
    fail('human authorization must remain product-local')
if human_policy.get('caller_bearer_as_downstream_authorization') != 'forbidden':
    fail('caller bearer must not become downstream authorization')
if human_policy.get('jwt_verification') != 'local verification with pinned issuer, audience, and JWKS policy':
    fail('Shared Auth JWT verification policy is not fail-closed and local')
introspection_policy = human_policy.get('introspection', {})
if introspection_policy.get('raw_token_role') != 'inspected-data-only':
    fail('Shared Auth introspection must treat a raw token only as inspected data')
if introspection_policy.get('service_credential') != 'required-and-separate':
    fail('Shared Auth introspection must use a separate service credential')

write_policy = interoperability.get('repository_write_constraints', {})
if write_policy.get('canonical_repository_format') != 'owner/repo':
    fail('repository write authority must use canonical owner/repo scope')
if write_policy.get('lease_scope') != 'complete-atomic-normalized-path-set':
    fail('repository write leases must cover the complete atomic path set')
fencing_policy = write_policy.get('fencing_token', {})
if fencing_policy.get('minimum') != 1 or fencing_policy.get('maximum') != 9007199254740991:
    fail('repository write fencing token range is not cross-runtime safe')
if fencing_policy.get('required_on_protected_write') is not True:
    fail('protected repository writes must require a fencing token')

secret_policy = interoperability.get('secret_materialization_policy', {})
if (
    secret_policy.get('encrypted_files')
    != 'only SOPS-encrypted env/enc/*.env.enc files may be tracked'
):
    fail('architecture interoperability policy has invalid encrypted environment path')
if secret_policy.get('decrypted_files') != 'env/dec/*.env must be ignored and untracked':
    fail('architecture interoperability policy has invalid decrypted environment path')
if secret_policy.get('nix_store_plaintext') != 'forbidden':
    fail('plaintext environment material must not enter the Nix store')

architecture_schema = json.loads(
    (ROOT / 'architecture/repository-relationships.schema.json').read_text(encoding='utf-8')
)
if architecture_schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
    fail('architecture repository relationship schema must use JSON Schema draft 2020-12')
if 'interoperability_policy' not in architecture_schema.get('required', []):
    fail('architecture schema does not require the interoperability policy')

relationship_edges = {
    (edge.get('from'), edge.get('kind'), edge.get('to'))
    for edge in architecture_registry.get('relationships', [])
}
required_edges = {
    ('agent-pontifex/agent-sdk.rs', 'protocol_authority_for', 'agent-pontifex/ai-agent-bridge.rs'),
    ('agent-pontifex/agent-sdk.rs', 'protocol_authority_for', 'agent-pontifex/ai-agent-coordinator.rs'),
    ('organization://agent-pontifex', 'repository_writes_fenced_by', 'platform://fiducia-cloud'),
    ('organization://agent-pontifex', 'human_identity_via', 'platform://shared-auth'),
    ('organization://agent-pontifex', 'workload_identity_via', 'platform://fiducia-cloud'),
    ('organization://agent-pontifex', 'packaged_via', 'platform://zed-pkg'),
    ('organization://agent-pontifex', 'environment_secrets_encrypted_via', 'platform://sops'),
}
if missing_edges := required_edges - relationship_edges:
    fail(f'architecture interoperability relationships are missing: {sorted(missing_edges)}')
architecture_markdown = (
    ROOT / 'architecture/REPOSITORY_RELATIONSHIPS.md'
).read_text(encoding='utf-8')
expected_edge_count = f'- Relationship edges: **{len(architecture_registry.get("relationships", []))}**'
if expected_edge_count not in architecture_markdown:
    fail('architecture relationship documentation edge count differs from JSON')

workflow_paths = list((ROOT / '.github/workflows').glob('*.y*ml'))
workflow_paths += list((ROOT / 'workflow-templates').glob('*.y*ml'))
for path in workflow_paths:
    text = path.read_text(encoding='utf-8')
    if 'permissions:' not in text:
        fail(f'workflow lacks explicit permissions: {path.relative_to(ROOT)}')
    if 'timeout-minutes:' not in text:
        fail(f'workflow lacks timeout: {path.relative_to(ROOT)}')
    for number, line in enumerate(text.splitlines(), 1):
        match = re.search(r'^\\s*(?:-\\s+)?uses:\\s*([^\\s#]+)', line)
        if not match:
            continue
        ref = match.group(1)
        if ref.startswith('./'):
            continue
        if ref.startswith('docker://'):
            if not re.search(r'@sha256:[0-9a-fA-F]{64}$', ref):
                fail(f'external Docker action is not digest-pinned: {path.relative_to(ROOT)}:{number}: {ref}')
            continue
        if not re.search(r'@[0-9a-fA-F]{40}$', ref):
            fail(f'external Action is not pinned to a full SHA: {path.relative_to(ROOT)}:{number}: {ref}')
    if 'actions/checkout@' in text and 'persist-credentials: false' not in text:
        fail(f'checkout credentials persist in {path.relative_to(ROOT)}')

relationship_check = subprocess.run(
    [sys.executable, str(ROOT / 'scripts/validate_repository_relationships.py'), str(ROOT)],
    text=True, capture_output=True, check=False,
)
if relationship_check.returncode != 0:
    fail('relationship registry validation failed: ' + (relationship_check.stderr or relationship_check.stdout).strip())

print(f'PASS: validated {ROOT}')
