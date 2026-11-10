---
name: business-module
description: >-
  Design and build a reusable business module for digimuza client apps
  (system-template): manifest, permissions, subroles, flags, Convex tables and
  functions, Next.js pages, LT/EN strings, tests. Use when the user asks to add
  a module or feature area (finance, CRM, documents, reporting…), or to make
  existing backend logic reusable.
---

# Reusable business module

A module is written once and installed in many client apps. Treat each one like
a library with a stable contract, not like app code.

## Rules

- **Stable contract.** The module ID and every permission ID
  (`module:object:action`) never change meaning. Add new IDs; deprecate old
  ones. Existing subroles never gain permissions automatically.
- **No client specifics.** No client names, domains, IDs or branches in module
  code. Per-client differences are configuration: env keys registered by the
  module, feature flags, roles composed from the module's subroles, brand.
- **Depend only on system-core's public API** (`@digimuza/system-core/*`) and
  the app's typed wrappers (`convex/system.ts`). No imports from another
  business module; declare `dependsOn` if you need one (it never grants its
  permissions).
- **Shared generic code goes to system-core**, changed only in
  https://github.com/digimuza/system-core (branch, PR, release; see the
  `convex` skill), not into the module or the app.
- **Server enforces, UI hints.** Every function guards with `requirePermission`
  first; pages use `requireSession({ permission })` and `<Can>`.
- Business modules register **disabled**; only Super enables them.

## Shape

A reusable module lives **in system-core** as a subpath export,
`@digimuza/system-core/<id>` (repo https://github.com/digimuza/system-core,
`src/<id>/index.ts`; `finance` is the reference). The app installs it; the UI
stays in the app, because each client styles it.

| Part | Where |
| --- | --- |
| Manifest: id, kind `business`, description, permissions, initial subroles, feature flags, config keys | system-core `src/<id>/index.ts`: `export const <id> = defineModule({…})` and a `<Id>Permissions` map |
| Tables | system-core: `export const <id>Tables = { … }` with an index for every query |
| Functions | system-core: `export function define<Id>(system: ConvexSystem)` returning guarded `queryGeneric` / `mutationGeneric` functions (guard → object checks → write → audit, typed IDs, `operationId` in results) |
| Package entry | `"./<id>"` in system-core `package.json` exports (the pack check covers every entry) |
| Tests | system-core `test/<id>-app/` (installed like a client app) + `test/<id>.test.ts` with convex-test |
| Docs | system-core README / INTEGRATION.md: purpose, type, public operations, data owner, config keys, permissions, initial subroles, flags, one success and one denial scenario |
| Install in an app | `modules/index.ts` (manifest), `convex/schema.ts` (`...<id>Tables`), `convex/<id>.ts` (`export const { … } = define<Id>(system)`) |
| Pages and strings | app: `app/app/<id>/` with `requireSession({ permission })`, shadcn components, keys `<id>.…` in `lib/i18n/messages.ts` (lt + en) |

## AI tools

A module exposes its actions to the AI assistant (`@digimuza/system-core/ai`)
with `defineAiTool`, in system-core next to its functions (`src/<id>/ai-tools.ts`,
exported as `<id>Tools`; `src/finance/ai-tools.ts` is the reference):

- id `module.verb_object` (`finance.list_invoices`); a description for the model.
- `permission` = the module's own permission, never `ai:chat:use`.
- Anything that writes sets `requiresApproval: true` (the user approves each call).
- The handler reuses the module's shared operations and **validates everything
  before its first write**: a failed handler's earlier writes are committed (the
  failure is returned, not thrown, so the audit survives).
- Agents and their tools live in the app's `convex/aiConfig.ts` (no `"use node"`);
  add `...<id>Tools` to the agent's `tools` there.

## Checklist

1. In system-core, on a `feature/DIG-…` branch: manifest with permissions and at least one read-only and one full subrole.
2. Tables with indexes for every query.
3. Functions: guard → object checks → write → audit, return `operationId`.
4. Agent support: accept `apiKey` where agents should act.
5. Pages, empty states and errors through `useAction` (toasts show the
   operation ID); all strings in both languages.
6. Tests: unauthenticated, forbidden, disabled module, happy path, audit.
   If the module has AI tools: permission filter, approval, validation before write.
   Before the PR, run the `module-verify` skill on the change.
7. system-core PR, release (`release/X.Y.Z` → npm `next`, `production` → `latest`); install in the app on the RC, ship on `latest`; `npx convex run system:registerSystem`.
8. Linear issue per module or change (`linear` skill).
