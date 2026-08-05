# Agent Pontifex marketing site

This directory is the complete Astro source staged for the future public repository `agent-pontifex/agent-pontifex.github.io` and URL `https://agent-pontifex.github.io/`.

## Canonical planning

- Linear project: [github.com/agent-pontifex](https://linear.app/denman/project/githubcomagent-pontifex-1d2deb2be3c7)
- GitHub Project: [agent-pontifex-project #1](https://github.com/orgs/agent-pontifex/projects/1)
- Organization: [agent-pontifex](https://github.com/agent-pontifex)

## Product sources

- `agent-sdk.rs`: versioned protocol contracts and credential-safe Rust clients
- `ai-agent-bridge.rs`: bridge implementation
- `ai-agent-coordinator.rs`: coordinator implementation

The page uses exact public SDK operations (`Client::new`, `with_bearer`, `bridge`, `coordinator`, and discovery) plus the checked-in conformance descriptor. It deliberately labels the surface as Rust-first rather than inventing unpublished language packages.

## Publish

1. Create the public repository `agent-pontifex.github.io` in the `agent-pontifex` organization.
2. Copy the contents of this directory to its repository root.
3. Run `npm install && npm run build`.
4. Add the standard Astro GitHub Pages workflow and select **GitHub Actions** as the Pages source.
5. Verify the canonical HTTPS URL and update the linked GitHub and Linear tickets.
