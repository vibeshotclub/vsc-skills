# Virtual Couple Travel Vlog Skill

Create a complete virtual couple travel vlog workflow from a short theme, such as:

- `一对中国情侣在巴塞罗那的旅行vlog`
- `A young Japanese couple in Paris travel vlog`
- `A Korean couple in northern Italy autumn trip`

The skill generates a consistent travel-memory asset package: 4x4 iPhone-style photo grid, four 2x2 memory sheets, male/female character references, video prompts, optional Topview video clips, a manual Chinese music prompt, and an assembled final vlog.

## What It Does

1. Creates a dedicated project folder under a user-selected output root.
2. Generates one 4x4 nostalgic iPhone travel photo grid for identity consistency.
3. Splits the 4x4 grid into four 2x2 memory sheets.
4. Generates clean male and female character reference cards.
5. Exports four video prompts, one for each 2x2 memory sheet.
6. Checks available video generation providers.
7. Uses Topview Omni Reference automatically when connected, or gives manual platform instructions for tools like Krea, Lovart, LibTV, Seedance API, or Topview UI.
8. Writes `audio/music_prompt_zh.txt` for manual soundtrack generation.
9. Assembles clips with FFmpeg, or uses Remotion when richer editing is needed.
10. Writes QA notes and a generation report.

## Output Structure

Each run creates:

```text
<Output Root>/<Project Title>/
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

Some files may be omitted if the user chooses manual video generation or if a provider is unavailable.

## Requirements

The automated local workflow expects:

- Python 3.10+ or Python Launcher
- Python Pillow module
- FFmpeg and FFprobe
- Node, npm, and npx for Remotion editing
- Remotion plugin/skill for richer editing paths
- Optional: Topview skill for automated image and video generation

Run the cross-platform dependency checker:

```bash
python "<skill-folder>/scripts/check-tools.py" --show-install-hints
```

If required dependencies are missing, ask the user before installing them.

## Quick Start

Ask Codex to use the skill and provide a theme:

```text
[$virtual-couple-travel-vlog](<path-to-skill>/SKILL.md) 一对中国情侣在巴塞罗那的旅行vlog
```

Also provide an output root, or let the skill ask where to create the project folder. Examples:

```text
Use ~/Movies/VlogOutputs as the output root.
Use D:/AI/VlogOutputs as the output root.
```

The skill will:

1. Create the project folder.
2. Write prompts and music prompt.
3. Generate the 4x4 grid.
4. Split it into four 2x2 sheets.
5. Generate character references automatically.
6. Check video provider availability.
7. Ask before submitting Topview video tasks or guide manual generation.

## Video Provider Modes

### Topview Automated Mode

If Topview is installed and connected, the skill can use Topview Omni Reference.

Default video settings:

- Model: Standard
- Aspect ratio: 9:16
- Duration: 15 seconds per clip
- Resolution: 720p unless changed
- Sound: off
- Total: four clips, about 60 seconds

Before video submission, the skill shows cost/wait information and asks whether to use normal queue or Quick Generate. If the local Topview scripts do not expose Quick Generate, the skill will explain the limitation and provide the board link if UI-side acceleration is needed.

### Manual Platform Mode

If no video API is connected, the skill still prepares a complete handoff package:

- `images/memory_sheet_01.png` through `memory_sheet_04.png`
- `images/character_male.png`
- `images/character_female.png`
- `prompts/video_clip_01.txt` through `video_clip_04.txt`

Manual use pattern:

1. Create four video jobs in your chosen platform.
2. For each job, upload the matching 2x2 sheet as the memory/contact-sheet reference.
3. Upload the male and female character cards as identity references.
4. Paste the matching video prompt.
5. Set 9:16, 15 seconds, and disable music/voiceover.
6. Download outputs as `clip_01.mp4` through `clip_04.mp4`.

## Character Card Strategy

The workflow uses stricter character-card prompts to reduce identity drift and background residue:

- One same character only
- Orthographic character turnaround
- Front, side, and back views
- Same scale and same ground line
- Pure seamless white background
- Unified wardrobe
- No text, logo, watermark, scenic background, ghosted reference images, pasted photo strips, or collage remnants

If full turnaround cards keep failing after three attempts, the workflow falls back to cleaner single-character identity references rather than spending more credits on flawed cards.

## Music

The skill does not use Gemini CLI or any automatic music generator by default.

It writes:

```text
audio/music_prompt_zh.txt
```

Paste that prompt into your preferred music generation tool. If you want Codex to embed the soundtrack later, place the generated audio file in the `audio/` folder and ask Codex to assemble it with the video.

## Assembly

Simple assembly uses FFmpeg.

Use Remotion when you want:

- transitions
- trims
- captions
- overlays
- music-aware timing
- repeatable React-based composition

The skill keeps FFmpeg as the default for simple clip joining and uses Remotion for richer editing.

## Safety Rules

- All generated project assets go under the output root selected by the user.
- The workflow does not delete files. If cleanup is needed, ask the user for explicit second confirmation.
- Do not install third-party skills or packages without first doing an audit and asking the user.
- Do not silently spend extra Quick Generate credits.

## Troubleshooting

- If character identity drifts, regenerate the 4x4 grid rather than creating four independent 2x2 grids.
- If character cards contain scene residue, use the cleanup prompt or fallback identity reference.
- If Topview is unavailable, continue with manual platform handoff.
- If FFmpeg fails, check clip codec/dimensions or use Remotion/manual editor fallback.
