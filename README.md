# VSC Skills

VSC 社区维护的 Codex Skills 集合，面向 AIGC 创作、提示词设计、视觉风格探索、视频工作流和生成资产管理。

这个仓库将可重复使用的创作方法封装成独立 Skill。安装后，可以在 Codex 中通过 `$skill-name` 直接调用，也可以在此基础上继续扩展自己的创作工作流。

## Skill 导航

| Skill | 用途 | 适合场景 |
| --- | --- | --- |
| [`codex-image-to-eagle`](./codex-image-to-eagle/) | 将 Codex 生成图片归档到 Eagle，并保存提示词、标签和文件夹信息 | 图片归档、素材管理、提示词复盘 |
| [`rare-style-explorer`](./rare-style-explorer/) | 从 620 条稀有视觉亚风格中组合中文生图提示词 | 风格探索、产品图、人物、海报、场景创意 |
| [`shan-ze-school`](./shan-ze-school/) | 生成新东方神话、山海经异兽、工笔水墨奇幻方向的提示词 | 东方神怪、异兽、国风神话插画 |
| [`vibeshot-candid-photography`](./vibeshot-candid-photography/) | 生成真实生活感、偶然抓拍感、非常规机位的人像摄影提示词 | 韩系人像、生活写真、自然遮挡、批量摄影提示词 |
| [`virtual-couple-travel-vlog`](./virtual-couple-travel-vlog/) | 从旅行主题生成虚拟情侣照片墙、角色卡、视频提示词和成片工作流 | 虚拟情侣、旅行 Vlog、连续人物资产、视频制作 |

每个 Skill 的详细能力、依赖和示例，请进入对应目录查看 `README.md`。

## 快速安装

### 1. 克隆仓库

```bash
git clone https://github.com/vibeshotclub/vsc-skills.git
cd vsc-skills
```

### 2. 安装单个 Skill

以 `vibeshot-candid-photography` 为例：

```bash
mkdir -p ~/.codex/skills
cp -R vibeshot-candid-photography ~/.codex/skills/
```

安装其他 Skill 时，将目录名替换成对应的 Skill 名称即可。

### 3. 安装仓库中的全部 Skill

在仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
for skill_dir in */; do
  if [ -f "${skill_dir}SKILL.md" ]; then
    cp -R "${skill_dir%/}" ~/.codex/skills/
  fi
done
```

如果使用了自定义 `CODEX_HOME`，请将 `~/.codex/skills` 替换为对应的 Skills 目录。安装后新开一个 Codex 对话；如果 Skill 没有立即出现，请重启 Codex。

## 如何使用

在 Codex 中直接写出 `$skill-name`，再描述具体任务。

### 生成真实抓拍人像提示词

```text
使用 $vibeshot-candid-photography，生成 5 组，全部使用荷塘场景，BM 风，低机位为主。
```

### 探索稀有视觉风格

```text
使用 $rare-style-explorer，给「陶瓷猫香水瓶」生成 8 个稀有风格生图提示词，偏产品图方向。
```

### 生成东方神话异兽提示词

```text
使用 $shan-ze-school，为「九尾狐衔灯走过雪夜竹林」生成一组东方神怪工笔水墨提示词。
```

### 创建虚拟情侣旅行 Vlog

```text
使用 $virtual-couple-travel-vlog，制作一对中国情侣在巴塞罗那旅行的虚拟 Vlog。
```

### 归档 Codex 生成图片

```text
使用 $codex-image-to-eagle，把刚刚生成的图片和提示词归档到 Eagle。
```

## 仓库结构

```text
vsc-skills/
├── README.md
├── codex-image-to-eagle/
├── rare-style-explorer/
├── shan-ze-school/
├── vibeshot-candid-photography/
└── virtual-couple-travel-vlog/
```

一个 Skill 通常包含：

```text
skill-name/
├── SKILL.md              # Codex 读取的核心指令
├── README.md             # 面向使用者的说明和示例
├── agents/openai.yaml    # 可选的界面与调用元数据
├── references/           # 可选的参考资料
├── scripts/              # 可选的自动化脚本
└── assets/               # 可选的模板或素材
```

其中 `SKILL.md` 是必需文件，其余内容根据工作流需要添加。

## 创建或贡献 Skill

提交新 Skill 前，请确认：

- Skill 使用小写字母、数字和连字符命名
- `SKILL.md` 包含有效的 `name` 与 `description` YAML 元数据
- 触发条件明确，不会误匹配大量无关任务
- 用户指定的条件优先于默认规则
- README 至少说明用途、安装方式和一组输入输出示例
- 脚本、引用文件和资源都能从 `SKILL.md` 中找到明确入口
- 没有提交密钥、账号、私人路径或生成缓存

可以使用 Codex 自带的校验脚本检查 Skill：

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./skill-name
```

建议每次提交只解决一个清晰问题，并在 Pull Request 中说明：

1. Skill 解决什么任务
2. 什么情况下应该触发
3. 用户输入与预期输出
4. 是否需要额外工具、服务或本地依赖

## 使用说明

- 不同 Skill 的外部依赖不同，请以各目录 README 为准。
- 涉及第三方平台、API、付费生成或本地软件时，请先确认权限、费用和运行环境。
- 生成内容仍需使用者根据实际模型、平台规则和发布场景进行审核。
