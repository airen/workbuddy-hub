# Cover QA Checklist

Use this checklist for cover directions, final prompts, and generated cover images. Review both thumbnail and full-size views.

## Hard Failures

Reject the cover if any condition is true:

- The visual promise contradicts or exaggerates the article.
- The image tries to summarize the whole article.
- More than one scene competes for attention.
- The concept depends on long text or tiny labels.
- The IP identity, outfit, locked palette, or rendering style drifts.
- The cover replaces the IP rendering system with a conflicting treatment such as flat-vector, 3D, or pixel art.
- Any cover text was added locally after generation.
- Requested Chinese title/subtitle is garbled, deformed, misspelled, visually detached, or weakens the motif.
- The selected IP deployment mode is not recorded or is violated.
- A scene guide or brand anchor blocks the headline, primary hook, or thumbnail hierarchy.

## Content Accuracy

- One communication proposition is visible.
- The reader tension and promised payoff match the article.
- The cover does not imply unsupported numbers, outcomes, tools, or conclusions.
- The visual metaphor remains understandable after reading the article.

## Thumbnail Performance

- The main subject or visual event is recognizable at small size.
- One object, contrast, or visual relationship carries the visual hook.
- Contrast and hierarchy reveal the intended focal point immediately.
- Small decorative details are not required for comprehension.
- A small IP brand anchor remains recognizable without becoming the first focal point.

## IP Deployment

First confirm the selected mode, then apply its checks.

### Narrative actor

- The IP has one clear role and performs the central verb.
- The dominant emotion supports the reader tension.
- Removing the IP breaks the visual proposition.
- The IP action reads as a silhouette or large gesture at thumbnail size.

### Scene guide

- The motif carries the primary proposition without requiring the IP to cause the event.
- The IP's gesture, gaze, position, or emotion improves reader orientation or interpretation.
- The IP does not compete with the motif or title.

### Brand anchor

- The primary proposition works without the IP.
- The IP clearly strengthens series and author recognition.
- Its small posture, expression, or prop responds to the theme; it is not a blank repeated sticker.
- Its edge/lower-corner placement does not obstruct the headline, main subject, or visual hook.

For every mode:

- The primary visual master remains recognizable.
- The IP's scale and placement match the declared deployment mode.

## Visual Treatment

- The selected expression mode helps communicate the proposition rather than merely changing decoration.
- `typography` is used only when lettering is integrated into the visual event; otherwise use another expression mode.
- Text mode is `none`, `integrated-title-only`, or `integrated-title-and-short-subtitle`; text-rich cover copy is rejected.
- Mood (`subtle`, `balanced`, or `bold`) supports article tension without contradicting the IP's visual world.
- Contextual color emphasis only adjusts colors already allowed by `visual-spec.md`.
- Rendering remains locked from `visual-spec.md`.

## Composition

- One dominant subject or visual event.
- Any requested title/subtitle is integrated into the generated image, not post-composited.
- Foreground, middle ground, and background do not compete.
- The composition works with no in-image text.
- Labels, when necessary, are short and secondary.

## Curiosity and Brand

- The image creates a question, contrast, tension, or anticipated transformation.
- Curiosity comes from the article idea, not unrelated spectacle.
- Brand colors support hierarchy rather than flattening it.
- The cover fits beside previous IP covers without becoming repetitive.

## Final Decision

Record:

- `PASS`: no hard failures and all core checks are satisfied
- `REVISE`: concept is valid but composition, IP deployment, or hierarchy needs adjustment
- `REJECT`: proposition, hook, motif, IP deployment, or visual treatment must be redesigned

For `REVISE` or `REJECT`, name the failed layer:

- proposition
- hook
- motif
- IP deployment
- composition
- visual treatment
- integrated text
- identity consistency
