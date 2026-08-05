<!-- ore-org-baseline:begin -->
# Repository relationships for `agent-pontifex`

This file is rendered from `repository-relationships.json`. The JSON registry is authoritative.

- Audience: `public`
- Repositories represented: **4**
- Relationships represented: **3**
- Inventory digest: `sha256:dde78cc0c7c9a36588105a3b95f27ad203780fc9fd55b1e71a0b5d584037321b`

## Immutable routing identity

| Field | Value |
|---|---|
| Mapping ID | `context:agent-pontifex` |
| GitHub owner ID | `313080782` |
| Linear project ID | `71806431-748e-4332-b03a-820079d61ec0` |
| Linear team ID | `eb8ab169-5afe-4b6f-9cab-3f2aa3e887dc` |

## Repositories

| Repository | Visibility | Roles | Archived |
|---|---|---|---|
| `agent-pontifex/.github` | `public` | `community-health`, `governance`, `relationship-registry` | no |
| `agent-pontifex/agent-sdk.rs` | `public` | `sdk` | no |
| `agent-pontifex/ai-agent-bridge.rs` | `public` | `repository` | no |
| `agent-pontifex/ai-agent-coordinator.rs` | `public` | `repository` | no |

## Relationships

| From | Type | To | Status | Required |
|---|---|---|---|---|
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-sdk.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-bridge.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-coordinator.rs` | `declared` | yes |

## Editing relationships

Put reviewed public declarations in `repository-relationships.manual.json`; do not edit the generated registry directly.
Private repository names and private-only relationships belong in the private `approved-private-registry` mirror.
Inferred edges are advisory and must remain visibly labeled until reviewed.
<!-- ore-org-baseline:end -->
