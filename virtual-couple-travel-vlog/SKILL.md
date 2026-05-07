---
name: virtual-couple-travel-vlog
description: Create virtual couple travel vlog workflows and assets from a user-provided theme, destination, couple profile, output folder, or reference images. Use when Codex needs to generate nostalgic iPhone travel photo grids, split 4x4 grids into four 2x2 memory sheets, create male/female character reference cards, generate Topview Omni Reference video clips, write manual Chinese music prompts, assemble final vlog videos, and save all assets in a user-selected dedicated project folder.
---

# Virtual Couple Travel Vlog

Build a repeatable "virtual couple travel vlog" asset pipeline from a short theme such as "a young Japanese couple in Paris" or "a Chinese couple in northern Normandy."

## Operating Rules

- Address the user as the Chinese honorific for boss in Chinese replies.
- The skill files may be written in ASCII for portability. This does not restrict the user's input language; accept Chinese, English, French, Spanish, and mixed-language project briefs normally.
- Save every generated asset under a user-selected output root as `<Output Root>/<Project Title>/`.
- If the user gives an output folder, use it. If the user has a local default output root in their environment or project instructions, offer it as the default. Otherwise ask the user to choose an output root before creating project assets. Do not hard-code a drive letter or OS-specific output path.
- Never delete files. If cleanup is needed, ask the user for explicit second confirmation first.
- Try each blocked automation step up to 3 times. If it still fails, stop that step, explain the blocker plainly, and provide the best manual handoff asset or prompt.
- Keep the story coherent across all four 2x2 grids: same couple, same trip, same wardrobe logic, progressive travel moments.
- Prefer generating one 4x4 contact sheet in a single image task, then splitting it into four 2x2 sheets. Do not generate four independent 2x2 text-to-image sheets unless there is already a strong locked character reference image.
- Do not install third-party skills or packages unless the user approves after a poison/backdoor audit and a system resource check.

## Task List

Read [references/task_list.md](references/task_list.md) before running a new project. Use it as the working checklist and subagent delegation map.

Typical task ownership:

1. Intake and project folder setup.
2. Prompt planning for a 4-part travel memory sequence.
3. Image generation: one 4x4 contact sheet is the default primary route.
4. Grid splitting: split the 4x4 locally into four 2x2 sheets with the Python/Pillow splitter.
5. Character cards: male and female seven-panel technical turnaround sheets, white background, studio lighting, no text/logos/watermarks/UI. Proceed automatically after the 4x4 split unless identity drift is severe.
6. Video provider check: after assets and video prompts are ready, detect connected video generation providers or guide manual platform use.
7. Pre-submit Topview queue decision: when using Topview automation, show video settings, cost estimate, available queue/runtime estimate, and ask whether to use normal queue or Quick Generate before submitting video clips.
8. Video generation: generate or manually hand off four silent 15-second clips, defaulting to Standard 720p at 9:16 unless the user changes quality settings.
9. Manual music prompt: write `audio/music_prompt_zh.txt` and remind the user to generate music with their preferred tool.
10. Assembly decision: after four clips exist, ask whether to use FFmpeg for simple joining or Remotion/HyperFrames for richer editing such as transitions, trims, captions, light leaks, rhythm-aware edits, and reusable compositions.
11. Assembly: concatenate clips with FFmpeg, Remotion, or HyperFrames, optionally add a user-provided music file, export final MP4.
12. QA: check identity consistency, no grid layout in video, no text/watermark, all files in output folder.

## Tool Routing

### First-run dependency check

When a user installs or runs this skill on a new machine, run [scripts/check-tools.py](scripts/check-tools.py) before the workflow starts.

- Required for the automated local workflow: Python, Pillow, FFmpeg, FFprobe, and Remotion readiness checks for richer editing.
- Optional: Topview skill, HyperFrames plugin/skill for editing only, Node, npm, or other provider-specific CLIs.
- If required dependencies are missing, show the missing items and ask the user whether to install them before taking installation action.
- If optional video generation providers are missing, continue to asset and prompt preparation, then use the manual video platform handoff.

### Image generation

Use Codex Image Gen with `gpt-image-2` as the preferred image route for identity-critical assets.

- Character cards must default to Codex Image Gen / `gpt-image-2`, using the `imagegen` skill and the built-in image generation/editing path.
- Do not generate character cards with Topview image models by default. Topview's default image route can use lower-fidelity models that may preserve source-image fragments or mix identities.
- Use Topview `ai_image.py` only for memory grids or other image tasks when the user explicitly selects Topview or accepts that provider for the current image step.
- Default aspect ratio: `1:1` for grids and character cards.
- Save final selected downloads or generated image assets to the project output folder. Do not leave project assets only under the default Codex generated-images directory.

Identity rule:

- Do not create the four 2x2 memory sheets as four separate text-to-image tasks by default. Separate generations drift identities even when the prompt says "same couple."
- Generate a single 4x4 grid first. This keeps all 16 snapshots inside one model context and is much more reliable for face and wardrobe continuity.
- After the 4x4 image is generated, inspect it before splitting. If the man or woman clearly changes identity across cells, rerun the 4x4 prompt instead of creating character cards or videos.
- Only use direct 2x2 generation when the workflow already has a strong couple reference image or character cards, and pass those references into an image-edit workflow.

### Local 2x2 splitting

Use [scripts/split-grid.py](scripts/split-grid.py) to split the approved 4x4 image into four 2x2 memory sheets. This is the only default crop route. Do not use design tools for this step, and do not fall back to independent 2x2 text-to-image generation unless the user accepts the identity drift risk or a locked reference image exists.

If the Python splitter fails, try to fix the local image or Pillow issue first. After 3 failed attempts, provide manual crop instructions rather than generating four independent 2x2 sheets by default.

### Character card generation

Create character cards automatically after the 4x4 grid is generated and split into four 2x2 sheets. Do not ask the user to confirm before generating the cards unless the 4x4 has severe identity drift that would make the workflow unusable.

- Generate character cards with Codex Image Gen / `gpt-image-2`, not Topview, unless the user explicitly asks for Topview for this step after being warned about possible lower model quality.
- Treat Topview character-card generation as a downgrade/fallback route, not the default route.
- When the source references are local files, inspect or load the selected 2x2 sheets into the conversation context before using Codex Image Gen so the model can use them as visual references.
- Use the clean studio character card templates in [references/prompts.md](references/prompts.md).
- Generate one card for the man and one card for the woman.
- Keep one unified wardrobe per card. Do not allow outfit changes inside one card.
- Use the same fixed seven-panel layout for both male and female cards: top row has four full-body standing views in this order: front, left profile facing screen left, right profile facing screen right, back; bottom row has three close-up portraits in this order: front small smile, left profile serious, right profile serious.
- Keep a pure white studio background with clean panel separation, consistent scale, consistent head height, same foot baseline for full-body views, and consistent facial scale for portraits.
- Do not include travel photo fragments, scenic overlays, ghosted reference images, inset memories, grids, labels, readable text, logos, watermarks, measurement marks, screenshots, or UI.
- Reject and rerun any character card that contains background remnants from the reference photos or that mixes multiple identities.
- Use the approved clean male summer card format as the visual target: technical model turnaround sheet, 1:1 frame, top full-body row, bottom portrait row, no labels, no scenery.
- Use turnaround-sheet language: exact same character, four full-body views plus three portraits, same scale, same ground line, orthographic camera, flat even studio lighting, no perspective scene, and no storytelling background.
- If full turnaround cards keep importing scene fragments after 3 attempts, switch to fallback identity references: one clean full-body white-background image plus clean head-angle crops/portraits. Use the fallback for video instead of spending more attempts on flawed character sheets.

### Video provider selection

After the four 2x2 sheets, character cards, and video prompts are ready, run [scripts/check-video-providers.py](scripts/check-video-providers.py).

- If Topview is connected and the user wants Topview automation, use the Topview skill and its scripts.
- If another video generation API is connected, adapt the same exported assets and prompts to that provider's supported reference-image workflow.
- If no video generation API is connected, ask which platform the user wants to use, such as Lovart, Krea, LibTV, Seedance API, Topview UI, or another tool. Then provide manual instructions using the exported 2x2 sheets, character cards, and video prompts.
- Never block the workflow solely because Topview is unavailable.

### Topview video generation

For Topview automation, use `video_gen.py run --type omni` with:

- `--model "Standard"` unless the user requests speed or cost savings.
- `--duration 15`; each clip should be exactly 15 seconds when supported.
- `--aspect-ratio "9:16"` fixed for vlog clips unless the user explicitly requests another format.
- Use `--resolution 720` for Topview Standard Omni clips when 2K is not directly available. If Topview UI/API exposes Auto Upscale to 2K, enable it when available; if the local script cannot set it, record that the user can enable 2K upscale in the Topview UI.
- `--sound off`.
- `--input-images` containing the current 2x2 sheet as `Image1`, male character card as `Image2`, and female character card as `Image3`.
- Prompt references as `<<<Image1>>>`, `<<<Image2>>>`, `<<<Image3>>>`.

Before the first paid Topview generation in a session, follow the Topview skill's cost/auth confirmation rules.

Before submitting video tasks, pause for an explicit queue decision:

- Show the exact settings: Omni Reference, Standard, 9:16, 15 seconds, 720p, sound off, four clips unless changed by the user.
- Show the credit estimate from Topview when available. If only observed cost is available, label it as observed, not guaranteed.
- Give the best available wait estimate. If no pre-submit ETA is exposed by the local Topview script, say so plainly and use recent observed runtime or an existing task detail as a rough reference only.
- Ask the user whether to use normal queue or Quick Generate before submitting the four video clips.
- Do not continue to video submission until the user answers.

If Topview reports a heavy queue, long ETA, or a "Quickly Generate" option that costs 15 credits, pause and ask the user whether to spend the extra 15 credits for quick generation. The user has said they are a Business member with enough credits, but still ask before each 15-credit acceleration unless they explicitly grant auto-approval for the current batch. If the local Topview script does not expose a quick-generate API, explain that acceleration must be confirmed or clicked through Topview's official UI/board, then continue polling or provide the board link.

The finished vlog target is about 1 minute: four 15-second clips assembled in order, with optional music matched to the final 60-second duration.

### HyperFrames editing only

HyperFrames is not a default provider for creating the four photoreal 15-second image-to-video clips. Do not offer HyperFrames as a clip generation route before Topview, other APIs, or manual platform selection. Use a real video generation provider or manual video platform for the four source clips.

Use HyperFrames only after the four video clips already exist and the user wants richer editing instead of simple FFmpeg joining.

HyperFrames is appropriate for:

- HTML/GSAP-based video composition.
- Transitions, trims, crops, subtitles, light leaks, overlays, and rhythm-aware edits.
- Reusable composition structure for later projects.

When authoring HyperFrames, follow the HyperFrames and HyperFrames CLI skills. Use a 9:16 composition, about 60 seconds total, four 15-second scenes, and read the relevant HyperFrames transition/caption/audio-reactive references before authoring. Run `npx hyperframes lint`, `npx hyperframes inspect`, and `npx hyperframes render` when a HyperFrames project is authored.

If HyperFrames renders blurry or over-compressed output, stop using it for clip synthesis and keep it only for edits over already-generated clips. Prefer provider-native video generation for the source clips, then use HyperFrames only for final layout/editing if it preserves acceptable quality.

### Music prompt handoff

Do not use Gemini CLI or any automatic music generation tool by default. Always write the final Chinese music prompt to `audio/music_prompt_zh.txt`, then remind the user to generate the soundtrack manually with their preferred tool because music tools and user habits vary.

If the user later provides a generated music file, save or reference it under `audio/` and use it for assembly only after the user asks to embed music.

### Video assembly

After four clips are generated, ask the user which assembly route they want:

- FFmpeg for a simple join and optional music mux.
- Remotion for React-based transitions, trims, captions, overlays, music-aware timing, or reusable React composition.
- HyperFrames for HTML/GSAP-based transitions, trims, captions, light leaks, rhythm-aware edits, overlays, and reusable HyperFrames composition.

Use [scripts/assemble-vlog.py](scripts/assemble-vlog.py) when FFmpeg is enough. When Remotion is requested or useful, follow the Remotion plugin best practices and scaffold a small Remotion project instead of hand-writing ad hoc video code. When HyperFrames is requested or useful, follow the HyperFrames and HyperFrames CLI skills, scaffold or author a HyperFrames project, lint/inspect it, then render. If none of FFmpeg, Remotion, or HyperFrames is usable after 3 attempts, provide the ordered clip list and any user-provided music file for manual assembly in Clipchamp, CapCut, Premiere, or another editor.

## Required References

- Use [references/prompts.md](references/prompts.md) for reusable prompt blocks.
- Use [references/tooling.md](references/tooling.md) for command patterns, dependency checks, and fallback decisions.

## Output Contract

Each project folder should contain:

- `brief.md` - theme, couple profile, location, style notes.
- `prompts/` - final prompts used for grids, character cards, videos, and music.
- `images/` - 4x4 source, 2x2 sheets, and character cards.
- `videos/` - four generated clips and the final assembled video if available.
- `audio/` - `music_prompt_zh.txt` for manual soundtrack generation, plus any user-provided generated music.
- `qa.md` - final review notes and any manual steps still required.
