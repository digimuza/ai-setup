---
name: module-verify
description: >-
  Read-only verification that a change to a reusable business module (system-core
  `src/<id>/**`, its tests, or its install in an app) keeps the module contract
  from the `business-module` skill: stable permission IDs, guards on every
  function, client-neutral code, required tests, AI tool rules, docs. Use after
  editing a module and before its PR, when `definition-of-done` marks the
  business-module row, or when asked to check a module change.
---

# Module verify

Prove a business-module change keeps the contract in the `business-module`
skill. Load that skill first: it is the rulebook, this is the audit. Run as a
**read-only subagent** with a fresh context when your harness has one. Never
edit, commit, release, publish, or run anything against a deployment.

## Process

1. **Find the module(s).** From the argument, or from
   `git diff --name-only $(git merge-base HEAD origin/main)` under
   `src/<id>/`, `test/<id>*`, `modules/index.ts`, `app/app/<id>/`.
2. **Read the diff** and list: permissions, subroles, feature flags and config
   keys added / removed / renamed; functions added / removed; tables and
   indexes changed; AI tools added or changed; public exports changed.
3. **Contract checks** (cite `file:line` for each violation):
   - No permission ID or module ID was renamed or changed meaning; removals
     are deprecations, not deletions. No existing subrole gained a permission.
   - Every new query or mutation calls `requirePermission` first, then object
     checks, then the write, then the audit; results carry `operationId`.
   - Every query has an index; no full-table scans in the diff.
   - No client names, domains, IDs or branches anywhere in module code.
   - Imports only from `@digimuza/system-core/*` public paths; no import from
     another business module (a needed one is in `dependsOn`).
   - The module registers disabled.
   - AI tools: id `module.verb_object`; `permission` is the module's own, never
     `ai:chat:use`; every write has `requiresApproval: true`; the handler
     validates all input before its first write.
   - App side: pages call `requireSession({ permission })`; every new string
     has `lt` and `en` keys.
4. **Tests.** The six required cases exist for each new function:
   unauthenticated, forbidden, disabled module, happy path, audit, plus
   permission filter / approval / validation-before-write for AI tools. Run
   the repo's test command for the module (e.g. `pnpm test -- test/<id>`) and
   the typecheck; quote failing lines.
5. **Public surface.** A new subpath is in `package.json` `exports` and the
   pack check covers it. A changed export is additive, or the report says what
   breaks for installed apps.
6. **Docs.** README / INTEGRATION.md list the module's purpose, operations,
   config keys, permissions, initial subroles, flags, and one success and one
   denial scenario, matching the code.

## Output

1. **Module(s) and change summary.**
2. **Gate results:** command, pass / fail / skipped (why), key output line.
3. **Contract violations:** rule, `file:line`, fix.
4. **Missing tests:** function, missing case.
5. **Remaining steps before merge**, in order. Releasing system-core and
   installing in an app are the author's steps; list them, don't run them.
