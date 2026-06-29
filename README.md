# Minecraft Server Development

面向 Minecraft Java 服务端开发的跨 Agent 规范包和复用工具。

这个仓库不是 Minecraft 插件 jar，而是一套给 AI 编程 Agent 使用的开发规范。它用于辅助设计、实现、审查和调试 Spigot、Paper、Folia、Velocity、BungeeCord 插件与代理项目，覆盖从旧版 1.8.x 到当前 26.x/26.2 时代的服务端开发。

## 支持内容

- Codex：通过 `AGENTS.md` 和 `SKILL.md` 使用
- Claude Code：通过 `CLAUDE.md` 使用
- Gemini CLI：通过 `GEMINI.md` 使用
- 通用 AI 编程 Agent：通过 `AGENTS.md` 使用
- Bukkit、Spigot、Paper、Folia、Velocity、BungeeCord 项目设计
- 协议、NMS、数据包、插件消息、调度器、底层架构开发
- 从 1.8.x 旧版服务端到 26.x 目标版本的跨版本兼容规划

## 仓库结构

```text
.
|-- AGENTS.md                  # Codex 和通用 Agent 的共享主规范
|-- CLAUDE.md                  # Claude Code 入口
|-- GEMINI.md                  # Gemini CLI 入口
|-- SKILL.md                   # Codex skill 入口
|-- agent-plugin.json          # 跨 Agent 插件清单
|-- gemini-extension.json      # Gemini/Antigravity 扩展元数据
|-- plugin.yaml                # 通用插件宿主元数据
|-- package.json               # npm/OpenCode 风格包元数据
|-- .codex-plugin/             # Codex 插件清单
|-- .claude-plugin/            # Claude Code 插件清单
|-- agents/openai.yaml         # Codex UI 元数据
|-- commands/                  # slash command 风格命令提示
|-- skills/                    # skill-capable 宿主可加载的技能
|-- references/                # 平台、Folia、协议、架构、构建测试参考资料
`-- scripts/                   # 项目生成器、安装和校验脚本
```


## 参考 Ponytail 的设计

这个仓库参考了 `DietrichGebert/ponytail` 的多宿主插件设计：

- 根目录保留 `AGENTS.md` 作为所有 Agent 的共享核心规则。
- 为不同宿主提供轻量入口：`.codex-plugin/`、`.claude-plugin/`、`gemini-extension.json`、`plugin.yaml`。
- 把可触发能力拆成 `skills/` 和 `commands/`，而不是只靠 README 描述。
- 用 `agent-plugin.json` 描述支持的 Agent、入口文件、参考资料、脚本和目标平台。
- 不引入不需要的 hooks、MCP、benchmark 或品牌资源，保持这个包专注于 Minecraft 开发规范。

## 安装到现有项目

把所有 Agent 入口文件安装到另一个 Minecraft 插件项目：

```bash
python scripts/install_agent_rules.py --target /path/to/plugin --agent all --references --manifest
```

只安装某一个 Agent 的入口：

```bash
python scripts/install_agent_rules.py --target /path/to/plugin --agent codex --references
python scripts/install_agent_rules.py --target /path/to/plugin --agent claude --references
python scripts/install_agent_rules.py --target /path/to/plugin --agent gemini --references
```

如果目标项目已经有同名文件，可以加 `--force` 覆盖。

## 生成插件项目骨架

创建一个最小化的多模块 Gradle 项目：

```bash
python scripts/create_minecraft_project.py \
  --name ExamplePlugin \
  --package dev.example.plugin \
  --platforms bukkit,velocity,bungee \
  --output ./generated
```

生成的项目包含：

- `common`：不依赖平台 API 的业务逻辑
- `bukkit`：面向 Spigot、Paper、Folia 的服务端代码
- `velocity`：Velocity 代理端代码
- `bungee`：BungeeCord 代理端代码

发布前请根据真实目标版本调整依赖版本、Java toolchain、插件元数据、Folia 支持状态和测试矩阵。

## 核心规范

- 业务逻辑不要和平台适配器混在一起。
- Folia 是不同的线程模型，不是普通 Paper 的简单替代品。
- 不要从任意异步线程访问 Bukkit 的世界、实体、区块或玩家状态。
- 协议、NMS、反射、Netty 代码必须隔离在窄接口适配器后面。
- 优先使用稳定平台 API，再考虑原始数据包或反射。
- 至少验证最旧和最新的目标服务端版本。
- 没有测试或查证当前资料前，不要声明 Folia 或 26.x/26.2 兼容。

## 参考资料

- `references/platforms.md`：Spigot、Paper、Folia、Velocity、BungeeCord 差异
- `references/folia-threading.md`：Folia 调度器和区域化线程规则
- `references/protocol-and-nms.md`：数据包、NMS、反射和协议安全
- `references/architecture.md`：多模块项目和服务器网络架构设计
- `references/build-and-test.md`：Gradle、Maven、Java、shade、CI 和测试矩阵

## Codex Skill 用法

这个仓库也是一个有效的 Codex skill。把本仓库复制或克隆到 Codex skills 目录后，可以这样调用：

```text
Use $minecraft-server-development to design a cross-platform Minecraft plugin.
```

## 许可证

MIT License。
