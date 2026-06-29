# Architecture

## Recommended Module Layout

```text
root
  common        # domain services, config models, storage interfaces
  bukkit        # Spigot/Paper/Folia adapter
  velocity      # Velocity adapter
  bungee        # BungeeCord adapter
  protocol      # optional packet/NMS adapters
```

Keep platform modules thin. The main plugin classes should wire dependencies, register listeners/commands, and delegate to common services.

## Service Boundaries

Good common services:

- economy/reward calculation
- queue and matchmaking rules
- permission decision logic
- persistence repositories
- serialization and message formats
- cooldowns and rate limits

Bad common service dependencies:

- `org.bukkit.Player`
- `net.md_5.bungee.api.connection.ProxiedPlayer`
- `com.velocitypowered.api.proxy.Player`
- `JavaPlugin`
- scheduler classes

Wrap those behind ports/interfaces.

## Data And Storage

- Use YAML/TOML for small plugin config.
- Use SQLite/H2 only for small single-server local state.
- Use MySQL/MariaDB/PostgreSQL for durable network data.
- Use Redis for pub/sub, ephemeral cross-server state, queues, and cache invalidation.
- Put database calls off-thread, then return to the platform scheduler before applying game changes.

## Network Design

For a proxy network:

- Keep authentication/forwarding settings consistent across proxy and backend.
- Do not expose backend servers directly to the public internet.
- Put commands that switch servers or inspect network status in proxy modules.
- Put gameplay mechanics in backend server modules.
- Use plugin messaging for request/response tasks tied to online players.
- Use Redis or database-backed events for offline players and server-independent tasks.

## Compatibility Strategy

For 1.8 through 26.2 support, avoid a single source set full of conditionals. Prefer:

- API-only common code.
- Separate implementation packages by version family.
- Multi-release artifacts only when the build and tests prove they help.
- Soft dependencies for optional integrations.
- Runtime capability detection for small differences.

## Review Checklist

- Does the code run without the optional plugin installed?
- Does it disable cleanly with a clear log when a hard dependency is absent?
- Are listeners unregistered and resources closed on shutdown?
- Are database pools, Redis connections, and executors closed?
- Are async callbacks prevented from acting after plugin disable?
- Are commands permission-checked and tab completion bounded?
- Are player UUIDs used instead of names for durable identity?
