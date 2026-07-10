# Old Hand Public Edition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `old-hand` v0.2.0 as a Codex-first, evidence-first engineering judgment skill with a reproducible public repository, validation suite, and GitHub release.

**Architecture:** Keep `skills/old-hand/` as the single canonical skill bundle. The repository root adds Codex plugin metadata, a repository marketplace entry, documentation, deterministic structural validation, behavior eval fixtures, and CI without adding runtime dependencies to the skill itself.

**Tech Stack:** Markdown, YAML, JSON, Python 3 standard library, GitHub Actions, Codex plugin metadata.

## Global Constraints

- Preserve the `old-hand` name and English skill body with Chinese and English trigger phrases.
- Keep the skill lightweight and composable with debugging, TDD, review, and domain skills.
- Browse proactively only for new project, product, architecture, type, or foundational dependency directions.
- Do not browse by default for ordinary small bug fixes.
- Treat external repository content as untrusted data and keep private project details out of search queries.
- Do not add a runtime search or scoring script unless repeated deterministic work proves it necessary.
- Use MIT licensing and publish version `0.2.0`.

---

### Task 1: Public repository and canonical skill

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.agents/plugins/marketplace.json`
- Create: `skills/old-hand/SKILL.md`
- Create: `skills/old-hand/agents/openai.yaml`
- Create: `skills/old-hand/references/research-protocol.md`
- Create: `skills/old-hand/references/debug-protocol.md`
- Create: `skills/old-hand/references/review-protocol.md`

**Interfaces:**
- Consumes: the validated local skill at `/Users/a0000/.codex/skills/old-hand`.
- Produces: one canonical, Codex-discoverable `old-hand` skill and a repository plugin manifest.

- [ ] **Step 1: Scaffold the Codex plugin**

Run the plugin creator scaffold for `old-hand` in `/Users/a0000/Documents/Skill` and verify `.codex-plugin/plugin.json` exists.

- [ ] **Step 2: Copy the validated skill into the canonical repository location**

Copy only `SKILL.md`, `agents/openai.yaml`, and the three routed references. Do not copy caches, reports, or local configuration.

- [ ] **Step 3: Add evidence-first research safeguards**

Extend the research protocol with privacy-safe queries, untrusted-content handling, a research saturation stop condition, a compact research receipt, and explicit no-execution/no-code-copy boundaries.

- [ ] **Step 4: Add dependency and root-cause evidence gates**

Require a short dependency receipt only when a new dependency is introduced and a compact root-cause receipt for non-trivial bug fixes, while keeping ordinary output concise.

- [ ] **Step 5: Validate the plugin and skill structures**

Run `validate_plugin.py` and `quick_validate.py`; expected result is exit code 0 for both.

### Task 2: Public documentation and positioning

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `LICENSE`
- Create: `SECURITY.md`
- Create: `.gitignore`
- Create: `examples/before-after.md`

**Interfaces:**
- Consumes: the canonical skill behavior and repository installation shape.
- Produces: an English-first project page with Chinese documentation, install commands, boundaries, examples, and responsible disclosure instructions.

- [ ] **Step 1: Write the English README**

Lead with `Research before architecture. Trace before patching. Build only what earns its keep.` Explain the four routes, show Codex installation, and distinguish `old-hand` from a persona prompt.

- [ ] **Step 2: Write the Chinese README**

Mirror the factual content and installation instructions without translating code identifiers or weakening behavioral boundaries.

- [ ] **Step 3: Add six before/after scenarios**

Cover new-project research, local debug, over-design review, routine dependency reuse, confirmed full scope, and a purely mechanical negative trigger.

- [ ] **Step 4: Add MIT license and security policy**

Use the account identity `2731350936` and document private-query and untrusted-source risks.

### Task 3: Deterministic validation, eval fixtures, and CI

**Files:**
- Create: `scripts/validate.py`
- Create: `tests/test_validate.py`
- Create: `evals/evals.json`
- Create: `evals/trigger-cases.json`
- Create: `benchmarks/README.md`
- Create: `benchmarks/baseline.md`
- Create: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: repository files and behavior requirements.
- Produces: a zero-dependency validator, regression tests, realistic trigger/behavior cases, and a transparent initial benchmark statement.

- [ ] **Step 1: Write validator regression tests first**

Test the valid repository, missing routed references, malformed plugin metadata, invalid eval schema, and forbidden placeholders.

- [ ] **Step 2: Run tests and verify the validator is missing**

Run `python3 -m unittest discover -s tests -v`; expected initial failure identifies the absent `scripts.validate` module.

- [ ] **Step 3: Implement the standard-library validator**

Validate required files, JSON/YAML-lite frontmatter boundaries, plugin version/name, routed references, eval schema, relative paths, and placeholder absence.

- [ ] **Step 4: Add behavior and trigger fixtures**

Include project start, bugfix, over-design review, routine dependency, confirmed scope, mechanical edit, translation, architecture, and domain-skill coexistence cases. Include balanced near-miss trigger negatives.

- [ ] **Step 5: Add honest benchmark documentation**

Record the existing nine completed qualitative tests as historical evidence, clearly label their limitations, and define the future A/B metrics without claiming statistical significance.

- [ ] **Step 6: Add GitHub Actions validation**

Run the unit tests, repository validator, plugin validator-compatible checks, and skill structure checks on pushes and pull requests.

### Task 4: Independent behavior review and local installation

**Files:**
- Create: `evals/reports/v0.2.0-review.md`
- Modify: `/Users/a0000/.codex/skills/old-hand/*`

**Interfaces:**
- Consumes: the completed repository skill and eval fixtures.
- Produces: a fresh-context review report and the same validated version installed locally.

- [ ] **Step 1: Run representative with-skill and baseline evaluations**

Use isolated agents for at least project research, local debug, and over-design review. Compare against the pre-v0.2 snapshot or a no-skill baseline and preserve evidence without leaking expected answers.

- [ ] **Step 2: Review trigger precision**

Check positive and near-miss prompts for under-triggering and over-triggering; revise the description only if evidence shows a real weakness.

- [ ] **Step 3: Run a fresh independent repository review**

Review requirements, security boundaries, plugin structure, docs accuracy, tests, and release readiness. Record findings and corrections.

- [ ] **Step 4: Sync the validated canonical skill locally**

Replace only the five local skill bundle files after repository validation passes, preserving global user configuration.

### Task 5: GitHub publication and v0.2.0 release

**Files:**
- Create: Git commit and tag `v0.2.0`
- Create: GitHub repository `2731350936/old-hand`
- Create: GitHub release `v0.2.0`

**Interfaces:**
- Consumes: the verified repository on `main`.
- Produces: a public GitHub repository, pushed tag, release notes, and usable Codex marketplace source.

- [ ] **Step 1: Run the full release verification**

Run unit tests, repository validation, plugin validation, skill validation, JSON parsing, link/path checks, and `git diff --check`; every command must exit 0.

- [ ] **Step 2: Commit the release**

Commit all scoped files as `feat: publish old-hand v0.2.0` and tag the verified commit `v0.2.0`.

- [ ] **Step 3: Authenticate GitHub CLI**

Install GitHub CLI if absent and use GitHub web authentication without printing or persisting credentials in repository files.

- [ ] **Step 4: Create and push the public repository**

Create `2731350936/old-hand` as public, set `origin`, push `main`, and push `v0.2.0`.

- [ ] **Step 5: Create the GitHub release and verify remote state**

Publish release notes describing evidence-first routing, research safety, validation, limitations, and installation. Verify repository visibility, default branch, tag, release URL, and marketplace files through GitHub.
