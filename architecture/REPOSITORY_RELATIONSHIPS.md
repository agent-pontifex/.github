# `agent-pontifex` repository relationships

Generated from reviewed policy and the current **public** repository inventory.

- Public repositories declared: **4**
- Private repository names withheld: **0**
- Relationship edges: **4**

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
| `organization://agent-pontifex` | `packaged_via` | `platform://zed-pkg` | `platform-default` / `platform-policy`: Zed resolves artifacts while submodules compose editable source |

## Composition, service, and observability contract

Git submodules compose editable source; Zed packages resolve packages/artifacts; dual-managed commits must match. Production deploys immutable image digests, not runtime source builds. Cross-service access uses APIs/SDKs/events rather than another service database. MCP uses the product API/SDK. Services emit OpenTelemetry traces, bounded metrics, and correlated structured logs.

## Privacy boundary

This public registry deliberately omits private repository names and edges; the count above makes the boundary explicit.
