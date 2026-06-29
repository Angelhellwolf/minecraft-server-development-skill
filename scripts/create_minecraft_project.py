#!/usr/bin/env python3
"""Create a minimal multi-module Minecraft plugin/proxy project."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VALID_PLATFORMS = {"bukkit", "velocity", "bungee"}


def package_path(package: str) -> Path:
    return Path(*package.split("."))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def java_identifier(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "", value)
    if not cleaned:
        return "MinecraftPlugin"
    if cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned[0].upper() + cleaned[1:]


def plugin_id(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_-]", "-", value.lower())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-_")
    return cleaned or "minecraft-plugin"


def parse_platforms(value: str) -> list[str]:
    platforms = [part.strip().lower() for part in value.split(",") if part.strip()]
    unknown = sorted(set(platforms) - VALID_PLATFORMS)
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown platforms: {', '.join(unknown)}")
    return platforms or ["bukkit"]


def create_project(args: argparse.Namespace) -> None:
    root = Path(args.output).resolve() / args.name
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {root}")

    class_name = java_identifier(args.name)
    plugin_identifier = plugin_id(args.name)
    pkg_dir = package_path(args.package)
    platforms = args.platforms
    modules = ["common"] + platforms

    write(
        root / "settings.gradle.kts",
        f"""pluginManagement {{
    repositories {{
        gradlePluginPortal()
        mavenCentral()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        mavenCentral()
        maven("https://repo.papermc.io/repository/maven-public/")
        maven("https://hub.spigotmc.org/nexus/content/repositories/snapshots/")
        maven("https://oss.sonatype.org/content/repositories/snapshots/")
    }}
}}

rootProject.name = "{args.name}"
{chr(10).join(f'include("{module}")' for module in modules)}
""",
    )

    write(
        root / "build.gradle.kts",
        f"""plugins {{
    java
}}

subprojects {{
    apply(plugin = "java")

    group = "{args.package}"
    version = "0.1.0"

    java {{
        toolchain.languageVersion.set(JavaLanguageVersion.of({args.java}))
    }}

    tasks.withType<JavaCompile>().configureEach {{
        options.encoding = "UTF-8"
    }}
}}
""",
    )

    write(
        root / "common" / "build.gradle.kts",
        """plugins {
    `java-library`
}
""",
    )
    write(
        root / "common" / "src/main/java" / pkg_dir / "common/PluginService.java",
        f"""package {args.package}.common;

public final class PluginService {{
    public String startupMessage() {{
        return "{args.name} enabled";
    }}
}}
""",
    )

    if "bukkit" in platforms:
        write(
            root / "bukkit" / "build.gradle.kts",
            f"""dependencies {{
    implementation(project(":common"))
    compileOnly("io.papermc.paper:paper-api:{args.minecraft_version}-R0.1-SNAPSHOT")
}}
""",
        )
        write(
            root / "bukkit" / "src/main/resources/plugin.yml",
            f"""name: {args.name}
version: 0.1.0
main: {args.package}.bukkit.{class_name}BukkitPlugin
api-version: "{args.minecraft_version}"
folia-supported: false
""",
        )
        write(
            root / "bukkit" / "src/main/java" / pkg_dir / "bukkit" / f"{class_name}BukkitPlugin.java",
            f"""package {args.package}.bukkit;

import {args.package}.common.PluginService;
import org.bukkit.plugin.java.JavaPlugin;

public final class {class_name}BukkitPlugin extends JavaPlugin {{
    private final PluginService service = new PluginService();

    @Override
    public void onEnable() {{
        getLogger().info(service.startupMessage());
    }}
}}
""",
        )

    if "velocity" in platforms:
        write(
            root / "velocity" / "build.gradle.kts",
            f"""dependencies {{
    implementation(project(":common"))
    compileOnly("com.velocitypowered:velocity-api:{args.velocity_version}")
    annotationProcessor("com.velocitypowered:velocity-api:{args.velocity_version}")
}}
""",
        )
        write(
            root / "velocity" / "src/main/java" / pkg_dir / "velocity" / f"{class_name}VelocityPlugin.java",
            f"""package {args.package}.velocity;

import {args.package}.common.PluginService;
import com.google.inject.Inject;
import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.event.proxy.ProxyInitializeEvent;
import com.velocitypowered.api.plugin.Plugin;
import org.slf4j.Logger;

@Plugin(id = "{plugin_identifier}", name = "{args.name}", version = "0.1.0")
public final class {class_name}VelocityPlugin {{
    private final Logger logger;
    private final PluginService service = new PluginService();

    @Inject
    public {class_name}VelocityPlugin(Logger logger) {{
        this.logger = logger;
    }}

    @Subscribe
    public void onProxyInitialization(ProxyInitializeEvent event) {{
        logger.info(service.startupMessage());
    }}
}}
""",
        )

    if "bungee" in platforms:
        write(
            root / "bungee" / "build.gradle.kts",
            f"""dependencies {{
    implementation(project(":common"))
    compileOnly("net.md-5:bungeecord-api:{args.bungee_version}")
}}
""",
        )
        write(
            root / "bungee" / "src/main/resources/bungee.yml",
            f"""name: {args.name}
version: 0.1.0
main: {args.package}.bungee.{class_name}BungeePlugin
""",
        )
        write(
            root / "bungee" / "src/main/java" / pkg_dir / "bungee" / f"{class_name}BungeePlugin.java",
            f"""package {args.package}.bungee;

import {args.package}.common.PluginService;
import net.md_5.bungee.api.plugin.Plugin;

public final class {class_name}BungeePlugin extends Plugin {{
    private final PluginService service = new PluginService();

    @Override
    public void onEnable() {{
        getLogger().info(service.startupMessage());
    }}
}}
""",
        )

    write(
        root / ".gitignore",
        """.gradle/
build/
out/
*.iml
""",
    )

    print(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Project/plugin name")
    parser.add_argument("--package", required=True, help="Base Java package")
    parser.add_argument("--output", required=True, help="Parent output directory")
    parser.add_argument("--platforms", type=parse_platforms, default=["bukkit"], help="Comma-separated: bukkit,velocity,bungee")
    parser.add_argument("--minecraft-version", default="1.21.8", help="Paper API Minecraft version")
    parser.add_argument("--velocity-version", default="3.4.0-SNAPSHOT", help="Velocity API version")
    parser.add_argument("--bungee-version", default="1.21-R0.3-SNAPSHOT", help="BungeeCord API version")
    parser.add_argument("--java", type=int, default=21, help="Gradle toolchain Java version")
    create_project(parser.parse_args())


if __name__ == "__main__":
    main()
