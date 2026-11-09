---
name: linear
description: >-
  Routes every Linear request through the local `linear` CLI (schpet/linear-cli).
  Use when the user mentions Linear, an issue key like DIG-123, a project,
  milestone, cycle, project update, or asks to create, find, move, comment on,
  or link an issue. Do not use the Linear MCP, a browser, or direct GraphQL/REST.
---

# Linear via the `linear` CLI

Every Linear action goes through the `linear` binary (schpet/linear-cli, at
`~/.local/bin/linear`). Work is tracked in team **DIG**; issue keys look like
`DIG-123`.

## Hard rule

Use `linear` for every read and every write: issues, comments, states,
relations, projects, milestones, project updates, cycles, labels.

Forbidden clients, with no exception for speed, missing flags, or an
already-authenticated session:

- the Linear MCP server (it has auth and session-loading problems)
- browser automation
- `curl`, SDKs, or any HTTP call to `api.linear.app`
- `linear api` raw GraphQL, unless the user asks for it by name

If `linear` has no command for the request, say so and stop. A missing command
is not permission to switch clients.

BAD

> ❌ Look up DIG-123 with the Linear MCP, or `curl https://api.linear.app/graphql`.

GOOD

> ✅ `linear issue view DIG-123 --json --no-pager --no-input`

## Before every call

1. Make sure the binary is on the path: `export PATH=$HOME/.local/bin:$PATH`,
   then `linear --version`. If it is missing, stop and tell the user. Leave
   install and upgrade to them.
2. Check auth: `linear auth whoami`. If it fails, stop. Print the login steps
   and wait: create a personal API key in Linear (Settings → Security & access
   → Personal API keys), then `linear auth login`. Never read, print or pass an
   API key yourself.
3. Pick the command from [references/commands.md](references/commands.md). If
   the needed flags are not listed there, run `linear <command> --help` and use
   only flags that help prints.

## How to call

- Always pass `--no-input`, so nothing waits on a prompt. Create commands also
  need `-y` (`--yes`).
- Add `-j` / `--json` only where help lists it (`issue view`, `issue list`,
  `issue query`, `project list`). `issue create` has no `--json`: read the key
  from its `✓ Created issue DIG-123` line.
- Add `--no-pager` to `view`, `list` and `query`, or long output hangs.
- `issue list` shows only your unstarted issues by default. For everything in a
  project pass `--team DIG --project <slug> --all-states --all-assignees`.
- States are names: `Backlog`, `Todo`, `In Progress`, `In Review`,
  `In Staging`, `Done`, `Canceled`, `Duplicate`.
- Put multi-line descriptions, comments and project updates in a file and pass
  `--description-file` or `--body-file`.
- Ask the user before `delete`, `archive`, or changing many issues when the
  request did not name the exact keys. After they confirm, run them one by one.
- Treat auth output as private. Do not repeat the account email unless the user
  asked who is logged in.

## The DIG workflow

Follow the release cycle in `work/README.md`:

| When | Do |
| --- | --- |
| Work starts | One issue per change. `linear issue update DIG-123 -s "In Progress" --no-input`. Branch `feature/DIG-123-<slug>` |
| PR opened to `main` | PR title includes `DIG-123`. Move to `In Review` |
| Merged to a `release/*` branch, live on staging | `In Staging` (the release workflow does this when `LINEAR_API_KEY` is set) |
| Merged to `production`, live in prod | `Done` (the production workflow does this) |
| Each release | One project milestone `vX.Y.Z` with the shipping issues on it |
| After each work session or deploy | A project update: `linear project-update create <project> --body-file … --health on-track -y --no-input` |

Relate follow-up work instead of burying it in comments:
`linear issue relation add DIG-124 related DIG-123 --no-input`.

## Command map

| Intent | Command |
| --- | --- |
| View one issue | `linear issue view DIG-123 --json --no-pager --no-input` |
| List a project's issues | `linear issue list --team DIG --project <slug> --all-states --all-assignees --json --no-pager --no-input` |
| Search | `linear issue query --search "csv export" --team DIG --json --no-pager --no-input` |
| Create | `linear issue create -t "..." --team DIG --project <slug> -s "In Progress" --description-file desc.md -y --no-input` |
| Change state | `linear issue update DIG-123 -s "In Review" --no-input` |
| Edit fields | `linear issue update DIG-123 -t "..." --add-label <label> --no-input` |
| Assign | `linear issue update DIG-123 -a @me --no-input` |
| Comment | `linear issue comment add DIG-123 --body-file comment.md --no-input` |
| Relate | `linear issue relation add DIG-124 related DIG-123 --no-input` |
| Start work (branch + state) | `linear issue start DIG-123 --no-input` |
| Commit trailer | `linear issue describe DIG-123` |
| Projects | `linear project list --all-teams --json --no-input` |
| Milestone | `linear milestone create --project <slug> --name v1.2.0 -y --no-input` |
| Project update | `linear project-update create <slug> --body-file update.md --health on-track -y --no-input` |
| Team states | `linear team states DIG --no-input` |

## After the call

A write succeeded only when `linear` exited 0. Report the key and the fields
that changed, with the issue URL (`linear issue url DIG-123`) when the user will
want to open it.
