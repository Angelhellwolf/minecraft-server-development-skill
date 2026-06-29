---
name: minecraft-server-development
description: Design, implement, review, and debug Minecraft Java server and proxy projects across Spigot, Paper, Folia, Velocity, and BungeeCord from legacy 1.8 servers through current 26.x/26.2-era servers. Use when Codex works on Bukkit/Spigot/Paper/Folia plugins, Velocity or BungeeCord proxy plugins, protocol adapters, packet/NMS/reflection code, Gradle/Maven project structure, Folia-safe scheduling, cross-version compatibility, server-network architecture, plugin messaging, performance, or migration between Minecraft server platforms.
---

# Minecraft Server Development

## Agent Compatibility

This package is both a Codex skill and a cross-agent instruction pack. Use `AGENTS.md` as the canonical shared rule set. `CLAUDE.md` and `GEMINI.md` import it for Claude Code and Gemini CLI compatibility.

## Core Workflow

1. Identify the runtime target before editing code:
   - Server plugin: Bukkit/Spigot/Paper/Folia.
   - Proxy plugin: Velocity/BungeeCord/Waterfall-like legacy proxy.
   - Shared library: no platform APIs in the core module.
   - Protocol layer: ProtocolLib, Netty, proxy API, or direct NMS.
2. Identify the version band:
   - Legacy: 1.8.x through 1.12.x.
   - Transitional: 1.13.x through 1.16.x.
   - Modern: 1.17.x through 1.21.x.
   - Current calendar-version line: 26.x, including 26.2 when requested.
3. Choose the lowest-risk API surface:
   - Prefer stable platform API and Adventure/audience abstractions.
   - Use Paper APIs only when the target is Paper/Folia.
   - Use NMS, reflection, or raw packets only when the feature cannot be built through stable APIs.
4. Design for platform boundaries:
   - Keep business logic in `common`.
   - Put Bukkit/Paper/Folia code behind a server adapter.
   - Put Velocity and BungeeCord code behind proxy adapters.
   - Put version-specific packet/NMS code behind small interfaces.
5. Validate with the oldest and newest target versions the user cares about, plus Folia when `folia-supported: true` is present.

## Reference Routing

- Read `references/platforms.md` for platform-specific rules, lifecycle, schedulers, plugin metadata, commands, events, and proxy differences.
- Read `references/folia-threading.md` before adding async logic, Bukkit scheduler calls, entity/world access, teleporting, or `folia-supported: true`.
- Read `references/protocol-and-nms.md` before touching packets, ProtocolLib, channels, Netty, Mojang mappings, obfuscation, data versions, or reflection.
- Read `references/architecture.md` before creating or restructuring a plugin, multi-module repo, database/cache layer, service network, or cross-platform abstraction.
- Read `references/build-and-test.md` before changing Gradle/Maven, Java versions, shading/relocation, CI, or compatibility testing.

## Scaffolding

For a new Java plugin/proxy project, run:

```bash
python scripts/create_minecraft_project.py --name ExamplePlugin --package dev.example.plugin --platforms bukkit,velocity,bungee --output /path/to/output
```

Use the generated project as a starting point, then adapt versions, metadata, dependencies, and CI to the actual target matrix. The script intentionally keeps generated code minimal so project-specific design stays explicit.

To install this package's shared rules into an existing project for Codex, Claude Code, Gemini CLI, or all three:

```bash
python scripts/install_agent_rules.py --target /path/to/plugin --agent all --references
```

## Implementation Rules

- Do not mark a plugin as Folia-supported until every world/entity/chunk/player access runs in the correct region or entity context.
- Do not use Bukkit API from arbitrary async threads. For Folia, do not assume the old main-thread model exists.
- Do not store mutable `Player`, `Entity`, `World`, `Server`, or command sender objects in long-lived async state. Store UUIDs/keys and reacquire on the correct scheduler.
- Do not put NMS or ProtocolLib code in the same class that owns business logic. Isolate it behind interfaces and version adapters.
- Do not claim support for a Minecraft version until it is compiled or smoke-tested against that version's API/server.
- For 1.8 support, assume old APIs, old chat/item metadata behavior, Java 8 constraints, and missing modern Adventure/Paper conveniences unless explicitly provided by dependencies.
- For 26.x/26.2 support, verify current Paper/Folia/Velocity/Bungee availability and protocol details from official docs or maintained data before hardcoding constants.
- Prefer Gradle toolchains, dependency locking or version catalogs, reproducible builds, and relocation for shaded libraries used inside plugin jars.

## Output Expectations

When completing a task, report:

- Target platforms and versions used for the decision.
- Any API that is intentionally platform-specific.
- Folia safety status when relevant.
- Protocol/NMS risks when relevant.
- Build/test commands run, including any versions not verified.
