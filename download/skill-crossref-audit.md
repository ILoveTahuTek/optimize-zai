# Skill cross-reference audit

Scope: 90 audited skills out of 169 installed · RESOLVED 388 · SELF 33 · EXTERNAL 10 · **BROKEN 0** · **UNKNOWN 3**

Only strong call patterns are audited: `/name` (when the name is a cataloged skill), `**name**`, `the name skill`, `Skill(command="name")`, `pstack:name`. Ordinary paths and prose are ignored.

## Summary

| skill | RESOLVED | SELF | EXTERNAL | BROKEN | UNKNOWN |
|---|---:|---:|---:|---:|---:|
| ask-matt | 68 | 0 | 0 | 0 | 0 |
| code-review | 1 | 0 | 0 | 0 | 0 |
| codebase-design | 0 | 0 | 0 | 0 | 0 |
| cursor-architect | 19 | 3 | 0 | 0 | 0 |
| cursor-arena | 4 | 1 | 0 | 0 | 0 |
| cursor-automate-me | 4 | 0 | 0 | 0 | 0 |
| cursor-benchmark-checklist | 0 | 0 | 0 | 0 | 0 |
| cursor-blast-radius | 0 | 0 | 0 | 0 | 0 |
| cursor-bro | 0 | 0 | 0 | 0 | 0 |
| cursor-correct | 0 | 1 | 0 | 0 | 0 |
| cursor-create-formal-verification-skill | 2 | 1 | 0 | 0 | 0 |
| cursor-create-verification-skill | 1 | 1 | 0 | 0 | 0 |
| cursor-figure-it-out | 12 | 1 | 0 | 0 | 0 |
| cursor-how | 1 | 0 | 0 | 0 | 0 |
| cursor-in-your-own-words | 0 | 1 | 0 | 0 | 0 |
| cursor-interrogate | 2 | 0 | 0 | 0 | 0 |
| cursor-ketchup | 1 | 2 | 0 | 0 | 0 |
| cursor-ketchup-video | 2 | 2 | 0 | 0 | 0 |
| cursor-maintain-formal-verification-skill | 2 | 1 | 0 | 0 | 1 |
| cursor-maintain-verification-skill | 2 | 1 | 0 | 0 | 1 |
| cursor-make-bot-ui | 0 | 0 | 0 | 0 | 0 |
| cursor-no-comments | 6 | 1 | 0 | 0 | 0 |
| cursor-poteto-help | 126 | 2 | 3 | 0 | 0 |
| cursor-poteto-mode | 77 | 2 | 7 | 0 | 0 |
| cursor-principle-attack-the-premise | 4 | 0 | 0 | 0 | 0 |
| cursor-principle-boundary-discipline | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-build-the-lever | 3 | 0 | 0 | 0 | 0 |
| cursor-principle-encode-lessons-in-structure | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-exhaust-the-design-space | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-experience-first | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-explain-the-number | 2 | 0 | 0 | 0 | 0 |
| cursor-principle-fix-root-causes | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-foundational-thinking | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-guard-the-context-window | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-laziness-protocol | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-make-operations-idempotent | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-migrate-callers-then-delete-legacy-apis | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-minimize-reader-load | 1 | 0 | 0 | 0 | 0 |
| cursor-principle-model-the-domain | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-never-block-on-the-human | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-outcome-oriented-execution | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-prove-it-works | 1 | 0 | 0 | 0 | 0 |
| cursor-principle-redesign-from-first-principles | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-separate-before-serializing-shared-state | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-sequence-verifiable-units | 2 | 0 | 0 | 0 | 0 |
| cursor-principle-subtract-before-you-add | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-test-behavior-not-implementation | 0 | 0 | 0 | 0 | 0 |
| cursor-principle-type-system-discipline | 2 | 0 | 0 | 0 | 0 |
| cursor-recall | 4 | 0 | 0 | 0 | 0 |
| cursor-reflect | 2 | 1 | 0 | 0 | 0 |
| cursor-setup-pstack | 2 | 1 | 0 | 0 | 0 |
| cursor-sharpen | 0 | 1 | 0 | 0 | 0 |
| cursor-show-me-your-work | 3 | 1 | 0 | 0 | 0 |
| cursor-statechart | 0 | 1 | 0 | 0 | 0 |
| cursor-swarm | 1 | 1 | 0 | 0 | 0 |
| cursor-tdd | 0 | 0 | 0 | 0 | 0 |
| cursor-teach | 1 | 0 | 0 | 0 | 0 |
| cursor-technical-writing | 1 | 1 | 0 | 0 | 1 |
| cursor-typescript-best-practices | 5 | 0 | 0 | 0 | 0 |
| cursor-unslop | 0 | 0 | 0 | 0 | 0 |
| cursor-why | 1 | 1 | 0 | 0 | 0 |
| diagnosing-bugs | 0 | 0 | 0 | 0 | 0 |
| domain-modeling | 0 | 0 | 0 | 0 | 0 |
| git-guardrails-claude-code | 0 | 0 | 0 | 0 | 0 |
| grill-me | 0 | 0 | 0 | 0 | 0 |
| grill-with-docs | 0 | 0 | 0 | 0 | 0 |
| grilling | 0 | 0 | 0 | 0 | 0 |
| handoff | 0 | 0 | 0 | 0 | 0 |
| harness-ppc | 0 | 0 | 0 | 0 | 0 |
| implement | 0 | 0 | 0 | 0 | 0 |
| implement-spec | 5 | 0 | 0 | 0 | 0 |
| improve-codebase-architecture | 4 | 0 | 0 | 0 | 0 |
| migrate-to-shoehorn | 0 | 0 | 0 | 0 | 0 |
| pr | 0 | 0 | 0 | 0 | 0 |
| prototype | 0 | 1 | 0 | 0 | 0 |
| research | 0 | 0 | 0 | 0 | 0 |
| retro | 0 | 0 | 0 | 0 | 0 |
| scaffold-exercises | 0 | 0 | 0 | 0 | 0 |
| setup-matt-pocock-skills | 9 | 0 | 0 | 0 | 0 |
| setup-pre-commit | 0 | 0 | 0 | 0 | 0 |
| tdd | 0 | 0 | 0 | 0 | 0 |
| teach | 0 | 1 | 0 | 0 | 0 |
| to-questionnaire | 0 | 0 | 0 | 0 | 0 |
| to-spec | 1 | 0 | 0 | 0 | 0 |
| to-tickets | 2 | 0 | 0 | 0 | 0 |
| triage | 1 | 2 | 0 | 0 | 0 |
| wait-what | 0 | 0 | 0 | 0 | 0 |
| wayfinder | 1 | 0 | 0 | 0 | 0 |
| wizard | 0 | 1 | 0 | 0 | 0 |
| writing-for-agents | 0 | 0 | 0 | 0 | 0 |

## Broken references (pre-rename pstack name or missing target — must fix)

(none)

## Unknown references (strong call, but not installed and not known-external)

- **cursor-maintain-formal-verification-skill** SKILL.md:9 `project-local` — A formal check proves a property of what it describes. When the code changes and the verification do
- **cursor-maintain-verification-skill** SKILL.md:25 `project-local` — 0. **Locate the target.** Find the verification skill to maintain: the project-local skill whose bod
- **cursor-technical-writing** SKILL.md:35 `how-to` — - Action + work: **how-to**.

## External references (other plugin / built-in / agent — unavailable in this sandbox by design)

- **cursor-poteto-help** SKILL.md:46 `pstack:poteto-mode` — pstack is built for Cursor, and it also installs in Claude Code with `/plugin marketplace add cursor
- **cursor-poteto-help** SKILL.md:116 `deslop` — - `/deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` plugin.
- **cursor-poteto-help** SKILL.md:117 `create-skill` — - `/loop` and `/create-skill` are Cursor built-ins.
- **cursor-poteto-mode** SKILL.md:27 `create-skill` — - Any prose surface, your reply to the user included → the **cursor-unslop** skill. Write the reply 
- **cursor-poteto-mode** SKILL.md:29 `deslop` — - Before commit → the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`).
- **cursor-poteto-mode** playbooks/authoring-a-skill.md:5 `create-skill` — 1. Use the **create-skill** skill (Cursor's built-in for authoring SKILL.md files).
- **cursor-poteto-mode** playbooks/autopilot-full.md:10 `deslop` — Open the PR early so CI and bots run alongside the work. The code is ready only after the slop-strip
- **cursor-poteto-mode** playbooks/multi-phase-plan.md:59 `deslop` — - [ ] Run `/deslop` before each commit and `/cursor-no-comments` before review.
- **cursor-poteto-mode** playbooks/opening-a-pr.md:9 `deslop` — **PRs.** Run `/deslop` from `cursor-team-kit` over the diff before commit and `/cursor-no-comments` 
- **cursor-poteto-mode** playbooks/opening-a-pr.md:34 `deslop` — A subagent that opens a PR runs `/deslop` and `/cursor-no-comments`, and posts the URL. It returns t

## Notes

- pstack was installed as `cursor-*` (58 skills); internal refs were rewritten by `scripts/transform_pstack_refs.py`, then audited here.
- EXTERNAL deps of the original stacks: `deslop`/`babysit`/`bugbot`/`create-skill` (Cursor built-ins or cursor-team-kit plugin), `poteto-agent`/`comment-sicko` (pstack agents/), `pstack:*` (Claude Code adapter command style). The affected steps need those hosts; everything else works in this sandbox.
- mattpocock set and harness-ppc are referenced with their installed names; all their strong refs resolve.
