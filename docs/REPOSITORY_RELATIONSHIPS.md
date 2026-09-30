# Repository relationships for `agent-pontifex`

This file is rendered from `repository-relationships.json`. The JSON registry is authoritative.

- Audience: `public`
- Repositories represented: **21**
- Relationships represented: **27**
- Inventory digest: `sha256:023b431cb965999339d899e24f3963b2f6389eb37afd4041ff4fccf1badda95f`

## Repositories

| Repository | Visibility | Roles | Archived |
|---|---|---|---|
| `agent-pontifex/.github` | `public` | `community-health`, `governance`, `relationship-registry` | no |
| `agent-pontifex/agent-pontifex-api-server.rs` | `public` | `api-server` | no |
| `agent-pontifex/agent-pontifex-cli` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-clients` | `public` | `clients` | no |
| `agent-pontifex/agent-pontifex-daemon.rs` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-desktop-app.rs` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-flutter` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-infra` | `public` | `infrastructure` | no |
| `agent-pontifex/agent-pontifex-interfaces` | `public` | `interfaces` | no |
| `agent-pontifex/agent-pontifex-lambdas` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-lib-core` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-mcp-server.rs` | `public` | `mcp-server` | no |
| `agent-pontifex/agent-pontifex-monorepo` | `public` | `monorepo` | no |
| `agent-pontifex/agent-pontifex-orm-core` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-pub-lib-core` | `public` | `repository` | no |
| `agent-pontifex/agent-pontifex-sync` | `public` | `sync` | no |
| `agent-pontifex/agent-pontifex-web-server.rs` | `public` | `web-server` | no |
| `agent-pontifex/agent-pontifex.github.io` | `public` | `documentation-site` | no |
| `agent-pontifex/agent-sdk.rs` | `public` | `sdk` | no |
| `agent-pontifex/ai-agent-bridge.rs` | `public` | `repository` | no |
| `agent-pontifex/ai-agent-coordinator.rs` | `public` | `repository` | no |

## Relationships

| From | Type | To | Status | Required |
|---|---|---|---|---|
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-api-server.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-cli` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-clients` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-daemon.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-desktop-app.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-flutter` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-infra` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-interfaces` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-lambdas` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-lib-core` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-mcp-server.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-monorepo` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-orm-core` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-pub-lib-core` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-sync` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex-web-server.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-pontifex.github.io` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/agent-sdk.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-bridge.rs` | `declared` | yes |
| `agent-pontifex/.github` | `governs` | `agent-pontifex/ai-agent-coordinator.rs` | `declared` | yes |
| `agent-pontifex/agent-pontifex-api-server.rs` | `depends_on` | `agent-pontifex/agent-pontifex-interfaces` | `inferred` | no |
| `agent-pontifex/agent-pontifex-clients` | `depends_on` | `agent-pontifex/agent-pontifex-interfaces` | `inferred` | no |
| `agent-pontifex/agent-pontifex-infra` | `deploys` | `agent-pontifex/agent-pontifex-monorepo` | `inferred` | no |
| `agent-pontifex/agent-pontifex-mcp-server.rs` | `depends_on` | `agent-pontifex/agent-pontifex-interfaces` | `inferred` | no |
| `agent-pontifex/agent-pontifex-sync` | `depends_on` | `agent-pontifex/agent-pontifex-interfaces` | `inferred` | no |
| `agent-pontifex/agent-pontifex-web-server.rs` | `depends_on` | `agent-pontifex/agent-pontifex-interfaces` | `inferred` | no |
| `agent-pontifex/agent-pontifex.github.io` | `documents` | `agent-pontifex/.github` | `inferred` | no |

## Editing relationships

Put reviewed public declarations in `repository-relationships.manual.json`; do not edit the generated registry directly.
Private repository names and private-only relationships belong in the private `approved-private-registry` mirror.
Inferred edges are advisory and must remain visibly labeled until reviewed.
