# Task List and Subagent Map

Use this checklist for every virtual couple travel vlog project.

## Task -1 - Install-Time Dependency Check

Owner: main agent.

Timing:

- Run when the skill is installed on a new machine or before the user's first workflow run.

Actions:

- Run `python scripts/check-tools.py --show-install-hints`.
- Required dependencies for automated local workflow:
  - Python 3.10+ or Python Launcher.
  - Python Pillow module for local 4x4 to 2x2 splitting.
  - FFmpeg and FFprobe for final assembly.
  - Node/npm/npx and Remotion plugin readiness for Remotion-based editing.
- Optional dependencies:
  - Topview skill for automated Topview image/video generation.
  - HyperFrames plugin/skill for richer editing after the four source clips already exist.
  - Node/npm or platform-specific CLIs only when the selected provider needs them.
- If required dependencies are missing, ask the user whether to install them before running install commands.
- If optional video providers are missing, do not stop the workflow; prepare assets and prompts for manual platform use.

Acceptance:

- The user knows what is missing.
- No dependency is installed without explicit user approval.
- The workflow can proceed in manual-handoff mode when video automation is unavailable.

## Task 0 - Intake and Folder Setup

Owner: main agent.

Inputs:

- Theme and destination, e.g. "young Japanese couple in Paris."
- Couple ethnicity/nationality, age range, wardrobe direction, season, and mood if provided.
- Preferred output root and project title. If the output root is missing, ask the user to choose one before creating assets. If the title is missing, create a concise English folder title.

Actions:

- Create `<Output Root>/<Project Title>/`.
- Create subfolders: `prompts`, `images`, `videos`, `audio`.
- Write `brief.md`.

Fallback:

- If the selected output root is unavailable, ask the user for an alternate folder.

## Task 1 - Story and Prompt Planning

Suggested subagent: prompt director.

Actions:

- Split the trip into four memory chapters.
- Keep the same couple and visual continuity.
- Avoid luxury ad, fashion editorial, cinematic polish, or perfect AI faces.
- Produce one 4x4 prompt that contains all four chapters in a single contact sheet.

Acceptance:

- The 4x4 sheet reads as one trip, not unrelated shoots.
- Each 2x2 quadrant has distinct locations/actions and a clear emotional beat after splitting.

## Task 2 - Memory Grid Generation

Suggested subagent: image generation operator.

Primary route:

- Generate one 4x4 iPhone contact sheet.
- Save it as `images/memory_grid_4x4.png`.
- Inspect the 4x4 before splitting. The same husband and wife must appear throughout the grid with locked facial identity and coherent wardrobe continuity.
- If the 4x4 contains different couples or major identity drift, reject it and rerun the 4x4 prompt. Do not create character cards from an inconsistent 4x4.
- If the 4x4 is acceptable, proceed directly to splitting and character cards without asking the user to confirm.

Fallback route:

- If crop automation is blocked, fix crop automation first or provide the 4x4 for manual splitting. Only generate four 2x2 sheets directly when a locked reference image or character cards already exist:
  - `images/memory_sheet_01.png`
  - `images/memory_sheet_02.png`
  - `images/memory_sheet_03.png`
  - `images/memory_sheet_04.png`

Attempt limit:

- 3 attempts total for the chosen image generation route before asking the user whether to adjust style, model, or proceed manually.

## Task 3 - Local 2x2 Splitting

Suggested subagent: asset operator.

Preferred route:

1. Use `scripts/split-grid.py` to split the approved 4x4 source into four 2x2 memory sheets.
2. If local splitting fails, fix the image/Pillow issue and retry up to 3 times.
3. If local splitting still fails, write manual crop instructions and ask the user before switching to direct four 2x2 generation.

Acceptance:

- Four 2x2 images preserve the original grid's cell order.
- No text or extra design elements are introduced.
- All four 2x2 sheets come from the same approved 4x4 source unless the user explicitly accepts the alternate route.

## Task 4 - Character Cards

Suggested subagent: character consistency operator.

Inputs:

- The approved 4x4 source image and the four derived 2x2 sheets.

Outputs:

- `images/character_male.png`
- `images/character_female.png`

Rules:

- White background.
- Studio photography lighting.
- No text, labels, logos, watermarks, measurement lines, or UI.
- Use the fixed seven-panel technical reference format for both male and female cards.
- Top row: four full-body standing views in this exact order: front, left profile facing screen left, right profile facing screen right, back.
- Bottom row: three close-up head portraits in this exact order: front with a small natural smile, left profile serious, right profile serious.
- Use orthographic turnaround language: same character, same scale, same ground line, same proportions, consistent head height, consistent foot baseline, consistent facial scale, no perspective scene.
- Preserve the couple's age, face structure, hair, clothing style, and ordinary travel vibe.
- Keep one unified wardrobe per character card. Do not allow multiple outfits inside one card unless the user explicitly asks for a variant sheet.
- Reject any card with reference photo remnants, scenic overlays, ghosted background memories, inset travel photos, grid/collage artifacts, or other people.
- Use the clean `character_male_summer` style as the visual target: 1:1 sheet, top full-body row, bottom portrait row, pure white background, no labels, no scenery, clean panel separation.
- For the female card, use the same fixed seven-panel format as the male card. Extract the woman's identity only, enforce a single wardrobe lock, use pure white studio background, and explicitly negate original reference image fragments.
- If the character card introduces a different person or mixes multiple identities, discard it and regenerate from the approved 4x4 source; do not use it for video.
- Do not ask the user before generating the first character cards. Run them directly after splitting.
- If one card has a stable identity but visible scenery remnants, run the cleanup prompt once or twice.
- Stop after 3 failed attempts for a character. If a clean turnaround is still not possible, generate the fallback single-character identity reference and use the cleanest available reference for video.

## Task 5 - Video Provider Check and Handoff

Owner: main agent.

Timing:

- Run this after the 2x2 sheets, both character cards, and four video prompts are ready.

Actions:

- Run `python scripts/check-video-providers.py`.
- If a connected provider is found, ask whether the user wants to use that provider for automation.
- If no provider is found, ask which platform the user wants to use and provide manual instructions for that platform.
- Do not offer HyperFrames as a source-clip generation provider. HyperFrames is reserved for editing after the four source clips already exist.
- Always export the handoff package:
  - `images/memory_sheet_01.png` through `images/memory_sheet_04.png`
  - `images/character_male.png`
  - `images/character_female.png`
  - `prompts/video_clip_01.txt` through `prompts/video_clip_04.txt`

Manual platform guidance:

- For each clip, upload the matching 2x2 sheet as the memory/contact-sheet reference.
- Upload both character cards as the identity references.
- Paste the matching `video_clip_XX.txt` prompt.
- Set aspect ratio to 9:16, duration to 15 seconds, resolution to the user's acceptable setting, and disable music/voiceover when the platform exposes those controls.
- Ask the user for the platform name if platform-specific button names or settings are needed.

Acceptance:

- The workflow does not assume Topview is the only provider.
- A user without any connected API can still generate the clips manually from the exported assets.

## Task 6 - Topview Queue Decision

Owner: main agent.

Timing:

- Run this only when Topview automation is selected, after the video provider check and before submitting any Topview video generation tasks.

Actions:

- Show the planned settings: Topview Omni Reference, Standard, aspect ratio 9:16, duration 15 seconds per clip, resolution 720p unless changed, sound off, four clips total.
- Show the best available credit estimate. Prefer the Topview estimate command. If only prior observed cost is available, label it as observed and not guaranteed.
- Give the best available wait estimate:
  - If Topview exposes a pre-submit queue ETA, report it.
  - If only an existing task exposes ETA, report the existing task's `queueCount` and `estimatedWaitSeconds`.
  - If no pre-submit ETA is exposed by the local script, say that plainly and use recent observed runtime only as a rough reference.
- Ask the user to choose normal queue or Quick Generate before submitting videos.
- Do not submit video tasks until the user replies.

Quick Generate policy:

- Quick Generate costs 15 extra credits per use based on the Topview UI.
- If the user approves the full batch, apply the decision to the four clips in the current batch when the API/UI supports it.
- If the local Topview script cannot trigger Quick Generate directly, explain the limitation. If Topview requires a queued task before the Quick Generate button appears, ask whether to create the queued task for UI-side acceleration, then provide the board/task link.
- Never silently spend the extra credits.

## Task 7 - Four Video Clips

Suggested subagent: video operator.

For each memory sheet:

- Input `Image1`: current 2x2 sheet.
- Input `Image2`: male character card.
- Input `Image3`: female character card.
- Generate one silent 15-second clip through the selected automated provider, or provide a manual handoff for the selected platform.
- Default to Standard 720p at 9:16 for each clip unless the user changes quality settings. If the user requests 2K and Topview/model constraints do not expose it, report the limitation and use the closest supported setting after confirmation.
- If Topview is used and reports a heavy queue or ETA of about 15 minutes or more after submission, ask whether to use Quick Generate for the clip or the full batch. Note that Quick Generate costs 15 extra credits per use, based on the Topview UI.
- If the user grants batch approval, apply the same quick-generation decision to the remaining queued clips in that batch. Otherwise ask before each extra 15-credit acceleration.
- If the Topview script cannot trigger Quick Generate directly, provide the board/task link and tell the user the official UI action needed, then continue normal polling unless the user confirms acceleration.

Outputs:

- `videos/clip_01.mp4`
- `videos/clip_02.mp4`
- `videos/clip_03.mp4`
- `videos/clip_04.mp4`

Acceptance:

- Four clips total about 60 seconds before music.
- The original grid layout is not visible.
- Same couple identity across shots.
- No text, watermark, new people, voiceover, or music.
- Handheld iPhone memory style remains messy and intimate.

## Task 8 - Manual Music Prompt

Suggested subagent: audio prompt operator.

Actions:

- Adapt the music prompt to the trip location, culture, and mood.
- Target final duration equal to the assembled video, about 60 seconds for four 15-second clips.
- Save the prompt as `audio/music_prompt_zh.txt`.
- Do not run Gemini CLI or any automatic music generation tool by default.
- Remind the user to paste `audio/music_prompt_zh.txt` into their preferred music generation tool and save the generated music back into `audio/` if they want it embedded later.

Fallback:

- If the user does not want music yet, continue with silent video assembly and leave `audio/music_prompt_zh.txt` as the handoff artifact.

## Task 9 - Assembly Decision and Assembly

Suggested subagent: video editor.

Actions:

- After four video clips exist, ask the user which edit route they want before assembling:
  - FFmpeg for direct simple concatenation and optional music mux.
  - Remotion for transitions, trims, captions, overlays, music-aware timing, or reusable React composition.
  - HyperFrames for transitions, crops/trims, captions, light leaks, rhythm-aware edits, overlays, or reusable HTML/GSAP composition over existing clips.
- Join the four clips in order.
- Use FFmpeg for direct concatenation, codec-safe joining, and simple music embedding.
- Use Remotion when the user wants richer editing: timed transitions, trims, light leaks, captions, animated overlays, music-aware timing, or repeatable React-based composition.
- When using Remotion, follow the `remotion-best-practices` skill. Scaffold a minimal Remotion project if one does not exist, import the four clips as assets, define a 9:16 720x1280 composition around 60 seconds, and render the final MP4.
- Use HyperFrames only after the four source clips exist, when the user wants HTML-based composition, transitions, crops/trims, captions, light leaks, rhythm-aware edits, overlays, or a reusable HyperFrames composition. Follow the `hyperframes` and `hyperframes-cli` skills, use a 9:16 composition around 60 seconds, run `npx hyperframes lint`, `npx hyperframes inspect`, and render with `npx hyperframes render`.
- Add music only if the user provides a generated music file and asks to embed it.
- Export `videos/final_vlog.mp4`.

Fallback:

- If FFmpeg is unavailable, write `videos/manual_edit_order.txt` with clip order and audio path.

## Task 10 - QA

Suggested subagent: independent reviewer.

Check:

- All outputs are inside `<Output Root>/<Project Title>/`.
- Four clips exist or blockers are documented.
- The final video exists or manual assembly handoff exists.
- `audio/music_prompt_zh.txt` exists and the user was reminded to generate soundtrack manually with their preferred tool.
- Character identity stays consistent.
- No visible grid/collage layout in final video clips.
- No text, logo, watermark, unexpected people, voiceover, or AI-polished fashion look.

Write findings to `qa.md`.
