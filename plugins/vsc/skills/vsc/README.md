# VSC 创作入口

描述你想做的作品，`vsc` 会结合当前对话，选择合适且可用的 VSC 技能并直接执行。已有的具体技能仍可独立调用。

## 使用

在 Codex 中使用 `$vsc`：

```text
$vsc 给陶瓷猫香水瓶探索 8 种稀有视觉风格，只要提示词。
```

会进入风格探索技能，执行其工作流程并交付提示词，不要求再复制一段技能调用指令。

```text
$vsc 两位成年朋友 COS 蒂法与爱丽丝，泳装、泳池泼水、朋友视角，生成一张照片。
```

会选择夏季 POV 技能；实际生图需要宿主提供可用的图片生成工具。

```text
$vsc
```

已有需求时接着处理；新对话没有需求时，简短介绍能力并询问想做什么。也可以输入 `$vsc 有哪些能力？`。

技能也将 `/vsc` 作为文本触发方式。它能否成为客户端原生斜杠命令、是否需要命名空间，由客户端和安装方式决定；本仓库当前以 Codex 的 `$vsc` 为调用示例，未对其他客户端的原生斜杠命令作兼容性承诺。

## 安装

推荐按[仓库安装说明](../README.md#快速安装)安装全部技能，这样入口可以调用当前全部创作能力。仅复制 `vsc` 目录不会自动安装其他技能。

也可在仓库根目录只安装入口和需要的技能：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R vsc rare-style-explorer "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后新开 Codex 对话，必要时重启客户端。技能发现脚本需要 Python 3.10+，仅使用标准库；Python 不可用时，入口可读取随包目录并核对宿主提供的技能路径。各创作技能的依赖仍以各自说明为准。

## 工作边界

- 默认选择一个技能并执行，不做通用多技能自动编排。
- 用户只要提示词或方案时，不自动生成图片或视频。
- 最匹配技能未安装或当前没有合适能力时，说明缺口，不强行替换。
- 同名不同内容的技能存在于多个目录时，先核对宿主实际使用的路径。
- 图片和视频工具暂不可用时，说明替代交付与原目标的差别。
- 不自动联网更新目录、安装技能或安装工具。

## 本地发现

```bash
python3 vsc/scripts/discover_skills.py
```

默认检查入口同级目录、最近项目的技能目录、用户的 `.agents/skills`、Codex 技能目录（尊重 `CODEX_HOME`）和 `.claude/skills`。不递归扫描整个磁盘，也不假定插件都安装在这些位置。

指定安装目录时，`--root` 替换全部默认范围，可重复指定：

```bash
python3 vsc/scripts/discover_skills.py --root /path/to/skills
```

返回 `available`、`missing`、`invalid` 或 `conflict`。`available` 仅表示定义可读；`needs_review` 表示该安装内容不同于发布目录，需要按实际技能校准能力。

## 新增或更新技能

路由信息维护在每个创作技能的 `SKILL.md` frontmatter 中。入口只保存生成后的目录，不手写第二份能力说明。

```yaml
metadata:
  vsc-category: "风格探索"
  vsc-deliverables: "prompt"
  vsc-distinction: "说明适用对象，以及与最容易混淆的技能有什么区别。"
```

`vsc-deliverables` 使用逗号分隔，可选 `prompt`、`image`、`video`、`workflow`、`archive`。只登记技能实际支持的交付，不能把“有生图提示词”写成“支持实际图片”。分类用于导航，不作为关键词路由表。

维护工具需要 PyYAML，用户运行入口不需要安装它。维护环境可安装 `tools/requirements.txt`，然后在仓库根目录运行：

```bash
python3 tools/build_vsc_catalog.py
python3 tools/build_vsc_catalog.py --check
python3 -m unittest discover -s tests -v
```

提交技能变更时一并提交生成的 `vsc/references/catalog.json`。目录带内容校验值，因此正文更新也需要重新构建。构建时会拒绝缺少路由信息的新技能，避免新增后悄悄漏出目录。

目录随 `vsc` 分发，已有用户需更新本地入口才能发现新登记技能。更新子技能后仍使用旧目录时，会提示读取实际定义校准。

模型路由验收用例见 [tests/vsc-routing-cases.md](../tests/vsc-routing-cases.md)。目录自动化检查不等于模型路由准确率测试。
