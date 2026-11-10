---
name: docs-drift-check
description: >-
  Find statements in a repo's documentation that no longer match the code:
  README.md, INTEGRATION.md, AGENTS.md, CLAUDE.md, docs/*.md and
  .agents/skills/*/SKILL.md versus package.json scripts, CLI usage text, file
  paths, env keys, workflow steps and counts. Read-only; it reports, it does
  not rewrite. Use before a PR that changes scripts, env, workflows or public
  APIs, when a documented command or path turns out to be stale, or when
  `definition-of-done` asks which docs mention a change.
---

# Docs drift check

Find every statement a reader would act on that is no longer true, and report
it with the correction. Run this as a **read-only subagent** with a fresh
context when your harness has one (`Agent` in Claude Code, a native subagent
in Codex). Give it the repo path and, if there is one, the diff range. It does
not edit files.

## 1. Build the ground truth

- Scripts: `jq -r '.scripts | keys[]' package.json` (each workspace package too).
- CLI commands and flags: the `--help` / `usage()` text and argument parsers
  of anything under `scripts/` or `bin/`.
- Env keys: `env.ts`, `lib/server-env.ts`, `.env.example`, and
  `process.env.<KEY>` reads (`grep -rhoE 'process\.env\.[A-Z0-9_]+'`).
- Workflows: names, triggers and steps in `.github/workflows/*.yml`.
- Paths: everything that exists (`git ls-files`).
- Public API: `exports` in `package.json`, `src/*/index.ts`.
- Counts that docs quote (modules, permissions, tests, packages).

## 2. Extract the claims

From each document: every backticked command (`pnpm …`, `npx …`), flag
(`--foo`), file path, env key, workflow name, exported symbol, number, and
"currently / today / as of" statement. For skills, also every reference to
another skill (`` `<name>` skill ``): the skill must exist.

## 3. Verify

- Path: exists in `git ls-files` (or is clearly a placeholder like `<id>`).
- Script or flag: present in `package.json` or the usage text.
- Env key: read somewhere in code, and listed in `.env.example`.
- Count: matches the ground truth.
- Same fact stated in two documents: both say the same thing.
- New behaviour is documented: every script, env key and workflow appears in
  at least one document.

If the diff range is given, start with claims about what the diff touches,
then sweep the rest.

## Rules

- Report only actionable drift: a reader following the doc would fail or be
  misled. Style is out of scope.
- A fact with a date ("as of 2026-09-10") is not drift; flag it only when it
  is stated as timeless and is false.
- Sections labelled as history are not drift unless they present themselves
  as current.
- If a count needs a slow command (a full test run), report it as unverified
  instead of running it.

## Output

1. **Summary:** documents checked, claims verified, drift count by severity
   (breaks a command / misleads / factual but harmless).
2. **Drift per document**, most-read first (`README.md`, `AGENTS.md`/`CLAUDE.md`,
   skills, then the rest): `file:line`, the stale text, the evidence, the
   correction.
3. **Undocumented behaviour:** scripts, env keys, flags or workflow steps no
   document mentions.
4. **Verified consistent:** one line per document, so coverage is clear.
