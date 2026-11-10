---
name: workos
description: >-
  WorkOS AuthKit sign-in for digimuza apps and the WorkOS CLI (`npx
  workos@latest`): environments, client IDs, redirect/logout/CORS URIs, the JWT
  template, branding, test users. Use when the user mentions WorkOS, AuthKit,
  sign-in/login setup, "invalid client ID", redirect URI, SSO, or the WorkOS
  dashboard.
---

# WorkOS via the CLI

Apps sign in with WorkOS AuthKit (hosted page). system-core decides access:
a WorkOS session grants nothing without an invite or a `SUPER_USER_EMAILS` match.

## Hard rules

- **One WorkOS environment per app environment** (dev, staging, production).
  Never configure an environment another app uses: read its redirect URIs first
  (`workos authkit redirect-uris list`); if they belong to another app
  (e.g. invoice-tool), stop and ask.
- **`set` replaces the whole list** (`redirect-uris set`, `logout-uris set`,
  `cors set`). Always list first and include the existing entries you keep.
- **Never print API keys, claim tokens or session tokens.** Filter CLI JSON
  (`sed -E 's/sk_[A-Za-z0-9_]+/sk_<hidden>/g'`, drop `apiKey`/`claimToken`
  fields). The CLI's own logs in `~/.workos/logs/` contain keys in plain text:
  never `cat` or `grep` them unfiltered.
- **Never run the bare installer** (`npx workos` / `npx workos install`) in a
  project without asking: it rewrites `.env.local` and `.gitignore` and creates
  its own environment.
- Claiming an environment is permanent; claiming and minting keys need the
  user (browser). Ask first.
- Apps run without `WORKOS_API_KEY` (public PKCE client). Don't add it to an app
  unless it needs WorkOS management APIs.

## Before every call

```sh
cd /tmp   # run the CLI outside the project
npx -y workos@latest whoami --json
```

Not logged in: `npx -y workos@latest auth login --mode agent --json` prints a
URL and a code (`https://signin.workos.com/device`). Show both to the user and
wait; the dashboard token is short-lived.

Two planes:
- **Dashboard plane** (`environment`, `authkit …`, `branding`): uses the login;
  target an environment with `--environment-id <id>`.
- **API plane** (`api`, `user`, `organization`, …): uses the **active profile's
  API key**. Check which environment that is before every write
  (`npx -y workos@latest profile list --json`): `environment use` can be
  "healed" back to the profile's original client ID.

## Per app environment

| Setting | Value |
| --- | --- |
| Redirect URI | `<SITE_URL>/callback` |
| Initiate login URI | `<SITE_URL>/sign-in` (dashboard) |
| Logout redirect | `<SITE_URL>/login` |
| CORS origin | `<SITE_URL>` (account page widgets) |
| JWT template | `{"email": {{ user.email }}, "email_verified": {{ user.email_verified }}}` (required: system-core needs a verified email) |
| Infisical `/` | `WORKOS_CLIENT_ID`, `WORKOS_COOKIE_PASSWORD` (`openssl rand -base64 32`) |
| Convex | `WORKOS_CLIENT_ID` (copied by `pnpm deploy:convex`; redeploy after changing it) |

## Command map

| Intent | Command |
| --- | --- |
| Environments (no client IDs in this output) | `npx -y workos@latest environment list --json` |
| Create an environment (ask first) | `npx -y workos@latest environment create "<app> staging" --sandbox --json` |
| Read URIs | `npx -y workos@latest authkit redirect-uris list --environment-id <id> --json` (also `logout-uris list`, `cors get`) |
| Set URIs (list first) | `npx -y workos@latest authkit redirect-uris set --environment-id <id> --uri <a> --uri <b> --default <a> --json` |
| JWT template (API plane) | `npx -y workos@latest api /user_management/jwt_template -X PUT -y --json -d '{"content":"{\"email\": {{ user.email }}, \"email_verified\": {{ user.email_verified }}}"}'` |
| New environment with keys for the CLI | `npx -y workos@latest profile provision --mode agent --json` (filter output), then `profile claim` gives the user a claim URL |
| Users | `npx -y workos@latest user list --json` |
| Sandbox test user (delete after) | `npx -y workos@latest api /user_management/users -X POST -y --json -d '{"email":"…","password":"…","email_verified":true}'` with the password read from a `umask 077` temp file |
| Diagnose an app | `npx -y workos@latest doctor` (read-only) |

Unclaimed (trial) environments send password sign-ins to `signin.workos.com`
and may expire: claim before relying on one.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| "Invalid client ID" on the WorkOS page | the app sends a placeholder or another environment's `WORKOS_CLIENT_ID` (check the `client_id` in `/sign-in`'s redirect) |
| redirect_uri error | `<SITE_URL>/callback` not in that environment's redirect URIs |
| Sign-in ends on `/login?state=jwt-template` | JWT template missing `email` / `email_verified` |
| `UNAUTHENTICATED` from `completeSignIn` with a verified email | identity mapping must read the raw `email_verified` claim (`convex/system.ts`) |
| Account widgets fail | site origin missing from CORS |
