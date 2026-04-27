# Codex Image to Eagle

将 Codex 生成的图片归档到 Eagle，并把生成提示词写入 Eagle 的注释字段，方便后续检索、复盘和复用。

## 功能

- 自动读取 Codex 默认图片目录中的最新图片
- 支持导入最新一张图片或最新一次生成会话中的全部图片
- 将提示词写入 Eagle `annotation`
- 自动添加基础标签：`Codex`、`AI生成`、`Prompt`
- 支持指定 Eagle 文件夹名称或文件夹 ID
- 支持跨平台默认路径：`~/.codex/generated_images`
- 支持用环境变量覆盖图片目录

## 前置条件

1. 已安装并打开 Eagle
2. Eagle MCP 插件已启用
3. Eagle MCP Server 正在运行，默认地址为 `http://localhost:41596`
4. 本机已安装 Node.js
5. Codex 生成图片保存在默认目录，或你已指定自定义目录

可用下面命令测试 Eagle MCP 是否可访问：

```bash
node -e 'const http=require("http");const body=JSON.stringify({tool:"get_app_info",params:{}});const req=http.request({hostname:"localhost",port:41596,path:"/api/tools/call",method:"POST",headers:{"Content-Type":"application/json","Content-Length":Buffer.byteLength(body)}},res=>res.pipe(process.stdout));req.on("error",err=>{console.error(err.message);process.exit(1)});req.end(body);'
```

## 安装为 Codex 全局 Skill

将本目录复制到 Codex 全局 skills 目录：

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

## 指定 Eagle 文件夹

按文件夹名称导入，若不存在会自动创建：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --folder-name "Codex 生成图" --prompt "完整提示词"
```

按文件夹 ID 导入：

```bash
node scripts/archive-codex-image-to-eagle.js --latest --folder-id "FOLDER_ID" --prompt "完整提示词"
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
