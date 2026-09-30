# Agent Pontifex governance hardening — 2026-09-30

This note records the organization-level governance defects addressed by this change and the evidence used to close them.

## 1. Branch-policy contradiction

The mandatory delivery policy defines `dev` as the integration branch and `main`/`master` as production/release branches. The agent instruction mirror also contained a later block instructing agents to prefer `main` before `dev` and to work directly on the selected primary branch. Those instructions could cause routine work to bypass the documented integration and promotion boundary.

The lowercase canonical instructions and uppercase compatibility mirror now agree on `dev`-first feature/fix/hardening work. The baseline validator also rejects the old main-first/direct-primary wording if it reappears.

## 2. Stale public repository relationship inventory

The public relationship registry was a point-in-time four-repository snapshot even though the live organization had grown to 21 public repositories. Static schema/digest validation could not detect that drift.

The registry has been regenerated from GitHub's public-only organization endpoint and now represents all 21 live public repositories. The public graph contains no private repository names. Its private-registry metadata remains an opaque pointer/digest and only records that non-public inventory exists; the public refresh path deliberately does not publish private repository names or counts.

Two independent fail-closed checks now protect the evidence:

- `validate_live_public_inventory.py` compares the registered public names with GitHub's live public-only inventory;
- `refresh_public_relationships.py --check` independently rebuilds the public graph and rendered Markdown with the shared relationship library and rejects any stale or hand-edited result.

## 3. Deterministic refresh path

`refresh_public_relationships.py` is the reviewed way to refresh this public evidence. It reuses the repository's existing normalization, relationship inference, digest, validation and Markdown rendering functions. It preserves richer reviewed owner metadata and the opaque private-registry digest while keeping private inventory out of the public graph.

The relationship workflow runs on PRs plus `dev`/`main` pushes, has bounded execution, uses read-only permissions, SHA-pinned checkout with non-persistent credentials, validates the graph, checks live public inventory, and requires deterministic regenerated evidence.

## Promotion rule

Do not weaken or bypass inventory, privacy, branch-policy, scratch-ignore or baseline checks to make CI green. Refresh authoritative evidence, preserve the privacy boundary, and require exact-head checks before promotion from `dev` to production branches.
