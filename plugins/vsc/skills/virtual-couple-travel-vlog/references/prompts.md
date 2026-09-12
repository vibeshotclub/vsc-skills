# Prompt Library

Replace bracketed placeholders before use.

## 4x4 Memory Grid Prompt

```text
A 4x4 grid collage of 16 candid nostalgic iPhone travel photos of ONE SAME FIXED COUPLE: [COUPLE_DESCRIPTION] on vacation in [DESTINATION_AND_REGION]. The same husband and same wife appear throughout all 16 snapshots. Lock their identities across every cell: same faces, same facial proportions, same age, same hair color and hairstyle, same body types, same casual travel wardrobe logic, same relationship energy. Treat this as one private camera roll from one real trip, not a collection of different couples.

The couple takes selfies together and photos of each other during the trip: [SCENE_LIST].

Shot on iPhone 14, POV selfie style, casual amateur photography, no clear theme, no deliberate composition, ordinary vacation snapshots. Slight motion blur, uneven lighting, occasional overexposure, awkward angles, imperfect framing, random cropping, confusing composition, realistic tourist photo feeling. Some photos are vertical, some horizontal, mixed perspectives, slightly tilted horizons, natural facial expressions, unposed moments, emotional but understated atmosphere.

Visual style: nostalgic, realistic, slightly vintage, soft phone-camera colors, [LOCAL_LIGHT_AND_WEATHER], muted tones, subtle digital noise, imperfect focus, casual social-media photo dump aesthetic, highly realistic iPhone photo quality, not cinematic, not professional, not polished.

No identity drift between cells, no different couples, no alternate faces, no changing hair color, no changing age, no unrelated people as the main couple. No perfect studio lighting, no fashion shoot, no dramatic composition, no luxury travel advertising, no flawless poses, no AI-looking faces, no overly sharp details, no clean symmetrical layout, no professional camera look. No text, no logos, no watermarks.
```

## Direct 2x2 Sheet Prompt

Use this only when a locked couple reference image or character cards already exist. Do not use this as the default first step because separate generations commonly drift identity.

```text
A 2x2 grid collage of 4 candid nostalgic iPhone travel photos, chapter [CHAPTER_NUMBER] of a four-part continuous private camera roll about the exact same locked couple shown in the uploaded reference image(s): [COUPLE_DESCRIPTION] traveling in [DESTINATION_AND_REGION].

Continuity from all chapters: same young couple, same faces copied from the references, same age, consistent hair, consistent ordinary travel wardrobe, same relationship energy, realistic tourist snapshots. This chapter focuses on [CHAPTER_BEAT] with scenes including [FOUR_SCENES].

Shot on iPhone 14, POV selfie style, casual amateur photography, ordinary vacation snapshots. Slight motion blur, uneven lighting, occasional overexposure, awkward angles, imperfect framing, random cropping, mixed vertical and horizontal perspectives, natural facial expressions, understated romance.

Visual style: nostalgic, realistic, slightly vintage, soft phone-camera colors, [LOCAL_LIGHT_AND_WEATHER], muted tones, subtle digital noise, imperfect focus, casual social-media photo dump aesthetic, highly realistic iPhone photo quality, not cinematic, not professional, not polished.

No identity drift, no different couple, no alternate faces, no different hair color, no changed age. No perfect studio lighting, no fashion shoot, no dramatic composition, no luxury travel advertising, no flawless poses, no AI-looking faces, no overly sharp details, no professional camera look. No text, no logos, no watermarks.
```

## Character Card Prompt - Male

```text
Create a 1:1 clean professional character turnaround reference sheet for ONE SAME [MALE_ROLE] only, based strictly on the uploaded approved 4x4 memory grid and derived 2x2 sheets. Extract only the man's identity, face, hair, body type, and wardrobe logic. Do not copy, paste, fade, blend, or include any reference photo backgrounds, travel scenes, memory sheets, or source-image fragments.

Character identity to preserve: [MALE_IDENTITY_LOCK]. Keep the exact same face, hairline, hairstyle, age, facial proportions, skin texture, body type, and ordinary realistic travel feeling across every panel.

Wardrobe must be fully unified across the entire sheet: [MALE_WARDROBE_LOCK]. No alternate outfits. No wardrobe changes between views.

Fixed layout, exactly seven panels in two horizontal rows:

Top row: four full-body standing views placed side-by-side in this exact order: front view, left profile view facing screen left, right profile view facing screen right, back view. The subject must stand in a relaxed A-pose in every full-body panel, with consistent scale, consistent head height, consistent foot baseline, accurate anatomy, clear silhouette, and even spacing.

Bottom row: three highly detailed close-up head portraits aligned beneath the full-body row in this exact order: front portrait with a natural small smile, left profile portrait facing screen left with a serious neutral expression, right profile portrait facing screen right with a serious neutral expression. Keep the same facial scale, same hairline, same head shape, and same identity across all three portraits.

Background and presentation: pure seamless white background only, technical model turnaround sheet, clean panel separation, uniform framing, crisp print-ready reference-sheet look, sharp realistic details. Use orthographic camera treatment for the full-body views, flat even studio lighting, same light direction, same intensity, same softness, and natural controlled shadows. Match the realism level, rendering approach, texture, color treatment, and overall aesthetic of the uploaded reference images while removing all source-image scenery.

Strict exclusions: no wife, no other people, no travel destination, no city, no skyline, no street, no river, no mountain, no transit station, no restaurant, no hotel, no shop, no market, no architecture, no beach, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays, no faded background panels, no pasted photo strips, no screenshots, no UI, no readable text, no labels such as FRONT/SIDE/BACK, no subtitles, no logo, no watermark block, no measurement lines. No cartoon, no anime, no stylized illustration, no deformed fingers, no extra limbs, no distorted faces.

The final image must look like one clean studio technical character turnaround sheet on a plain white background, not a mixed collage. If any reference scenery, memory image, extra person, label, or source-photo remnant appears, the image is wrong.
```

## Character Card Prompt - Female

```text
Create a 1:1 clean professional character turnaround reference sheet for ONE SAME [FEMALE_ROLE] only, based strictly on the uploaded approved 4x4 memory grid and derived 2x2 sheets. Extract only the woman's identity, face, hair, body type, and wardrobe logic. Do not copy, paste, fade, blend, or include any reference photo backgrounds, travel scenes, memory sheets, or source-image fragments.

Character identity to preserve: [FEMALE_IDENTITY_LOCK]. Keep the exact same face, hairline, hairstyle, age, facial proportions, skin texture, body type, and ordinary realistic travel feeling across every panel.

Wardrobe must be fully unified across the entire sheet: [FEMALE_WARDROBE_LOCK]. No alternate outfits. No wardrobe changes between views.

Fixed layout, exactly seven panels in two horizontal rows:

Top row: four full-body standing views placed side-by-side in this exact order: front view, left profile view facing screen left, right profile view facing screen right, back view. The subject must stand in a relaxed A-pose in every full-body panel, with consistent scale, consistent head height, consistent foot baseline, accurate anatomy, clear silhouette, and even spacing.

Bottom row: three highly detailed close-up head portraits aligned beneath the full-body row in this exact order: front portrait with a natural small smile, left profile portrait facing screen left with a serious neutral expression, right profile portrait facing screen right with a serious neutral expression. Keep the same facial scale, same hairline, same head shape, and same identity across all three portraits.

Background and presentation: pure seamless white background only, technical model turnaround sheet, clean panel separation, uniform framing, crisp print-ready reference-sheet look, sharp realistic details. Use orthographic camera treatment for the full-body views, flat even studio lighting, same light direction, same intensity, same softness, and natural controlled shadows. Match the realism level, rendering approach, texture, color treatment, and overall aesthetic of the uploaded reference images while removing all source-image scenery.

Strict exclusions: no husband, no other people, no travel destination, no city, no skyline, no street, no river, no mountain, no transit station, no restaurant, no hotel, no shop, no market, no architecture, no beach, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays, no faded background panels, no pasted photo strips, no screenshots, no UI, no readable text, no labels such as FRONT/SIDE/BACK, no subtitles, no logo, no watermark block, no measurement lines. No cartoon, no anime, no stylized illustration, no deformed fingers, no extra limbs, no distorted faces.

The final image must look like one clean studio technical character turnaround sheet on a plain white background, not a mixed collage. If any reference scenery, memory image, extra person, label, or source-photo remnant appears, the image is wrong.
```

Current fixed seven-panel character-card standard:

- Use one role only, e.g. "ONE SAME young American wife only."
- Write an explicit identity lock, e.g. age, ethnicity/nationality, build, hair color/length, face type, smile, and ordinary travel feeling.
- Write one wardrobe lock, e.g. "cream knit sweater, light blue jeans, clean white sneakers."
- Negate every source-image remnant: no husband, no city, no skyline, no transit, no restaurant, no hotel, no shop, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays.
- Keep the fixed seven-panel layout: top row has four full-body views, bottom row has three head portraits. Do not allow extra panels, missing panels, captions, labels, or scenic image inserts.

## Character Card Cleanup Prompt

Use this when a card has a good identity but visible travel-photo remnants.

```text
Clean up this existing character reference sheet. Keep the same character identity, hairstyle, face, body proportions, and unified outfit. Convert the sheet into the fixed seven-panel technical turnaround layout if needed: top row four full-body views in the order front, left profile, right profile, back; bottom row three close-up portraits in the order front small smile, left profile serious, right profile serious. Remove every non-white reference-photo remnant from the background.

The output must be a clean studio character sheet on a pure seamless white background only. Replace all city scenery, market photo fragments, restaurant fragments, hotel/elevator fragments, architecture, beach, transit, inset travel images, ghosted photos, faded panels, collage remnants, pasted strips, and any other background artifacts with plain white studio background.

Do not add another person. Do not change the face. Do not change the outfit. Do not crop away the required full-body or head views. No text, no logo, no watermark, no grid, no labels, no UI.
```

## Character Card Fallback Prompt

Use this after 3 failed turnaround attempts. The fallback is acceptable for video reference when it is cleaner than a flawed turnaround sheet.

```text
Create a clean single-character identity reference on pure seamless white background for ONE SAME [ROLE] only. Extract only the character identity from the uploaded travel references. Prefer the fixed seven-panel layout: top row four full-body standing views in the order front, left profile, right profile, back; bottom row three clean head portraits in the order front small smile, left profile serious, right profile serious. If the model cannot make the full seven-panel sheet cleanly, output one clean full-body standing front view plus three clean head portraits: neutral front, soft smile front, and profile. Same face, same hairstyle, same outfit, same body proportions. Studio photography lighting, ordinary realistic person, not a fashion model.

No other people, no travel scenery, no architecture, no city, no restaurant, no market, no beach, no hotel, no transit, no collage, no reference photo fragments, no transparent ghost images, no text, no logo, no watermark.
```

## Topview Omni Reference Video Prompt

```text
Use the uploaded 2x2 grid <<<Image1>>> as a contact sheet of memories, not as a literal grid. Use <<<Image2>>> and <<<Image3>>> as the main character references. Transform the individual photos into one cohesive nostalgic music video sequence about the same young man and young woman falling in love through candid iPhone moments.

Create a 15-second emotional indie-pop MV montage. Preserve the same couple's faces, age, hair, clothing style, and relationship energy across all shots. The video should feel like real iPhone footage from a private camera roll: imperfect, intimate, handheld, slightly shaky, amateur framing, accidental zooms, motion blur, blown highlights, soft grain, muted vintage colors, [LOCAL_COLOR_MOOD], tiny focus mistakes.

The sequence should flow like fragmented memories from [CHAPTER_BEAT].

Editing style: cohesive music video montage, romantic but not cheesy, dreamy memory fragments, rhythmic cuts synced to an imagined melancholic indie-pop song, natural handheld movement, soft whip-pan transitions, phone-camera flash transitions, match cuts between similar poses from different photos.

Visual style: candid iPhone photography, 2010s camera roll nostalgia, vintage emotional aesthetic, amateur home-video realism, soft film grain, subtle VHS-like imperfection, warm faded colors, realistic skin texture, natural expressions.

Important rules: do not show the original grid layout, do not create a collage, do not add text, do not add watermarks, do not introduce new people, do not make them look like fashion models, do not over-cinematize, do not make the camera too smooth, do not change their identities between shots. Keep it intimate, messy, romantic, and emotionally real.

No music. No voiceover.
```

## Manual Music Prompt - Chinese

```text
Write the final music prompt in Simplified Chinese at runtime. Use this structure:

Create a [DURATION] track in [LOCATION_OR_CULTURE_INSPIRED_MUSIC_STYLE]. The overall mood is [MOOD_WORDS], calm, warm, and full of private travel memories. Use a light, airy, whisper-like [LANGUAGE] female vocal, low in the mix, with hall reverb, as if murmuring close to the listener.

The arrangement should center on gentle arpeggios from [PRIMARY_INSTRUMENT], with faint synth ambience and very light percussion such as brushed snare or shaker. Keep a warm major-key direction, avoid heavy sadness, keep the rhythm steady, and avoid sudden dynamic explosions.

The atmosphere should match [DESTINATION_AND_WEATHER]: intimate, graceful, and memory-like. Do not create dialogue, voiceover, or obvious narrative lyrics; the vocal should feel closer to humming and soft murmuring.
```
