---
name: rare-style-explorer
description: Generate and refine AIGC image prompts by combining rare, prompt-ready visual sub-style tags from a bundled 260-entry style library. Use when the user wants style exploration, image prompt variants, rare visual styles, non-generic aesthetics, style mixing, prompt matrices, or subject-to-style ideation for image generation.
---

# Rare Style Explorer

## Overview

Use this skill to turn a subject into reusable AIGC prompt variants using rare sub-style tags rather than broad labels such as minimalism, Bauhaus, or cyberpunk.

The bundled library lives at `references/style_library.json`. Load it only when the user asks for specific style lookup, filtering, auditing, or manual curation. For normal prompt generation, run `scripts/explore_styles.py`.

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
python3 scripts/explore_styles.py "SUBJECT" --mode minimal --count 8
```

3. Review the generated style IDs and remove combinations that conflict with the subject, platform, or brand.

4. Output in this order unless the user requests another format:
   1. analysis dimensions
   2. selected style logic
   3. prompt variants
   4. variable slots
   5. negative constraints
   6. reusable template

## Combination Rules

Build each prompt from:

```text
{subject}, {base_style}, {surface_or_light}, {format_or_space},
clear silhouette, strong visual identity, high detail,
avoid generic modern minimalism, avoid random extra text, avoid messy symbols,
avoid losing subject identity
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
```

Useful options:

- `--mode`: `minimal`, `product`, `character`, `poster`, `scene`, `material-series`.
- `--count`: number of prompt variants.
- `--seed`: reproducible random seed.
- `--style-id`: force a base style by library ID, then vary supporting layers.
- `--format`: `markdown` or `json`.

## Manual Library Lookup

Use `references/style_library.json` when you need to:

- inspect all 260 entries
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
        print(s['style_id'], s['中文风格名'], s['English prompt tokens'])
PY
```

## Output Standards

Keep prompts specific, visual, and generation-ready. Include both Chinese explanation and English prompt text when useful.

Always include anti-drift constraints for exploration outputs:

```text
avoid generic modern minimalism, avoid random extra text, avoid messy symbols,
avoid distorted hands/faces, avoid losing subject identity
```

For product prompts, add:

```text
readable shape, clean background, no clutter, product remains recognizable
```

For character prompts, add:

```text
clear face, expressive pose, 1-2 key accessories only
```

For poster or cover prompts, add:

```text
limited pseudo-typography, strong title area, no long readable text
```
