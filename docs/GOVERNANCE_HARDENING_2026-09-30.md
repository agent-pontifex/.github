# Agent Pontifex governance hardening — 2026-09-30

This note records the two organization-level policy defects addressed by the accompanying change.

## 1. Branch-policy contradiction

The mandatory delivery policy defines `dev` as the integration branch and `main`/`master` as production/release branches. The agent instruction mirror also contained a later block instructing agents to prefer `main` before `dev` and to work directly on the selected primary branch. Those instructions could cause routine work to bypass the documented integration and promotion boundary.

The instruction mirrors now align with the mandatory policy, and the baseline validator rejects the contradictory main-first/direct-primary wording if it reappears.

## 2. Stale public repository relationship inventory

The generated public relationship registry is a point-in-time inventory. Static schema/digest validation cannot prove that it still matches GitHub after repositories are created, archived, transferred, or made public/private.

A new validator compares the public registry with GitHub's live **public-only** organization inventory. It intentionally does not enumerate or disclose private repository names. Inventory drift fails closed until the generated relationship evidence is refreshed.

At the time this hardening change was opened, the checked-in public registry was known to be stale, so the new live-inventory gate is expected to remain red until the registry generator/rollout refreshes `repository-relationships.json` and its matching documentation/evidence.

## Promotion rule

Do not weaken or bypass the live-inventory check to make CI green. Refresh the generated registry from the authoritative inventory, preserve the privacy boundary, then rerun exact-head checks before promotion.
