# ai-setup

Shared agent skills for AI-assisted development with T3 Code. The skills
live in `.agents/skills/`.

## Install

Codex and T3 Code read `.agents/skills/` in a repo. Claude Code reads
`.claude/skills/`, so link it in the target repo (a real symlink, committed as
one):

```sh
cp -R <ai-setup>/.agents/skills <repo>/.agents/
mkdir -p <repo>/.claude && ln -s ../.agents/skills <repo>/.claude/skills
```

Check that it resolves: `ls <repo>/.claude/skills/sdlc/SKILL.md`.

## Checks

`scripts/check-skills` lints every skill: frontmatter `name` matches the
directory, every referenced skill exists, relative links resolve, bundled
scripts are executable. CI (`.github/workflows/check.yml`) runs it with the
`babysit-pr` tests and a shell syntax check. Run it before committing a skill
change. A skill installed from elsewhere (`impeccable`) goes in its
`EXTERNAL` set.

## Credits

Most of these skills come from two open-source collections. Thank you to
their authors.

- **[t3dotgg/tstack](https://github.com/t3dotgg/tstack)** by Theo Browne (MIT):
  `babysit-pr`, `council`, `file-pr`, `full-send`, `full-stop`,
  `leaving-pr-comments`, `modernize`, `sol-loop`, `takeover`
- **[mattpocock/skills](https://github.com/mattpocock/skills/tree/main)** by
  Matt Pocock (MIT): `code-review`, `codebase-design`, `diagnosing-bugs`,
  `grill-me`, `grilling`, `retro`, `to-spec`, `wizard`

Written for this repo:

- `sdlc`: ties together skills from both collections into one lifecycle.
- Process: `definition-of-done` (classify a change, run its checks, give a
  merge verdict; ships a `pre-push` hook template that fails only on findings
  the base doesn't have), `pre-pr` (read-only run of it, user-invoked),
  `docs-drift-check` (docs vs code), `module-verify` (business-module
  contract audit). The process ideas come from First Horizon's
  transmit-infrastructure repo.
- Our stack: `nextjs` (main framework), `convex` (backend, written for reuse),
  `business-module` (reusable modules; shared logic goes to
  `@digimuza/system-core`), `workos` (AuthKit sign-in), `infisical` (secrets),
  `coolify` (hosting and deploys), `linear` (work tracking via the `linear` CLI).
