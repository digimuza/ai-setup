# acli command reference

Flags below were read from `acli` 1.3.15. If a flag is rejected, run `acli <command> --help` and follow that output. Do not invent flags.

Global groups: `acli auth`, `acli jira`, `acli confluence`, `acli admin`, `acli config`.

## Auth

| Command | Purpose |
| --- | --- |
| `acli jira auth status` | Jira account. This is the check that matters for Jira work. |
| `acli jira auth login --web` | User runs this. The agent does not. |
| `acli jira auth logout` | Log out of Jira. |
| `acli jira auth switch --site <site> --email <email>` | Switch Jira account. Pass `--site`, `--email`, or both. With no flags the command prompts. |
| `acli confluence auth status` | Confluence account. Independent of Jira. |
| `acli confluence auth login --web` | User runs this. The agent does not. |
| `acli admin auth status` | Org-admin account. |
| `acli auth status` | Global OAuth. Irrelevant when the product status succeeds. |

Jira and Confluence login also accept `--site`, `--email`, and `--token` (token on stdin). Do not use that path. Org-admin login is `--email` plus `--token` on stdin only. It has no `--web` and no `--site`.

## Jira work items

### view

`acli jira workitem view KEY-123 [--fields <list>] [--json]`

`--fields` default is `key,issuetype,summary,status,assignee,description`. Use `*all`, `*navigable`, a comma list (`summary,comment`), or a minus to exclude (`-description`).

### search

`acli jira workitem search --jql "<jql>" [--fields <list>] [--limit N] [--paginate] [--count] [--json] [--csv] [--filter <id>]`

Default fields: `issuetype,key,assignee,priority,status,summary`.

### create

`acli jira workitem create --summary "..." --project KEY --type "Task|Bug|Story|Epic" [--assignee <email|accountId|@me|default>] [--description "..."] [--description-file <path>] [--label a,b] [--parent KEY] [--json]`

Also `--from-file`, `--from-json`, `--generate-json`, `--editor`.

### create-bulk

`acli jira workitem create-bulk --from-json <file> | --from-csv <file> [--ignore-errors] [--yes]`

CSV columns: `summary, projectKey, issueType, description, label, parentIssueId, assignee`. `--generate-json` prints a sample.

### edit

`acli jira workitem edit (--key "A-1,A-2" | --jql "..." | --filter <id>) [--summary] [--description] [--description-file] [--assignee] [--remove-assignee] [--type] [--labels] [--remove-labels] [--yes] [--json] [--ignore-errors]`

Also `--from-json`, `--generate-json`.

### transition

`acli jira workitem transition (--key | --jql | --filter) --status "Exact Status Name" [--yes] [--json] [--ignore-errors]`

`--status` is the destination status name, not a transition id.

### assign

`acli jira workitem assign (--key | --jql | --filter | --from-file) (--assignee <email|accountId|@me|default> | --remove-assignee) [--yes] [--json] [--ignore-errors]`

### delete

`acli jira workitem delete (--key | --jql | --filter | --from-file) [--yes] [--json] [--ignore-errors]`

Require an explicit user request that names the targets before adding `--yes`.

### clone

`acli jira workitem clone (--key | --jql | --filter | --from-file) --to-project KEY [--to-site <site>] [--yes] [--json] [--ignore-errors]`

### archive / unarchive

`acli jira workitem archive` and `acli jira workitem unarchive`. Run `--help` before use.

### comment

`acli jira workitem comment create (--key | --jql | --filter) (--body "..." | --body-file <path>) [--edit-last] [--json] [--ignore-errors]`

`acli jira workitem comment list --key KEY [--limit 50] [--order +created] [--paginate] [--json]`

`acli jira workitem comment update --key KEY --id <commentId> (--body | --body-file | --body-adf) [--visibility-role] [--visibility-group] [--notify]`

`acli jira workitem comment delete --key KEY --id <commentId>`

The built-in delete example uses `--issue`. That flag does not exist. Use `--key`.

`acli jira workitem comment visibility (--role --project <projectKey> | --group)` lists roles or groups that `--visibility-role` and `--visibility-group` accept.

### link

`acli jira workitem link type [--json]` lists link types. `--type` on create takes the outward description (for example `Blocks`).

`acli jira workitem link create --out <outwardKey> --in <inwardKey> --type "<outward name>" [--yes]`

Also `--from-json`, `--from-csv`, `--generate-json`.

`acli jira workitem link list --key KEY [--json]`

`acli jira workitem link delete --id <linkId> [--yes]` (also `--from-json`, `--from-csv`)

### attachment

`acli jira workitem attachment list` and `attachment delete`. Run `--help`. There is no upload command.

### watcher

`acli jira workitem watcher list` and `watcher remove`. Run `--help`. There is no add command.

## Jira projects

| Command | Required flags |
| --- | --- |
| `project list` | optional `--limit` (default 30), `--paginate`, `--recent`, `--json` |
| `project view` | `--key` |
| `project create` | `--from-project <key> --key --name`, or `--from-json`. Optional `--description`, `--url`, `--lead-email`. `--generate-json` prints a sample. |
| `project update`, `archive`, `delete`, `restore` | Run `--help`. `delete` and `archive` need an explicit user request. |

## Boards, sprints, filters, fields, dashboards

### board

`acli jira board search [--name] [--project <key>] [--type scrum|kanban|simple] [--filter <id>] [--limit 50] [--paginate] [--json]`

`acli jira board list-sprints --id <boardId> [--state future,active,closed] [--limit] [--paginate] [--json]`

`acli jira board get`, `list-projects`, `create`, `delete`: run `--help`.

### sprint

`acli jira sprint list-workitems --sprint <id> --board <id> [--jql] [--fields] [--limit] [--paginate] [--json]`

`acli jira sprint view --id <id> [--json]`

`acli jira sprint create --name "..." --board <id> [--start ISO] [--end ISO] [--goal] [--json]`

`sprint update` and `sprint delete`: run `--help`.

### filter

`acli jira filter list (--my | --favourite) [--json]`

`acli jira filter search [--name] [--owner <email>] [--limit] [--paginate] [--json]`

`filter get`, `get-columns`, `update`, `change-owner`, `add-favourite`, `reset-columns`: run `--help`.

### field

`acli jira field create|update|delete|cancel-delete`. Custom-field admin. Run `--help`. `delete` trashes the field.

### dashboard

`acli jira dashboard search`. Run `--help`. Search only.

## Confluence

Auth is separate from Jira. Check `acli confluence auth status` first.

| Command | Flags |
| --- | --- |
| `confluence page view` | `--id <pageId>` required. Optional `--body-format storage\|atlas_doc_format\|view`, `--json`, `--include-labels`, `--include-direct-children`, `--version`, `--get-draft`, `--status`. No create, update, or search command exists. |
| `confluence space list` | `--type global\|personal`, `--status current\|archived` (default `current`), `--keys`, `--limit` (default 50), `--expand description,homepage,permissions`, `--json` |
| `confluence space view` | `--id <spaceId>`, optional `--include-all`, `--json` |
| `confluence space create`, `update`, `archive`, `restore` | Run `--help`. `archive` needs an explicit user request. |
| `confluence blog list` | `--space-id`, `--id`, `--title`, `--status`, `--body-format`, `--limit` (default 25), `--cursor`, `--json` |
| `confluence blog view` | `--id`, optional `--body-format` (default `view`), `--include`, `--version`, `--draft`, `--json` |
| `confluence blog create` | `--space-id --title` plus `--body` (storage XHTML) or `--from-file` or `--from-json`. Optional `--status current\|draft` (default `current`), `--private`, `--json`. `--generate-json` prints a sample. |

## Admin

`acli admin user activate|deactivate|delete|cancel-delete`. These change org accounts. Run `--help`, and run one only after the user names the account and the action.
