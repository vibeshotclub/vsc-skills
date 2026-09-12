# SUMMER BOYFRIEND POV

成年人物夏季泳装自然抓拍 Skill：每次生成 **一张独立照片**，支持单人、双人、多人同框，人物垫图和任意媒介角色 COS。

## 适合场景

- Boyfriend / Partner / Friend / Companion POV 的私人夏季旅行抓拍。
- 多人物参考分别保持身份，在同一地点、同一瞬间自然互动。
- 电影、游戏、动漫、漫画、电视剧、小说、特摄、虚拟角色、原创 IP 或 OC 的现实成年 COS。
- 人物、构图、姿势、服装、场景和摄影风格参考分开使用。

角色保留视觉 DNA 和人格，服装转译为真实可穿的角色泳装。全部相关泳装人物明确为 21–30 岁成年人；默认现实夏季场景和 Level 2 可辨识真人 COS。

**单图不等于单人。** 所有人共处一个连续场景；禁止拼图、contact sheet、grid、split screen、storyboard、multi-panel 和多照片合一。

## 安装

在仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
cp -R summer-boyfriend-pov ~/.codex/skills/
```

使用自定义 `CODEX_HOME` 时，将安装位置替换为 `$CODEX_HOME/skills/`。安装后新开 Codex 对话；未出现时重启 Codex。

## 使用示例

### 自由生成

```text
使用 $summer-boyfriend-pov，生成一张夏季旅行自然抓拍照片，其他自由选择。
```

预期输出：一张成年人物在夏季水边自然活动的独立照片，真实皮肤、自然光和熟悉的伴侣视角。

### 双人垫图 + 双角色 COS

```text
使用 $summer-boyfriend-pov，参考图 A 对应人物 A，COS 蒂法；参考图 B 对应人物 B，COS 爱丽丝。两位 25 岁成年朋友在泳池泼水，Friend POV。
```

预期输出：两人同时出现在一张照片中，各自保持参考身份、角色发型、独立泳装和人格，动作属于同一泼水事件。

### 多人同框

```text
使用 $summer-boyfriend-pov，三位成年旅行伙伴在海边，一人递浴巾、一人接住、另一人在旁笑，Companion POV，一张独立照片。
```

### 分职责参考

```text
使用 $summer-boyfriend-pov，第一张只参考成年人物身份，第二张只参考姿势和构图，第三张只参考 CCD 摄影风格，COS 2B，9:16。
```

### 只要提示词

```text
使用 $summer-boyfriend-pov，只给一段完整提示词：25 岁成年 COSER、我的 OC、Level 3、湖边木码头、Partner POV。OC 设定为银色短发、青白配色、月牙发饰、性格克制。
```

## 输出与依赖

- 默认执行目标为 **ONE STANDALONE PHOTOGRAPH**，需要当前会话提供图像生成工具；垫图模式需要工具支持参考图输入。
- 只要提示词时输出一段可直接用于生图的摄影提示词；无图像工具时说明限制并提供提示词。
- 不绑定特定图像服务，无专属脚本、API 密钥或本地运行库要求。
- 角色身份、用户指定条件和参考职责保持稳定，其余摄影细节按场景选择。

## 文件结构

```text
summer-boyfriend-pov/
├── SKILL.md
├── README.md
├── agents/openai.yaml
└── references/creative-direction.md
```

`SKILL.md` 是执行入口；[完整创作规则](references/creative-direction.md) 保存人物、COS、参考、场景、摄影与单图检查细节。
