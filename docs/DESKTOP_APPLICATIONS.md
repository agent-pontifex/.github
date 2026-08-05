# Desktop application allocation

Verified **2026-08-05**.

Agent Pontifex **might** benefit from paired native desktop operator clients after the web control plane and local-agent requirements are proven:

- Rust: [`agent-pontifex/agent-pontifex-desktop.rs`](https://github.com/agent-pontifex/agent-pontifex-desktop.rs) — **proposed**, not yet verified as a published repository.
- Flutter: [`agent-pontifex/agent-pontifex-flutter`](https://github.com/agent-pontifex/agent-pontifex-flutter) — **proposed**, not yet verified as a published repository.

These names are optional allocation targets, not proof that either remote exists and not a commitment to build them. Keep the coordinator and primary control plane service/web-first unless local worker status, approvals, budget alerts, credential state, intervention queues, tray notifications, or always-on operator workflows justify native clients.

## Potential product boundary

A future pair could cover semantic parity for local worker discovery and health, approval queues, task status, budget and quota alerts, intervention requests, credential-state warnings, notifications, logs, local configuration, and safe pause/resume controls.

A shared Rust agent/control client may sit behind an explicit library, FFI, or local-service boundary, but any Flutter application must remain independently buildable, testable, and releasable. Shared schemas, clients, fixtures, event models, and conformance tests should be versioned deliberately.

## Promotion rule

Promote this pair from optional proposal to planned only when a native workflow is demonstrably better than the web control plane. Once planned, desktop-facing changes must inspect both implementations, define shared acceptance criteria, update both or record an explicit no-change rationale, and report Rust and Flutter status separately.

## Project routing

- GitHub Project: [`agent-pontifex-project` — Project 1](https://github.com/orgs/agent-pontifex/projects/1)
- Linear project: `github.com/agent-pontifex`
- Central registry: [`approved-private-registry`](private-registry://canonical/registry/desktop-applications.json)
- Portfolio rollout: [`DEN-2469`](https://linear.app/denman/issue/DEN-2469/roll-out-paired-rust-flutter-desktop-repositories-across-the-portfolio)

Promotion, repository creation, renames, transfers, archival, or platform-status changes must update this document, Linear, the central registry, and both companion repositories together.
