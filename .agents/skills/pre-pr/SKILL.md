---
name: pre-pr
description: Run the definition-of-done checks on the current branch, read-only, and end with a mergeable / not-mergeable verdict. Use when the user says "pre-pr" or "/pre-pr".
disable-model-invocation: true
allowed-tools: Bash(git diff *), Bash(git status *), Bash(git log *), Bash(git merge-base *), Bash(git fetch *), Bash(git worktree *), Bash(pnpm typecheck), Bash(pnpm lint), Bash(pnpm test), Bash(pnpm build), Read, Grep, Glob
---

# Pre-PR

Load the `definition-of-done` skill and run all five of its sections on the
current branch and working tree.

Current state:

- Branch: !`git branch --show-current`
- Changed files vs main: !`git diff --name-status $(git merge-base HEAD origin/main 2>/dev/null || echo HEAD) | head -50`
- Uncommitted: !`git status --short | head -30`

Rules for this run:

1. Classify with the skill's table first and list the marked rows.
2. Run the checks one at a time. Paste failing lines verbatim. Separate
   failures the base also has from new ones.
3. Do the "what CI cannot catch" review on the diff.
4. List every document that mentions the changed commands, paths or
   behaviour, and whether it is already updated.
5. End with the verdict table and the exact remaining actions.

Do not edit files, commit, push, or run anything with `--write`, `--yes`, a
deploy, or a migration. $ARGUMENTS
