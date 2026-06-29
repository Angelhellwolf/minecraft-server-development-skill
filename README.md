# Minecraft Server Development

Cross-agent development rules and reusable tooling for Minecraft Java server projects.

This repository is not a Minecraft plugin jar. It is an AI agent instruction package for designing, implementing, reviewing, and debugging plugins and proxy projects across Spigot, Paper, Folia, Velocity, and BungeeCord from legacy 1.8.x through the 26.x/26.2-era line.

## What It Supports

- Codex through `AGENTS.md` and `SKILL.md`
- Claude Code through `CLAUDE.md`
- Gemini CLI through `GEMINI.md`
- Generic AI coding agents through `AGENTS.md`
- Bukkit, Spigot, Paper, Folia, Velocity, and BungeeCord project design
- Protocol, NMS, packet, plugin messaging, scheduler, and architecture work
- Cross-version planning from 1.8.x legacy servers to current 26.x targets

## Repository Layout

```text
.
|-- AGENTS.md                  # Canonical shared rules for Codex and generic agents
|-- CLAUDE.md                  # Claude Code entry point
|-- GEMINI.md                  # Gemini CLI entry point
|-- SKILL.md                   # Codex skill entry point
|-- agent-plugin.json          # Cross-agent plugin manifest
|-- agents/openai.yaml         # Codex UI metadata
|-- references/                # Detailed platform, Folia, protocol, architecture, build docs
`-- scripts/                   # Project generator and rule installer
```

## Use In An Existing Project

Install all agent entry files into another Minecraft project:

```bash
python scripts/install_agent_rules.py --target /path/to/plugin --agent all --references --manifest
```

Install only one agent entry:

```bash
python scripts/install_agent_rules.py --target /path/to/plugin --agent codex --references
python scripts/install_agent_rules.py --target /path/to/plugin --agent claude --references
python scripts/install_agent_rules.py --target /path/to/plugin --agent gemini --references
```

Use `--force` to overwrite existing instruction files.

## Generate A Starter Project

Create a minimal multi-module Gradle project:

```bash
python scripts/create_minecraft_project.py \
  --name ExamplePlugin \
  --package dev.example.plugin \
  --platforms bukkit,velocity,bungee \
  --output ./generated
```

The generated project contains:

- `common` for platform-free domain logic
- `bukkit` for Spigot/Paper/Folia-facing code
- `velocity` for Velocity proxy code
- `bungee` for BungeeCord proxy code

Adjust dependency versions, Java toolchains, plugin metadata, Folia support, and tests for your real target matrix before release.

## Core Rules

- Keep business logic out of platform adapters.
- Treat Folia as a different threading model, not as normal Paper.
- Do not touch Bukkit world, entity, chunk, or player state from arbitrary async code.
- Keep protocol, NMS, reflection, and Netty code behind narrow adapters.
- Prefer stable platform APIs before raw packets or reflection.
- Validate against the oldest and newest supported server versions.
- Do not claim Folia or 26.x/26.2 compatibility without testing or checking current docs/data.

## References

- `references/platforms.md`: Spigot, Paper, Folia, Velocity, and BungeeCord differences
- `references/folia-threading.md`: Folia scheduler and regionized threading rules
- `references/protocol-and-nms.md`: packet, NMS, reflection, and protocol safety
- `references/architecture.md`: multi-module and server-network design
- `references/build-and-test.md`: Gradle, Maven, Java, shading, CI, and test matrix

## Codex Skill Usage

The repository is also a valid Codex skill. Copy or clone this folder into your Codex skills directory, then invoke:

```text
Use $minecraft-server-development to design a cross-platform Minecraft plugin.
```

## License

MIT License.
