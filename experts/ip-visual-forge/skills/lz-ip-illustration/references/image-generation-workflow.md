# Image Generation Workflow

Use this reference when the skill should generate actual bitmap images, not only prompts.

## Tool Selection

Use the image-generation tool actually exposed by the current runtime. The workflow is portable; a runtime-specific tool name or authentication path is not.

### Hermes

- Use Hermes `image_generate` when it is available.
- Inspect its active capability description before deciding whether to pass `image_url` or `reference_image_urls`.
- If it advertises image-to-image / editing, attach the accepted primary visual master as the default identity reference for downstream images.
- If it advertises text-to-image only, do not pass image inputs. Keep the fixed identity, palette, and rendering constraints explicit in the prompt instead.
- Do not assume that a model family supporting editing means the configured Hermes provider or auth route exposes editing; the runtime tool schema is authoritative.

### Codex

- In Codex threads, use the image-generation capability actually exposed in that thread.
- Do not conclude that it is unavailable based only on missing namespace text, missing prompt mentions, or prior-thread assumptions. Confirm by attempting the built-in call when image generation is needed.
- Do not assume Codex-specific tool names or OAuth behavior exist in Hermes.

Use CLI/API fallback only when the user explicitly requests CLI/API mode, or when the current runtime has no usable built-in path and the user chooses the fallback. Do not require an API key for a built-in path; an API fallback may require its provider's credentials.

### Provider-Specific Aspect-Ratio and Resolution Constraints

Image providers differ in which aspect ratios and resolutions they support. Common failure modes:

- Some providers reject aspect ratios with insufficient pixel counts (e.g. Doubao Seedream requires minimum 3,686,400 pixels per image; its 3:4 portrait default resolution is too small and returns `size not valid`).
- For non-Xiaohongshu outputs, when portrait (3:4) or landscape (16:9) fails with a pixel-minimum error, fall back to **square (1:1)** — it typically generates at the highest supported resolution.
- For non-Xiaohongshu outputs, crop the square output to the target aspect ratio locally only when the platform requires it, and document the crop in QA notes. Xiaohongshu/Green Book cards must not be post-generation cropped: regenerate at a supported composition-safe ratio or record the provider limitation.

Inspect the provider's capabilities before generating — if a non-Xiaohongshu portrait generation fails with a pixel error, do not retry with the same parameters. Switch to square and note the limitation in the run's QA notes. For Xiaohongshu/Green Book cards, preserve the no-crop rule: regenerate only at a supported composition-safe ratio or record the limitation.

## Generation Modes

### Visual Master

Purpose: create or refine the stable character identity.

Output should be:

- character-first
- clean background
- full body or clear half-body
- stable outfit and palette
- minimal supporting props
- suitable as a reference image

After generation:

1. Inspect the image.
2. Run `references/ip/visual-master-review.md`.
3. If accepted, copy the image into `ip-assets/<ip-slug>/reference-images/`.
4. Update `visual-spec.md` with the filename and locked identity traits.

### Article Illustration

Purpose: explain one article cognitive anchor with the IP acting inside the scene.

Output should be:

- usually 16:9
- one clear scene
- IP action-driven
- short labels or no labels
- consistent with the primary visual master

Reference rule:

- if the current image tool supports reference images, attach the accepted primary visual master by default as the identity reference
- keep palette, rendering style, and signature identity constraints explicit in text even when the reference image is attached
- if the tool does not support reference images, rely on repeated text constraints only

After generation:

1. Inspect identity stability.
2. Check that the IP is doing the core action.
3. Check text language and readability.
4. Create the target `images/` directory before copying an accepted result; save accepted images into the article output folder.
5. Record the prompt and QA notes.

### Transient Generation Failure Handling

A single provider timeout or transient upstream error is not proof that image generation is unavailable. When a generation call does not return an image path:

1. Do not claim that image was generated or archived.
2. Check the current image cache for a newly produced result before retrying; some providers may finish upstream while the client call times out.
3. If no matching result is present and connectivity remains reachable, retry once with the same identity/style locks but a shorter, non-redundant prompt.
4. Archive and decode-verify only outputs returned by the tool or otherwise unambiguously matched to the current run.
5. If retry succeeds, record only the successful asset in the QA handoff; do not turn the transient error into a permanent capability limitation.

Always distinguish **technical asset verification** (file archived and decodes) from **human visual acceptance** (the user approves the full test set).

### Cover Image

Purpose: make a recognizable first-view article/social cover.

Before generation:

1. Read `references/cover-workflow.md`.
2. Produce and review 2-4 cover directions.
3. Confirm one communication proposition, visual hook, motif, selected IP deployment mode, and mode-appropriate IP role.
4. Save the final prompt using `templates/cover-prompt-template.md`.
5. When supported, attach the primary visual master as the identity reference, not as the default composition reference.

Output should be:

- platform-specific aspect ratio
- an integrated title region only when the selected text mode requests title lettering; never an empty title-safe area for later overlay
- strong IP recognition
- fewer explanatory labels than inline illustrations
- aligned with the IP's palette and visual system

After generation:

1. Review at thumbnail and full size.
2. Run `references/cover/cover-qa-checklist.md`.
3. Save accepted images and QA notes in the cover run directory.

### Xiaohongshu / Green Book Card Series

Purpose: deliver a phone-first, swipeable series where each card advances one reader beat.

Before generation:

1. Read `references/xhs-card-workflow.md`.
2. Confirm one series visual direction using `templates/xhs-series-style-template.md`.
3. Confirm a 3-6 card plan using `templates/xhs-card-plan-template.md`.
4. Save one prompt per card using `templates/xhs-card-prompt-template.md`.
5. Attach the primary visual master as the identity reference when supported.

Output should be:

- 3:4 vertical cards unless another ratio is required
- one readable takeaway and one visual anchor per card
- stable IP identity and series-wide visual system
- sparse, readable Chinese text or no text

After generation:

1. Review each card at phone size.
2. Review the full sequence in order.
3. Run `references/xhs-card/xhs-card-qa-checklist.md`.
4. Save accepted images and QA notes in the XHS run directory.

## Saving Generated Images

When the image is project-bound, copy the accepted generated image into the project or skill asset folder. Keep the original generated image in its default location unless the user explicitly asks to delete it.

### Provider Response Normalization

An OpenAI-compatible image endpoint may return either `data[0].b64_json` or `data[0].url`. Treat both as successful image outputs:

1. If `b64_json` is present, decode it and save the bytes as PNG.
2. If `url` is present, download the returned asset and save the bytes as PNG.
3. Validate that the saved file decodes before marking generation complete.

Do not regenerate merely because a storage helper expected base64 while the provider returned a URL. Normalize and persist the already-generated asset first; this prevents needless duplicates and preserves the prompt-to-output record.

Use stable, reproducible layout rules:

- stable identity references go to `ip-assets/<ip-slug>/reference-images/`
- article illustration prompts go to `ip-assets/<ip-slug>/article-runs/<article-slug>/prompts/`
- article illustration images go to `ip-assets/<ip-slug>/article-runs/<article-slug>/images/`
- article analysis and shot planning stay beside the prompts/images inside the same article run directory
- cover prompts go to `ip-assets/<ip-slug>/cover-runs/<article-slug>/prompts/`
- cover images go to `ip-assets/<ip-slug>/cover-runs/<article-slug>/images/`
- Xiaohongshu/Green Book card prompts go to `ip-assets/<ip-slug>/xhs-runs/<post-slug>/prompts/`
- Xiaohongshu/Green Book card images go to `ip-assets/<ip-slug>/xhs-runs/<post-slug>/images/`

Do not scatter one run across unrelated cache, workspace output, and asset directories without copying the accepted result into the proper run folder.

Recommended names:

- `reference-images/<ip-slug>-visual-master-v1.png`
- `reference-images/<ip-slug>-pose-explain-v1.png`
- `article-runs/<article-slug>/prompts/01-<anchor-slug>.md`
- `article-runs/<article-slug>/images/01-<anchor-slug>.png`
- `cover-runs/<article-slug>/prompts/cover-v1.md`
- `cover-runs/<article-slug>/images/cover-v1.png`
- `xhs-runs/<post-slug>/prompts/01-cover.md`
- `xhs-runs/<post-slug>/images/01-cover.png`

When the source article comes from a local file path, copy the source into:

- `article-runs/<article-slug>/source/source-<article-slug>.<ext>`

Only write back an article-with-images file if the user explicitly asked for insertion or rewrite.

## Prompt Discipline

For every generated image, include:

- stable IP identity
- scene goal
- mode-appropriate IP participation statement: an action sentence for inline article scenes and animation; selected deployment mode plus role for covers; declared participation role and purposeful pose for Xiaohongshu cards
- composition pattern
- label policy
- palette constraints
- style constraints
- avoid list

When the tool supports image references, use the accepted primary visual master as the default identity reference. Keep palette, rendering style, and signature identity details explicit in text even then. When the tool does not support image references, repeat fixed identity, palette, and rendering details in the prompt.

### Reference-Transmission Verification

Passing a local path or URL as `image_url` / `reference_image_urls` is not itself proof that the provider consumed it. After every image-reference generation, inspect the returned tool metadata and any available provider log for an image/edit modality, source count, or equivalent evidence.

- If the response positively confirms image input, record the reference path and confirmation in the run QA notes.
- If the response labels the generation as text-only, or supplies no reliable input evidence, record the result as a **prompt-level style test**. Do not claim image-to-image identity continuity has passed merely because the prompt named a reference image.
- Human visual review may still accept a coherent result, but production validation must keep identity-reference transmission as an unresolved check until verified.

This rule is especially important for reusable-IP validation: style consistency and identity-reference transmission are separate acceptance criteria.
