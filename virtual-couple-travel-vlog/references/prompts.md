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
Create a clean professional orthographic character turnaround reference sheet for ONE SAME [MALE_ROLE] only, based on the uploaded approved 4x4 memory grid and derived 2x2 sheets. Extract only the man's identity; do not copy, paste, fade, blend, or include any reference photo backgrounds.

Character identity to preserve: [MALE_IDENTITY_LOCK]. Keep one consistent face across every view and expression.

Wardrobe must be fully unified across the entire sheet: [MALE_WARDROBE_LOCK]. No alternate outfits. No wardrobe changes between views.

Layout: pure seamless white background only, orthographic camera, flat even studio lighting, same scale, same body proportions, same ground line. Include full-body front view, full-body left side view, full-body back view, plus clean close-up head views: neutral front, soft smile front, candid half-smile, profile, three-quarter view. Keep him realistic, ordinary, not model-like, not cinematic, not stylized.

Strict exclusions: no wife, no other people, no travel destination, no city, no skyline, no transit station, no restaurant, no hotel, no shop, no market, no architecture, no beach, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays, no faded background panels, no pasted photo strips, no grid lines, no text, no labels, no logo, no watermark, no measurement lines, no UI.

The final image must look like a clean studio character turnaround sheet on a plain white background, not a mixed collage. If any reference scenery appears, the image is wrong.
```

## Character Card Prompt - Female

```text
Create a clean professional orthographic character turnaround reference sheet for ONE SAME [FEMALE_ROLE] only, based on the uploaded approved 4x4 memory grid and derived 2x2 sheets. Extract only the woman's identity; do not copy, paste, fade, blend, or include any reference photo backgrounds.

Character identity to preserve: [FEMALE_IDENTITY_LOCK]. Keep one consistent face across every view and expression.

Wardrobe must be fully unified across the entire sheet: [FEMALE_WARDROBE_LOCK]. No alternate outfits. No wardrobe changes between views.

Layout: pure seamless white background only, orthographic camera, flat even studio lighting, same scale, same body proportions, same ground line. Include full-body front view, full-body left side view, full-body back view, plus clean close-up head views: neutral front, soft smile front, candid smile, profile, three-quarter view. Keep her realistic, ordinary, not model-like, not cinematic, not stylized.

Strict exclusions: no husband, no other people, no travel destination, no city, no skyline, no transit station, no restaurant, no hotel, no shop, no market, no architecture, no beach, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays, no faded background panels, no pasted photo strips, no grid lines, no text, no labels, no logo, no watermark, no measurement lines, no UI.

The final image must look like a clean studio character turnaround sheet on a plain white background, not a mixed collage. If any reference scenery appears, the image is wrong.
```

Validated pattern from the successful `character_female_v3` run:

- Use one role only, e.g. "ONE SAME young American wife only."
- Write an explicit identity lock, e.g. age, ethnicity/nationality, build, hair color/length, face type, smile, and ordinary travel feeling.
- Write one wardrobe lock, e.g. "cream knit sweater, light blue jeans, clean white sneakers."
- Negate every source-image remnant: no husband, no city, no skyline, no transit, no restaurant, no hotel, no shop, no travel-photo fragments, no inset reference images, no collage remnants, no transparent ghosted background images, no scenic overlays.

## Character Card Cleanup Prompt

Use this when a card has a good identity but visible travel-photo remnants.

```text
Clean up this existing character reference sheet. Keep the same character identity, full-body views, head views, hairstyle, face, body proportions, and unified outfit. Remove every non-white reference-photo remnant from the background.

The output must be a clean studio character sheet on a pure seamless white background only. Replace all city scenery, market photo fragments, restaurant fragments, hotel/elevator fragments, architecture, beach, transit, inset travel images, ghosted photos, faded panels, collage remnants, pasted strips, and any other background artifacts with plain white studio background.

Do not add another person. Do not change the face. Do not change the outfit. Do not crop away the main front, side, back, and head views. No text, no logo, no watermark, no grid, no labels.
```

## Character Card Fallback Prompt

Use this after 3 failed turnaround attempts. The fallback is acceptable for video reference when it is cleaner than a flawed turnaround sheet.

```text
Create a clean single-character identity reference on pure seamless white background for ONE SAME [ROLE] only. Extract only the character identity from the uploaded travel references. Output a clean full-body standing front view plus three clean head portraits: neutral front, soft smile front, and profile. Same face, same hairstyle, same outfit, same body proportions. Studio photography lighting, ordinary realistic person, not a fashion model.

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
