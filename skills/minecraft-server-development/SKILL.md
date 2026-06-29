---
name: minecraft-server-development
description: Design, implement, review, and debug Minecraft Java server and proxy projects across Spigot, Paper, Folia, Velocity, and BungeeCord from legacy 1.8 servers through current 26.x/26.2-era servers. Use for Bukkit/Spigot/Paper/Folia plugins, Velocity/BungeeCord proxy plugins, protocol adapters, packet/NMS/reflection code, Gradle/Maven structure, Folia-safe scheduling, cross-version compatibility, plugin messaging, performance, and server-network architecture.
license: MIT
---

# Minecraft Server Development

Use the repository root `AGENTS.md` as the canonical rule set. Read the relevant file in `references/` before acting:

- `references/platforms.md` for Spigot, Paper, Folia, Velocity, and BungeeCord lifecycle/API differences.
- `references/folia-threading.md` before scheduler, async, world, entity, chunk, player, or teleport code.
- `references/protocol-and-nms.md` before packet, NMS, ProtocolLib, Netty, reflection, mapping, or plugin-message work.
- `references/architecture.md` before project/module/network/storage design.
- `references/build-and-test.md` before Gradle, Maven, Java version, shading, CI, or compatibility testing.

Always report the target platform/version matrix, Folia support status, protocol/NMS risk, commands run, and unverified versions.
