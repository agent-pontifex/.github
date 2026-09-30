#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
GRAPH_PATH = ROOT / 'repository-relationships.json'


def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)


try:
    graph = json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
except (OSError, json.JSONDecodeError) as exc:
    fail(f'cannot read public relationship graph: {exc}')

owner = str((graph.get('owner') or {}).get('login') or '').strip()
if not owner:
    fail('repository-relationships.json is missing owner.login')
if graph.get('audience') != 'public':
    fail('live public inventory validation requires audience=public')

headers = {
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'agent-pontifex-public-inventory-validator/1',
    'X-GitHub-Api-Version': '2022-11-28',
}
token = os.environ.get('GITHUB_TOKEN', '').strip()
if token:
    headers['Authorization'] = f'Bearer {token}'

live: set[str] = set()
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
        fail(f'cannot query live public GitHub repository inventory: {exc}')
    if not isinstance(payload, list):
        fail('GitHub repository inventory response is not an array')
    for repo in payload:
        if not isinstance(repo, dict):
            fail('GitHub repository inventory contains a non-object entry')
        full_name = str(repo.get('full_name') or '').strip()
        visibility = str(repo.get('visibility') or '')
        private = bool(repo.get('private', False))
        if not full_name or '/' not in full_name:
            fail('GitHub repository inventory contains an invalid full_name')
        if private or visibility not in {'', 'public'}:
            fail(f'public-only GitHub query returned a non-public repository: {full_name}')
        live.add(full_name.casefold())
    if len(payload) < 100:
        break
    page += 1
    if page > 100:
        fail('refusing to paginate beyond 10,000 public repositories')

registered: set[str] = set()
for repo in graph.get('repositories', []):
    if not isinstance(repo, dict):
        fail('repository-relationships.json contains a non-object repository entry')
    full_name = str(repo.get('full_name') or '').strip()
    if repo.get('visibility') != 'public':
        fail(f'public graph contains non-public repository metadata: {full_name or "<missing>"}')
    registered.add(full_name.casefold())

missing = sorted(live - registered)
extra = sorted(registered - live)
if missing or extra:
    details: list[str] = []
    if missing:
        details.append('missing public repositories: ' + ', '.join(missing))
    if extra:
        details.append('stale/non-live public repositories: ' + ', '.join(extra))
    fail('public relationship inventory drift: ' + '; '.join(details))

print(f'PASS: public relationship registry matches {len(live)} live public repositories for {owner}')
