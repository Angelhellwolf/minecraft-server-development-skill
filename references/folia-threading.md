# Folia Threading

## Mental Model

Folia splits loaded worlds into independently ticking regions. Code that was safe on one Bukkit main thread may be unsafe when multiple region threads tick in parallel. The key question is always: "Which region or entity owns this data right now?"

## Scheduler Selection

- Entity-specific work: use the entity scheduler when the action follows an entity, especially players.
- Location or chunk work: use a region scheduler for the target world/location.
- Non-world global work: use the global region scheduler only for global data that Folia designates as global.
- Blocking IO, database, HTTP, Redis, and expensive computation: use async execution, then return to the correct entity/region/global scheduler before touching Bukkit objects.

## Audit Checklist

Before setting `folia-supported: true`, search for:

- `Bukkit.getScheduler`
- `runTask`
- `runTaskTimer`
- `runTaskAsynchronously`
- `new Thread`
- `CompletableFuture`
- `getWorld`
- `getNearbyEntities`
- `teleport`
- `getChunk`
- `loadChunk`
- direct mutable maps keyed by `Player` or `Entity`

For each hit, write down the owned context. If ownership is unclear, refactor to pass UUID/location data through common services and reacquire the platform object on the correct scheduler.

## Safe Patterns

Store identifiers, not live objects:

```java
record PendingReward(UUID playerId, String rewardKey) {}
```

Reenter the correct context before touching the player:

```java
scheduler.runForPlayer(playerId, () -> {
    Player player = Bukkit.getPlayer(playerId);
    if (player != null) {
        player.sendMessage("Reward ready");
    }
});
```

Keep caches thread-safe, but do not let a thread-safe collection hide unsafe Bukkit API access.

## Dangerous Patterns

- Iterating all online players from async code and mutating inventories.
- Reading chunk/entity state from a database callback.
- Teleporting a player from a global task without using the entity scheduler.
- Sharing mutable arena/game state across regions without ownership rules.
- Assuming a command, listener, and scheduled task all run on the same thread.

## Source Pointers

- Paper guide for Folia support: https://docs.papermc.io/paper/dev/folia-support/
- Folia reference overview: https://docs.papermc.io/folia/reference/overview/
- Folia project notes: https://github.com/PaperMC/Folia
