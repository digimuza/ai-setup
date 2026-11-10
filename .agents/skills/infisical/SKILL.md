---
name: infisical
description: >-
  Secrets and env vars through the `infisical` CLI against the self-hosted
  instance https://infiscal.digimuza.ai. Use when the user mentions Infisical,
  secrets, env vars, API keys, a project's dev/staging/prod environment, or a
  value an app or CI needs. Never print secret values; never put secrets in
  .env files, git, chat, Linear, or Coolify by hand.
---

# Infisical via the `infisical` CLI

Infisical is the source of truth for every secret and env var. The instance is
**https://infiscal.digimuza.ai** (no second "i" in `infiscal`). The CLI is
`~/.local/bin/infisical` (v0.45.4).

## Hard rules

- **Never print a secret value** into chat, logs, commit messages, Linear,
  PR descriptions, or files that are not git-ignored. List names, not values.
  Never pass `--show-values`. Never `cat` an env file to "check" it.
- **Never put a value on the command line** (`secrets create KEY=value` lands in
  shell history and `ps`). Write values to a temporary file (`umask 077`), pass
  `--file`, delete the file in the same command.
- Generate random secrets locally and never echo them:
  `openssl rand -base64 32`.
- One Infisical project per app, environments `dev`, `staging`, `prod`.
  Staging and prod never share a value (database, bucket, OAuth client,
  cookie password, encryption key).
- Do not use Infisical cloud. Always point the CLI at the self-hosted instance:

  ```sh
  export PATH=$HOME/.local/bin:$PATH
  export INFISICAL_DOMAIN=https://infiscal.digimuza.ai/api
  ```

## Before every call

1. `infisical --version`. If missing, stop and tell the user.
2. Auth:
   - Human: the user runs `infisical login` (browser). Do not run it for them.
   - Agent: a Machine Identity with Universal Auth. With the client ID and
     secret in the environment (never typed into the command):
     `infisical login --method=universal-auth --client-id "$INFISICAL_CLIENT_ID" --client-secret "$INFISICAL_CLIENT_SECRET" --silent --plain`
     prints an access token; pass it with `--token` or `INFISICAL_TOKEN`.
   If neither works, stop and ask. Never ask the user to paste a secret into chat;
   use the harness secret prompt if one exists.
3. Know the target: `--projectId`, `--env` (`dev`/`staging`/`prod`) and `--path`.

## Layout (apps from system-template)

| Path | Holds | Read by |
| --- | --- | --- |
| `/` | runtime config: `APP_ENV`, `SITE_URL`, `CONVEX_URL`, `CONVEX_SITE_URL`, `WORKOS_CLIENT_ID`, `WORKOS_COOKIE_PASSWORD`, `SUPER_USER_EMAILS`, `MAIL_FROM`, `RESEND_API_KEY` | the running app (runtime machine identity) |
| `/ci` | CI only: `CONVEX_DEPLOY_KEY` or `CONVEX_SELF_HOSTED_*`, `REGISTRY_USERNAME`, `REGISTRY_PASSWORD`, `COOLIFY_TOKEN`, `COOLIFY_APP_UUID`, `LINEAR_API_KEY` | GitHub Actions (CI machine identity) |

The app's own bootstrap variables are spelled `INFISCAL_*` (`INFISCAL_BASE_URL`,
`INFISCAL_CLIENT_ID`, `INFISCAL_SECRET`, `INFISCAL_PROJECT_ID`, `INFISCAL_ENV`,
`INFISCAL_PATH`). They live in Coolify and GitHub, never in Infisical itself.

## Command map

| Intent | Command |
| --- | --- |
| List projects | `infisical secrets-manager projects get` |
| Create a project (default dev/staging/prod) | `infisical secrets-manager projects create --help`, then run it |
| List secret **names** | `infisical secrets-manager secrets get --projectId <id> --env staging --path / -o json \| python3 -c 'import json,sys; print("\n".join(s["secretKey"] for s in json.load(sys.stdin)))'` |
| Create secrets | `umask 077; f=$(mktemp); printf 'KEY=%s\n' "$value" > "$f"; infisical secrets-manager secrets create --file "$f" --projectId <id> --env staging --path /; rm -f "$f"` |
| Update secrets | same with `secrets update --file` (fails if a key doesn't exist) |
| Delete | `infisical secrets-manager secrets delete KEY --projectId <id> --env staging` (ask first) |
| Folders (`/ci`) | `infisical secrets-manager folders --help` |
| Run with secrets | `infisical secrets-manager run --projectId <id> --env dev -- pnpm dev` |

For any flag not listed, run `infisical secrets-manager <cmd> --help` and use
only flags it prints.

## Access after creating a project

A project created by a machine identity has that identity as its only member,
so Andrius won't see it. Add him right after: Project → Access Control →
Members, or `POST /api/v2/workspace/<projectId>/memberships` with
`{"usernames":["andrius@digimuza.ai"],"roleSlugs":["admin"]}`.

## After the call

Report what changed by **key name and environment only**, for example
"created `WORKOS_COOKIE_PASSWORD` in `staging` `/`". A write succeeded only when
the CLI exited 0.
