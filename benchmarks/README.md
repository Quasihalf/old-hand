# Benchmark Plan

`old-hand` should be judged by correctness and engineering outcomes, not by
whether an answer merely sounds experienced.

## Current Status

Version `0.2.3` adds repeated trace-based routing checks for substantive coding,
mechanical boundaries, local debugging, and six creator categories to the
earlier qualitative baseline and creator-research regressions. This is stronger
regression evidence, not a randomized A/B benchmark or a universal invocation
rate. See [baseline.md](baseline.md),
[the v0.2.2 review](../evals/reports/v0.2.2-review.md), and
[the v0.2.3 review](../evals/reports/v0.2.3-review.md) for the evidence and its
limits.

## Planned Comparison

A reproducible benchmark should run the same realistic tasks in isolated
worktrees under three configurations:

1. coding agent without `old-hand`
2. coding agent with `old-hand`
3. a named comparison skill when its license and installation permit it

Run every task multiple times with the same model, effort, repository state,
tool access, and time budget. Keep evaluators blind to the configuration.

## Gates And Metrics

Correctness, security, data integrity, and explicit requirement compliance are
hard gates. A shorter incorrect patch loses.

After the gates pass, record:

- changed lines and files
- new dependencies
- duplicated local helpers
- whether a bug was fixed at the shared root or one symptom path
- targeted checks executed
- research candidate relevance, maintenance signals, source citations, and
  benchmark selection for project-start cases
- tokens, elapsed time, and tool calls

Publish prompts, repositories, revisions, model configuration, raw outputs,
grading rules, failed runs, and variance. Do not collapse project research,
small debugging, and review into one headline number; the skill intentionally
routes those workloads differently.

## Reproduction Boundary

The deterministic repository tests validate files and fixtures only. They do
not pretend to measure model judgment. A future agentic harness belongs in this
directory only after repeated runs can be reproduced without private data or
undisclosed infrastructure.
