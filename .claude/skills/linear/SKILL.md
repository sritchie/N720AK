---
name: linear
description: Query or update Linear (task manager) for the RV team via the GraphQL API. Use when creating, closing, or searching Linear issues.
---

# Linear API

Use the Linear GraphQL API via Python. The CLI (`npx @linear/cli`) requires interactive auth and doesn't work in non-TTY shells.

**RV team ID**: `363699f6-bb3c-4d72-8bd1-a79aabbbef7c`

```python
import urllib.request, json

def linear_api(query, variables=None):
    payload = {"query": query}
    if variables: payload["variables"] = variables
    data = json.dumps(payload).encode()
    req = urllib.request.Request('https://api.linear.app/graphql', data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': '<API_KEY>'  # Ask user for key if not available
    })
    return json.loads(urllib.request.urlopen(req).read())

# Create a triage issue (no project)
linear_api("""
mutation($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { identifier url }
  }
}
""", {"input": {"teamId": "363699f6-bb3c-4d72-8bd1-a79aabbbef7c", "title": "...", "description": "..."}})
```

**First-time setup**: The CLI requires an API key on first run (interactive prompt). Once authenticated, the key is stored locally.

## Gotchas

- Closing an issue by its RV-### identifier sometimes fails silently (status comes back "Backlog"). Use the UUID `id` field instead — it works reliably — and always check the returned `status` field to confirm the close took effect.
- Remember the CLAUDE.md policy: Linear is a task manager only — never store content or attachments there, never link Linear URLs from repo or GDrive content, and strip all Linear provenance when archiving content out.
