---
name: minecraft-folia-audit
description: Audit Minecraft Bukkit/Paper plugins for Folia compatibility and regionized-threading safety. Use when a plugin claims or wants Folia support, uses schedulers, async callbacks, world/entity/chunk/player access, teleporting, game state, or shared mutable state.
license: MIT
---

# Minecraft Folia Audit

Read `references/folia-threading.md` first. Then inspect code for:

- `Bukkit.getScheduler`, `runTask`, `runTaskTimer`, and `runTaskAsynchronously`.
- `CompletableFuture`, `new Thread`, executor callbacks, database callbacks, HTTP callbacks, and Redis callbacks.
- Access to `Player`, `Entity`, `World`, `Chunk`, `Location`, teleporting, inventory, scoreboard, boss bar, and nearby entities.
- Mutable global game state shared across region contexts.
- `folia-supported: true` in plugin metadata.

Classify each issue as blocker, risky, or acceptable. Do not approve Folia support unless every Bukkit object access has a clear entity, region, global, or async ownership model.
