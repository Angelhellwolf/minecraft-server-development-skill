# Platform Rules

## Platform Selection

Use Spigot/Bukkit when the plugin must run on old server software or very broad Bukkit-compatible hosts. Use Paper when modern server API, performance fixes, Adventure integration, and Paper-specific APIs matter. Use Folia only when the plugin is explicitly written for regionized threading. Use Velocity for new proxy plugins unless the network is committed to BungeeCord compatibility. Use BungeeCord for legacy proxy networks and plugins that depend on the Bungee API.

## Bukkit, Spigot, Paper

- Main class extends `JavaPlugin`.
- Metadata normally lives in `plugin.yml`; Paper-specific plugins may use `paper-plugin.yml` when targeting Paper-only features.
- Register listeners during `onEnable`.
- Register commands through metadata plus executor/tab completer, or platform-specific command APIs when available.
- Use Bukkit scheduler only for classic Bukkit/Paper threading. See `folia-threading.md` before using it in Folia-targeted code.
- Prefer Bukkit/Paper APIs for inventory, scoreboard, boss bars, recipes, permissions, persistence, and config.

## Folia

- Treat Folia as a different execution model, not a faster Paper drop-in.
- Add `folia-supported: true` only after auditing every scheduler call and every world/entity access.
- Use region, entity, async, or global schedulers according to ownership of the data being touched.
- Avoid global mutable state that assumes one tick thread.

## Velocity

- Main plugin class is annotated with `@Plugin`.
- Constructor injection is normal for `ProxyServer`, `Logger`, data directory, and event manager services.
- Register listeners through Velocity's event manager.
- Use Velocity's plugin messaging and modern forwarding APIs for proxy-to-server coordination.
- Prefer Velocity for new proxy work because its API and lifecycle are designed for modern networks.

## BungeeCord

- Main class extends `net.md_5.bungee.api.plugin.Plugin`.
- Metadata lives in `bungee.yml`.
- Use Bungee scheduler and event API, not Bukkit APIs.
- Plugin messaging differs from Velocity and Bukkit even when the concept is similar.
- Keep Bungee support in a separate module or adapter when also supporting Velocity.

## Cross-Platform Boundaries

Use interfaces in `common`:

```java
public interface PlatformScheduler {
    void runAsync(Runnable task);
    void runGlobal(Runnable task);
    void runForPlayer(UUID playerId, Runnable task);
}
```

Implement the interface separately for Bukkit/Paper, Folia, Velocity, and Bungee. Do not leak platform types into common services unless the common module is intentionally platform-specific.

## Source Pointers

- Paper development docs: https://docs.papermc.io/paper/dev/
- Paper `plugin.yml`: https://docs.papermc.io/paper/dev/plugin-yml/
- Velocity plugin basics: https://docs.papermc.io/velocity/dev/api-basics/
- BungeeCord plugin development: https://www.spigotmc.org/wiki/bungeecord-plugin-development/
