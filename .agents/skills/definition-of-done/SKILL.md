---
name: definition-of-done
description: >-
  Definition of done for a change in a digimuza app or system-core: classify
  what the diff touches, run the repo's CI checks, review what CI cannot
  catch, list the docs to update, and end with a mergeable / not-mergeable
  verdict. Use when the user asks "is this ready", "prepare a PR", "run the
  checks", "what do I need to update", or before committing or filing a PR;
  `sdlc` Phase 4 and `full-send` "Prove it" use it.
---

# Definition of done

Turns "run the checks CI runs" into a fixed sequence. Run everything from the
repo root. Report the actual output, including failures, never a summary of
it. Read-only: this skill never commits, pushes, or runs anything with
`--write`, `--yes`, a deploy, or a migration.

## 1. Classify the change

```sh
git fetch origin --quiet
base=$(git merge-base HEAD origin/main)
git diff --name-status "$base"   # committed
git status --short               # uncommitted and untracked
```

Mark every row whose path matches. Each marked row adds its steps. When a
path belongs to a stack area, also load that area's skill (`nextjs`,
`business-module`, …) and apply its "Checks" or "Checklist" section.

| Touches | Extra steps |
| --- | --- |
| `app/**`, `components/**` (anything the user sees) | `impeccable` context step, `polish` and detector on the changed files; screenshots at desktop and phone widths, light and dark |
| `lib/i18n/messages.ts` or any new user-facing string | every key exists in both `lt` and `en`; no hard-coded strings in the diff |
| A business module (system-core `src/<id>/**`, or `modules/index.ts` in an app) | `business-module` checklist: permissions and subroles, the six required tests, AI tool rules; run the `module-verify` skill |
| `package.json` exports, `src/*/index.ts` in system-core | the public API changed: the pack check passes, the change is additive or the PR says what breaks |
| `env.ts`, `lib/server-env.ts`, `.env.example` | every new key is in `.env.example` and the README env table; no value committed |
| `.github/workflows/**` | permissions and triggers unchanged unless intended; README workflow section updated |
| `scripts/**`, CLI code | `--help` / usage text matches the flags; README command table updated |
| Tests only | they fail without the change they guard (or say why that cannot be shown) |

## 2. Run the checks

Find the commands in the repo, do not guess them: the CI workflow under
`.github/workflows/` first, then the `package.json` scripts. A typical app
runs:

```sh
pnpm typecheck
pnpm lint
pnpm test
pnpm build
```

Run them one at a time so the failing one is unambiguous. Paste failing lines
verbatim.

**Pre-existing failures.** If a check fails, check whether the base fails the
same way. Do not stash; use a worktree:
`git worktree add --detach /tmp/dod-base "$base"`, link `node_modules`, run the
check there, then `git worktree remove /tmp/dod-base`. A change may not add
failures. List pre-existing ones separately and say they remain.

## 3. Review what CI cannot catch

- The diff contains only the intended change: no stray files, debug output,
  `.env`, lockfile churn without a dependency change, or unrelated reformat.
- No secrets, tokens, client names, client domains or client IDs (system-core
  and modules must stay client-neutral).
- Renamed or removed exports, permissions, routes or env keys: every caller
  updated (`grep -rn` the old name). Permission IDs never change meaning.
- Every behaviour change has evidence you saw this session: a test that
  failed first, or a run of the app.
- The PR stays one thing: refactors, dependency bumps and the feature are
  separate commits at least, separate PRs when large.

## 4. Docs in the same change

- `README.md`, `INTEGRATION.md`, command and env tables, counts.
- Any skill (`.agents/skills/*/SKILL.md`) or `AGENTS.md` / `CLAUDE.md` line
  that describes the changed behaviour.
- `docs/decisions.md`: one dated line for a decision or trap the next change
  will hit.

Run the `docs-drift-check` skill when unsure which documents mention the
changed command, path or behaviour.

## 5. Verdict

End with:

```md
**Verdict:** mergeable | not mergeable
| Check | Result | Key line |
| --- | --- | --- |
| pnpm typecheck | pass | |
| pnpm test | FAIL (new) | `export.test.ts > empty state: expected …` |

**Remaining:** exact commands or edits, in order.
```

"Mergeable" needs every check passing or failing only as it does on the base,
every marked row's steps done, and no open item in section 3.

## Guardrail: pre-push hook

A repo with no hook and no CI job for its checks is a finding (see `retro`).
[scripts/pre-push](scripts/pre-push) is a template that runs the same checks
before every push and **fails only on failures the base does not have**, so it
works in repos with existing lint debt. Install it in the target repo:

```sh
mkdir -p .githooks && cp <skills>/definition-of-done/scripts/pre-push .githooks/pre-push
chmod +x .githooks/pre-push
git config core.hooksPath .githooks   # or a "prepare" script in package.json
```

Edit its `CHECKS` list to match the CI workflow. Bypass once with
`SKIP_PRE_PUSH=1 git push` or `git push --no-verify`, and say so when you do.
