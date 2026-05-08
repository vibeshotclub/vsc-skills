# Rare Style Explorer

用 620 条稀有 AIGC 亚种风格标签，为任意主体随机组合中文生图提示词。

这个 skill 适合做：

- 风格探索
- 生图 prompt 变体
- 产品、人物、海报、场景的视觉方向测试
- 批量寻找新鲜、具体、低频的视觉方向
- 避免“极简主义、包豪斯、赛博朋克”等泛化风格词

## 更新亮点

- 风格库从 260 条扩展到 620 条。
- 默认输出中文提示词，便于中文创作者直接筛选和复盘。
- 新增 `--freshness high`，优先抽取更新、更低频、更具体的风格条目。
- 新增 `--style-family`，可以按电影、时装、产品、摄影、插画、平面、工艺、数字、空间、材质等方向定向探索。
- 默认开启泛化词抑制，减少只抽到 cinematic、retro、surreal 这类宽泛标签。
- 新增相似度去重逻辑，降低同一批 prompt 内风格重复的概率。

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

## 在 Codex 中使用

直接调用：

```text
使用 $rare-style-explorer，帮我给「陶瓷猫香水瓶」生成 8 个稀有风格生图 prompt，偏产品图方向
```

更适合自动化探索的写法：

```text
使用 $rare-style-explorer，每 15 分钟为我的主题池随机生成 5 条高新鲜度 prompt，并保存风格 ID、prompt 和生成时间。
```

## 命令行用法

进入 skill 目录：

```bash
cd ~/.codex/skills/rare-style-explorer
```

快速随机探索：

```bash
python3 scripts/explore_styles.py "陶瓷猫香水瓶" --mode minimal --count 8 --freshness high
```

产品方向：

```bash
python3 scripts/explore_styles.py "盲盒玩具" --mode product --style-family product --freshness high --count 8
```

人物方向：

```bash
python3 scripts/explore_styles.py "武侠女侠角色" --mode character --style-family fashion --freshness high --count 5
```

海报方向：

```bash
python3 scripts/explore_styles.py "AI 知识库应用图标" --mode poster --style-family graphic --count 8 --format json
```

固定某个风格 ID，再随机变化辅助层：

```bash
python3 scripts/explore_styles.py "复古咖啡馆吉祥物" --style-id S008 --count 4
```

## 模式

- `minimal`：快速随机探索
- `product`：产品图、包装、品牌物料
- `character`：角色、头像、虚拟 IP
- `poster`：海报、封面、社媒图
- `scene`：叙事场景
- `material-series`：同主体材质系列

## 风格族

`--style-family` 可选：

- `film`：电影、影像类型、光色氛围
- `fashion`：时装、妆造、亚文化人物造型
- `product`：玩具、产品、收藏品、材质呈现
- `photography`：摄影工艺、影像缺陷、媒介质感
- `illustration`：动画、漫画、插画、绘本媒介
- `graphic`：海报、包装、目录、印刷版式
- `craft`：地域工艺、民艺纹样、历史媒介
- `digital`：UI、游戏、旧软件、屏幕媒介
- `space`：建筑、空间、场景气质
- `material`：表面材质与触感变体

## 常用参数

- `--mode`：选择生成模式。
- `--count`：生成 prompt 数量。
- `--seed`：固定随机种子，方便复现。
- `--style-id`：强制使用某个风格 ID 作为主风格。
- `--format markdown|json`：选择输出格式。
- `--freshness normal|high`：`high` 会偏向更新、更具体的条目。
- `--style-family`：限定主风格池。
- `--avoid-generic` / `--no-avoid-generic`：默认开启泛化词抑制。

## 文件结构

```text
rare-style-explorer/
  SKILL.md
  agents/openai.yaml
  references/style_library.json
  scripts/explore_styles.py
```

## 说明

`references/style_library.json` 是关键词优先的风格库。部分 2026-05 条目来自公开 Midjourney SREF 风格参考画廊与文档的关键词提炼，但本 skill 不保存、不输出 SREF code。
