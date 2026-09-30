# Agent Pontifex × ORES integration contract

This document defines how `agent-pontifex` consumes shared ORES capabilities without creating duplicate authorities or enabling unnecessary runtime capability.

## Core rule

Agent Pontifex owns product semantics: jobs, workers, leases, approvals, budgets, incidents, provider routing, agent discovery, agent messaging, repository ownership and handoff state.

Shared ORES repositories own reusable infrastructure/runtime concerns. Product repositories consume those capabilities through narrow adapters and pinned, reviewed revisions. An ORES dependency never becomes an authority for Agent Pontifex product data merely because it supplies transport, telemetry, middleware, secrets, local orchestration, background execution or generated bindings.

All integrations are **least-capability by surface**. A repository must not enable every fleet component merely because a config file or SDK exists.

## Authorities and shared capabilities

| Capability | Shared authority | Agent Pontifex ownership / boundary |
| --- | --- | --- |
| Product contracts | `agent-pontifex/ap-interfaces` | TypeSpec + JSON Schema are independent human-authored peer authorities for Agent Pontifex domain contracts. |
| Fleet-generic semantic primitives | `ORESoftware/ores-interfaces` | Import only generic admitted primitives. Product-specific job/lease/approval/provider contracts remain in `ap-interfaces`. |
| Contract parity | `ORESoftware/typespec-json-schema-validator` | Fail closed when authored TypeSpec and JSON Schema disagree. Generated evidence is never an editable authority. |
| WIT / Component Model | `ORESoftware/ores-wit` | WIT is a portable ABI/code-contract projection by default. It must remain traceable to admitted Agent Pontifex Contract IR and may not silently replace TypeSpec/JSON Schema authority. |
| Request middleware | `ORESoftware/ores-middleware` | Each HTTP server owns its exact middleware selection, order, route scope and provider revisions. No global one-size-fits-all chain. |
| Telemetry | `ores-otel/*`, especially `ores-otel/ores.otel.log` | Emit correlated structured logs/traces/metrics without secrets, raw prompts, repository source or unrestricted payloads. Applications own concrete exporters. |
| Secrets in Git / local activation | `ORESoftware/ores-sops` | Encrypt reviewed dotenv ciphertext at rest; never use it as runtime secret distribution, auth or logging. Plaintext remains ignored/local only. |
| Local mixed-runtime orchestration | `ORESoftware/ores-compose` | `ap-infra` owns the project topology; individual executable repos may carry a minimal root `.ores-compose.yaml` only when they are directly runnable units. |
| Browser/background workers | `ORESoftware/ores-sw.js` | Browser worker lifecycle, cross-tab coordination and bounded ephemeral browser job leases. Durable Agent Pontifex jobs remain server/native state. |
| Cross-device sync | `opto-sync/*` | Sync product state/envelopes where appropriate; do not make sync transport authoritative for server-side job leases. |
| Web/API transport | `ORESoftware/ores-transport` | Transport adapters only; product request/response semantics stay in `ap-interfaces`. |
| Locks / leases | `ORESoftware/ores-locks-and-leases` | `ap-lib-core` maps Agent Pontifex resource keys and fencing semantics onto the shared primitive. |
| Local/fleet packages | `zed-pkg/*` | Resolve pinned packages/artifacts; editable source composition and package identity must agree. |
| CLI argv/env contract | `flags-2-env/*` | Executables declare only flags they actually consume; secrets stay env/secret-store only. |

## Canonical repository responsibilities

### `ap-interfaces`

- Own Agent Pontifex TypeSpec + JSON Schema peer authorities.
- Import or reference `ORESoftware/ores-interfaces` only for genuinely fleet-generic primitives.
- Define product contracts for jobs, workers, leases, approvals, incidents, budgets, provider routing, discovery, messages, repository-path ownership and handoff state.
- Maintain an admitted WIT projection lane through TJSV + `ores-wit` for portable SDK/ABI semantics.
- Preserve canonical snake_case wire names and lowercase canonical HTTP header names; incoming HTTP header matching remains case-insensitive.

### `ap-lib-core`

- Be the server-side integration seam.
- Wrap `ores-locks-and-leases` with Agent Pontifex resource keys and fencing requirements.
- Expose narrow ports/adapters for telemetry, middleware provider decisions, secret/config lookup, sync observation and transport; executable repos should not duplicate product policy.
- Keep database/ORM state private behind the existing opaque boundary.

### HTTP servers (`ap-api-server.rs`, `ap-web-server.rs`, admin variants)

- Consume `ores-middleware` at the actual router boundary.
- Author and validate a service-specific middleware order; do not inherit a fleet default blindly.
- Propagate W3C `traceparent`/`baggage` plus bounded request IDs through `ores-otel`.
- Treat test auth bypass/fault injection as a production configuration error.
- Declare only required connectors and only the environment-variable *names* needed by those connectors; never commit values.

Recommended baseline order is conceptual, not mandatory: recovery/deadline -> correlation/trusted transport -> payload limits -> authentication -> principal-aware rate limits/authorization -> idempotency -> handler -> response policy/security headers -> telemetry completion. If the service chooses a different order, encode the dependency explicitly and test it.

### `ap-mcp-server.rs`

- Default to stdio and read-only diagnostics/tools.
- Do not enable HTTP authentication, public rate limiting, cloud SDKs or SaaS connectors merely because fleet configs exist.
- Any future network transport or mutating tool is an explicit capability change with auth, authorization, fencing and audit evidence.
- Missing credentials should remain per-tool capability errors rather than process-start failures unless the tool is mandatory.

### `ap-infra`

- Own production/deployment topology and the canonical multi-service `.ores-compose.yaml` for local integration testing.
- Keep admin and non-admin network/data planes isolated.
- Materialize runtime secrets from approved deployment secret stores; `ores-sops` may protect Git-held ciphertext but must not be baked into images or decrypted during image build.
- Deploy immutable artifacts and preserve roll-forward/rollback evidence.

### `ap-clients`, `ap-pub-lib-core`, `ap-cli`

- Consume generated/admitted product interfaces; do not redefine product wire contracts.
- Use WIT bindings/adapters only after the product WIT projection has passed parity/provenance/compatibility gates.
- Keep privileged admin and server-only operations out of public/client libraries.

### `ap-desktop-app.rs`, `ap-flutter`, `ap-sync`

- Consume client-safe interfaces and sync semantics.
- Native/desktop lifecycle telemetry may use the shared `ores-otel` lifecycle adapters.
- Browser/Flutter Web surfaces may use `ores-sw.js` for worker lifecycle, outbox, validation/compute, pooled sockets and bounded live-tab jobs where supported.
- Browser SharedWorker leases never replace durable Agent Pontifex server/native leases.

## Required root config policy

Config files are capability declarations, not checklist badges. Add one only when the repository consumes the associated capability.

| File | Add when |
| --- | --- |
| `.ores-mw.toml` | The executable actually installs `ores-middleware` or validates a middleware plan. |
| `.ores-otel.toml` | The executable/library emits through the ORES telemetry contract. |
| `.ores-sops.toml` / `.sops.yaml` | The repository intentionally stores SOPS-managed ciphertext. Never add placeholder recipients that look valid. |
| `.ores-compose.yaml` | The repository is directly runnable under `ores-compose`; prefer the canonical multi-service topology in `ap-infra`. |
| `.ores-wit.toml` | The repository owns/consumes an admitted WIT package or projection. |
| `.cli-flags.toml` | The executable uses `flags-2-env`; secret-bearing variables are ignored from argv exposure. |
| `.opto-sync.toml` | The repository actually participates in Opto-Sync semantics. |
| `.ores-rl.toml` / `.ores-lru.toml` | The service actually consumes those libraries and has reviewed consistency/failure semantics. |

Unknown, unused or placeholder connectors must default disabled/absent. Empty identifiers are preferable to fabricated values, but an `enabled = true` declaration must still correspond to an intentional capability.

## Hardening invariants

1. **Fail closed at contract/config admission.** Unsupported schema versions, runtime names, middleware stages, WIT compatibility, security modes and connector declarations are errors rather than silent fallback.
2. **Fenced mutations.** Job, lease, repository-path, approval and mutable-control operations carry the live holder/generation/fencing identity; stale workers cannot mutate current state.
3. **Idempotency.** GitHub deliveries, retries, job enqueue, mutating RPC/HTTP operations and durable handoffs use explicit idempotency keys where replay is possible.
4. **Least privilege.** Prefer GitHub App installation tokens scoped to assigned repositories. Separate admin and non-admin credentials/data planes. MCP read-only is not a synonym for broad cloud read access.
5. **Secret containment.** Never place provider keys, GitHub tokens, private prompts, repository source, database URLs, service-role keys or decrypted SOPS material in URLs, logs, traces, browser worker payloads, issues, PRs or generated fixtures.
6. **Bounded telemetry.** Record stable identifiers, result codes, durations, queue depths and safe cardinality fields; do not emit unrestricted prompt/body/source contents.
7. **Bounded queues/caches/workers.** Every in-memory queue, topic room, browser outbox, socket pool, cache and retry system has explicit item/byte/time/concurrency limits and overload behavior.
8. **No split authority.** ORES middleware/transport/WIT/generated clients may project or carry Agent Pontifex semantics but may not redefine them.
9. **Exact runtime boundaries.** Browser, native desktop, server, MCP stdio, worker and admin surfaces receive only the capabilities meaningful for that runtime.
10. **Evidence before promotion.** Contract parity, compile/lint/test/security checks and cross-repository integration evidence must correspond to the exact head being promoted.

## Integration test matrix

At minimum, the organization should maintain automated evidence for:

- TypeSpec ↔ JSON Schema parity for every Agent Pontifex contract family;
- admitted WIT projection + digest/provenance + consumer compatibility for exported SDK surfaces;
- middleware order and request-context propagation on every HTTP server;
- `traceparent`, `baggage` and request-ID continuity across web -> API -> worker/job boundaries;
- secret redaction and negative tests proving credentials/source/prompts do not enter telemetry;
- stale lease/generation/fencing rejection at exact expiry/reassignment boundaries;
- duplicate GitHub/webhook/idempotency delivery behavior;
- `ores-compose` local topology with dynamic ports/UDS and no cross-service endpoint collisions;
- browser-worker offline/outbox behavior without treating ephemeral SharedWorker leases as durable jobs;
- SOPS keyless verification proving no tracked plaintext and exact environment rules wherever SOPS is adopted;
- admin/non-admin network and credential isolation.

## Rollout order

1. `ap-interfaces`: shared primitive references, WIT lane and conformance fixtures.
2. `ap-lib-core`: narrow ORES adapters/ports and fencing/idempotency helpers.
3. `ap-api-server.rs` + `ap-web-server.rs`: middleware + telemetry at real router boundaries.
4. Admin server pair: same primitives with separate auth/network/secret policy.
5. `ap-infra`: canonical compose topology, telemetry collectors, secret/deployment wiring and isolation checks.
6. `ap-clients` / `ap-cli` / `ap-mcp-server.rs`: generated interfaces and least-capability client/tool surfaces.
7. Desktop/Flutter/sync: native lifecycle telemetry and bounded browser/background worker integration.
8. Compatibility repositories: point to canonical `ap-*` ownership; do not independently evolve equivalent implementations.
