# Prompt Template

Use this structure for image prompts. Adapt wording to the target image model.

## Scene Prompt

```text
Create a [format/aspect ratio] illustration for an article.

Stable IP character:
[insert identity constraints from visual-spec.md]

Article idea:
[one cognitive anchor only]

Scene:
[describe the physical scene. The IP must be performing the core action.]

IP action:
The IP is actively [verb] [object] so the reader understands [cognitive anchor].

Composition:
[composition pattern, spatial layout, foreground/background, whitespace]

Labels:
[short labels only, or "no labels"]

Style:
[line quality, rendering style, palette, background, texture, simplicity]

Avoid:
[identity drift, extra characters, crowded PPT diagram, excessive text, unrelated props, inconsistent clothing/style]
```

## Visual Master Prompt

Use this when creating the first character reference image.

```text
Use case: illustration-story
Asset type: personal IP visual master reference
Primary request: Create a reusable character visual master for [IP name].

Subject:
[fixed species/person/object, body proportions, face, expression, temperament]

Clothing and signature props:
[signature outfit, props, motifs]

Pose and expression:
[front or three-quarter view, stable neutral/expert pose]

Scene/backdrop:
Minimal clean background. Supporting props may show the IP's domain, but keep the character as the focus.

Style/medium:
[stable rendering style, line quality, texture, palette]

Composition/framing:
Centered character sheet style, no cropping, enough padding, no poster-like scene.

Constraints:
The image must work as a long-term identity reference.

Avoid:
[identity drift, overly complex scene, extra main characters, dense text, one-off decorations]
```

## Text Language Rule

For Chinese article illustrations, prefer no in-image text unless labels are necessary. When labels are necessary, use short Chinese labels. Avoid long English whiteboard text in article images unless the user's content is English.

## Cover Prompt Difference

For cover images, use `templates/cover-prompt-template.md` after completing `references/cover-workflow.md`.

Cover prompts must add:

- integrated title region only when the selected text mode requests title lettering; never an empty title-safe area for later overlay
- platform format
- strong first-viewport IP recognition
- fewer explanatory labels
- clearer brand color use
- one communication proposition
- one primary visual hook
- one cover motif
- one declared IP deployment mode and mode-appropriate role
- one explicit content boundary

For article inline illustrations, prioritize explanation clarity over promotional impact.
