# Implicit Skill-Creation Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make new reusable-agent artifact requests implicitly select `old-hand` and research comparable open-source work before design.

**Architecture:** Keep `skills/old-hand/` as the canonical bundle. Strengthen discovery in frontmatter, enforce the pre-design gate in the routed research protocol, preserve specialized creator skills for artifact mechanics, and guard the behavior with deterministic fixtures plus a fresh-task forward test.

**Tech Stack:** Markdown, YAML, JSON, Python 3 standard library, Codex CLI, GitHub Actions.

## Global Constraints

- The exact prompt `帮我做一个剪辑视频的 skill` must require no explicit research wording.
- Small mechanical edits to existing skills must remain negative triggers.
- No runtime search/scoring script or provider-specific dependency.
- Trigger fixtures remain design checks, not product invocation telemetry.
- Release version is `0.2.1`.

---

### Task 1: Deterministic Regression Gate

**Files:**
- Modify: `tests/test_validate.py`
- Modify: `scripts/validate.py`

**Interfaces:**
- Consumes: `validate_repository(root: Path) -> list[str]`
- Produces: validation errors when the explicit creation trigger or research-first gate is removed

- [ ] **Step 1: Add failing tests**

Add one test that removes creation artifact terms from the skill description
and one that removes the pre-design research gate. Each must expect a specific
validator error.

- [ ] **Step 2: Verify RED**

Run:

```sh
python3 tests/test_validate.py ValidateRepositoryTests.test_rejects_missing_creation_trigger ValidateRepositoryTests.test_rejects_missing_creation_research_gate -v
```

Expected: both tests fail because the current validator returns no matching
error.

- [ ] **Step 3: Implement the validator checks**

Use a single `RELEASE_VERSION = "0.2.1"` constant for manifest and fixture
checks. Require the frontmatter description to contain `skill`, `plugin`,
`agent`, `mcp`, and `workflow`, and require the research protocol to contain
the explicit pre-design gate.

- [ ] **Step 4: Verify GREEN**

Run the two tests again. Expected: both pass.

### Task 2: Trigger And Research Behavior

**Files:**
- Modify: `skills/old-hand/SKILL.md`
- Modify: `skills/old-hand/references/research-protocol.md`
- Modify: `evals/trigger-cases.json`
- Modify: `evals/evals.json`

**Interfaces:**
- Consumes: Codex skill discovery from frontmatter metadata
- Produces: implicit creation-task routing followed by research before design

- [ ] **Step 1: Rewrite the trigger description**

List creating or substantially redesigning skills, plugins, agents, MCP
servers, automations, workflows, tools, apps, products, and architectures as
concrete use contexts. Keep process details in the body.

- [ ] **Step 2: Add the pre-design gate**

Route creation tasks to `research-protocol.md` before specialized creator
procedures. Search immediately when the target is clear; otherwise ask no more
than two blocking questions before searching.

- [ ] **Step 3: Add fixtures**

Add the exact Chinese acceptance prompt and an English no-search-word prompt as
positive triggers. Add a metadata-only edit to an existing skill as a negative
trigger. Add a behavior case requiring source-backed research before design.

- [ ] **Step 4: Bump fixture versions**

Set plugin and fixture versions to `0.2.1` and update version assertions.

### Task 3: Public Documentation And Local Verification

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `examples/before-after.md`
- Create: `evals/reports/v0.2.1-review.md`

**Interfaces:**
- Consumes: implemented trigger and research gate
- Produces: accurate user-facing behavior and release evidence

- [ ] **Step 1: Document implicit creation research**

State that creation requests do not need explicit search wording and retain the
small-edit boundary.

- [ ] **Step 2: Run complete local validation**

Run the unit suite, repository validator, official plugin validator, official
skill validator, JSON parsing, Markdown link checks, and `git diff --check`.

- [ ] **Step 3: Sync and forward-test**

Sync the five canonical skill files to `~/.codex/skills/old-hand`. In a fresh
Codex task, submit the exact acceptance prompt and verify an `old-hand` read and
a real search call occur before design.

- [ ] **Step 4: Record evidence honestly**

Write the result and limitations to `evals/reports/v0.2.1-review.md`. Do not
turn one run into a statistical or cross-platform claim.

### Task 4: Publish v0.2.1

**Files:**
- Create: Git commit and annotated tag `v0.2.1`
- Create: GitHub Release `v0.2.1`

**Interfaces:**
- Consumes: final verified commit on `main`
- Produces: updated remote marketplace source and installed plugin

- [ ] **Step 1: Commit and push `main`**

Commit the scoped files, push, and wait for the final commit's GitHub Actions
run to succeed.

- [ ] **Step 2: Tag and release**

Create annotated tag `v0.2.1`, push it, wait for tag CI, and publish release
notes describing the trigger fix and evidence boundary.

- [ ] **Step 3: Reinstall and verify**

Re-add the GitHub marketplace if absent, install `old-hand@old-hand`, verify
version `0.2.1`, and perform a clean `CODEX_HOME` installation from `main`.
