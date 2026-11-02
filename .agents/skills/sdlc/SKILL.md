---
name: sdlc
description: >-
  Standard development lifecycle for delivering a feature or ticket end to end:
  intake, plan, spec, implement, and ship a PR. Use when the user says "sdlc",
  asks to run the full lifecycle, or hands over a Jira ticket to take from
  idea to merged PR.
---

# SDLC

Take one feature from a vague request to a merged PR in five phases. Each
phase writes one artifact to `.sdlc/<name>/`. The next phase reads that file,
not your memory of the conversation.

Phase 1 is the only one where you talk to the user. After the user confirms
the intake, do not contact them again until you send the final report: no
questions, no check-ins, no progress updates that wait for a reply. See
"Working alone". Since you cannot ask later, Phase 1 must settle everything
up front.

## Setup

1. **Name the work.** `<name>` is the Jira key plus a short slug, for example
   `PROJ-123-export-csv`. If there is no ticket, use a slug alone.
2. **Create a worktree.** Every feature starts in its own worktree on a new
   branch from the latest default branch:

   ```sh
   git fetch origin
   git worktree add ../<repo>-<name> -b <name> origin/main
   ```

   In T3 Code, start the thread in worktree mode instead. Never work on the
   default branch, and never reuse a worktree that has someone else's changes.
3. **Create `.sdlc/<name>/`** at the worktree root. Keep it out of Git by
   adding `.sdlc/` to `.git/info/exclude`, unless the repo already commits
   these artifacts.

### Resuming

If `.sdlc/<name>/` already exists, read every artifact in it and continue
from the first phase whose artifact is missing or incomplete. Do not redo
finished phases unless the user asks.

## Phase 1: Intake (with the user)

Goal: no open question remains that would change the result.

1. **Gather facts yourself.** Use the `jira` skill to read the ticket, its
   comments, linked issues, and acceptance criteria. Read the code the
   ticket touches. Never ask the user for something you can look up.
2. **Grill the user.** Use the `grilling` skill on the decisions the facts
   leave open: scope, edge cases, UX, data, rollout, what "done" means.
   Give a recommended answer with each question.
3. **Clear future blockers now.** Find out what would stop you later and
   ask about it while the user is still here:
   - **Proof:** how each acceptance criterion can be proven in this
     environment. Check that you can run the app, the tests, and any
     simulator or browser you need.
   - **Access:** credentials, env vars, test accounts, seed data, and
     third-party sandboxes. Check that they work, don't just ask about them.
   - **Risky actions:** migrations, feature flags, config outside the repo,
     anything that touches shared or production systems. Get a yes or no
     for each one.
   - **Fallbacks:** if a criterion can't be proven here, agree on what
     counts as enough proof (a fake, a recorded fixture, a manual check
     after merge).
4. **Write `INTAKE.md`** with these sections:
   - **Source**: ticket link and key, plus the user's original request.
   - **Goal**: one or two sentences, from the user's point of view.
   - **Acceptance criteria**: a checklist that can be tested.
   - **Proof and access**: how each criterion will be proven, and the
     access and fallbacks agreed in step 3.
   - **Decisions**: every question asked and the answer given.
   - **Out of scope**
   - **Assumptions**: anything you decided without the user. Keep this
     short.
5. **Confirm and hand off.** Show the user the acceptance criteria and the
   proof plan, and ask them to confirm. Tell them you won't contact them
   again until you report the finished PR.

**Done when** the user has confirmed `INTAKE.md`. Never start Phase 2
without that confirmation.

## Phase 2: Plan (alone)

Goal: decide how to build it and how you will prove it works.

1. Read `INTAKE.md` and explore the code it touches.
2. Use the `codebase-design` skill to design the modules: which modules
   change, what their interfaces are, and where the seams go. Prefer
   existing seams. Use as few new ones as you can.
3. Plan the testing before the code. Answer these in the plan:
   - Which seam each acceptance criterion is tested at.
   - Which commands prove it (the repo's CI checks, the test runner, running
     the app).
   - **Testing limits.** What you cannot test here: missing credentials,
     third-party services, devices, production-only data. For each limit,
     use the fallback agreed in `INTAKE.md`. If none was agreed, pick the
     strongest proof you can get and record the gap.
4. **Write `PLAN.md`** with these sections: approach, modules and
   interfaces, ordered steps (each small enough for one commit), test plan,
   testing limits, and risks.

**Done when** every acceptance criterion maps to a step and to a test.

## Phase 3: Spec (alone)

Goal: one document a reviewer can check the PR against.

Follow the `to-spec` template and rules for content, with these overrides:

- Base the spec on `INTAKE.md` and `PLAN.md`, not on a new interview.
- Do not check the seams with the user. They were settled in Phase 2.
- Write the spec to `.sdlc/<name>/SPEC.md`. Do not publish it to the issue
  tracker or add labels unless the user asked for that.

**Done when** each acceptance criterion in `INTAKE.md` appears in the spec's
user stories or testing decisions, and nothing in the spec contradicts the
intake. If you find a contradiction, the intake wins. Fix the spec.

## Phase 4: Implement (alone)

Goal: working code, with evidence for every change.

1. Work through the steps in `PLAN.md` in order. Make small commits.
2. For each behavior, write the test first when the repo has a test setup.
   Watch it fail, then make it pass.
3. Run the checks the repo's CI runs: typecheck, lint, tests.
4. For UI or runtime behavior, run the app and look at the result. Passing
   mocked tests do not prove the user experience works.
5. If the code has to differ from the plan, update `PLAN.md` or `SPEC.md`
   first, and add a line saying why.
6. **Write `EVIDENCE.md`**: one entry per acceptance criterion, with the
   command you ran and its output (trimmed), a test name, or a screenshot
   path, and whether it passed. Redact secrets. Phase 5 copies this into
   the PR, so write it in the shape "PR evidence" asks for.

**Done when** every acceptance criterion has evidence you saw yourself in
this session, or a recorded gap that explains why not, and all CI checks
pass locally.

## Phase 5: Ship (alone)

Use the `full-send` skill to take the branch to a merged PR. Running `sdlc`
gives the same permission as "full send". If the user asked you to stop
before merging, use `full-stop` instead.

- Phase 4 already covers full-send's "Finish the change" and "Prove it"
  steps. In place of its "Get feedback" step, run the two reviews in
  "Review" below. Then continue from "File the PR".
- The PR description must include the evidence. See "PR evidence" below.
  This replaces full-send's one-line proof note.
- Use the `jira` skill to move the ticket to the status that matches the PR,
  such as In Review, and then Done after the merge, if the project uses
  those statuses.

**Done when** the PR is merged (or ready, under `full-stop`) and you have
sent the final report from `full-send`, with a link to `.sdlc/<name>/`.

### Review

Commit all of the work first, so both reviewers see the same diff. Then
start two reviews at the same time, each in its own agent with a fresh
context. Neither agent sees your conversation.

1. **`sol-loop`**: GPT Sol reviews for bugs. Follow the `sol-loop` skill.
   Its reviewer runs as a separate delegate (`delegate_task` in T3 Code,
   a native Sol subagent elsewhere). In the brief, take the intent and
   out-of-scope from `INTAKE.md`.
2. **`code-review`**: checks the code against the repo's standards and
   the spec. Start a separate read-only agent that follows the
   `code-review` skill, with:
   - **Fixed point:** the merge-base with the PR's base branch, the same
     base Sol gets.
   - **Spec:** `.sdlc/<name>/SPEC.md`. Do not let it look elsewhere for a
     spec or ask the user for one.

   Tell it not to edit, commit, push, or comment.

You are the only one who edits code. Don't edit while either review is
running. When both report back:

- Check each finding yourself, using the rules in sol-loop's "Answer
  findings". Fix the findings that are real with the smallest change, and
  prove each fix before the next round.
- Run sol-loop's later rounds on the fixed code, within its budget. Run
  `code-review` once more only if a fix changed what the code does for the
  spec.
- Record every finding in `.sdlc/<name>/REVIEW.md`: which reviewer found
  it, severity, and outcome (fixed, declined with a reason, or disputed).

These replace the steps in `sol-loop` and `code-review` that ask the user:

- If a finding is still disputed after two replies, decide it yourself
  and record both sides. If the disputed finding is a blocker, do not
  merge. Leave the PR open, as in `full-stop`.
- If Sol is unavailable, do not swap in another model. Finish with
  `code-review` alone, note it in the report, and do not merge.
- Running `sdlc` counts as permission to push once the reviews end.

In the PR description, add the sol-loop line (`Reviewed with sol-loop:
...`) and one line for code-review: findings per axis and how each was
resolved.

### PR evidence

Write the description with the `file-pr` skill: a short problem and
solution first. Then add an `## Evidence` section built from `EVIDENCE.md`,
before the line that credits the model:

```md
## Evidence

Ticket: [PROJ-123](<link>)

| Acceptance criterion | Proof | Result |
| --- | --- | --- |
| Export button downloads a CSV | `ExportButton.test.tsx` "downloads csv"; ran app, screenshot below | ✅ |
| Empty table shows a message | `export.test.ts` "empty state" | ✅ |

**Checks run locally:** `pnpm typecheck`, `pnpm lint`, `pnpm test` (all passed)

<details><summary>Test output</summary>

<trimmed output>

</details>

<screenshots, when the change is visible>
```

- One row per acceptance criterion in `INTAKE.md`. Do not leave any out.
- Use only proof you saw yourself in this session. Never write ✅ for
  something you did not run.
- Trim the output to the lines that show the result. Redact secrets and
  private data.
- Attach screenshots for UI changes when you can upload them. Otherwise
  name the screenshot files in the table.
- If a criterion is not fully proven, mark it ⚠️ and say what is missing
  and why. Do not merge while any row is ⚠️. Use the `full-stop` behavior
  for that PR.
- When a review fix changes behavior, update the table and the output
  before you push, so the description always matches the latest commit.

## Working alone

After Phase 1 confirmation, do not message or ask the user anything until
the final report. This overrides "Asking the user" in `full-send`.

- Make every decision yourself with sensible defaults, and record it in
  the artifact for that phase.
- If you are blocked, take the safe path and keep going where you can:
  - Never take a risky action the user did not approve in `INTAKE.md`.
    Deleting data, touching production, and changing things outside the
    repo count as risky.
  - If you can't prove a criterion, or the merge gate can't pass, finish
    everything else. Leave the PR open and unmerged, with the gaps marked
    ⚠️ in the evidence table.
  - If the goal turns out to be ambiguous, choose the reading that best
    fits `INTAKE.md` and list it as a decision in the report.
- Put every blocker and open question at the top of the final report, with
  your recommendation for each.
- Harness approval prompts are outside your control. If one appears, it is
  not a question from you.

## Rules

- Write each artifact before you start the next phase. If an artifact and
  your memory disagree, trust the artifact.
- Keep scope to `INTAKE.md`. If you find something unrelated, note it in the
  final report. Do not fix it.
