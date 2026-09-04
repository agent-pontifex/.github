# Agent Pontifex — repository-family contract

Canonical prefix for this org is the **full org name**: `agent-pontifex-*`.
Do not introduce an abbreviated prefix (`apx-`, `pontifex-`). The public
`agent-pontifex.github.io` repository establishes the full-name form, and a second spelling
creates two homes for one family — the DEN-3048 defect (`apme-`/`apostille-me-`,
`evgl-`/`evento-globolo-`, `hhm-`/`hacker-house-medellin-`).

## Contract layer

| Repo | Role |
|---|---|
| `agent-pontifex-interfaces` | **Declares** the shared contract in TypeSpec + JSON Schema as two co-equal, independently authored authorities. The target external SDK surface is 15+ languages, with Rust, TypeScript, Dart/Flutter, and Gleam as the primary lanes. Linting and conformance fixtures enforce the contract across languages. |
| `agent-pontifex-lib-core` | **Implements** what `-interfaces` declares, also driven by TypeSpec + JSON Schema. Internal. |
| `agent-pontifex-pub-lib-core` | Public core-library surface, split out of `-lib-core`. |
| `agent-pontifex-orm-core` | All backend-only ORM code. Consumed by servers and by the server-side portion of `-lib-core`. Independently derived Diesel code-first and SeaORM database-first representations must converge with the TypeSpec- and JSON-Schema-derived catalogs before release. |

**Shared runtime config** lives as a module in `-lib-core` and `-pub-lib-core`;
`flags-2-env` assigns its values at runtime.

The Rust wire contract already lives in `agent-sdk.rs/agent-pontifex-protocol`. It is
deliberately **not** duplicated into `-interfaces`; that repo is the language-neutral
authority and the Rust crate is a consumer. Revisit only as a deliberate move, never as a copy.

## Server roles

All four use **github.com/shared-auth**, **github.com/ores-rate-limit**, and
**github.com/oresoftware/ores-middleware**. No exceptions.

The public governance repository documents role contracts, not the names or
inventory of private repositories. Concrete private topology belongs in the
private documentation repository.

| Pattern | Notes |
|---|---|
| `*-web-server.rs` | MASH (maud, axum, Supabase, SeaORM, htmx) plus Leptos/Dioxus islands |
| `*-api-server.rs` | Product JSON API with product-local authorization |
| `*-admin-api-server.rs` | **Separate admin VPC** from product web/API; write access only to the admin data plane |
| `*-admin-web-server.rs` | **Separate admin VPC**; super-admins only and no public ingress |

Web↔API must support all four avenues: direct read-only DB via ORM, stateless HTTP,
stateful TCP, and async NATS/MQ.
## Clients and apps

| Repo | Notes |
|---|---|
| `agent-pontifex-clients` | **Public** clients, 15+ languages. Primary: **Rust, TypeScript, Dart/Flutter, Gleam.** |
| `agent-pontifex-cli` | Rust. **Must use flags-2-env** at the argv boundary; imports `-clients` via zed-pkg. |
| `agent-pontifex-flutter` | iOS, Android, mobile web **and** desktop. |
| `agent-pontifex-desktop-app.rs` | Rust desktop app using FFI. **Deliberately competes** with the Flutter desktop app — they are rivals, not layers. No webviews, no React. |
| `agent-pontifex-daemon.rs` | Public cross-platform Rust worker runtime: systemd, launchd, and Windows services. Specialized private supervisors must have a non-overlapping responsibility and are not inventoried here. |
| `agent-pontifex-mcp-server.rs` | Borrow concepts from the MCP servers already across our orgs; inherit the ORESoftware MCP base. |

## Data, infra, delivery

| Repo | Notes |
|---|---|
| `agent-pontifex-sync` | Uses **opto-sync** for full-stack sync across SQLite on clients, Postgres, Supabase, NeonDB, and IndexedDB in the browser. |
| `agent-pontifex-lambdas` | Cross-platform lambda workers for heavier, less frequent ops — image manipulation/processing. |
| `agent-pontifex-infra` | Cloudflare Workers config and k8s manifests; `supabase/` and `neon/` IaC folders live here. |
| `agent-pontifex-monorepo` | App-of-apps. **`apps/` contains every deployable as a git submodule.** Push each submodule before bumping its pin. |
| `*-docs` | Internal, external, operational, and legal documentation. Private repository names and topology are not published from this governance repository. |

## Naming exception, unresolved

`agent-sdk.rs`, `ai-agent-bridge.rs` and `ai-agent-coordinator.rs` carry **no org prefix**.
That is a third naming scheme in one org. They are public with MIT and topics, so renaming
is a product decision — but it should be made, not left to drift.

## Privacy and status

This file defines naming and ownership conventions. It is not a live repository
inventory and must not be used to infer the existence, visibility, or deployment
state of private repositories. The generated public inventory remains
`architecture/repository-relationships.json`; private inventory belongs only in
the private documentation authority.
