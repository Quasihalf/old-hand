#!/usr/bin/env python3
"""Validate the public old-hand repository without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


RELEASE_VERSION = "0.2.2"
CREATION_COLOAD_PREFIX = (
    "always use old hand together with skill-creator or plugin-creator before "
    "creating or substantially redesigning"
)
CREATION_TRIGGER_TERMS = ("skill", "plugin", "agent", "mcp", "workflow")
CREATION_DISCOVERY_ORDER = (
    "before finalizing the initial stack, architecture, scope, benchmark, or "
    "scaffold"
)
CREATION_RESEARCH_GATE = (
    "Research before design, scaffolding, or implementation even when the user "
    "did not ask for research."
)
CREATION_RESEARCH_ORDER_GATE = (
    "Before the initial search completes, do not finalize an implementation "
    "stack, architecture, feature scope, benchmark, or scaffold location, and "
    "do not begin design or scaffolding."
)

REQUIRED_FILES = (
    ".agents/plugins/marketplace.json",
    ".codex-plugin/plugin.json",
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "SECURITY.md",
    "examples/before-after.md",
    "skills/old-hand/SKILL.md",
    "skills/old-hand/agents/openai.yaml",
    "skills/old-hand/references/debug-protocol.md",
    "skills/old-hand/references/research-protocol.md",
    "skills/old-hand/references/review-protocol.md",
    "evals/evals.json",
    "evals/trigger-cases.json",
    "benchmarks/README.md",
    "benchmarks/baseline.md",
)

ROUTED_REFERENCES = (
    "references/research-protocol.md",
    "references/debug-protocol.md",
    "references/review-protocol.md",
)

PUBLIC_TEXT_FILES = (
    "README.md",
    "README.zh-CN.md",
    "SECURITY.md",
    "examples/before-after.md",
    "skills/old-hand/SKILL.md",
    "skills/old-hand/agents/openai.yaml",
    "skills/old-hand/references/debug-protocol.md",
    "skills/old-hand/references/research-protocol.md",
    "skills/old-hand/references/review-protocol.md",
    "benchmarks/README.md",
    "benchmarks/baseline.md",
)


def _load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name} is not valid JSON: {exc}")
        return None


def _frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None

    values: dict[str, str] = {}
    current_key: str | None = None
    for line in lines[1:end]:
        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            current_key = match.group(1)
            value = (match.group(2) or "").strip()
            values[current_key] = "" if value in {">", ">-", "|", "|-"} else value
        elif current_key and line.startswith("  "):
            values[current_key] = (values[current_key] + " " + line.strip()).strip()
    return values


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _parse_agent_metadata(text: str) -> dict[str, dict[str, Any]]:
    """Parse the small, generated openai.yaml shape used by this skill."""
    result: dict[str, dict[str, Any]] = {}
    section: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        section_match = re.fullmatch(r"([a-zA-Z][a-zA-Z0-9_-]*):", line)
        if section_match:
            section = section_match.group(1)
            result.setdefault(section, {})
            continue
        value_match = re.fullmatch(
            r"  ([a-zA-Z][a-zA-Z0-9_-]*):\s*(.+)", line
        )
        if section is None or value_match is None:
            continue
        key, raw_value = value_match.groups()
        if raw_value == "true":
            value: Any = True
        elif raw_value == "false":
            value = False
        elif raw_value.startswith('"') and raw_value.endswith('"'):
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError:
                value = raw_value
        else:
            value = raw_value
        result[section][key] = value
    return result


def _validate_eval_cases(payload: Any, errors: list[str]) -> None:
    if not isinstance(payload, dict) or payload.get("skill_name") != "old-hand":
        errors.append("evals/evals.json must set skill_name to 'old-hand'")
        return
    if payload.get("version") != RELEASE_VERSION:
        errors.append(
            f"evals/evals.json must set version to '{RELEASE_VERSION}'"
        )
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("evals/evals.json cases must be a non-empty array")
        return
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"evals/evals.json cases[{index}] must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            errors.append(f"evals/evals.json cases[{index}].id must be unique and non-empty")
        else:
            seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"evals/evals.json cases[{index}].prompt must be non-empty")
        route = case.get("route")
        if not isinstance(route, str) or not route.strip():
            errors.append(f"evals/evals.json cases[{index}].route must be non-empty")
        expect = case.get("expect")
        if not isinstance(expect, dict):
            errors.append(f"evals/evals.json cases[{index}].expect must be an object")
            continue
        for field in ("behaviors", "avoid"):
            values = expect.get(field)
            if not isinstance(values, list) or not values or not all(
                isinstance(item, str) and item.strip() for item in values
            ):
                errors.append(
                    f"evals/evals.json cases[{index}].expect.{field} must be a non-empty array"
                )


def _validate_trigger_cases(payload: Any, errors: list[str]) -> None:
    if not isinstance(payload, dict) or payload.get("skill_name") != "old-hand":
        errors.append("evals/trigger-cases.json must set skill_name to 'old-hand'")
        return
    if payload.get("version") != RELEASE_VERSION:
        errors.append(
            f"evals/trigger-cases.json must set version to '{RELEASE_VERSION}'"
        )
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("evals/trigger-cases.json cases must be a non-empty array")
        return
    positives = 0
    negatives = 0
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"evals/trigger-cases.json cases[{index}] must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            errors.append(
                f"evals/trigger-cases.json cases[{index}].id must be unique and non-empty"
            )
        else:
            seen.add(case_id)
        if not isinstance(case.get("query"), str) or not case["query"].strip():
            errors.append(f"evals/trigger-cases.json cases[{index}].query must be non-empty")
        if not isinstance(case.get("reason"), str) or not case["reason"].strip():
            errors.append(f"evals/trigger-cases.json cases[{index}].reason must be non-empty")
        trigger = case.get("should_trigger")
        if not isinstance(trigger, bool):
            errors.append(
                f"evals/trigger-cases.json cases[{index}].should_trigger must be boolean"
            )
        elif trigger:
            positives += 1
        else:
            negatives += 1
    if positives < 5 or negatives < 5:
        errors.append("evals/trigger-cases.json must include at least 5 positive and 5 negative cases")


def validate_repository(root: Path) -> list[str]:
    root = Path(root)
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"required file is missing: {relative}")

    skill_path = root / "skills/old-hand/SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        metadata = _frontmatter(skill_text)
        if metadata is None:
            errors.append("SKILL.md must contain closed YAML frontmatter")
        else:
            if metadata.get("name") != "old-hand":
                errors.append("SKILL.md frontmatter must set name to 'old-hand'")
            description = metadata.get("description", "").strip()
            if not description:
                errors.append("SKILL.md frontmatter description must be non-empty")
            else:
                lowered_description = description.lower()
                if not lowered_description.startswith(CREATION_COLOAD_PREFIX):
                    errors.append(
                        "SKILL.md description must front-load creator-skill co-loading"
                    )
                if not all(
                    term in lowered_description for term in CREATION_TRIGGER_TERMS
                ):
                    errors.append(
                        "SKILL.md description must explicitly trigger for skill, "
                        "plugin, agent, MCP, and workflow creation"
                    )
            if description and CREATION_DISCOVERY_ORDER not in description.lower():
                errors.append(
                    "SKILL.md description must make old-hand discoverable before "
                    "creation design decisions"
                )
        for reference in ROUTED_REFERENCES:
            if reference not in skill_text:
                errors.append(f"SKILL.md does not route to {reference}")
            if not (skill_path.parent / reference).is_file():
                errors.append(f"routed reference is missing: {reference}")

    plugin_path = root / ".codex-plugin/plugin.json"
    if plugin_path.is_file():
        plugin = _load_json(plugin_path, errors)
        if not isinstance(plugin, dict):
            errors.append("plugin manifest must be an object")
        else:
            if plugin.get("name") != "old-hand":
                errors.append("plugin manifest must set name to 'old-hand'")
            if plugin.get("version") != RELEASE_VERSION:
                errors.append(
                    f"plugin manifest must set version to '{RELEASE_VERSION}'"
                )
            if plugin.get("license") != "MIT":
                errors.append("plugin manifest must set license to 'MIT'")
            skills = plugin.get("skills")
            if not isinstance(skills, str) or Path(skills).is_absolute():
                errors.append("plugin manifest skills must be a relative path")
            elif skills != "./skills/":
                errors.append("plugin manifest skills must equal './skills/'")
            else:
                resolved = root / skills
                if not _inside(root, resolved) or not resolved.is_dir():
                    errors.append("plugin manifest skills must resolve to a directory inside the repo")
        if not (root / "skills/old-hand/SKILL.md").is_file():
            errors.append("plugin skills bundle must contain skills/old-hand/SKILL.md")

    marketplace_path = root / ".agents/plugins/marketplace.json"
    if marketplace_path.is_file():
        marketplace = _load_json(marketplace_path, errors)
        plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
        if not isinstance(plugins, list) or len(plugins) != 1:
            errors.append("marketplace must contain exactly one plugin")
        else:
            entry = plugins[0]
            if not isinstance(entry, dict):
                errors.append("marketplace plugins[0] must be an object")
            else:
                if entry.get("name") != "old-hand":
                    errors.append("marketplace plugin must be named 'old-hand'")
                source = entry.get("source")
                if source != {"source": "local", "path": "./"}:
                    errors.append("marketplace source must point to the repository root")

    agent_path = root / "skills/old-hand/agents/openai.yaml"
    if agent_path.is_file():
        agent = _parse_agent_metadata(agent_path.read_text(encoding="utf-8"))
        interface = agent.get("interface", {})
        policy = agent.get("policy", {})
        if interface.get("display_name") != "Old Hand":
            errors.append("openai.yaml interface.display_name must be 'Old Hand'")
        short_description = interface.get("short_description")
        if not isinstance(short_description, str) or not 25 <= len(short_description) <= 64:
            errors.append("openai.yaml interface.short_description must be 25-64 characters")
        default_prompt = interface.get("default_prompt")
        if not isinstance(default_prompt, str) or "$old-hand" not in default_prompt:
            errors.append("openai.yaml interface.default_prompt must mention '$old-hand'")
        if policy.get("allow_implicit_invocation") is not True:
            errors.append("openai.yaml policy.allow_implicit_invocation must be true")

    eval_path = root / "evals/evals.json"
    if eval_path.is_file():
        _validate_eval_cases(_load_json(eval_path, errors), errors)
    triggers_path = root / "evals/trigger-cases.json"
    if triggers_path.is_file():
        _validate_trigger_cases(_load_json(triggers_path, errors), errors)

    research_path = root / "skills/old-hand/references/research-protocol.md"
    if research_path.is_file():
        research_text = research_path.read_text(encoding="utf-8")
        if CREATION_RESEARCH_GATE not in research_text:
            errors.append(
                "research protocol must require creation research before design "
                "without an explicit research request"
            )
        if CREATION_RESEARCH_ORDER_GATE not in research_text:
            errors.append(
                "research protocol must prevent finalized design or scaffolding "
                "before the initial search"
            )

    forbidden = ("TODO", "TBD", "[PLACEHOLDER")
    for relative in PUBLIC_TEXT_FILES:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in text:
                errors.append(f"{relative} contains forbidden placeholder '{marker}'")

    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated old-hand repository: {root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
