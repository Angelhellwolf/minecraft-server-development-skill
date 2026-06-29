# Protocol And NMS

## Decision Order

1. Use stable Bukkit/Paper/Velocity/Bungee API.
2. Use Adventure for text, titles, boss bars, and audiences when available.
3. Use ProtocolLib for Bukkit packet interception when the target server supports it.
4. Use proxy APIs for login, forwarding, server switching, and network routing.
5. Use direct NMS, Netty injection, or reflection only when all safer options fail.

## Version Bands

- 1.8.x: legacy chat, item metadata, scoreboard behavior, old NMS package names, Java 8, and many missing APIs.
- 1.9-1.12: combat/offhand changes and pre-flattening block/item IDs.
- 1.13: flattening changed block/item identifiers and many data assumptions.
- 1.16-1.17: Java/runtime changes and mapping ecosystem changes.
- 1.19+: signed chat and player profile/security-sensitive changes.
- 1.20.5+: item/component and registry-related changes affect item/NBT code.
- 26.x/26.2: verify live protocol, data pack, resource pack, and management protocol details before hardcoding constants.

## Adapter Shape

Keep version-specific code small:

```java
public interface PacketFacade {
    void sendActionBar(UUID playerId, String message);
    void inject(PlayerHandle player);
    void close(PlayerHandle player);
}
```

Implement one adapter per version family when unavoidable. Prefer capability checks over giant version strings when possible.

## Reflection Rules

- Resolve reflective handles once at startup and fail fast with a clear message.
- Keep all reflection in one package such as `internal.nms.v1_8` or `protocol`.
- Do not swallow `ReflectiveOperationException`; include target Minecraft version and server brand in logs.
- Avoid relying on private fields when public API or maintained libraries exist.

## Packet Safety

- Never trust packet data from clients.
- Validate sizes, strings, enum indexes, coordinates, and item payloads.
- Avoid blocking work in Netty event loops.
- Reenter the platform scheduler before touching world/entity/plugin state.
- Disconnect or ignore malformed data intentionally; do not let parse exceptions spam logs.

## Plugin Messaging

Use plugin messaging for small, trusted coordination between proxy and backend servers. Use Redis, a database, or a message broker for durable cross-server state. Namespace channels clearly and version your payload:

```text
myplugin:control
version: 1
type: PLAYER_TRANSFER
```

## Source Pointers

- Minecraft Java 26.2 notes: https://www.minecraft.net/en-us/article/minecraft-java-edition-26-2
- wiki.vg protocol archive: https://c4k3.github.io/wiki.vg/Protocol.html
- Protocol version numbers archive: https://c4k3.github.io/wiki.vg/Protocol_version_numbers.html
- PrismarineJS minecraft-data: https://github.com/PrismarineJS/minecraft-data
- Paper plugin messaging: https://docs.papermc.io/paper/dev/plugin-messaging/
- Velocity plugin messaging: https://docs.papermc.io/velocity/dev/plugin-messaging/
- Bukkit/Bungee plugin messaging: https://www.spigotmc.org/wiki/bukkit-bungee-plugin-messaging-channel/
