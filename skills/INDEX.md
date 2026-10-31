# skills/ — index

Three stacks, organized by origin so each skill can be invoked by its
`name:` (the Skill tool matches the install dir). Restoring = copying a
group back into the sandbox's flat `skills/` dir (see RESTORE.md).

| group | count | source |
|---|---|---|
| `harness-ppc/` | 1 | authored in this sandbox (PPC loop) |
| `mattpocock/` | 31 | github.com/mattpocock/skills @  |
| `cursor/` | 58 | github.com/cursor/plugins `pstack` @ cursor/plugins 4dd1d05 2026-10-29, installed as `cursor-*` with internal refs rewritten |

Cross-reference audit (all strong calls resolve):
`download/skill-crossref-audit.md`.

## harness-ppc

- `harness-ppc` — "Harness-agnostic Propose-Probe-Compose (PPC) quality loop: improve the harness around the model (instructions, skills, scripts, output contracts) instead of the model, using behavioral-contrast evidence, blind selection, sealed ground-truth audit, and a persistent per-domain library. Use when the user asks to apply the harness workflow ('pakai harness loop', 'pakai workflow PPC', 'apply the harness template', 'optimize pakai PPC'), when migrating a previously adopted harness to new data in the same domain, or for any non-trivial task in a repeated domain where reliability matters."
- spec: `harness-template/PROTOCOL.md`; triggers: "pakai harness loop", "pakai workflow PPC"
## mattpocock/

| install dir | invoke as | description |
|---|---|---|
| `ask-matt` | `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. disable-model-invocation: true |
| `code-review` | `code-review` | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding stand |
| `codebase-design` | `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a se |
| `diagnosing-bugs` | `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `domain-modeling` | `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR. |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destru |
| `grill-me` | `grill-me` | A relentless interview to sharpen a plan or design. disable-model-invocation: true |
| `grill-with-docs` | `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. disable-model-invocation: true |
| `grilling` | `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| `handoff` | `handoff` | Compact the current conversation into a handoff document for another agent to pick up. argument-hint: "What will the next session be used for?" disable-model-in |
| `implement` | `implement` | "Implement a piece of work based on a spec or set of tickets." disable-model-invocation: true |
| `implement-spec` | `implement-spec` | "Implement the result of /to-spec and /to-tickets in code." disable-model-invocation: true |
| `improve-codebase-architecture` | `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. disable-model-invocation: true |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial te |
| `pr` | `pr` | "Use when writing a PR body." |
| `prototype` | `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a U |
| `research` | `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, d |
| `retro` | `retro` | "Conduct a retrospective on a coding session." disable-model-invocation: true |
| `scaffold-exercises` | `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exe |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the othe |
| `setup-pre-commit` | `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Hus |
| `tdd` | `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| `teach` | `teach` | Teach the user a new skill or concept, within this workspace. disable-model-invocation: true argument-hint: "What would you like to learn about?" |
| `to-questionnaire` | `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. disable-model-invocation: true |
| `to-spec` | `to-spec` | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed." disable- |
| `to-tickets` | `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edg |
| `triage` | `triage` | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. disable-model-invocatio |
| `wait-what` | `wait-what` | "Stop. That last message did not land: re-pitch it." disable-model-invocation: true |
| `wayfinder` | `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until |
| `wizard` | `wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI s |
| `writing-for-agents` | `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
## cursor/ (pstack, renamed)

| install dir | invoke as | description |
|---|---|---|
| `cursor-architect` | `cursor-architect` | "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /cursor-architect, 'architect this', ' |
| `cursor-arena` | `cursor-arena` | "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /cursor-arena, 'arena this', 'throw it in t |
| `cursor-automate-me` | `cursor-automate-me` | "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow h |
| `cursor-benchmark-checklist` | `cursor-benchmark-checklist` | "Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you  |
| `cursor-blast-radius` | `cursor-blast-radius` | "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of wri |
| `cursor-bro` | `cursor-bro` | Restate the last message in plain human language, with no jargon. disable-model-invocation: true |
| `cursor-correct` | `cursor-correct` | "Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, t |
| `cursor-create-formal-verification-skill` | `cursor-create-formal-verification-skill` | "Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verificati |
| `cursor-create-verification-skill` | `cursor-create-verification-skill` | "Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /cursor-create-verificatio |
| `cursor-figure-it-out` | `cursor-figure-it-out` | "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales  |
| `cursor-how` | `cursor-how` | "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which p |
| `cursor-in-your-own-words` | `cursor-in-your-own-words` | "Restate in your own words what you think the user's goals are and what problem they're trying to solve. Use for /cursor-in-your-own-words." disable-model-invoc |
| `cursor-interrogate` | `cursor-interrogate` | "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this ap |
| `cursor-ketchup` | `cursor-ketchup` | "Catch the user up on what changed in this chat since their last message, in plain words and small visuals. List every item waiting on them with what they need  |
| `cursor-ketchup-video` | `cursor-ketchup-video` | "Catch the user up like /cursor-ketchup, with a short subtitled video of slides for what happened and the waiting calls as text under it. Use for /cursor-ketchu |
| `cursor-maintain-formal-verification-skill` | `cursor-maintain-formal-verification-skill` | "Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness |
| `cursor-maintain-verification-skill` | `cursor-maintain-verification-skill` | "Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at |
| `cursor-make-bot-ui` | `cursor-make-bot-ui` | >- Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when |
| `cursor-no-comments` | `cursor-no-comments` | "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints." disable-model-invocation: true |
| `cursor-poteto-help` | `cursor-poteto-help` | Guides users through pstack setup, /cursor-poteto-mode, and picking the skill, playbook, or principle for a task. Type /cursor-poteto-help with a question. disa |
| `cursor-poteto-mode` | `cursor-poteto-mode` | poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /cursor-poteto-mode |
| `cursor-principle-attack-the-premise` | `cursor-principle-attack-the-premise` | "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that as |
| `cursor-principle-boundary-discipline` | `cursor-principle-boundary-discipline` | "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust inter |
| `cursor-principle-build-the-lever` | `cursor-principle-build-the-lever` | "Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, o |
| `cursor-principle-encode-lessons-in-structure` | `cursor-principle-encode-lessons-in-structure` | "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime c |
| `cursor-principle-exhaust-the-design-space` | `cursor-principle-exhaust-the-design-space` | "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side b |
| `cursor-principle-experience-first` | `cursor-principle-experience-first` | "Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough o |
| `cursor-principle-explain-the-number` | `cursor-principle-explain-the-number` | "Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. F |
| `cursor-principle-fix-root-causes` | `cursor-principle-fix-root-causes` | "Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is leg |
| `cursor-principle-foundational-thinking` | `cursor-principle-foundational-thinking` | "Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data str |
| `cursor-principle-guard-the-context-window` | `cursor-principle-guard-the-context-window` | "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not  |
| `cursor-principle-laziness-protocol` | `cursor-principle-laziness-protocol` | "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that so |
| `cursor-principle-make-operations-idempotent` | `cursor-principle-make-operations-idempotent` | "Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of  |
| `cursor-principle-migrate-callers-then-delete-legacy-apis` | `cursor-principle-migrate-callers-then-delete-legacy-apis` | "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatib |
| `cursor-principle-minimize-reader-load` | `cursor-principle-minimize-reader-load` | "Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller |
| `cursor-principle-model-the-domain` | `cursor-principle-model-the-domain` | "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files." disable-model-invocation: true |
| `cursor-principle-never-block-on-the-human` | `cursor-principle-never-block-on-the-human` | "Apply when tempted to ask 'should I do X?' on reversible work." disable-model-invocation: true |
| `cursor-principle-outcome-oriented-execution` | `cursor-principle-outcome-oriented-execution` | "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states wit |
| `cursor-principle-prove-it-works` | `cursor-principle-prove-it-works` | "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, |
| `cursor-principle-redesign-from-first-principles` | `cursor-principle-redesign-from-first-principles` | "Apply when integrating a new requirement into an existing design." disable-model-invocation: true |
| `cursor-principle-separate-before-serializing-shared-state` | `cursor-principle-separate-before-serializing-shared-state` | "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shar |
| `cursor-principle-sequence-verifiable-units` | `cursor-principle-sequence-verifiable-units` | "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verif |
| `cursor-principle-subtract-before-you-add` | `cursor-principle-subtract-before-you-add` | "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base." di |
| `cursor-principle-test-behavior-not-implementation` | `cursor-principle-test-behavior-not-implementation` | "Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when |
| `cursor-principle-type-system-discipline` | `cursor-principle-type-system-discipline` | "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semant |
| `cursor-recall` | `cursor-recall` | "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a  |
| `cursor-reflect` | `cursor-reflect` | Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user s |
| `cursor-setup-pstack` | `cursor-setup-pstack` | Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the ski |
| `cursor-sharpen` | `cursor-sharpen` | "Make a task deeper, not bigger, then rewrite the prompt. Use for /cursor-sharpen." disable-model-invocation: true |
| `cursor-show-me-your-work` | `cursor-show-me-your-work` | "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; comm |
| `cursor-statechart` | `cursor-statechart` | "Check a TLA+ model of a system that moves between states, such as a product flow, a protocol, or a service, and draw it as a Mermaid statechart. The report giv |
| `cursor-swarm` | `cursor-swarm` | "Fan out N parallel workers, drain them, and return one report. Use for /cursor-swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration." d |
| `cursor-tdd` | `cursor-tdd` | "Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target. Skip when the tes |
| `cursor-teach` | `cursor-teach` | "Explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use f |
| `cursor-technical-writing` | `cursor-technical-writing` | "Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /cursor-technic |
| `cursor-typescript-best-practices` | `cursor-typescript-best-practices` | TypeScript best practices. Use when reading or editing any .ts or .tsx file. |
| `cursor-unslop` | `cursor-unslop` | Cut AI tells from any writing. disable-model-invocation: true |
| `cursor-why` | `cursor-why` | "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and quer |
