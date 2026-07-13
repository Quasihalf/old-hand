# Implicit Skill-Creation Research Design

## Problem

`old-hand` v0.2.0 allows implicit invocation, but its trigger description uses
generic terms such as "new project" and "new type." In observed fresh Codex
tasks, a request equivalent to "帮我做一个剪辑视频的 skill" sometimes loaded
specialized creation skills without loading `old-hand`; another run read
`old-hand` but proceeded to clarification and design without web research.

The body cannot repair an under-trigger by itself because Codex reads that body
only after selecting the skill.

## Required Behavior

When the user asks Codex to create or substantially redesign a skill, plugin,
agent, MCP server, automation, reusable workflow, or developer tool:

1. Codex should implicitly select `old-hand` even when the prompt contains no
   words such as "search," "research," or "open source."
2. If the target is specific enough to form useful privacy-safe queries, Codex
   should research comparable skills and open-source projects before design,
   scaffolding, or implementation.
3. If the target is too vague to search responsibly, Codex may ask one or two
   blocking questions, then must research before design.
4. A specialized creator skill remains responsible for artifact-specific
   mechanics after the research gate; it does not replace `old-hand`.

The acceptance prompt is exactly:

```text
帮我做一个剪辑视频的 skill
```

A passing fresh task must read `old-hand`, initiate real web or GitHub search,
and only then begin design work.

## Non-Goals

- Do not force broad research for a typo, metadata-only edit, mechanical rename,
  or other small correction to an existing skill.
- Do not add a runtime search or scoring script.
- Do not add a global `AGENTS.md` routing rule; the published plugin must carry
  the portable behavior.
- Do not claim deterministic invocation rates from fixture files or one forward
  test.

## Implementation

- Rewrite the `SKILL.md` description around concrete creation and engineering
  contexts so skill discovery sees the missing trigger before body loading.
- Add a creation-research route and an explicit pre-design gate to `SKILL.md`.
- Add the same gate to `references/research-protocol.md` with the clear-target
  and vague-target branches.
- Add exact positive and near-miss negative fixtures plus a behavior case.
- Extend the standard-library validator and its regression tests so future
  edits cannot silently remove the trigger or gate.
- Update public documentation and publish the behavior change as `v0.2.1`.

## Verification

- Observe the new deterministic tests fail before implementation and pass after.
- Run all repository and official plugin/skill validators.
- Sync the canonical bundle to the local personal skill.
- Run the acceptance prompt in a fresh Codex task and inspect tool provenance.
- Push only after local checks pass; tag and release only after GitHub Actions
  passes on the final commit.
