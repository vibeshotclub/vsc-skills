---
name: shan-ze-school
description: Generate or refine prompts for 杉泽流派 / Shan Ze school-inspired new-oriental mythic ink-and-color fantasy images, especially when the user asks for 山海经、神怪、异兽、妖怪、国风神话、工笔水墨奇幻、东方幻想生物插画, or wants an existing prompt rewritten into this visual language. Use for original image-generation prompts, prompt rewrites, style transfer phrasing, and concise style analysis that translates any living-artist reference into broader art-historical visual grammar.
---

# 杉泽流派

## Core Rule

Translate requests for "Shan Ze / 杉泽 style" into an original art-historical visual grammar. Do not put a living artist's name in the final image prompt. Use precise descriptors: new-oriental mythic ink illustration, gongbi linework, xieyi ink atmosphere, shan-hai-jing bestiary, mineral pigments, silk-paper texture, smoke-cloud negative space.

If the user asks to generate an image, generate the image when an image tool is available. If direct image generation is not available, provide a ready-to-use prompt.

Default to prompt-writing rather than long art-history analysis. This skill is primarily for making prompts usable in image tools.

## Use This Skill When

- The user explicitly asks for 杉泽、Shan Ze、山海经异兽、东方神怪工笔奇幻一类的图像提示词。
- The user gives a rough creature idea and wants it rewritten into a mythic ink-and-color illustration prompt.
- The user provides an existing prompt and wants it "更像杉泽流派" but without naming a living artist directly.
- The user wants a short style breakdown in order to feed another image model or prompt workflow.

## Do Not Use This Skill When

- The main task is image criticism, art-history attribution, or academic classification without prompt generation.
- The subject is not mythic, spiritual, bestiary-like, or new-oriental fantasy in tone.
- The user wants contemporary graphic design, anime, photoreal concept art, or Western fantasy rendering.
- The user needs a broad Chinese illustration taxonomy rather than a narrow prompt language. In those cases, prefer `$中国插画`.

## Workflow

1. Identify the subject: mythic creature, deity, spirit, hybrid animal, scene, portrait, or artifact.
2. Choose a composition:
   - floating creature in blank paper space
   - horizontal handscroll pursuit scene
   - screen-painting tableau under flowering canopy
   - bestiary plate with seal and minimal inscription
3. Build the prompt with four layers:
   - **Structure**: gongbi baimiao contour, iron-wire line, hairline tendrils, anatomical hybridization.
   - **Color**: ink gray, cinnabar, rouge red, malachite green, azurite blue, ochre, pale shell white.
   - **Atmosphere**: ink-wash smoke, cloud-reserve negative space, mist diffusion, wet-on-dry paper bleeding.
   - **Finish**: silk or xuan-paper grain, translucent washes, no oil-paint impasto, no photoreal rendering.
4. Add negative constraints to prevent drift: no Western oil painting, no anime cel shading, no 3D render, no hard sci-fi armor, no glossy digital airbrush, no neon cyberpunk.
5. If the user supplied a draft prompt, preserve the core subject and only rewrite the style layer.
6. If the user asks for variants, change one axis at a time: composition, pigment emphasis, atmosphere, or creature anatomy.

## Output Modes

- **Direct image generation**: generate the image if an image tool is available.
- **Ready-to-use prompt**: default output for most requests.
- **Prompt rewrite**: keep the user's subject, simplify weak adjectives, and replace artist-name shorthand with material, brushwork, composition, and negative constraints.
- **Mini style note**: when asked "为什么这像杉泽流派", answer briefly and stay tied to promptable visual features.

## Prompt Template

Use this compact template unless the user asks for a different format:

```text
Original new-oriental mythic ink-and-color illustration of [SUBJECT], inspired by shan-hai-jing bestiary imagery and classical East Asian gongbi painting. [POSE/COMPOSITION]. Fine baimiao contour drawing, iron-wire linework, hairline ink tendrils, translucent mineral-pigment washes, ink-gray smoke-cloud negative space, cinnabar and rouge accents, malachite green and azurite blue details, ochre undertones, xuan-paper or silk texture, layered fenran and zhaoran dyeing, broken-ink mist, dry-brush flying-white edges, restrained decorative patterning, seal-script red chop mark, ethereal but anatomical hybrid creature design.

Negative prompt: photorealism, oil painting impasto, Western chiaroscuro, anime cel shading, 3D render, plastic gloss, cyberpunk neon, hard sci-fi armor, cute mascot proportions, flat vector art, excessive symmetry, cluttered background.
```

## Style Reference

For deeper vocabulary, read [references/style-grammar.md](references/style-grammar.md). Load it when the user asks for a very detailed prompt, variations, art direction, or style analysis.
