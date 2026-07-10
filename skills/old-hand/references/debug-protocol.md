# Debug Protocol

## Default Stance

Do not browse by default. Debugging starts with the local code, the error, the
reproduction path, and the callers.

A tiny wrong fix is still wrong. Understand first, then minimize.

When a specialized debugging skill is active, follow its deeper reproduction
and diagnosis procedure. Use this protocol to keep the fix local-first,
root-cause-oriented, and small.

## Process

1. Read the error message, failing behavior, or test failure.
2. Find the relevant files with `rg` or the fastest available local search.
3. Inspect the caller chain and nearby sibling paths before editing.
4. Reproduce the issue if feasible.
5. Identify the root cause.
6. Fix at the shared/root location when possible.
7. Avoid adding a new abstraction unless it removes real duplication or risk.
8. Add the smallest runnable check for non-trivial logic.
9. Run targeted tests or checks.

## Root-Cause Evidence Gate

For a non-trivial bug fix, include a compact root-cause receipt. A fix is
non-trivial when it changes shared behavior, data handling, a public contract,
or more than an obvious local typo. The receipt must state:

- the observed symptom and reproduction or failing check
- the causal chain or code-path evidence
- the root location changed and why it fixes the cause
- the targeted verification run and any remaining uncertainty

Do not require this receipt for an obvious mechanical correction. Keep it short
enough that it supports the fix instead of becoming a second investigation.

## When Browsing Is Allowed

Browse only when current external behavior materially affects the fix:

- external API or library behavior is uncertain
- official docs are needed
- security, legal, or current platform behavior matters

Prefer primary sources in those cases and cite them.

## Output Format

Use a short shape:

1. What broke
2. Root cause
3. Fix
4. Check run
5. Root-cause receipt, only for a non-trivial fix

Keep small fixes small.
