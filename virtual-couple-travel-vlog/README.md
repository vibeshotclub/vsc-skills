# 虚拟情侣旅拍 Vlog Skill

这个 Skill 用来从一句简单主题生成一套完整的“虚拟情侣旅拍 Vlog”工作流资产，例如：

- `一对中国情侣在巴塞罗那的旅行vlog`
- `A young Japanese couple in Paris travel vlog`
- `一对美国夫妻在上海的旅行vlog`

它会生成一套保持人物身份一致的旅行回忆资产：4x4 iPhone 风格照片墙、自动切出的四张 2x2 记忆图、男女角色卡、四段视频生成提示词、可选的视频生成任务、中文音乐生成提示词，以及最终视频拼接方案。

注意：为了避免真人肖像权、隐私和授权风险，建议公开演示时使用纯 AI 生成的数字人情侣，不使用真实人物照片或未经授权的肖像。

## 它能做什么

1. 让使用者选择输出根目录，并在其中创建独立项目文件夹。
2. 根据主题生成一张 4x4 怀旧 iPhone 旅行照片墙，用单次生成尽量锁定同一对情侣的身份。
3. 自动把 4x4 图切成四张 2x2 记忆图，分别作为四段视频的记忆参考图。
4. 自动根据 4x4 / 2x2 参考图生成男女角色卡，包含白底、摄影棚灯光、统一服装、三视图和头像角度。
5. 为四张 2x2 图分别输出视频生成提示词。
6. 检查本机是否有可用的视频生成平台 API 或相关 Skill。
7. 默认支持 Topview Omni Reference 自动化路径；也可以和 AI 沟通接入其他平台 API，或手动复制提示词到视频生成平台。
8. 生成 `audio/music_prompt_zh.txt`，供使用者到音乐创作平台手动生成配乐。
9. 使用 FFmpeg 做简单视频拼接；需要转场、字幕、音乐节奏或可复用 React composition 时，使用 Remotion 插件能力。
10. 输出 QA 记录和生成报告。

## 输出结构

每次运行会在使用者选择的输出根目录下创建项目文件夹：

```text
<输出根目录>/<项目标题>/
  brief.md
  generation_report.md
  qa.md
  prompts/
    memory_grid_4x4.txt
    character_male.txt
    character_female.txt
    video_clip_01.txt
    video_clip_02.txt
    video_clip_03.txt
    video_clip_04.txt
  images/
    memory_grid_4x4.png
    memory_sheet_01.png
    memory_sheet_02.png
    memory_sheet_03.png
    memory_sheet_04.png
    character_male.png
    character_female.png
  videos/
    clip_01.mp4
    clip_02.mp4
    clip_03.mp4
    clip_04.mp4
    final_vlog.mp4
  audio/
    music_prompt_zh.txt
```

如果使用者选择手动生成视频，或者某个视频平台 API 不可用，部分视频文件可能暂时不会出现，但图片、角色卡和提示词仍会被完整准备好。

## 依赖要求

自动化本地工作流需要：

- Python 3.10+
- Python Pillow 模块，用于本地把 4x4 图切成四张 2x2 图
- FFmpeg 和 FFprobe，用于简单视频拼接
- Node、npm、npx，用于 Remotion 编辑路径
- Remotion plugin / skill，用于更复杂的视频编辑
- 可选：Topview skill，用于自动图片和视频生成

运行跨平台依赖检查：

```bash
python "<skill-folder>/scripts/check-tools.py" --show-install-hints
```

如果缺少必要依赖，Skill 会先提示使用者，不会静默安装。安装第三方包或 Skill 前，应先做安全审计和资源支持检查。

## 快速开始

让 Codex 使用这个 Skill，并提供主题：

```text
[$virtual-couple-travel-vlog](<path-to-skill>/SKILL.md) 一对中国情侣在巴塞罗那的旅行vlog
```

同时可以指定输出根目录，例如：

```text
使用 ~/Movies/VlogOutputs 作为输出根目录
使用 D:/AI/VlogOutputs 作为输出根目录
```

如果没有指定输出根目录，Skill 会先询问使用者要把项目保存在哪里。

运行后，Skill 会：

1. 创建项目文件夹。
2. 写入主题 brief、图片提示词、视频提示词和音乐提示词。
3. 生成一张 4x4 旅行照片墙。
4. 自动切成四张 2x2 记忆图。
5. 自动生成男女角色卡。
6. 检查可用的视频生成平台。
7. 根据平台情况自动提交视频任务，或提供手动生成指导。

## 4x4 到 2x2 的身份一致性策略

这个工作流默认不直接生成四张独立的 2x2 图，因为独立生成很容易导致情侣长相、发型、服装和年龄漂移。

更可靠的路径是：

1. 先生成一整张 4x4 旅行照片墙。
2. 在同一个图像生成上下文里锁定同一对情侣。
3. 再用本地 Python 脚本自动裁切成四张 2x2 图。
4. 用这些 2x2 图和 4x4 源图继续生成角色卡。

这样能显著降低四段视频里人物不一致的问题。

## 角色卡策略

角色卡用于帮助视频平台在四段视频里尽量保持男女主角身份一致。

角色卡提示词会强调：

- 只出现同一个角色
- 白底摄影棚灯光
- 统一服装
- 全身正面、侧面、背面
- 多个头像角度和表情
- 同比例、同地面线、正交视角
- 不要文字、logo、水印
- 不要旅行照片残影、背景碎片、拼贴残留或其他人物

如果三视图角色卡多次失败，工作流会退回到更干净的单人身份参考图，避免继续浪费生成额度。

## 视频生成平台

### Topview 自动化路径

Topview AI 是默认可选的视频生成路径。如果本机已经安装并连接 Topview skill，工作流可以使用 Topview Omni Reference 自动生成四段视频。

默认设置：

- 模式：Omni Reference
- 模型：Standard
- 画幅：9:16
- 时长：每段 15 秒
- 清晰度：默认 720p，除非使用者另行指定
- 声音：关闭
- 总长度：四段视频，约 60 秒

提交 Topview 视频任务前，Skill 会显示设置、预计消耗和等待信息，并询问使用者选择普通排队还是 Quick Generate。Quick Generate 会额外消耗积分，不会静默启用。

### 其他平台 API

Topview 不是唯一选择。使用者可以和 AI 沟通，把这个工作流接入其他支持参考图生视频的平台 API，例如：

- Seedance API
- Krea
- Lovart
- LibTV
- 其他支持多图参考、角色参考或 image-to-video 的平台

核心资产映射保持一致：

- `memory_sheet_01.png` 到 `memory_sheet_04.png`：每段视频的记忆 / contact sheet 参考图
- `character_male.png`：男主角身份参考
- `character_female.png`：女主角身份参考
- `video_clip_01.txt` 到 `video_clip_04.txt`：每段视频的生成提示词

### 手动平台模式

如果没有连接任何视频生成 API，Skill 仍然会准备完整的手动交付包。

使用方法：

1. 在你选择的视频生成平台里创建四个视频任务。
2. 每个任务上传对应的 2x2 图作为记忆参考。
3. 同时上传男女角色卡作为人物身份参考。
4. 复制对应的 `video_clip_XX.txt` 提示词。
5. 设置 9:16、15 秒，并关闭音乐和旁白。
6. 下载结果并命名为 `clip_01.mp4` 到 `clip_04.mp4`。

## 音乐说明

由于音乐版权、平台授权和使用者订阅习惯不同，这个 Skill 目前不直接生成或抓取音乐文件。

它只会生成中文音乐创作提示词：

```text
audio/music_prompt_zh.txt
```

请把这个 prompt 复制到你常用的音乐创作平台中手动生成配乐。生成后，如果希望 Codex 帮你合并音乐，把音乐文件放回项目的 `audio/` 文件夹，再让 Codex 执行最终合成。

## 视频拼接

简单拼接使用 FFmpeg：

- 四段视频按顺序连接
- 可选地嵌入使用者提供的音乐文件
- 输出 `videos/final_vlog.mp4`

需要更复杂编辑时使用 Remotion：

- 转场
- 修剪
- 字幕
- 叠加层
- 根据音乐节奏调整剪辑点
- 可复用的 React composition

默认原则：简单直连用 FFmpeg；需要设计感和可复用结构时用 Remotion。

## 安全规则

- 所有项目资产都保存在使用者选择的输出根目录下。
- 工作流不会删除文件；如需清理，必须获得使用者二次确认。
- 不会静默安装第三方 Skill 或包。
- 不会静默消耗 Quick Generate 额外积分。
- 不建议使用未经授权的真人肖像公开发布。

## 常见问题

- 如果人物身份漂移，优先重新生成 4x4 图，而不是生成四张独立 2x2 图。
- 如果角色卡含有场景残影，使用清理提示词或退回到单人身份参考图。
- 如果 Topview 不可用，继续使用手动平台交付包。
- 如果 FFmpeg 拼接失败，检查视频编码、尺寸和帧率，或切换到 Remotion / 手动剪辑软件。
