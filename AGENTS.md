# Minecraft Server Development Agent Rules

These instructions apply to AI coding agents working on Minecraft Java server and proxy projects.

## Supported Agent Entry Points

- Codex reads this file as `AGENTS.md`.
- Claude Code reads `CLAUDE.md`, which imports this file.
- Gemini CLI reads `GEMINI.md`, which imports this file.
- Other agents should use this file as the canonical project instruction source.
- `agent-plugin.json` describes this package's supported entry points, references, scripts, targets, and compatibility surface.

## Mission

Design, implement, review, and debug Minecraft Java projects for Spigot, Paper, Folia, Velocity, and BungeeCord from legacy 1.8.x through the current 26.x/26.2-era line. Treat protocol, scheduler, proxy, persistence, and version-compatibility work as high-risk areas that require explicit verification.

## Required Workflow

1. Identify the runtime target before editing code:
   - Server plugin: Bukkit, Spigot, Paper, or Folia.
   - Proxy plugin: Velocity or BungeeCord.
   - Shared library: no platform API types in public common interfaces.
   - Protocol layer: ProtocolLib, proxy API, Netty, or direct NMS.
2. Identify the version band:
   - Legacy: 1.8.x through 1.12.x.
   - Transitional: 1.13.x through 1.16.x.
   - Modern: 1.17.x through 1.21.x.
   - Calendar-version line: 26.x, including 26.2 when requested.
3. Prefer the safest API surface:
   - Stable platform API first.
   - Paper/Folia API only when the target allows it.
   - ProtocolLib or proxy APIs before direct Netty/NMS.
   - NMS/reflection only behind narrow adapters.
4. Keep architecture modular:
   - Put domain logic in `common`.
   - Put Bukkit/Paper/Folia code in a server adapter.
   - Put Velocity and BungeeCord code in separate proxy adapters.
   - Put NMS/protocol code in versioned implementation packages.
5. Validate against the oldest and newest target versions. Validate Folia separately when support is advertised.

## Reference Routing

Read the relevant reference before acting:

- `references/platforms.md` for lifecycle, plugin metadata, commands, events, and proxy differences.
- `references/folia-threading.md` before async logic, scheduler calls, entity/world access, teleporting, or `folia-supported: true`.
- `references/protocol-and-nms.md` before packets, ProtocolLib, channels, Netty, mappings, obfuscation, data versions, or reflection.
- `references/architecture.md` before project structure, multi-module builds, database/cache design, service networks, or cross-platform abstractions.
- `references/build-and-test.md` before Gradle/Maven, Java versions, shading, CI, or compatibility testing.

## Folia Rules

- Do not mark a plugin as Folia-supported until every world, entity, chunk, and player access runs in the correct region or entity context.
- Do not use old Bukkit scheduler assumptions in Folia-targeted code.
- Store UUIDs, keys, locations, or immutable DTOs in async state. Reacquire Bukkit objects on the correct scheduler.
- Treat thread-safe collections as data safety only; they do not make Bukkit API calls safe.

## Protocol And NMS Rules

- Never mix protocol/NMS code with business logic.
- Validate packet input from clients and proxy/backend channels.
- Do not block Netty event loops.
- Resolve reflection handles at startup and fail with clear server/version diagnostics.
- Do not hardcode 26.x/26.2 protocol constants without checking current maintained data or official notes.

## Build Rules

- Use `compileOnly` or `provided` for server/proxy APIs.
- Relocate shaded dependencies.
- Use Java 8 bytecode only when legacy 1.8-era runtime support is required.
- Use Gradle toolchains or equivalent Maven compiler settings.
- Keep generated jars and local server files out of version control.

## Scaffolding

For new projects, prefer the bundled generator:

```bash
python scripts/create_minecraft_project.py --name ExamplePlugin --package dev.example.plugin --platforms bukkit,velocity,bungee --output /path/to/output
```

Then adapt dependency versions, Java toolchain, metadata, Folia support, and tests to the requested target matrix.

## Response Contract

When finishing work, report:

- Target platform and Minecraft version matrix.
- Whether Folia is supported or intentionally unsupported.
- Any protocol/NMS/reflection risk.
- Build and test commands run.
- Any versions or platforms not verified.
