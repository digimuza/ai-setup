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
- **Shared generic code goes to system-core**, through its repo, PR and
  release, not into the module or the app (see the `convex` skill).
- **Server enforces, UI hints.** Every function guards with `requirePermission`
  first; pages use `requireSession({ permission })` and `<Can>`.
- Business modules register **disabled**; only Super enables them.

## Shape

Keep everything a module owns together and easy to copy:

| Part | Where (system-template) |
| --- | --- |
| Manifest: id, kind `business`, description, permissions, initial subroles, feature flags, config keys | `modules/<id>.ts` (`defineModule`), listed in `modules/index.ts` |
| Tables (spread into the schema) | `convex/schema.ts` → move into an exported `<id>Tables` object as the module grows |
| Functions | `convex/<id>.ts` (Convex needs functions under `convex/`); keep the logic in plain functions that take `(ctx, sys, actor, args)` so another app can re-export them |
| Config | a Zod schema for the module's keys, registered with `SystemConfig.register(schema, { moduleId: "<id>" })` / validated in Convex |
| Pages | `app/app/<id>/` with `requireSession({ permission })`; components from `components/ui` + `components/app` |
| Strings | `lib/i18n/messages.ts`, keys prefixed with the module (`<id>.…`), both `lt` and `en` |
| Tests | `convex/<id>.test.ts` with convex-test |
| Docs | purpose, type, public operations, data owner, config keys, permissions, initial subroles, flags, one success and one denial scenario (system-core README contract) |

## Checklist

1. Manifest with permissions and at least one read-only and one full subrole.
2. Tables with indexes for every query.
3. Functions: guard → object checks → write → audit, return `operationId`.
4. Agent support: accept `apiKey` where agents should act.
5. Pages, empty states and errors through `useAction` (toasts show the
   operation ID); all strings in both languages.
6. Tests: unauthenticated, forbidden, disabled module, happy path, audit.
7. `npx convex run system:registerSystem` locally; README module section.
8. Linear issue per module or change (`linear` skill).
