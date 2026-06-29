#!/usr/bin/env python3
"""Validate the cross-agent Minecraft development package."""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agent-plugin.json",
    "gemini-extension.json",
    "plugin.yaml",
    "package.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "skills/minecraft-server-development/SKILL.md",
    "skills/minecraft-plugin-review/SKILL.md",
    "skills/minecraft-folia-audit/SKILL.md",
    "commands/minecraft-server-development.toml",
    "commands/minecraft-plugin-review.toml",
    "commands/minecraft-folia-audit.toml",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid json {path}: {exc}")


def validate_required_files() -> None:
    missing = [file for file in REQUIRED_FILES if not (ROOT / file).exists()]
    if missing:
        fail("missing files: " + ", ".join(missing))


def validate_json_versions() -> None:
    package = load_json(ROOT / "package.json")
    manifest = load_json(ROOT / "agent-plugin.json")
    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    gemini = load_json(ROOT / "gemini-extension.json")

    versions = {
        package.get("version"),
        manifest.get("version"),
        codex.get("version"),
        claude.get("version"),
        gemini.get("version"),
    }
    if len(versions) != 1:
        fail(f"version mismatch: {sorted(str(v) for v in versions)}")

    names = {
        manifest.get("name"),
        codex.get("name"),
        claude.get("name"),
        gemini.get("name"),
    }
    if names != {"minecraft-server-development"}:
        fail(f"name mismatch: {sorted(str(v) for v in names)}")


def validate_commands() -> None:
    for path in (ROOT / "commands").glob("*.toml"):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        if not data.get("description") or not data.get("prompt"):
            fail(f"command missing description or prompt: {path}")


def validate_skills() -> None:
    for path in (ROOT / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            fail(f"skill missing frontmatter: {path}")
        if "description:" not in text:
            fail(f"skill missing description: {path}")


def main() -> None:
    validate_required_files()
    validate_json_versions()
    validate_commands()
    validate_skills()
    print("package is valid")


if __name__ == "__main__":
    main()
