# Agent Pontifex — repository architecture

Canonical prefix for this org is the **full org name**: `agent-pontifex-*`.
Do not introduce an abbreviated prefix (`apx-`, `pontifex-`). `agent-pontifex-docs` and
`agent-pontifex.github.io` already establish the full-name form, and a second spelling
creates two homes for one family — the DEN-3048 defect (`apme-`/`apostille-me-`,
`evgl-`/`evento-globolo-`, `hhm-`/`hacker-house-medellin-`).

## Contract layer

| Repo | Role |
|---|---|
| `agent-pontifex-interfaces` | **Declares** the shared contract in TypeSpec + JSON Schema as two co-equal, independently authored authorities. Exports SDK/lib types for 15+ languages. Linting enforces the contract across languages. |
| `agent-pontifex-lib-core` | **Implements** what `-interfaces` declares, also driven by TypeSpec + JSON Schema. Internal. |
| `agent-pontifex-pub-lib-core` | Public core-library surface, split out of `-lib-core`. |
| `agent-pontifex-orm-core` | All ORM code. Consumed by every server **and** by `-lib-core`. Primary ORMs: **Diesel and SeaORM** (code-first SeaORM cross-checked against db-first Diesel). |

**Shared runtime config** lives as a module in `-lib-core` and `-pub-lib-core`;
`flags-2-env` assigns its values at runtime.

The Rust wire contract already lives in `agent-sdk.rs/agent-pontifex-protocol`. It is
deliberately **not** duplicated into `-interfaces`; that repo is the language-neutral
authority and the Rust crate is a consumer. Revisit only as a deliberate move, never as a copy.

## Servers

All four use **github.com/shared-auth**, **github.com/ores-rate-limit**, and
**github.com/oresoftware/ores-middleware**. No exceptions.

| Repo | Notes |
|---|---|
| `agent-pontifex-web-server.rs` | MASH (maud, axum, supabase, seaorm, htmx) + Leptos/Dioxus islands |
| `agent-pontifex-api-server.rs` | JSON API, SeaORM |
| `agent-pontifex-admin-api-server.rs` | **Separate VPC** from web/api. Write access to the admin RDS. |
| `agent-pontifex-admin-web-server.rs` | **Separate VPC.** Super-admins only, no public ingress. |

Web↔API must support all four avenues: direct read-only DB via ORM, stateless HTTP,
stateful TCP, and async NATS/MQ.
## Clients and apps

| Repo | Notes |
|---|---|
| `agent-pontifex-clients` | **Public** clients, 15+ languages. Primary: **Rust, TypeScript, Dart/Flutter, Gleam.** |
| `agent-pontifex-cli` | Rust. **Must use flags-2-env** at the argv boundary; imports `-clients` via zed-pkg. |
| `agent-pontifex-flutter` | iOS, Android, mobile web **and** desktop. |
| `agent-pontifex-desktop-app.rs` | Rust desktop app using FFI. **Deliberately competes** with the Flutter desktop app — they are rivals, not layers. No webviews, no React. |
| `agent-pontifex-daemon.rs` | Cross-platform Rust background service: systemd, launchd, Windows services. |
| `agent-pontifex-mcp-server.rs` | Borrow concepts from the MCP servers already across our orgs; inherit the ORESoftware MCP base. |

## Data, infra, delivery

| Repo | Notes |
|---|---|
| `agent-pontifex-sync` | Uses **opto-sync** for full-stack sync across SQLite on clients, Postgres, Supabase, NeonDB, and IndexedDB in the browser. |
| `agent-pontifex-lambdas` | Cross-platform lambda workers for heavier, less frequent ops — image manipulation/processing. |
| `agent-pontifex-infra` | Cloudflare Workers config and k8s manifests; `supabase/` and `neon/` IaC folders live here. |
| `agent-pontifex-monorepo` | App-of-apps. **`apps/` contains every deployable as a git submodule.** Push each submodule before bumping its pin. |
| `agent-pontifex-docs` | Internal/external/legal docs. Already existed. |

## Naming exception, unresolved

`agent-sdk.rs`, `ai-agent-bridge.rs` and `ai-agent-coordinator.rs` carry **no org prefix**.
That is a third naming scheme in one org. They are public with MIT and topics, so renaming
is a product decision — but it should be made, not left to drift.
