# `linear` CLI reference (v3.1.0)

Flags checked against `linear <command> --help`. Global flags on every command:
`--workspace <SLUG>`, `--no-input`.

## issue

| Command | Flags |
| --- | --- |
| `issue view [ISSUE]` | `-j/--json`, `--no-comments`, `--show-resolved-threads`, `--no-pager`, `--no-download`, `-w/--web`, `-a/--app` |
| `issue list` | `-s/--state <STATE>` (repeatable; default `unstarted`), `--all-states`, `--team`, `--assignee <USER>`, `-A/--all-assignees`, `-U/--unassigned`, `--project`, `--project-label`, `--cycle`, `--milestone`, `-l/--label`, `--created-after`, `--updated-after`, `--limit <N or all>`, `--sort manual\|priority`, `-j/--json`, `--no-pager` |
| `issue query` | `--search <TEXT>`, `--search-comments`, `--team`, `--all-teams`, `-s/--state`, `--assignee`, `-U`, `--project`, `--project-label`, `--cycle`, `--milestone`, `-l/--label`, `--created-after`, `--updated-after`, `--limit`, `--include-archived`, `--sort`, `-j/--json`, `--no-pager` |
| `issue create` | `-t/--title`, `-d/--description`, `--description-file <FILE or ->`, `--team`, `-a/--assignee`, `--delegate <AGENT>`, `-s/--state`, `-p/--priority none\|urgent\|high\|medium\|low`, `--estimate`, `-l/--label`, `--due-date YYYY-MM-DD`, `--parent DIG-1`, `--project`, `--milestone`, `--cycle`, `--template`, `--no-use-default-template`, `--start`, `-y/--yes` (no `--json`) |
| `issue update [ISSUE]` | `-t/--title`, `-d/--description`, `--description-file`, `--team`, `-a/--assignee`, `--unassign`, `--delegate`, `--clear-delegate`, `-s/--state`, `-p/--priority`, `--estimate`, `--clear-estimate`, `-l/--label` (replace), `--add-label`, `--remove-label`, `--due-date`, `--clear-due-date`, `--parent`, `--clear-parent`, `--project`, `--clear-project`, `--milestone`, `--clear-milestone`, `--cycle`, `--clear-cycle` |
| `issue comment add [ISSUE]` | `-b/--body`, `--body-file`, `-p/--reply-to <COMMENT>`, `-a/--attach <FILE>`, `--public`, `-y/--yes`. Also `comment list`, `update`, `delete`, `resolve`, `unresolve` |
| `issue relation add <ISSUE> <RELATION> <RELATED>` | RELATION: `blocks`, `blocked-by`, `related`, `duplicate`. Also `relation list`, `relation delete` |
| `issue start [ISSUE]` | `-b/--branch <BRANCH>`, `-f/--from-ref <REF>`, `--team`, `-A`, `-U`. Checks out the issue's git branch and marks it started |
| `issue describe [ISSUE]` | `-r/--references`. Title plus a `Linear-issue` trailer for commit messages |
| `issue url`, `issue title`, `issue id` | Print the URL, title, or the current branch's issue ID |
| `issue link [ISSUE] <URL>` | Link a URL (for example a PR) |
| `issue attach [ISSUE] <FILE>` | Upload a file |
| `issue pull-request [ISSUE]` | Open a GitHub PR for the issue (prefer `gh pr create` with `DIG-123` in the title) |
| `issue archive`, `issue delete` | Ask the user first |

Omitting `[ISSUE]` uses the issue of the current branch (`feature/DIG-123-…`).

## project, milestone, project-update

| Command | Flags |
| --- | --- |
| `project list` | `--all-teams`, `-j/--json` |
| `project create` | `-n/--name`, `-d/--description`, `-s/--status backlog\|planned\|started\|paused\|completed\|canceled`, `-t/--team`, `-y` |
| `milestone list` / `view` | `--project <PROJECT>` |
| `milestone create` | `--project`, `--name`, `--description`, `--target-date`, `-y/--yes` |
| `project-update create <PROJECT>` | `--body`, `--body-file`, `--health on-track\|at-risk\|off-track`, `-y/--yes` |

## team, user, cycle, label

| Command | Use |
| --- | --- |
| `team list` | Teams and keys |
| `team states DIG` | Workflow states of the team |
| `user list` | Workspace members (for `--assignee`) |
| `cycle` | `linear cycle --help` for the current, next, and previous cycles |
| `label` | `linear label --help` |

## Not covered

No command for: editing workflow states, creating teams, project milestones'
issue membership in bulk. Report the gap and stop.
