#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT_DEFAULT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DEFAULT / 'scripts'))

from repository_relationships_lib import (  # noqa: E402
    PUBLIC_AUDIENCE,
    build_relationship_graph,
    parse_manual_declarations,
    pretty_json,
    render_relationship_markdown,
    stabilize_generated_at,
    validate_relationship_graph,
)


def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)


def fetch_public_repositories(owner: str) -> list[dict[str, object]]:
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'agent-pontifex-public-relationship-refresh/1',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    token = os.environ.get('GITHUB_TOKEN', '').strip()
    if token:
        headers['Authorization'] = f'Bearer {token}'

    repositories: list[dict[str, object]] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({
            'type': 'public',
            'sort': 'full_name',
            'direction': 'asc',
            'per_page': 100,
            'page': page,
        })
        request = urllib.request.Request(
            f'https://api.github.com/orgs/{urllib.parse.quote(owner)}/repos?{query}',
            headers=headers,
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            fail(f'cannot query public GitHub inventory: {exc}')
        if not isinstance(payload, list):
            fail('GitHub public inventory response is not an array')
        for repo in payload:
            if not isinstance(repo, dict):
                fail('GitHub public inventory contains a non-object entry')
            if bool(repo.get('private', False)):
                fail(f"public-only query returned private repository {repo.get('full_name')!r}")
            visibility = str(repo.get('visibility') or '')
            if visibility not in {'', 'public'}:
                fail(f"public-only query returned non-public repository {repo.get('full_name')!r}")
            repositories.append(repo)
        if len(payload) < 100:
            return repositories
        page += 1
        if page > 100:
            fail('refusing to paginate beyond 10,000 public repositories')


def render(root: Path) -> tuple[str, str]:
    graph_path = root / 'repository-relationships.json'
    manual_path = root / 'repository-relationships.manual.json'
    existing_text = graph_path.read_text(encoding='utf-8')
    existing = json.loads(existing_text)
    owner_block = existing.get('owner') or {}
    owner = str(owner_block.get('login') or '').strip()
    if not owner:
        fail('existing registry is missing owner.login')

    private_registry = existing.get('private_registry')
    if not isinstance(private_registry, dict):
        fail('existing public registry is missing opaque private_registry metadata')
    private_digest = str(private_registry.get('digest') or '')
    if not private_digest.startswith('sha256:'):
        fail('existing private_registry digest is invalid')

    linear = owner_block.get('linear_project') or {}
    target = {
        'owner': owner,
        'account_type': owner_block.get('account_type', 'organization'),
        'linear_project': linear.get('name'),
        'linear_url': linear.get('url'),
    }
    manual = parse_manual_declarations(
        manual_path.read_text(encoding='utf-8'), owner, audience=PUBLIC_AUDIENCE
    )
    graph = build_relationship_graph(
        target,
        fetch_public_repositories(owner),
        audience=PUBLIC_AUDIENCE,
        manual=manual,
        private_graph_digest=private_digest,
    )
    graph = stabilize_generated_at(graph, existing_text)

    # Preserve richer reviewed owner metadata from the existing public record.
    graph['owner'] = owner_block

    # The public refresher intentionally cannot enumerate private repositories.
    # Preserve only the opaque mirror pointer/digest and a boolean that a
    # non-public inventory exists; do not publish private names or counts.
    graph['private_registry'] = dict(private_registry)
    graph['private_registry']['contains_non_public_inventory'] = True
    graph['generated'].pop('omitted_repository_count', None)
    graph['generated'].pop('private_repositories_omitted', None)

    validate_relationship_graph(graph)
    return pretty_json(graph), render_relationship_markdown(graph)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', type=Path, default=ROOT_DEFAULT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    expected_json, expected_markdown = render(root)
    graph_path = root / 'repository-relationships.json'
    docs_path = root / 'docs/REPOSITORY_RELATIONSHIPS.md'

    if args.check:
        mismatches: list[str] = []
        if graph_path.read_text(encoding='utf-8') != expected_json:
            mismatches.append(str(graph_path.relative_to(root)))
        if docs_path.read_text(encoding='utf-8') != expected_markdown:
            mismatches.append(str(docs_path.relative_to(root)))
        if mismatches:
            fail('public relationship evidence is stale: ' + ', '.join(mismatches))
        print('PASS: public relationship evidence matches live public inventory')
        return

    graph_path.write_text(expected_json, encoding='utf-8')
    docs_path.write_text(expected_markdown, encoding='utf-8')
    print('updated public relationship registry and rendered documentation')


if __name__ == '__main__':
    main()
