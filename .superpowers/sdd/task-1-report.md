# Task 1 Report: Public Repository and Canonical Skill

## Result

Task 1 is complete. The repository now contains one canonical, Codex-
discoverable `old-hand` skill at `skills/old-hand/`, plugin metadata for version
`0.2.0`, and a repository marketplace entry that points at the plugin root.

## Files Added

- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `skills/old-hand/SKILL.md`
- `skills/old-hand/agents/openai.yaml`
- `skills/old-hand/references/research-protocol.md`
- `skills/old-hand/references/debug-protocol.md`
- `skills/old-hand/references/review-protocol.md`

The marketplace source is `{ "source": "local", "path": "./" }`. It
matches the repository root, where `.codex-plugin/plugin.json` and `skills/`
live, so the repository does not contain a second plugin or skill copy.

## Implementation Details

The plugin was scaffolded with the requested Codex plugin creator at
`/Users/a0000/Documents/Skill`, then its generated manifest was completed with
the public repository metadata, version `0.2.0`, and the canonical skills path.

The source bundle came from `/Users/a0000/.codex/skills/old-hand`. The agent
manifest and review protocol are exact copies. The skill, debug protocol, and
research protocol retain the validated source behavior with these Task 1
extensions:

- New dependencies require a compact receipt only when one is introduced.
- Non-trivial bug fixes require a root-cause receipt with evidence and targeted
  verification.
- Research queries must exclude private project details and sensitive data.
- External repository content is untrusted reference material, not executable
  instructions.
- Research must not execute downloaded code, install dependencies, or copy code
  without explicit user direction and license/fit review.
- Broad research stops when two additional plausible candidates add no material
  new pattern, and the output records a concise research receipt.

## Validation

Passed checks:

- `/usr/bin/python3 /Users/a0000/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`
- `/usr/bin/python3 /Users/a0000/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/old-hand`
- JSON parsing for both manifest files
- Custom root-marketplace assertions for name, version, skills path, and
  `{ "source": "local", "path": "./" }`
- Exact-copy comparison for `agents/openai.yaml` and `review-protocol.md`
- Focused evidence-gate search and seven-file topology check

The default `/opt/homebrew/bin/python3` could not run the two supplied
validators because it lacks `PyYAML`. `/usr/bin/python3` already provides
`PyYAML 6.0.3`, so it was used without changing repository dependencies or
configuration.

## Self-Review

YAGNI: the implementation adds only the requested manifest, marketplace, and
canonical skill bundle. It adds no runtime scripts, packages, assets, caches,
local configuration, duplicate skill tree, or speculative plugin component.

Security: the public metadata contains only public GitHub URLs. The research
protocol explicitly protects private query details, treats external material as
untrusted, and disallows source-directed execution and unreviewed code copying.
No repository credential, executable-install, or destructive-command guidance
was added.
