# 杉泽流派 / Shan Ze School

把"杉泽风格 / 山海经异兽 / 东方神怪工笔奇幻"一类的需求，翻译成一套不依赖在世艺术家名字、可直接喂给图像模型的视觉语法 prompt。

这个 skill 适合做：

- 山海经、神怪、异兽、妖怪、国风神话题材的生图 prompt
- 把模糊的"想要更杉泽一点"改写成材料、笔法、构图、负面约束
- 工笔白描 + 水墨写意 + 矿物颜料的东方幻想插画方向探索
- 简短的风格说明，用来串到其它图像 / prompt 工作流里

## 安装

在本仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
cp -R shan-ze-school ~/.codex/skills/
```

如果你使用了自定义 `CODEX_HOME`：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R shan-ze-school "$CODEX_HOME/skills/"
```

安装后重启 Codex，让新 skill 生效。

## 基础用法

在 Codex 中直接调用：

```text
使用 $shan-ze-school，给我一只「九尾狐衔灯走过雪夜竹林」的杉泽流派生图 prompt
```

或者把已有 prompt 改写成杉泽流派：

```text
使用 $shan-ze-school，把这段 prompt 改成更像杉泽流派但不要出现在世艺术家的名字：……
```

## 输出模式

- **Ready-to-use prompt**：默认输出，可直接喂给图像模型
- **Prompt rewrite**：保留主体，只重写风格层和负面约束
- **Mini style note**：简短回答"为什么这像杉泽流派"，只讲可落到 prompt 上的视觉特征
- **Direct image generation**：当前会话里有图像工具时，直接出图

## 何时不要用

- 需求是艺术批评、归因、学术分类，而不是生图 prompt
- 主体不是神怪 / 异兽 / 东方幻想题材
- 想要的是当代平面设计、动漫、写实概念图、西方奇幻
- 想要更宽口径的中国插画分类，请改用 `$中国插画`

## 文件结构

```text
shan-ze-school/
  SKILL.md
  README.md
  agents/openai.yaml
  references/style-grammar.md
```
