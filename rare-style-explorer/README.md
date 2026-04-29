# Rare Style Explorer

用 260 条稀有 AIGC 亚种风格标签，为任意主体随机组合生图提示词。

这个 skill 适合做：

- 风格探索
- 生图 prompt 变体
- 产品、人物、海报、场景的视觉方向测试
- 避免“极简主义、包豪斯、赛博朋克”等泛化风格词

## 安装

在本仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
cp -R rare-style-explorer ~/.codex/skills/
```

如果你使用了自定义 `CODEX_HOME`：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R rare-style-explorer "$CODEX_HOME/skills/"
```

安装后重启 Codex，让新 skill 生效。

## 基础用法

在 Codex 中直接调用：

```text
使用 $rare-style-explorer，帮我给「陶瓷猫香水瓶」生成 8 个稀有风格生图 prompt
```

也可以直接运行脚本：

```bash
cd ~/.codex/skills/rare-style-explorer
python3 scripts/explore_styles.py "ceramic cat perfume bottle" --mode product --count 6 --seed 42
```

## 模式

- `minimal`：快速随机探索
- `product`：产品图、包装、品牌物料
- `character`：角色、头像、虚拟 IP
- `poster`：海报、封面、社媒图
- `scene`：叙事场景
- `material-series`：同主体材质系列

示例：

```bash
python3 scripts/explore_styles.py "martial arts heroine" --mode character --count 5
python3 scripts/explore_styles.py "AI knowledge base app icon" --mode poster --count 8 --format json
python3 scripts/explore_styles.py "retro cafe mascot" --style-id S008 --count 4
```

## 文件结构

```text
rare-style-explorer/
  SKILL.md
  agents/openai.yaml
  references/style_library.json
  scripts/explore_styles.py
```
