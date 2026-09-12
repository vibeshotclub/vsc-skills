# Tooling and Fallbacks

## Dependency Check

Use `scripts/check-tools.py` from this skill folder before running a full workflow on a new machine. It checks for common local tools without changing files and works on macOS, Windows, and Linux.

Expected tools:

- Required: Python or Python Launcher.
- Required: Python Pillow module for 4x4 to 2x2 local splitting.
- Required: FFmpeg and FFprobe for final assembly.
- Required for Remotion editing path: Node, npm, npx, and the Remotion plugin/skill.
- Optional: Topview skill when the user wants automated Topview generation.
- Optional: HyperFrames plugin/skill when the user wants richer HTML/GSAP editing after the four source clips already exist.
- Optional: Node/npm only when a chosen provider needs a local CLI.
- No music generation CLI is required. The workflow writes a manual Chinese music prompt instead.

Run:

```bash
python "<THIS_SKILL>/scripts/check-tools.py" --show-install-hints
```

If required dependencies are missing, ask the user before installing. Useful install hints:

```bash
python -m pip install Pillow
```

Install FFmpeg with the user's OS package manager, for example Homebrew on macOS, winget/choco on Windows, or apt/dnf/pacman on Linux.

Do not install optional provider CLIs unless the user selects that provider and approves the installation.

## Third-Party Video Skill Search Notes

Search findings as of 2026-05-02:

- `affaan-m/everything-claude-code/video-editing` appears popular, but it is broad and includes multiple external services. Treat as high audit scope before installing.
- `benchflow-ai/skillsbench/ffmpeg-video-editing` is narrower and Apache-2.0, mainly FFmpeg command guidance. Prefer this class of skill if the user later wants a third-party video editing skill.
- HeyGen video skills are useful for avatar/video production but require HeyGen account/API/MCP and are not needed for this workflow.

Default decision: do not install any third-party video editing skill. Use local FFmpeg command patterns directly.

If installation is requested, audit first:

- Look for outbound network calls beyond expected package download.
- Look for file writes outside the skill directory.
- Look for shell execution, startup hooks, profile edits, credential reads, or auto-run behavior.
- Check dependency size, browser/CLI requirements, CPU/RAM/disk needs, and rate limits.
- Ask the user before installing.

## Topview Command Pattern

Use the Topview skill's scripts, not raw HTTP calls.

For image generation:

```bash
python "<TOPVIEW_SKILL>/scripts/ai_image.py" run --type text2image --model "Nano Banana 2" --prompt "<PROMPT>" --aspect-ratio "1:1" --resolution "2K" --output-dir "<PROJECT>/images"
```

Do not use Topview image models for character cards by default. Character cards are identity-critical and should use Codex Image Gen / `gpt-image-2` unless the user explicitly accepts a lower-quality fallback.

For Omni Reference video:

```bash
python "<THIS_SKILL>/scripts/run-topview-omni.py" --prompt-file "<PROJECT>/prompts/video_clip_01.txt" --sheet "<PROJECT>/images/memory_sheet_01.png" --male-card "<PROJECT>/images/character_male.png" --female-card "<PROJECT>/images/character_female.png" --aspect-ratio "9:16" --resolution 720 --duration 15 --count 1 --sound off --board-id "<TOPVIEW_BOARD_ID>" --output-dir "<PROJECT>/videos"
```

Use the wrapper script because shell quoting differs across macOS, Windows, and Linux. The wrapper passes reference-image JSON safely to `video_gen.py`.

Before video submission, estimate cost when possible:

```bash
python "<TOPVIEW_SKILL>/scripts/video_gen.py" estimate-cost --model "Standard" --resolution 720 --duration 15 --sound off --count 4
```

If the estimate command fails or differs from observed charging, tell the user the estimate is uncertain. In the Shanghai Standard Omni trial, four 15-second 720p clips were charged as 18 credits per clip, 72 credits total. Treat that as observed history, not a guaranteed price.

For splitting a 4x4 grid into four 2x2 sheets, prefer the Python/Pillow splitter:

```bash
python "<THIS_SKILL>/scripts/split-grid.py" --input-image "<PROJECT>/images/memory_grid_4x4.png" --output-dir "<PROJECT>/images" --prefix "memory_sheet"
```

Do not use an OS-specific crop script by default. If Pillow cannot decode the image, regenerate or convert the image with a cross-platform image tool, then rerun the Python splitter.

Video quality rule:

- Topview clips should be 15 seconds each.
- Aspect ratio is fixed to 9:16 for this workflow unless the user changes it.
- Topview Standard Omni uses 720p when 2K is not directly exposed in the script.
- If Topview UI/API exposes Auto Upscale to 2K, enable it when available. If the local script cannot set Auto Upscale, record the limitation and provide the board/task link for optional UI-side 2K upscale.
- Assemble exactly four 15-second clips for an approximately 1-minute final vlog.

## Topview Queue and Quick Generate

Topview may report a heavy queue or ETA while a video task is waiting. The web UI can show a "Quickly Generate" action that costs 15 credits.

Pre-submit gate:

- After the four 2x2 sheets and both character cards are accepted, but before calling video generation, show the user:
  - settings: Omni Reference, Standard, 9:16, 15s, 720p, sound off, 4 clips;
  - credit estimate or observed historical cost;
  - best available queue/runtime estimate;
  - a choice between normal queue and Quick Generate.
- Wait for the user's answer before submitting any videos.

ETA sources:

- Current local Topview scripts do not expose a reliable pre-submit queue ETA.
- `board.py task-detail` can show `estimateInfo.queueCount` and `estimateInfo.estimatedWaitSeconds` for an existing task only.
- If the user shares a Topview UI ETA screenshot, use that value.
- If no ETA is available, state the limitation and give recent observed runtime as a rough reference only. In the Shanghai Standard Omni trial, completed clips took about 451-587 seconds each while polling in parallel.

Policy:

- Do not silently spend the extra 15 credits.
- Ask the user before submitting the video batch, and ask again after submission if Topview later reports a heavy queue or ETA at or above about 15 minutes.
- Because the user has a Business membership and enough credits, recommend Quick Generate when waiting would block the workflow, but still get confirmation unless batch auto-approval was granted.
- If the user approves only one clip, accelerate only that clip.
- If the user approves the batch, accelerate all currently queued clips in the current four-clip vlog batch if Topview supports it.
- No direct quick-generate switch was found in the current local Topview scripts. If this remains true, use the board/task detail link for the official Topview UI handoff. If Topview requires a queued task before showing the Quick Generate button, ask whether to create the queued task for UI-side acceleration before doing so.

Decision text to use:

```text
Before I submit the four Topview video clips, here are the settings: Omni Reference Standard, 9:16, 15s each, 720p, sound off. Estimated/observed cost is [COST]. Queue ETA is [ETA_OR_LIMITATION]. Do you want normal queue, or Quick Generate? Quick Generate costs 15 extra credits per use.
```

## Video Provider Check

After the 2x2 sheets, character cards, and video prompts are prepared, check whether a video generation provider is connected:

```bash
python "<THIS_SKILL>/scripts/check-video-providers.py"
```

The checker looks for source video generation providers:

- Topview skill in common local skill folders.
- Common API environment variables for Seedance, Krea, Lovart, and LibTV.

Do not treat HyperFrames as a source video generation provider. If a provider is detected, ask the user whether to use it for automation. If no provider is detected, ask which platform they want to use, then provide manual instructions.

Manual video generation package:

- `images/memory_sheet_01.png` through `images/memory_sheet_04.png`
- `images/character_male.png`
- `images/character_female.png`
- `prompts/video_clip_01.txt` through `prompts/video_clip_04.txt`

Manual instructions:

1. Create four video jobs, one per memory sheet.
2. For clip 1, upload `memory_sheet_01.png` as the memory/contact-sheet reference, plus both character cards as identity references. Paste `video_clip_01.txt`.
3. Repeat for clips 2-4 with matching sheet and prompt.
4. Set aspect ratio to 9:16, duration to 15 seconds, resolution to the user's acceptable setting, and disable music/voiceover.
5. Download outputs as `videos/clip_01.mp4` through `videos/clip_04.mp4`.

If the user names a platform, adapt the wording to that platform's UI. Keep the core mapping the same: 2x2 sheet = memory reference, male/female cards = identity references, matching prompt = video direction.

## FFmpeg Assembly

Use `scripts/assemble-vlog.py` for simple clip joining. It first tries same-codec concatenation; if clips differ in codec/resolution/framerate, it re-encodes to a web-safe MP4.

```bash
python "<THIS_SKILL>/scripts/assemble-vlog.py" --clips "<PROJECT>/videos/clip_01.mp4" "<PROJECT>/videos/clip_02.mp4" "<PROJECT>/videos/clip_03.mp4" "<PROJECT>/videos/clip_04.mp4" --output "<PROJECT>/videos/final_vlog.mp4"
```

## Remotion Assembly

Use the Remotion plugin for richer editing beyond direct FFmpeg concatenation. Read `remotion-best-practices` before creating or editing Remotion code.

Use Remotion when:

- the user wants transitions, trims, captions, overlays, animated timing, audio-reactive edits, or a reusable video composition;
- the clips need a designed edit rather than a straight join;
- future versions of the workflow should export the same 9:16 structure repeatedly.

Dependency expectations:

- Node.js, npm, and npx are available.
- The Remotion plugin/skill is installed.
- For a new empty project, scaffold with `npx create-video@latest --yes --blank --no-tailwind <project-name>`.
- Preview with `npx remotion studio` when interactive review is needed.
- Render final MP4 with the Remotion CLI after defining a 720x1280, 24fps, about-60-second composition.

Keep FFmpeg as the fallback for simple joining and audio muxing. Do not force Remotion when a direct concat is enough.

## HyperFrames Assembly

Use the HyperFrames plugin only after four source clips already exist and the user selects HyperFrames for richer editing. Do not use HyperFrames as the source provider for the four photoreal 15-second image-to-video clips; this route can compress stills heavily and produce lower-quality faux motion.

Use HyperFrames after four clips exist when the user wants:

- transitions;
- crops or trims;
- captions/subtitles;
- light leaks and animated overlays;
- rhythm-aware editing;
- reusable HTML/GSAP composition.

Post-generation assembly decision text:

```text
The four clips are ready. Do you want a simple FFmpeg join, or a richer edit with Remotion or HyperFrames for transitions, trims/crops, captions, light leaks, rhythm-aware timing, and reusable composition?
```

When authoring HyperFrames:

- Read the `hyperframes` and `hyperframes-cli` skills.
- Use a 9:16 composition, usually 720x1280 or 1080x1920.
- Keep the final duration around 60 seconds for four 15-second clips.
- Use `npx hyperframes lint`, `npx hyperframes inspect`, and `npx hyperframes render`.
- Keep FFmpeg as the fallback for simple joining when the user does not need a designed edit.

### HyperFrames Chrome Runtime Fix

HyperFrames may report that Chrome is available while rendering still fails because its expected `chrome-headless-shell.exe` cache path is missing. On Windows, this was fixed without deleting anything by copying the locally installed Chrome runtime into HyperFrames' cache path.

Use this as a last-mile runtime repair when `npx hyperframes inspect` or `npx hyperframes render` fails with a missing Chrome/headless-shell browser path:

1. Check the HyperFrames browser cache path in the error output, usually under:

```text
%USERPROFILE%\.cache\hyperframes\chrome\chrome-headless-shell\<platform-and-version>\
```

2. Check the local Chrome installation, commonly:

```text
C:\Program Files\Google\Chrome\Application
```

3. Copy Chrome's application files into the expected HyperFrames cache directory. If HyperFrames specifically expects `chrome-headless-shell.exe`, copy `chrome.exe` to that filename inside the cache directory.

4. Rerun:

```bash
npx hyperframes inspect . --samples 8 --json
npx hyperframes render . --output "<PROJECT>/videos/final_vlog.mp4"
```

Notes:

- This is a compatibility workaround, not a content-generation feature.
- Do not delete existing browser caches unless the user gives explicit second confirmation.
- Prefer a normal HyperFrames browser install/cache repair if the CLI exposes a working command on the current machine.

## Manual Music Prompt

Do not use Gemini CLI by default. Music generation tools, subscriptions, and user habits vary, so the workflow should only create a Chinese soundtrack prompt and hand it to the user.

Write the final prompt to:

```text
<PROJECT>/audio/music_prompt_zh.txt
```

Then remind the user:

```text
The music prompt is saved at audio/music_prompt_zh.txt. Please paste it into your preferred music generation tool, then place the generated audio file in the audio folder if you want me to embed it into the final video.
```
