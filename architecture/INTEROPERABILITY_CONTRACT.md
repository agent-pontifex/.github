# Agent Pontifex interoperability contract

Status: **normative** for public Agent Pontifex integrations.

This contract defines which system owns each cross-organization concern. An
integration may add product-specific policy, but it must not create a second
authority for any concern assigned here.

## Authority map

| Concern | Authority | Required integration behavior |
|---|---|---|
| Agent protocol | [`agent-pontifex/agent-sdk.rs`](https://github.com/agent-pontifex/agent-sdk.rs) | Bridge and coordinator implementations consume versioned SDK contracts and conformance fixtures. They must not publish an incompatible parallel envelope, discovery contract, or capability vocabulary. |
| Repository-write coordination | `platform://fiducia-cloud` | Treat Fiducia Cloud as the external authority for repository/path-set leases and fencing. Every protected write must carry a current positive fencing token for the exact leased scope; stale, missing, expired, or mismatched authority fails closed. |
| Human/operator identity | `platform://shared-auth` | Verify Shared Auth JWTs locally against pinned issuer, audience, and JWKS policy. Shared Auth authenticates humans/operators only; product authorization remains product-local. Never propagate the caller's raw bearer token as an agent, adapter, tool, or downstream service credential. |
| Machine/workload identity | `platform://fiducia-cloud` | Keep workload identity separate from human identity. Issue or exchange only least-privilege, audience-bound, short-lived Agent Pontifex credentials for the selected agent/tool scope. Fiducia remains the workload authority where its coordination contract applies. |
| Package/artifact resolution | `platform://zed-pkg` | Resolve versioned packages and artifacts through Zed metadata and locks. Editable-source composition may use reviewed Git submodules, and production deploys immutable signed artifacts or image digests. |
| Repository environment encryption | `platform://sops` | Track only SOPS ciphertext at `env/enc/*.env.enc`. Materialize local plaintext at `env/dec/*.env` through reviewed tooling and keep it ignored, untracked, and outside the Nix store and build outputs. |

Platform URIs are intentional public abstractions. Public organization policy
must not disclose private repository names merely to describe an authority
boundary.

## Request and write invariants

1. Authenticate a human/operator at ingress with Shared Auth and enforce
   product-local authorization before selecting an agent or tool.
2. Strip the caller's bearer credential at the trust boundary. The only
   permitted transmission of that raw token is to Shared Auth's authenticated
   introspection endpoint as the token being inspected. The caller service uses
   a separate service credential; the inspected token never becomes that
   credential or downstream authorization.
3. Represent the request, capabilities, discovery metadata, and result with the
   versioned Agent Pontifex SDK contract.
4. For a protected repository write, acquire Fiducia authority for the complete
   canonical `owner/repo` and normalized path-set scope before execution. Treat
   the full path set as one atomic lease unit. Carry the holder identity, exact
   scope, expiry, and returned fencing token through the write and finalization
   path. Renewal repeats the exact scope and current token. Reject partial,
   expired, mismatched, or stale authority; accepted fencing tokens are positive
   integers no greater than `9_007_199_254_740_991` for cross-runtime safety.
5. Give agents and tools only scoped workload credentials. Human claims do not
   become machine authority, and provider metadata does not imply product roles.
6. Resolve published dependencies through Zed and record immutable provenance
   for the implementation and protocol revisions used by the execution.

A `tool_request` is observable intent, never authority. A separately authorized
finalizer must re-read current state and recheck capability, approval, exact
lease scope, fencing token, idempotency, and policy immediately before an
irreversible GitHub, Linear, deployment, or other external side effect.

## Compatibility and failure behavior

- Contract additions are additive until a versioned compatibility window says
  otherwise. Consumers pin an SDK release or commit and run its conformance
  fixtures in CI.
- Authority services remain reachable through typed APIs, SDKs, or events.
  Integrations never read another service's database.
- Missing identity, invalid audience or issuer, unavailable verification keys,
  absent lease authority, stale fencing, unknown protocol versions, and
  unverifiable artifact provenance fail closed.
- Logs and traces may record stable subject, workload, lease, execution, and
  artifact identifiers, but never bearer tokens, signing material, or other
  replayable credentials.

## Secret materialization

- Only SOPS-encrypted environment files matching `env/enc/*.env.enc` may be
  tracked. Ciphertext files must retain SOPS metadata; changing the extension
  is not evidence of encryption.
- Decrypted files matching `env/dec/*.env` must remain ignored and untracked.
  Materialize them only through a reviewed `just` recipe, SOPS-aware Nix
  activation that writes outside the Nix store, or the runtime secret provider,
  and remove them according to that mechanism's lifecycle. Plaintext secrets
  must never enter the Nix store or a build output.
- Plaintext tokens, bearer credentials, signing material, and other replayable
  secrets are forbidden in source, fixtures, logs, build artifacts, and both
  environment trees.

## Ownership test

When a proposed change introduces a new token, lease, protocol type, or package
locator, its reviewer must be able to name exactly one authority from the map
above. If two systems can independently assert the same authority, the change
is incompatible with this contract.
