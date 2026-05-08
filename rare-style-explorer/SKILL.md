---
name: rare-style-explorer
description: Generate and refine AIGC image prompts by combining rare, prompt-ready visual sub-style tags from a bundled 620-entry style library. Use when the user wants style exploration, image prompt variants, rare visual styles, non-generic aesthetics, style mixing, prompt matrices, or subject-to-style ideation for image generation.
---

# Rare Style Explorer

## Overview

Use this skill to turn a subject into reusable AIGC prompt variants using rare sub-style tags rather than broad labels such as minimalism, Bauhaus, or cyberpunk.

The bundled library lives at `references/style_library.json`. Load it only when the user asks for specific style lookup, filtering, auditing, or manual curation. For normal prompt generation, run `scripts/explore_styles.py`.

The library is keyword-first. Some 2026-05 entries were distilled from public Midjourney SREF style-reference galleries and documentation, but this skill does not store SREF codes and should not output `--sref` parameters unless the user explicitly changes the goal.

Final prompt variants should be written in Chinese by default. English prompt tokens remain in the style metadata for lookup and manual conversion, but the user-facing prompt text should use Chinese style names, Chinese visual DNA, and Chinese anti-drift constraints.

## Default Workflow

1. Identify the subject and output goal.
   - Product or packaging: prefer `product`.
   - Character, avatar, IP, portrait: prefer `character`.
   - Poster, cover, social visual: prefer `poster`.
   - Narrative scene: prefer `scene`.
   - Same subject with multiple surfaces: prefer `material-series`.
   - Fast exploration: use `minimal`.

2. Generate combinations with:

```bash
python3 scripts/explore_styles.py "SUBJECT" --mode minimal --count 8 --freshness high
```

3. Review the generated style IDs and remove combinations that conflict with the subject, platform, or brand.

4. If the user asks for a more targeted direction, use `--style-family`:
   - `film`: cinematic genres and light color
   - `fashion`: editorial styling and subculture looks
   - `product`: toy/product/material presentation
   - `photography`: photographic tone and media defects
   - `illustration`: drawing, manga, animation, and picture-book media
   - `graphic`: posters, packaging, catalogs, and print layouts
   - `craft`: regional craft, folk pattern, and historical media
   - `digital`: UI, game, old software, and screen media
   - `space`: architectural and scene atmosphere
   - `material`: surface and tactile material variants

5. Output in this order unless the user requests another format:
   1. analysis dimensions
   2. selected style logic
   3. prompt variants
   4. variable slots
   5. negative constraints
   6. reusable template

## Combination Rules

Build each prompt from:

```text
{subject}，{base_style}，{surface_or_light}，{format_or_space}，
主体轮廓清晰，视觉识别度强，高细节，
避免泛化的现代极简风，避免随机多余文字，避免混乱符号，
避免丢失主体身份
```

Use one strong base style. Add zero or one surface/light style. Add zero or one format/space style. Add zero or one defect layer only when a more analog or media-specific finish is useful.

Do not stack too many strong style anchors. If the subject is fragile, such as a logo, facial identity, product silhouette, or readable packaging, prioritize recognizability over novelty.

## Script Usage

Run from the skill folder:

```bash
python3 scripts/explore_styles.py "ceramic cat perfume bottle" --mode product --count 6 --seed 42
python3 scripts/explore_styles.py "martial arts heroine" --mode character --count 5
python3 scripts/explore_styles.py "AI knowledge base app icon" --mode poster --count 8 --format json
python3 scripts/explore_styles.py "retro cafe mascot" --style-id S008 --count 4
python3 scripts/explore_styles.py "fashion portrait" --mode character --style-family fashion --freshness high --count 8
python3 scripts/explore_styles.py "blind box toy" --mode product --style-family product --freshness high --count 8
```

Useful options:

- `--mode`: `minimal`, `product`, `character`, `poster`, `scene`, `material-series`.
- `--count`: number of prompt variants.
- `--seed`: reproducible random seed.
- `--style-id`: force a base style by library ID, then vary supporting layers.
- `--format`: `markdown` or `json`.
- `--freshness`: `normal` or `high`; `high` biases toward newer, lower-frequency, visually specific entries.
- `--style-family`: narrow the base style pool to a concrete family such as `film`, `fashion`, `product`, `photography`, `illustration`, `graphic`, `craft`, `digital`, `space`, or `material`.
- `--avoid-generic` / `--no-avoid-generic`: generic suppression is on by default; turn it off only when you need broader styles.

## Manual Library Lookup

Use `references/style_library.json` when you need to:

- inspect all 620 entries
- search by Chinese style name, English prompt token, category, subject suitability, or failure mode
- select styles manually for a themed series
- quote style metadata such as `容易翻车` or `补救提示`

For quick shell lookup:

```bash
python3 - <<'PY'
import json
p='references/style_library.json'
data=json.load(open(p, encoding='utf-8'))
for s in data['styles']:
    if 'giallo' in s.get('English prompt tokens','').lower() or '铅黄' in s.get('中文风格名',''):
        print(s['style_id'], s['中文风格名'], s['视觉DNA / 关键词'], s['English prompt tokens'])
PY
```

## Output Standards

Keep prompts specific, visual, and generation-ready. The final prompt should be Chinese. Use English prompt tokens only as metadata or when the user explicitly asks for an English version.

Prefer precise sub-style phrases such as `sun-faded folk horror poster photography`, `chrome Y2K fashion editorial`, `pastel ceramic toy photography`, or `overexposed tropical VHS travelogue`. Avoid relying on isolated generic words such as cinematic, surreal, retro, futuristic, cyberpunk, minimalism, or aesthetic.

Always include anti-drift constraints for exploration outputs:

```text
避免泛化的现代极简风，避免随机多余文字，避免混乱符号，
避免手部和面部畸形，避免丢失主体身份
```

For product prompts, add:

```text
造型可读，干净背景，无杂物，产品保持可识别
```

For character prompts, add:

```text
面部清晰，姿态有表现力，只保留1-2个关键配饰
```

For poster or cover prompts, add:

```text
少量伪文字，明确标题区域，不要长段可读文字
```
