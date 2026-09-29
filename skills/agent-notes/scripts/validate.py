#!/usr/bin/env python3
"""Validate the portable Agent Notes tree and lifecycle-specific format."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LIFECYCLES = {"proposed", "implemented", "rejected", "archived"}
CLASSES = {"feature", "bug-fix", "simplification", "architecture", "process", "testing"}
NAME = re.compile(
    r"^(?P<stem>\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*)(?P<zh>\.zh)?\.md$"
)
REQUIRED = {
    "proposed": {"Problem", "Proposal", "Alternatives considered", "Acceptance criteria", "Risks"},
    "implemented": {"Problem", "Decision", "Alternatives considered", "Consequences"},
    "rejected": {"Problem", "Proposal", "Alternatives considered"},
}
REQUIRED_ZH = {
    "proposed": {"问题", "提案", "考虑过的替代方案", "验收标准", "风险"},
    "implemented": {"问题", "决策", "考虑过的替代方案", "影响"},
    "rejected": {"问题", "提案", "考虑过的替代方案"},
}


def validate_note(path: Path, lifecycle: str) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    is_zh = path.name.endswith(".zh.md")
    title_pattern = r"# Agent Note：\S.*" if is_zh else r"# Agent Note: \S.*"
    if not lines or not re.fullmatch(title_pattern, lines[0]):
        separator = "：" if is_zh else ": "
        errors.append(f"line 1 must be '# Agent Note{separator}<title>'")
    if len(lines) < 2 or lines[1] != "":
        errors.append("line 2 must be blank")
    status = lines[2] if len(lines) > 2 else ""
    expected = {
        "proposed": r"Status: proposed",
        "implemented": r"Status: implemented",
        "rejected": r"Status: rejected — \S.*",
        "archived": r"Status: implemented",
    }[lifecycle]
    if not re.fullmatch(expected, status):
        errors.append(f"status does not match {lifecycle}/")
    headings = {line[3:] for line in lines if line.startswith("## ")}
    required = REQUIRED_ZH if is_zh else REQUIRED
    if lifecycle != "archived":
        for heading in sorted(required[lifecycle] - headings):
            errors.append(f"missing section '## {heading}'")
    proposal_headings = {"提案", "验收标准", "风险"} if is_zh else {"Proposal", "Acceptance criteria", "Risks"}
    if lifecycle == "implemented" and headings & proposal_headings:
        errors.append("implemented Note retains proposal-era sections")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    root = args.repository.resolve() / ".agents" / "notes"
    if not root.is_dir():
        parser.error(f"Agent Notes directory not found: {root}")

    errors: list[str] = []
    checked = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if path.name in {"README.md", "AGENTS.md", "CLAUDE.md"}:
            continue
        parts = rel.parts
        if len(parts) != 3 or parts[0] not in LIFECYCLES or parts[1] not in CLASSES:
            errors.append(f"{rel}: expected <lifecycle>/<class>/<file>.md")
            continue
        match = NAME.fullmatch(path.name)
        if not match:
            errors.append(f"{rel}: invalid filename")
        else:
            counterpart_name = (
                f"{match.group('stem')}.md" if match.group("zh") else f"{match.group('stem')}.zh.md"
            )
            if not path.with_name(counterpart_name).is_file():
                errors.append(f"{rel}: missing bilingual counterpart '{counterpart_name}'")
        checked += 1
        errors.extend(f"{rel}: {message}" for message in validate_note(path, parts[0]))

    if errors:
        print("agent-notes validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"agent-notes validation passed: {checked} note(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
