# agent-pontifex organization handbook

> Shared operating defaults for repositories maintained under **agent-pontifex**. Repository-local policy may strengthen these rules but should not silently weaken them.

## Mission

agent-pontifex maintains agent orchestration, integration, routing, workflow-bridging, and connector software. This `.github` repository is the canonical home for shared policy, reusable templates, community health files, and planning links.

## Repository contract

Each active repository must document purpose, ownership, maturity, supported runtimes and connectors, development and test commands, authoritative message and state formats, release and rollback procedures, compatibility policy, and GitHub Project/Linear links. Agent components should also document tool permissions, trust boundaries, identity propagation, memory and state lifecycle, retries and idempotency, timeouts and budgets, approval gates, observability, and failure containment.

## Change workflow

1. Anchor work in an issue, Linear item, or documented maintenance objective.
2. Keep branches and pull requests focused.
3. Explain motivation, scope, safety and integration impact, validation, compatibility, migration, and rollback.
4. Test unavailable tools, denied permissions, malformed outputs, injection attempts, duplicate requests, timeout, retry, partial failure, and human escalation as relevant.
5. Resolve conflicts semantically by reconstructing both sides' intent.
6. Prefer squash merges for focused work unless commit structure materially improves auditability.

## Evidence, security, and documentation

Pull requests should include reproducible commands, synthetic fixtures, evaluation cases, expected and observed behavior, negative-path coverage, documentation updates, and CI or local-equivalent evidence. Never commit credentials, connector tokens, private conversations, production identities, or sensitive logs. Follow `SECURITY.md` for private reporting. Keep permissions least-privileged, examples sanitized, behavior limits explicit, and important routing, memory, compatibility, and operational decisions recorded.

## Planning ownership

GitHub owns code, reviews, checks, releases, and delivery evidence. Linear owns priority, dependencies, sequencing, and cross-project planning. The organization GitHub Project is the cross-repository execution view; see `PROJECTS.md` for routing details.

## Organization health

- [ ] Profiles, descriptions, topics, and READMEs are current.
- [ ] Community health files and reusable issue/PR guidance are present.
- [ ] Permissions, identity, state, retries, budgets, approvals, observability, and failure containment are documented.
- [ ] Required checks cover adversarial inputs, denied/unavailable tools, compatibility, privacy, and supply-chain risk.
- [ ] Stale repositories are archived or clearly marked.
- [ ] GitHub Project and Linear links resolve and reflect completed work.
