# Text as Visual Material

Use this reference for every lz-ip-illustration output that includes Chinese text, labels, titles, captions, callouts, cards, or UI-like lettering.

## Hard Rule

Do not add text locally after image generation. Local text overlay/compositing is forbidden for:

- article covers
- article inline illustrations
- Xiaohongshu / Green Book cards
- review cards, contact sheets intended as final visual outputs, and generated social images

Text must be treated as part of the visual composition. If the image needs text, the prompt must describe where the lettering lives, why it belongs there, how short it is, and how it avoids damaging the IP action or core visual idea.

## Why

Local overlay can destroy composition, cover the IP action, flatten the image into a slide, and make the character's role irrelevant. The image should be designed with the words from the start, not patched afterward.

## Pipeline Rules

### Covers

- Prefer no in-image text unless the requested output is explicitly a finished cover with title lettering.
- If title lettering is required, it must be generated as integrated cover typography within the scene.
- Do not create a clean title-safe area for later local text.
- Do not produce `*-with-title` local overlay variants.
- Reject the result if title text is deformed, misspelled, garbled, visually detached, or weakens the cover motif.

### Article Inline Illustrations

- Prefer no text when the scene explains the idea clearly.
- If image-only explanation is insufficient, include short integrated Chinese labels.
- Each label should be 5-10 Chinese characters when possible.
- Labels must sit on physical scene objects such as tags, tabs, module cards, route signs, sticky notes, callout flags, or diagram nodes.
- Labels must be close to what they explain and must not cover the IP's face, hands, signature props, or central action.
- Reject dense whiteboard paragraphs, fake UI copy, English filler, tiny labels, and post-production text overlay.

### Xiaohongshu / Green Book Cards

- Local text overlay is forbidden.
- Page header/footer text may be used when integrated into the design system.
- Other labels must be restrained, short, and visually placed as part of the illustration.
- Non-header/footer labels should be no more than 10 Chinese characters each.
- Use fewer labels instead of turning the card into a slide.
- If a card needs too much text to stay visual, split the idea into more cards or simplify the promise.
- Text must not overpower the IP action or central visual metaphor.

## Prompt Requirements

When text is needed, prompts must specify:

- exact Chinese text strings or strict maximum length
- placement as part of the scene, not a later overlay
- physical carrier: sign, tag, module card, route label, tab, notebook heading, screen label, or paper note
- size hierarchy: header, footer, label, tag, or callout
- visual integration rule: text follows the card/scene style and leaves IP action readable

## QA Hard Failures

Reject or revise if:

- any final text was added locally after image generation
- Chinese characters are deformed, garbled, misspelled, or replaced with pseudo-text
- text covers the IP's meaningful action
- text makes the image feel like a generic slide or poster pasted over an illustration
- a label exceeds 10 Chinese characters outside header/footer areas
- the card or scene only works because of paragraph text
- the IP becomes decorative after text is added
