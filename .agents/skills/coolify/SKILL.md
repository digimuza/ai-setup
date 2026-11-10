---
name: coolify
description: >-
  Hosting and deploys on the Hetzner server through Coolify
  (https://coolify.digimuza.ai) and the `coolify` CLI. Use when the user
  mentions Coolify, deploy, staging/production app, the server, logs, domains,
  the proxy, or docker.digimuza.ai. Read-only by default: ask before any change.
  Never Vercel, Netlify, or hand-run docker on the server.
---

# Coolify via the `coolify` CLI

One Hetzner box runs everything through Coolify. The CLI is
`~/.local/bin/coolify` (v1.11.0), context `digimuza`.

## Hard rules

- **Read-only by default.** The server is a root login on production. Ask the
  user before anything that changes state: create, update, deploy, restart,
  stop, delete, env changes, proxy or server settings. Approval for one change
  is not approval for the next.
- Change Coolify-managed config through Coolify (CLI/API/UI), never by editing
  files in `/data/coolify` over SSH: Coolify keeps its own copy and overwrites
  them.
- Proxy config is Docker Compose. Traefik settings go under `command:` as
  `--flags`, never as YAML keys on the service (a stray `entryPoints:` block
  once took every domain down).
- Never pass `-s` / `--show-sensitive`, never print env values or tokens. Never
  type secret values into Coolify: they come from Infisical.
- Images come from `docker.digimuza.ai`, not Docker Hub or GHCR.

## Before every call

```sh
export PATH=$HOME/.local/bin:$PATH
coolify context verify        # must say: Connection successful, Authentication valid
```

If it fails, stop. The user adds the token (Coolify → Keys & Tokens → API
tokens) with `coolify context add digimuza https://coolify.digimuza.ai "$COOLIFY_TOKEN" -d`.
Never write the token into a file or repo.

## How apps from system-template run

| | |
| --- | --- |
| Apps | `<app>-staging` and `<app>-production`, build pack **dockerimage** |
| Image | `docker.digimuza.ai/digimuza/<app>`, tag `X.Y.Z-<sha7>` (built once by CI) |
| Port / health | 3000, `/api/health` (reports `version` and `revision`) |
| Env set in Coolify | only `APP_ENV` and the `INFISCAL_*` bootstrap (runtime machine identity); everything else is read from Infisical at container start |
| Deploys | **CI-driven**: `release.yml` (staging) and `production.yml` (promote the same image). Don't deploy by hand unless the user asks; prefer re-running the workflow |

## Command map

| Intent | Command |
| --- | --- |
| Look around | `coolify resource list`, `coolify app list --format json`, `coolify server list` |
| One app | `coolify app get <uuid> --format json` |
| Logs | `coolify app logs <uuid> -n 200` |
| Deployments | `coolify deploy list`, `coolify app deployments list <uuid>` |
| Env names | `coolify app env list <uuid>` (names only; no `-s`) |
| Deploy a tag (ask first) | `coolify deploy uuid <uuid> --docker-tag 1.2.0-abc1234` |
| Restart (ask first) | `coolify app restart <uuid>` |
| Create a Docker Image app (ask first) | `coolify app create dockerimage --server-uuid … --project-uuid … --environment-name … --docker-registry-image-name docker.digimuza.ai/digimuza/<app> --docker-registry-image-tag <tag> --ports-exposes 3000 --domains <app>.staging.digimuza.ai --health-check-enabled --health-check-path /api/health` |
| Point at a tag without deploying (ask first) | `coolify app update <uuid> --docker-tag <tag>` |
| Native Infisical integration (alternative to the app's own bootstrap) | `coolify integration-token create --provider infisical …` then `coolify app secret-manager set <uuid> --integration-token <uuid> --settings '{"project_id":"…","environment":"staging","secret_path":"/"}'` |
| Rollback | prefer `production.yml` → Run workflow with `image_tag`; `coolify app rollback --help` only if asked |

For anything not listed, run `coolify <cmd> --help` and use only flags it prints.

## After the call

Report the app name, uuid, and what changed. For a deploy, wait for the
deployment to finish (`coolify deploy get <uuid>`), then check
`<site>/api/health` shows the expected `revision`.
