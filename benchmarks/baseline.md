# v0.2.0 Qualitative Baseline

Date: 2026-07-10
Model: GPT-5.6 family
Scope: isolated, qualitative forward tests

Nine completed scenarios were checked while developing the installed
pre-release skill:

| Scenario | Expected behavior | Result |
| --- | --- | --- |
| Small debug: empty string | local-first, root cause, targeted check | Pass |
| Small debug: numeric zero | preserve valid falsey value, no broad research | Pass |
| Ordinary implementation | reuse local transaction and error patterns | Pass |
| New project direction | inspect eight OSS candidates and select a benchmark | Pass |
| Over-design review | remove speculative infrastructure and abstractions | Pass |
| Routine dependency | reuse the installed HTTP client | Pass |
| Confirmed full scope | implement the clarified plugin requirement | Pass |
| Mechanical rename | do not load the engineering-judgment workflow | Pass |
| Unrelated translation | do not load a coding skill | Pass |

Three additional post-task provenance controls covered local-first debug, a
mechanical negative control, and coexistence with a macOS domain skill.

## Evidence Limits

- This was a small qualitative set, not a randomized A/B experiment.
- File-read provenance was reported by isolated agents after the task; it was
  not captured by a product-level instruction-injection trace.
- Two other agents timed out and produced no output, so they were excluded from
  both pass and fail counts.
- Raw private execution transcripts are not distributed in this repository.
- The results do not establish trigger rates across models, platforms, or
  future Codex versions.

The public fixtures in [`../evals/`](../evals/) preserve the intended scenarios
for future reproducible comparisons. Until those comparisons exist, this file
is supporting evidence, not a performance claim.
