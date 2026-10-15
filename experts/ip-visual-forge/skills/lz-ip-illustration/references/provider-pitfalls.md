# Provider Pitfalls

Known failure modes with specific image-generation providers. Add to this file when a session discovers a reproducible trap.

## gpt-image-2

### Complex multi-region character sheets time out

- **Symptom**: `gpt-image-2 request timed out after 480s` when the prompt describes a character sheet with 5+ labeled regions (main view, side view, expressions, action poses) in a single image.
- **Root cause**: The model's generation time scales with composition complexity. A single image with many labeled regions and distinct sub-scenes exceeds the 480s timeout.
- **Fix**: Split into single-subject prompts. Generate the primary visual master first, then generate additional views (expressions, action poses) as separate images if needed.
- **Session evidence**: 2026-07-14 — ming-investigator visual master. 5-region character sheet timed out; single-subject "three-quarter view standing full body" prompt succeeded in ~2 minutes.

### Incorrect `modality: text` on successful image-to-image calls

- **Symptom**: a local `image_url` is converted to a `data:image/...;base64,...` payload and submitted as an edit request, yet the successful tool response reports `modality: text`.
- **Root cause**: the `gpt-image-2` plugin called `success_response(...)` without setting its `modality`; the helper defaults to `text` even when `is_edit` is true.
- **Fix**: return `modality="image" if is_edit else "text"`. Keep request debug logging so `is_edit`, `source_count`, and the serialized `payload.image` can verify the attachment path.
- **Session evidence**: 2026-07-15 — Freehand Ink-Wash Narrative scenes logged `is_edit: true`, `source_count: 1`, and a 3.58 MB `data:image/png;base64,...` request payload; the output label was nevertheless `text`. The installed-first fix passed text and image-to-image mocked smoke tests.

### Chinese cultural gesture triggers content policy

- **Symptom**: `400 content_policy_violation` with `image_generation_user_error` when the prompt includes traditional Chinese gestures like 拱手 (hand salute) or classical phrases like 下回分解 (chapter-ending convention).
- **Root cause**: The provider's content filter may flag certain culturally-specific gestures or narrative conventions as policy violations, even in a clearly artistic/educational context.
- **Fix**: Simplify the prompt to neutral poses (standing, facing viewer, gentle smile) and plain CTA text. Avoid traditional gesture names and classical narrative conventions in the prompt text.
- **Session evidence**: 2026-07-14 — card 5 of baimiao-style-intro xhs series. Prompt with 拱手 and 下回分解 was rejected; simplified to "stands at center, facing the viewer, warm gentle smile" with plain footer text succeeded.