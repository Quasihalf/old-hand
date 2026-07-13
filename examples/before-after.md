# Before and After

These scenarios show routing decisions, not canned responses. `old-hand` keeps
the relevant discipline and omits process that the task does not need.

## 1. New-project research

**Before:** "Build a self-hosted incident tracker. Choose a framework and start
with a generic plugin system."

**After:** Classify this as a new product and architecture direction. Research
similar open-source projects with privacy-safe queries, shortlist relevant
patterns, select one closest benchmark, and propose a minimal design. Do not
execute downloaded code or copy a project's implementation merely because it
appears to fit.

## 2. Local debugging

**Before:** "A unit test fails after a timestamp change. Search for a library
that handles time zones and replace the parser."

**After:** Start with the failing test, error, parser callers, and a local
reproduction. Identify the root cause before changing a shared path. Browse
only if current external behavior matters; for a non-trivial fix, provide a
compact root-cause receipt and targeted verification.

## 3. Over-design review

**Before:** "There is one payment provider today. Add a provider factory,
configuration registry, and plugin interface so future providers are easy."

**After:** Review the proposal for evidence of a second implementation or
current variation. If none exists, call out the maintenance cost and recommend
a direct integration with a clear extension point only where the current code
already needs one.

## 4. Routine dependency reuse

**Before:** "Add a package to parse a small JSON configuration file."

**After:** Inspect the local implementation, standard library, platform
facilities, and installed dependencies first. Use an existing suitable option
when it meets the requirement. Add a new dependency only when it solves a real
gap, then record a short dependency receipt.

## 5. Confirmed full scope

**Before:** "The customer has confirmed the import flow, audit history, and
accessibility acceptance criteria. Keep proposing a smaller feature instead."

**After:** The scope is confirmed, so implement it. Keep the design simple,
but do not use YAGNI to remove stated requirements, accessibility basics,
security protections, or data-integrity work.

## 6. Mechanical negative trigger

**Before:** "Correct the typo in this existing Markdown heading."

**After:** Make the mechanical edit directly. This is not a reason to trigger
research, debugging, dependency analysis, or a design review.

## 7. Implicit research for skill creation

**Before:** "帮我做一个剪辑视频的 skill" immediately enters creator-specific
questions or scaffolding because the user did not explicitly request research.

**After:** Implicitly classify this as a new reusable agent artifact. Research
comparable video-editing skills and maintained open-source projects before
finalizing a stack, architecture, scope, or scaffold location, then let the
specialized skill creator handle artifact mechanics. The user does not need to
add "search" or invoke `old-hand` explicitly.
