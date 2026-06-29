# Build And Test

## Java Version Guidance

- Minecraft 1.8-1.16 plugin compatibility usually implies Java 8 bytecode unless the user controls the runtime.
- Modern Paper/Velocity targets often require newer Java. Verify the target server version before setting toolchains.
- Do not compile a single artifact to Java 21 if it must load on Java 8 legacy servers.

## Gradle Guidance

- Use Gradle toolchains for reproducible Java versions.
- Keep platform dependencies `compileOnly` unless the dependency must be shaded.
- Relocate shaded libraries to avoid conflicts with other plugins.
- Keep common code free of platform APIs unless the module name says otherwise.
- Prefer version catalogs for large projects.

## Maven Guidance

- Use `provided` scope for server/proxy APIs.
- Use shade plugin relocation for bundled libraries.
- Keep source/target bytecode aligned with the oldest target runtime.

## Local Testing Matrix

Minimum smoke tests:

- Plugin loads and disables cleanly.
- Commands register and permission failures are handled.
- Listeners fire once and do not leak after reload/disable.
- Config loads defaults and rejects malformed values.
- Database/cache connections close on disable.
- Protocol adapters fail loudly on unsupported versions.

Version matrix:

- Oldest supported server.
- Newest supported server.
- Folia when Folia support is advertised.
- Velocity and Bungee separately when both proxy jars are shipped.

## CI Suggestions

- Build on pull request and push.
- Run unit tests for common services.
- Run static analysis or Error Prone/SpotBugs when the project already uses them.
- Publish artifacts only from tagged releases.
- Keep server smoke tests optional if they are too heavy for every PR, but document the command.

## Common Commands

```bash
./gradlew clean build
./gradlew test
./gradlew shadowJar
```

On Windows:

```powershell
.\gradlew.bat clean build
```

## Release Notes Checklist

- Supported Minecraft versions.
- Supported platforms.
- Java runtime requirement.
- Folia support status.
- Proxy forwarding requirements.
- Known incompatible plugins or server forks.
