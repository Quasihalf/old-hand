# Review Protocol

## Review Stance

Findings first. Prefer evidence over taste.

The best review removes unnecessary risk, code, dependencies, and future
maintenance while preserving the user's real requirement.

## Look For

- interface with one implementation
- factory, provider, or plugin system for one concrete case
- config for values that do not vary
- new dependency where standard library, platform, or local code is enough
- duplicated helper already present nearby
- speculative caching, queueing, or abstraction
- bug fix applied only to one caller instead of the shared root
- tests that are too heavy or missing the one check that matters
- architecture copied from a larger project without matching constraints

## Severity

- **High**: likely bug, security/data-loss risk, or wrong architecture with
  near-term cost.
- **Medium**: unnecessary complexity that will slow maintenance.
- **Low**: cleanup or simplification opportunity.

## Output Format

Order findings by severity. For each finding, include:

- file/line reference when available
- why it matters
- smaller alternative
- residual risk or test gap

If there are no findings, say so clearly and mention any remaining verification
gap.
