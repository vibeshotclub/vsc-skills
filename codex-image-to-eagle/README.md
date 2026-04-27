# Codex Image to Eagle

将 Codex 生成的图片归档到 Eagle，并把生成提示词写入 Eagle 的注释字段，方便后续检索、复盘和复用。

## 功能

- 自动读取 Codex 默认图片目录中的最新图片
- 支持导入最新一张图片或最新一次生成会话中的全部图片
- 将提示词写入 Eagle `annotation`
- 自动添加基础标签：`Codex`、`AI生成`、`Prompt`
- 默认按本地生成日期归档到 `Codex 生成图/YYYY-M-D`
- 支持指定 Eagle 根文件夹名称或精确文件夹 ID
- 支持跨平台默认路径：`~/.codex/generated_images`
- 支持用环境变量覆盖图片目录

## 前置条件

1. 已安装并打开 Eagle
2. Eagle MCP 插件已启用
3. Eagle MCP Server 正在运行，默认地址为 `http://localhost:41596`
4. 本机已安装 Node.js
5. Codex 生成图片保存在默认目录，或你已指定自定义目录

推荐在 Codex 中配置 Eagle 的 stdio MCP。配置好后，本 Skill 会自动读取当前用户的 `~/.codex/config.toml`，不用在命令里手动传 Eagle 地址。

示例：

```toml
[mcp_servers.eagle]
command = "node"
args = ["/你的/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"]
```

如果你的 MCP 名称不是 `eagle`，通常也没关系。脚本会自动扫描看起来像 Eagle MCP 的配置。

测试连接：

```bash
node scripts/archive-codex-image-to-eagle.js --check-connection
```

## 安装为 Codex 全局 Skill

在本仓库根目录执行，将 Skill 复制到 Codex 全局 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R codex-image-to-eagle ~/.codex/skills/
```

如果你使用了自定义 `CODEX_HOME`：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R codex-image-to-eagle "$CODEX_HOME/skills/"
```

安装后重启 Codex，让新 Skill 生效。

## 基础用法

导入最新一张 Codex 生成图：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --prompt "这里写生成图片时使用的完整提示词"
```

导入最新一次生成会话中的全部图片：

```bash
node scripts/archive-codex-image-to-eagle.js --latest-session --prompt "这里写生成图片时使用的完整提示词"
```

指定某一张图片：

```bash
node scripts/archive-codex-image-to-eagle.js --path "/absolute/path/image.png" --prompt "这里写生成图片时使用的完整提示词"
```

先预览，不写入 Eagle：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --prompt "测试提示词" --dry-run
```

如果脚本不在 Skill 目录里执行，可以用全局安装后的绝对路径：

```bash
node "$HOME/.codex/skills/codex-image-to-eagle/scripts/archive-codex-image-to-eagle.js" --latest --prompt "完整提示词"
```

## `--latest` 与 `--latest-session` 的选择规则

- `--latest`：递归扫描图片目录，选择修改时间最新的一张图片。
- `--latest-session`：扫描图片目录下的会话子目录，选择“最近有图片更新”的那个会话目录，并导入该目录下全部图片。
- 默认图片目录：`~/.codex/generated_images`。
- 当前 shell 所在目录不会影响这两个参数的选择结果。
- 如果你要读取其他目录，用 `--image-dir "/path/to/generated_images"` 或环境变量 `CODEX_GENERATED_IMAGES_DIR` 指定。

## 指定 Eagle 文件夹

默认会按图片本地修改日期归档到日期子目录：

```text
Codex 生成图/
  2026-4-26/
  2026-4-27/
```

按根文件夹名称导入，若不存在会自动创建根文件夹和日期子目录：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --folder-name "Codex 生成图" --prompt "完整提示词"
```

按文件夹 ID 导入时，会把图片直接放入该 ID 对应的精确文件夹，不再自动创建日期子目录：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --folder-id "FOLDER_ID" --prompt "完整提示词"
```

如果你想恢复旧版扁平归档，不按日期分组：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --no-date-subfolders --prompt "完整提示词"
```

## 自定义图片目录

默认目录为当前用户家目录下的：

```text
~/.codex/generated_images
```

也可以用参数覆盖：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --image-dir "/path/to/generated_images" --prompt "完整提示词"
```

或用环境变量覆盖：

```bash
export CODEX_GENERATED_IMAGES_DIR="/path/to/generated_images"
node scripts/archive-codex-image-to-eagle.js --latest --prompt "完整提示词"
```

## 在 Codex 对话中触发

安装为全局 Skill 后，可以直接对 Codex 说：

```text
使用 codex-image-to-eagle，把刚刚生成的图存入 Eagle，并把完整提示词写入注释。
```

也可以在生成图片时一起要求：

```text
生成一张赛博禅意茶室图，完成后用 codex-image-to-eagle 保存到 Eagle，并附上本次提示词。
```

## 写入 Eagle 的注释格式

```text
Prompt:
这里是完整提示词

Archive:
- source: Codex
- original_path: /path/to/original/image.png
- archived_at: 2026-04-27T00:00:00.000Z
```

## 已验证用法

当前脚本已验证：

- `--help`
- `--latest --dry-run`
- `--latest-session --dry-run`
- `--path ... --dry-run`
- `--prompt-file ... --dry-run`
- `--prompt-stdin --dry-run`
- `--folder-name ... --dry-run`
- `--folder-id ... --dry-run`
- `--no-date-subfolders --dry-run`
- Eagle MCP 连通性
- Eagle `item_add` 实际写入链路，已用于批量归档 Codex 生成图

未建议随意反复测试实际写入命令，因为会在 Eagle 中产生重复素材。正式导入前建议先加 `--dry-run` 看清楚将要写入的图片、文件夹和注释。

## 常见问题

### Skill 会自动监听目录吗？

不会。Codex Skill 不是常驻后台服务。它会在 Codex 对话中识别到归档意图后触发，然后读取最新图片并导入 Eagle。

### Eagle MCP Server 必须开启吗？

必须。这个 Skill 通过 Eagle MCP 写入素材库，不直接修改 Eagle 资源库文件。

### 找不到图片怎么办？

先确认 Codex 是否已生成图片，并检查目录：

```bash
ls ~/.codex/generated_images
```

如果你的图片目录不同，用 `--image-dir` 或 `CODEX_GENERATED_IMAGES_DIR` 指定。

### 如何避免误导入？

先用 `--dry-run` 查看将要导入的图片、标签、文件夹和注释内容，确认后再执行正式导入。
