# `agent-pontifex` repository relationships

Generated from reviewed policy and the current **public** repository inventory.

- Public repositories declared: **4**
- Private repository names withheld: **0**
- Relationship edges: **10**

## Repository roles

| Repository | Role | Lifecycle |
|---|---|---|
| [`.github`](https://github.com/agent-pontifex/.github) | `organization_governance` | `active` |
| [`agent-sdk.rs`](https://github.com/agent-pontifex/agent-sdk.rs) | `client_sdk` | `active` |
| [`ai-agent-bridge.rs`](https://github.com/agent-pontifex/ai-agent-bridge.rs) | `library` | `active` |
| [`ai-agent-coordinator.rs`](https://github.com/agent-pontifex/ai-agent-coordinator.rs) | `library` | `active` |

## Declared edges

| From | Relationship | To | Status/basis |
|---|---|---|---|
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-sdk.rs` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-bridge.rs` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-coordinator.rs` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |
| `agent-pontifex/agent-sdk.rs` | `protocol_authority_for` | `agent-pontifex/ai-agent-bridge.rs` | `required` / `interop-contract`: the SDK owns versioned bridge protocol contracts and conformance fixtures |
| `agent-pontifex/agent-sdk.rs` | `protocol_authority_for` | `agent-pontifex/ai-agent-coordinator.rs` | `required` / `interop-contract`: the SDK owns versioned coordinator protocol contracts and conformance fixtures |
| `organization://agent-pontifex` | `repository_writes_fenced_by` | `platform://fiducia-cloud` | `platform-default` / `interop-contract`: Fiducia owns external repository/path-set lease authority and current fencing tokens |
| `organization://agent-pontifex` | `human_identity_via` | `platform://shared-auth` | `platform-default` / `interop-contract`: Shared Auth authenticates humans/operators; caller bearers never become downstream authorization and introspection uses separate service credentials |
| `organization://agent-pontifex` | `workload_identity_via` | `platform://fiducia-cloud` | `platform-default` / `interop-contract`: Fiducia owns workload identity where its coordination contract applies; scoped agent credentials remain distinct from human identity |
| `organization://agent-pontifex` | `packaged_via` | `platform://zed-pkg` | `platform-default` / `platform-policy`: Zed resolves artifacts while submodules compose editable source |
| `organization://agent-pontifex` | `environment_secrets_encrypted_via` | `platform://sops` | `platform-default` / `interop-contract`: only SOPS ciphertext at env/enc/*.env.enc is trackable; env/dec/*.env remains local plaintext |

## Interoperability authorities

[`architecture/INTEROPERABILITY_CONTRACT.md`](INTEROPERABILITY_CONTRACT.md) is
normative for public integrations:

- `agent-pontifex/agent-sdk.rs` is the canonical Agent Pontifex protocol
  authority. Bridges and coordinators consume its versioned contracts and
  conformance fixtures rather than creating parallel wire contracts.
- `platform://fiducia-cloud` is the external lease and fencing authority for
  protected repository writes. Exact canonical `owner/repo` and atomic path-set
  scope, holder, expiry, and a current positive fencing token are required;
  invalid authority fails closed.
- `platform://shared-auth` authenticates humans/operators only. Product
  authorization remains local, while machine/workload identity remains with
  Fiducia and scoped Agent Pontifex credentials. JWTs are verified locally
  against pinned issuer, audience, and JWKS policy. Raw bearer tokens are never
  propagated as agent, adapter, tool, or downstream service credentials; the
  only permitted raw-token transmission is authenticated Shared Auth
  introspection, where the token is inspected data and not authorization.
- `platform://zed-pkg` owns package and artifact resolution; production uses
  immutable signed artifacts or image digests.
- `platform://sops` owns repository environment encryption. Only SOPS-encrypted
  `env/enc/*.env.enc` files may be tracked. Decrypted `env/dec/*.env` files
  remain ignored and untracked and are materialized only through reviewed
  `just`, SOPS-aware Nix activation outside the Nix store, or runtime
  secret-provider paths; plaintext tokens are forbidden in the Nix store and
  build outputs as well as source.

## Composition, service, and observability contract

Git submodules compose editable source; Zed packages resolve packages/artifacts; dual-managed commits must match. Production deploys immutable image digests, not runtime source builds. Cross-service access uses APIs/SDKs/events rather than another service database. MCP uses the product API/SDK. Services emit OpenTelemetry traces, bounded metrics, and correlated structured logs.

## Privacy boundary

This public registry deliberately omits private repository names and edges; the count above makes the boundary explicit.
