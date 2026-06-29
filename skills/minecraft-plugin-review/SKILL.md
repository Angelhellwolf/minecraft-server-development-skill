---
name: minecraft-plugin-review
description: Review Minecraft Java plugins and proxy projects for platform compatibility, Folia thread safety, protocol/NMS risk, lifecycle bugs, build problems, missing tests, and unsafe architecture. Use for code reviews of Spigot, Paper, Folia, Velocity, BungeeCord, ProtocolLib, NMS, plugin messaging, scheduler, storage, and cross-version code.
license: MIT
---

# Minecraft Plugin Review

Review as a production Minecraft server engineer. Findings first, ordered by severity, with file and line references when available.

Check:

- Platform target and version claims.
- Folia safety for scheduler, world, entity, chunk, player, teleport, and async code.
- Bukkit API calls from async callbacks.
- NMS/reflection/ProtocolLib isolation and version guards.
- Proxy/backend trust boundaries and plugin messaging validation.
- Resource cleanup on disable.
- Java bytecode, Gradle/Maven dependency scope, shading, and relocation.
- Tests or smoke checks for oldest/newest target versions.

Do not spend findings on style unless it can cause operational risk.
