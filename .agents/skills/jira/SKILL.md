---
name: jira
description: >-
  Routes every Jira, Confluence, and Atlassian admin request through the local
  acli CLI. Use when the user mentions Jira, Confluence, Atlassian, acli, JQL,
  a Jira work item or issue key, a sprint, board, filter, dashboard, or a
  Confluence page, space, or blog. Do not use the Atlassian MCP, a browser, or
  direct REST.
---

# Atlassian via acli

Every Jira, Confluence, and Atlassian organization-admin action goes through the `acli` binary (Atlassian CLI).

## Hard rule

Use `acli` for every read and every write: work items, comments, transitions, links, projects, boards, sprints, filters, fields, dashboards, Confluence pages, spaces, blogs, and org users.

Forbidden clients, with no exception for speed, missing flags, or an already-authenticated session:

- the Atlassian MCP server, including its auth tool
- browser automation
- `curl`, SDKs, or any HTTP call to an Atlassian host, including `*.atlassian.net` and `api.atlassian.com`
- `acli rovodev` (same binary, separate agent)

If `acli` has no command for the request, say so and stop. A missing command is not permission to switch clients.

BAD

> ❌ Look up PROJ-123 with the Atlassian MCP, or `curl https://site.atlassian.net/rest/api/3/issue/PROJ-123`.

GOOD

> ✅ `acli jira workitem view PROJ-123 --json`

`acli --version` may print an upgrade notice and still exit 0. Ignore the notice. Do not install or upgrade.

## Before every call

1. Run `acli --version`. If the binary is missing, stop and tell the user. Leave install and upgrade to them.
2. Check the product that the task touches. Global auth and product auth are independent. `acli auth status` can fail while Jira is logged in.
   - Jira: `acli jira auth status`
   - Confluence: `acli confluence auth status`
   - Org admin: `acli admin auth status`
3. If that status is unauthorized, stop. Print the login command and wait. Never run login, never read an API token, never pass `--token`.
   - Jira: `acli jira auth login --web`
   - Confluence: `acli confluence auth login --web`
   - Org admin has no `--web` flag. The user runs `acli admin auth login --email <email> --token` and pipes the API key on stdin.
4. Pick the command from [references/commands.md](references/commands.md). If the needed flags are not listed there, run `acli <command> --help` and use only flags that help prints. The two `login --web` commands above are the only `--web` invocations to print, and they are for the user to run.

## How to call

- Add `--json`, `--csv`, `--paginate`, or `--limit` only when that command's help lists the flag. Confluence space list has `--limit` and no `--paginate`. Blog list pages with `--cursor`.
- Commands that prompt (`edit`, `transition`, `assign`, `delete`, `clone`, `create-bulk`, link create, link delete) need `--yes` or they hang. `comment create` has no `--yes`; pass `--body` or `--body-file` and do not pass `--editor`.
- `workitem view` takes the key as a positional argument. `search` takes `--jql` or `--filter`, not `--key`. Other work-item writes take `--key`, `--jql`, or `--filter`. Quote JQL. Keys look like `PROJ-123`.
- Assignee values are an email, an account ID, `@me`, or `default`.
- Put multi-line descriptions and comments in a file and pass `--description-file` or `--body-file`.
- `acli jira auth switch` with no flags is interactive. Pass `--site`, `--email`, or both.
- Ask the user before `delete`, `archive`, bulk edit, or bulk transition when the request did not name the exact keys or JQL. After they confirm, pass `--yes`.
- Treat auth output as private. Do not echo tokens. Do not repeat the account email unless the user asked who is logged in.

## Command map

| Intent | Command |
| --- | --- |
| View one work item | `acli jira workitem view KEY-123 --json` |
| Search | `acli jira workitem search --jql "..." --json --limit 50` |
| Create | `acli jira workitem create --project KEY --type Task --summary "..." --json` |
| Edit fields | `acli jira workitem edit --key KEY-123 --summary "..." --yes --json` |
| Change status | `acli jira workitem transition --key KEY-123 --status "In Progress" --yes --json` |
| Assign | `acli jira workitem assign --key KEY-123 --assignee "@me" --yes --json` |
| Comment | `acli jira workitem comment create --key KEY-123 --body "..."` |
| Link | `acli jira workitem link create --out KEY-1 --in KEY-2 --type Blocks --yes` |
| Projects | `acli jira project list --json` / `acli jira project view --key TEAM --json` |
| Boards and sprints | `acli jira board search --project TEAM --json`, then `acli jira board list-sprints --id <boardId> --json` |
| Confluence page | `acli confluence page view --id <pageId> --json` |
| Confluence spaces | `acli confluence space list --json` |

`acli jira workitem comment create` is the comment command. Built-in examples that omit `create` are wrong. Comment delete takes `--key` and `--id`. Its built-in example shows `--issue`, which is not a flag. Comment visibility options come from `acli jira workitem comment visibility`.

## Gaps in acli

These actions have no command. Report the gap and stop:

- create, edit, or search Confluence pages (`confluence page` only has `view` by id)
- upload a work item attachment (`attachment` only lists and deletes)
- add a watcher (`watcher` only lists and removes)

## After the call

A write succeeded only when `acli` exited 0. Report the key or id and the fields that changed. Include a browse URL only when the JSON response contains one.
