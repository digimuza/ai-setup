---
name: convex
description: >-
  Convex backend work in digimuza apps: functions, schema, env, local dev,
  deploys, tests, and the @digimuza/system-core patterns. Use when the user
  mentions Convex, a query/mutation/action, the schema, `npx convex`, the
  Convex dashboard, registerSystem, or backend logic. Backend code must be
  reusable across client apps.
---

# Convex

Every client app is Next.js + Convex on `@digimuza/system-core`. Backend logic
is written **for reuse**: the same module ships to many client apps.

## Hard rules

- **Write for reuse, not for one client.** Business logic lives in a module
  (see the `business-module` skill), not in a client's app code. No client
  names, hard-coded IDs, or one-off branches in backend code; differences
  between clients are configuration (env schema, feature flags, roles).
- **Generic logic belongs in system-core.** If code is not specific to one
  business module (access checks, audit, jobs, config, pagination helpers,
  identity mapping), put it in `@digimuza/system-core` (repo
  `~/Projects/digimuza/system-core`) through its own branch, PR and release
  (`next` from release branches, `latest` from production), then bump the app.
  Don't copy shared helpers between apps.
- **Every public function checks access on the server, first.** Use the app's
  `requirePermission(ctx, "module:object:action", { apiKey })` from
  `convex/system.ts` (typed wrapper; also enforces a Super's role view), then
  object-level checks, then the write, then `recordAudit(sys, actor, …)`,
  all in one mutation. Return `{ …, operationId: sys.operationId }`.
- Throw errors as `toConvexError(new SystemError(code, …))` with a stable code
  (`UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION`, `CONFLICT`,
  `UNAVAILABLE`). A record the actor may not see is `NOT_FOUND`, same as
  missing.
- Never deploy staging or production by hand: CI does it (`pnpm deploy:convex`
  in `release.yml` / `production.yml`). Never run anything with `--prod`
  without asking.
- Never print env values (`convex env list` shows names and values: don't).

## Before every call

- Use the project's CLI: `pnpm exec convex …` (or `npx convex …`) from the
  repo root.
- Local dev: `npx convex dev`. In an agent session with no login, use a local
  anonymous backend: `CONVEX_AGENT_MODE=anonymous npx convex dev`. It runs in
  the background; restart it when it stops. Codegen and pushes need it running.
- `convex/_generated/` is committed. Regenerate with `npx convex dev --once` or
  `npx convex codegen` after changing functions or schema, and commit it.

## Patterns (system-template)

| Need | Pattern |
| --- | --- |
| Tables | `systemTables` + module tables spread into `convex/schema.ts`; indexes for every lookup, no table scans in hot paths |
| Guard | `const { sys, actor } = await requirePermission(ctx, Perm.approve, args)` |
| Feature flag | `await isFeatureEnabled(sys, "module:flag")` *in addition to* the permission; a flag never grants access |
| Background job | store `toActorRef(actor)`; at run time `authorizeJob(sys, ref, permission)`, do nothing on `null`; external side effects via `claimOperation` / `completeOperation` |
| Agents | functions accept `apiKey` (`v.optional(v.string())`) and pass it to `requirePermission`; agents never act as Super |
| Catalog | after adding a module, permission or subrole: `npx convex run system:registerSystem` (CI does it on deploy). Idempotent; conflicts abort atomically |
| Env in functions | read keys **by name** (`process.env.KEY`); Convex's `process.env` is not enumerable. Validate with the Zod schema in `env.ts` (`getConvexEnv()`) |
| Auth | `convex/auth.config.ts` trusts WorkOS tokens via `WORKOS_CLIENT_ID`; it's read at push, so changing it needs a redeploy. Custom JWT claims arrive raw (`identity.email_verified`, not `emailVerified`) |
| Typed ctx | call system-core through the wrappers in `convex/system.ts` (`requirePermission`, `systemContext`): generated `QueryCtx` isn't assignable to system-core's `DbCtx` |

## Command map

| Intent | Command |
| --- | --- |
| Dev backend | `npx convex dev` (agents: `CONVEX_AGENT_MODE=anonymous npx convex dev`) |
| Push once / codegen | `npx convex dev --once --typecheck disable` · `npx convex codegen` |
| Run a function | `npx convex run system:registerSystem` · `npx convex run module:fn '{"arg":1}'` |
| Logs | `npx convex logs` (`--history N`, `--jsonl`) |
| Read data | `npx convex data <table> --limit 20` |
| Env names | `npx convex env list` only if you redact values; set with stdin: `printf '%s' "$v" \| npx convex env set NAME` |
| Deploy (CI only) | `pnpm deploy:convex` (env from Infisical `/` + `/ci`, `convex deploy`, `registerSystem`) |

## Tests

`convex-test` with the module map in `convex/test.setup.ts`. Cover for every
guarded function: anonymous → `UNAUTHENTICATED`, missing permission →
`FORBIDDEN`, module disabled, the happy path, and the audit record. Identities
in tests use the real token shape (`subject`, `issuer`, `email`,
`email_verified`).
