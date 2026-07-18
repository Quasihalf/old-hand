---
name: old-hand
description: >-
  Always use Old Hand together with skill-creator or plugin-creator before
  creating or substantially redesigning a skill, plugin, agent, MCP server,
  automation, reusable workflow, developer tool, app, or product, even when the
  user did not ask for research. Run an external comparable-project search
  before asking non-blocking creator questions and before finalizing the initial stack,
  architecture, scope, benchmark, or scaffold. Also use it as a cross-cutting judgment
  layer when implementing, debugging, refactoring, reviewing, choosing
  dependencies, or starting an architecture or foundational dependency direction.
  Also use for "old-hand", "老程序员", "像老手一样写", "创建 skill", "做一个 skill",
  "create a skill", "build a plugin", "找类似开源项目", "借鉴开源项目", "不要过度设计",
  "YAGNI", prior-art, root-cause, or smaller-solution requests. Skip only purely
  mechanical edits and unrelated non-coding prose or general knowledge.
---

# Old Hand

Old Hand is mature engineering discipline, not personality roleplay. Use it to
make the change smaller after understanding the real problem, not to skip the
reading that makes a small change correct.

## Work with other skills

Keep Old Hand active when another coding skill provides the deeper procedure.
Follow that skill for its specialty; use Old Hand to control scope, reuse,
dependency cost, and solution size. Do not treat another skill as a substitute.
For a new reusable agent artifact, complete Old Hand's research gate before a
specialized creator skill begins design or scaffolding; then let that creator
skill lead artifact-specific mechanics.

## Route the task

- **New or substantially redesigned skill, plugin, agent, MCP server,
  automation, reusable workflow, or developer tool**: read
  `references/research-protocol.md`; complete its creation-research gate before
  design, scaffolding, or implementation, even when the user did not ask for
  research. For a clear target, make an external web or GitHub search the first
  substantive action after loading required skill instructions. Local skill or
  repository inspection can supplement that search but cannot replace it.
- **Project start, product direction, architecture, or foundational dependency
  choice**: read `references/research-protocol.md`; search for similar
  open-source projects when web/search tools are available.
- **Routine dependency choice**: apply the core habits first. Use the research
  protocol only when the choice establishes a new foundation or the user asks
  for prior-art comparison.
- **Small debug or bugfix**: read `references/debug-protocol.md`; let a more
  specialized debugging skill lead its procedure, and do not browse by default.
- **Code review, plan review, or over-engineering check**: read
  `references/review-protocol.md`.
- **Normal implementation**: apply the core habits below directly.

## Core habits

- Understand the real path before editing.
- Reuse local code before writing new code.
- Prefer standard library and native platform features before dependencies.
- Prefer already-installed dependencies before new dependencies.
- Delete or simplify before adding abstractions.
- Fix the root cause once, not the same symptom repeatedly.
- Add the smallest useful runnable check for non-trivial logic.
- When introducing a new dependency, include a short dependency receipt:
  requirement, local or platform options considered, selected dependency, and
  its cost or risk.
- Ask when scope is vague, too large, or missing a decision the code cannot
  answer.

## When to search

- Search proactively for new project, product, type, architecture, or
  foundational dependency directions.
- Treat creation or substantial redesign of a skill, plugin, agent, MCP server,
  automation, reusable workflow, or developer tool as project-start research.
  Do not wait for the user to say "search," "research," or "open source."
- A category-level request is enough to start. Tool or backend choice, target
  app, installation location, and exact feature scope are shortlist dimensions,
  not blocking questions; search broad variants before asking about them.
- When a web/search tool is available, only an external search completes the
  creation gate. Local skills, repositories, and model memory are supporting
  evidence, not a substitute.
- Before that initial search, do not commit to a stack, architecture, feature
  scope, benchmark, or scaffold location.
- A small correction, metadata edit, rename, or formatting change to an
  existing artifact is not creation research.
- For routine dependency choices, inspect local code, standard library,
  platform features, and installed dependencies before searching broadly.
- Do not search for ordinary small debug tasks.
- Search official docs only when current external API, library, security, legal,
  or platform behavior materially affects the fix.
- If no web/search tool exists, say so and continue with local reasoning.

## Output style

- Small fixes: put code or result first, then state what broke, the root cause,
  the fix, and the check run in one short line each. Do not collapse a
  non-trivial fix into a completion notice.
- Project-start research: include research summary, borrowed patterns, selected
  benchmark, minimal implementation direction, and next steps.
- Reviews: findings first, with concrete evidence.
- Keep receipts compact: include the dependency receipt only for a new
  dependency, and the root-cause receipt only for a non-trivial bug fix.
- Make key tradeoffs visible; do not narrate every thought.

## Boundaries

- Do not simplify away security, data integrity, accessibility basics, input
  validation at trust boundaries, error handling that prevents data loss, or
  explicit user requirements.
- Do not copy open-source code unless license/use has been explicitly reviewed
  and the user asks for that.
- Do not add abstractions, configuration, dependencies, or scaffolding "for
  later".
- Once the user confirms the full scope after clarification, implement that
  scope without re-litigating the simplification.
- Do not turn this into a persona performance.

## References

- Read `references/research-protocol.md` for project-start research and similar
  open-source project borrowing.
- Read `references/debug-protocol.md` for small debugging and root-cause fixes.
- Read `references/review-protocol.md` for review, plan critique, and
  over-engineering checks.
