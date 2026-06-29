#!/usr/bin/env python3
"""Install Minecraft AI agent rules into another project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRY_FILES = {
    "codex": ["AGENTS.md"],
    "claude": ["CLAUDE.md", "AGENTS.md"],
    "gemini": ["GEMINI.md", "AGENTS.md"],
    "all": ["AGENTS.md", "CLAUDE.md", "GEMINI.md"],
}


def copy_file(source: Path, destination: Path, force: bool) -> None:
    if destination.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def install(args: argparse.Namespace) -> None:
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    files = ENTRY_FILES[args.agent]
    for filename in files:
        copy_file(ROOT / filename, target / filename, args.force)

    if args.manifest:
        copy_file(ROOT / "agent-plugin.json", target / "agent-plugin.json", args.force)

    if args.references:
        references_target = target / "references"
        if references_target.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing directory: {references_target}")
        if references_target.exists():
            shutil.rmtree(references_target)
        shutil.copytree(ROOT / "references", references_target)

    if args.scripts:
        scripts_target = target / "scripts"
        scripts_target.mkdir(parents=True, exist_ok=True)
        copy_file(ROOT / "scripts" / "create_minecraft_project.py", scripts_target / "create_minecraft_project.py", args.force)

    print(f"installed {args.agent} agent rules into {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Project directory to receive agent rules")
    parser.add_argument("--agent", choices=sorted(ENTRY_FILES), default="all", help="Agent entry files to install")
    parser.add_argument("--references", action="store_true", help="Copy references/ into the target project")
    parser.add_argument("--scripts", action="store_true", help="Copy reusable scripts into the target project")
    parser.add_argument("--manifest", action="store_true", help="Copy agent-plugin.json into the target project")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    install(parser.parse_args())


if __name__ == "__main__":
    main()
