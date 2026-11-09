# ai-setup

Shared agent skills for AI-assisted development with T3 Code. The skills
live in `.agents/skills/`.

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
- Our stack: `nextjs` (main framework), `convex` (backend, written for reuse),
  `business-module` (reusable modules; shared logic goes to
  `@digimuza/system-core`), `workos` (AuthKit sign-in), `infisical` (secrets),
  `coolify` (hosting and deploys), `linear` (work tracking via the `linear` CLI).
