---
name: sdlc
description: >-
  Standard development lifecycle for delivering a feature or ticket end to end:
  intake, plan, spec, implement, and ship a PR. Use when the user says "sdlc",
  asks to run the full lifecycle, or hands over a Linear issue (DIG-123) to take from
  idea to merged PR. Every run is tied to a DIG issue, moves it through
  In Progress and In Review, and babysits the PR until merged, including
  CodeRabbit comments.
---

# SDLC

Take one feature from a vague request to a merged PR in five phases. Each
phase writes one artifact to `.sdlc/<name>/`. The next phase reads that file,
not your memory of the conversation.

Setup and Phase 1 are the only places where you talk to the user. After the user confirms
the intake, do not contact them again until you send the final report: no
questions, no check-ins, no progress updates that wait for a reply. See
"Working alone". Since you cannot ask later, Phase 1 must settle everything
up front.

## Setup

1. **Settle the issue.** Every run has a DIG issue. Do this before anything
   else, with the `linear` skill:
   - **Key given** (in the request, branch name, or PR title): read it,
     assign it to yourself (`-a @me`) and move it to `In Progress`. If it is
     already assigned to someone else, ask the user before reassigning.
   - **No key given:** ask the user, with the harness's question tool,
     whether to **create an issue** or **use an existing key**. Do not start
     Phase 1 until one of the two has happened. To create one, draft the
     title and description from the request, show them, then create it with
     `-a @me -s "In Progress"`.
   Never invent a key and never run without one. If `linear` cannot reach
   Linear, stop and say so.
2. **Name the work.** `<name>` is the issue key plus a short slug, for
   example `DIG-123-export-csv`.
3. **Create a worktree.** Every feature starts in its own worktree on a new
   branch from the latest default branch:

   ```sh
   git fetch origin
   git worktree add ../<repo>-<name> -b feature/<name> origin/main
   ```

   In T3 Code, start the thread in worktree mode instead. Never work on the
   default branch, and never reuse a worktree that has someone else's changes.
4. **Create `.sdlc/<name>/`** at the worktree root. Keep it out of Git by
   adding `.sdlc/` to `.git/info/exclude`, unless the repo already commits
   these artifacts.

### Resuming

If `.sdlc/<name>/` already exists, read every artifact in it and continue
from the first phase whose artifact is missing or incomplete. Do not redo
finished phases unless the user asks. Re-read the issue and put its state
back in step with the phase you are in (`In Progress` before the PR exists,
`In Review` after).

## Phase 1: Intake (with the user)

Goal: no open question remains that would change the result.

1. **Gather facts yourself.** Use the `linear` skill to read the issue, its
   comments, related issues, and acceptance criteria. Read the code the
   issue touches. Never ask the user for something you can look up.
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
   - **Source**: Linear issue link and key (created or existing), its
     assignee and state after Setup, plus the user's original request.
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
4. **UI work goes through `impeccable`.** If the change adds or alters any
   screen, component, state or copy the user sees, run the `impeccable`
   skill: its `shape` command for a new surface or flow, otherwise note
   which command (`polish`, `layout`, `harden`, `clarify`, `adapt`…) Phase 4
   will run on which route. Record the surface's mode (usually Operate) and
   the design decisions in the plan.
5. **Write `PLAN.md`** with these sections: approach, modules and
   interfaces, ordered steps (each small enough for one commit), UI design
   (from step 4, or "no UI change"), test plan, testing limits, and risks.

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
3. Run the `definition-of-done` skill on the working tree: it classifies the
   change, runs the checks the repo's CI runs (typecheck, lint, tests,
   build), and lists the docs to update. Fix everything it marks as not
   done before Phase 5.
4. For UI or runtime behavior, run the app and look at the result. Passing
   mocked tests do not prove the user experience works.
   **Every UI change uses the `impeccable` skill**, every time, however small:
   run its context step, follow its craft floor while editing (shadcn/ui
   only, theme tokens, light and dark), finish with its `polish` pass and its
   detector on the changed files, and look at the rendered result at desktop
   and phone widths. Put the screenshots and the detector result in
   `EVIDENCE.md`.
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
- For a UI change, the PR evidence includes the screenshots (desktop and
  phone, light and dark where it differs) and the `impeccable` detector
  result.
- **As soon as the PR exists**, use the `linear` skill to move the issue to
  `In Review` and add a comment with the PR link. `In Staging` and `Done`
  follow the release cycle (release branch, then `production`); the release
  workflows set them, so do not set them yourself.
- **Babysit the PR** until it is merged. See "Babysit" below. Do not end
  your turn with checks or bot reviews pending.

**Done when** the PR is merged (or ready, under `full-stop`), the issue is
in `In Review` with the PR linked, and you have sent the final report from
`full-send`, with a link to `.sdlc/<name>/`.

### Babysit

Follow the `babysit-pr` skill (`watch_pull_request` in T3 Code, `pr-wait`
elsewhere) with these overrides:

- **CodeRabbit is not advisory here.** Wait for CodeRabbit to review the
  latest head, and handle every comment it leaves: fix the ones that are
  real with the smallest change and prove the fix before pushing, or reply
  with a written reason and resolve the thread. Use `leaving-pr-comments`
  for every reply. Do not merge while a CodeRabbit comment on the latest
  head is unanswered.
- After every push, wait for CI and CodeRabbit again. Repeat until the head
  has green checks and no open CodeRabbit or human threads.
- Human review comments are handled the same way. A human
  "changes requested" that you cannot resolve from `INTAKE.md` is a blocker:
  leave the PR open as in `full-stop` and put it at the top of the report.
- Keep the PR at the size `INTAKE.md` needs. Decline scope-growing bot
  suggestions with a reason and list them as follow-ups in the report
  (one related DIG issue each, with `linear issue relation add`).
- Record each PR comment and its outcome in `.sdlc/<name>/REVIEW.md`,
  under a "PR comments" heading, next to the sol-loop and code-review
  findings.
- When CodeRabbit does not review within a reasonable wait (it is not
  installed, or it is down), note that in the report and continue with the
  rest of the merge gate.

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

Issue: [DIG-123](<link>)

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
- Any UI work, in any phase or outside `sdlc`, uses the `impeccable` skill.
- Keep scope to `INTAKE.md`. If you find something unrelated, note it in the
  final report. Do not fix it.
- **Lessons outlive `.sdlc/`.** `.sdlc/` is not committed. When the work
  settles a decision or uncovers a trap the next change will hit (a
  convention, a flaky check, a gotcha in a tool), add one dated line to the
  repo's `docs/decisions.md` (create it if missing) in the same PR:
  `- <YYYY-MM-DD> (DIG-123): <decision or trap>. Why: <reason>.`
