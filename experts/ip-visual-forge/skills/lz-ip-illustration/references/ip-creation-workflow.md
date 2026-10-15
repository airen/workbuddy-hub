# IP Creation Workflow

Use this workflow only when no initialized IP exists, or when the user explicitly asks to create a new IP.

## 1. Structured Interview

Use a brief-first interview, not a questionnaire-first interview. Read `references/ip/brief-first-interview.md`.

Required decisions:

- IP type: expert, companion, observer, host, coach, critic, storyteller, operator.
- Audience: creators, designers, developers, operators, entrepreneurs, students, general readers, or a custom audience.
- Content domain: prompts, AI tools, writing, career, product, design, business, education, or custom.
- Personality: rational, warm, sharp, playful, calm, absurd, premium, practical.
- Visual style: **flat illustration**, **hand-drawn technical sketch**, **semi-realistic illustration**, **3D toy**, **clay**, **comic**, **pixel art**, **Classic Japanese children’s manga-animation**, **Japanese gag-reaction manga-animation**, **Modern color rubber-hose tech cartoon**, **Traditional Chinese baimiao realistic lianhuanhua**, **Pen-and-ink realistic lianhuanhua**, **Gongbi line-and-color realistic lianhuanhua**, **Woodcut-print realistic lianhuanhua**, **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration**, **Mianzhu woodblock New Year picture**, **Chinese shadow puppetry**, **Rule-Bound Crude Doodle / 规则化粗糙涂鸦**, **Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事** (candidate revision 2; not yet production-approved), or custom. The 18 bold styles are production presets; Freehand Ink-Wash Technical Narrative is a selectable candidate under independent validation; `custom` is an input option, not a production preset. When a named rendering preset is selected, read its matching preset under `references/` before generating directions, refining the visual master, or writing the final IP files.
- Primary scenes: article covers, article inline illustrations, social posts, slides, video covers, course assets.

When a named rendering preset is selected, first read `references/ip/styles/style-selection.md`, then the matching family guide and preset file. Examples: Chinese nostalgic styles route through `lianhuanhua-style-selection.md`; Japanese manga / animation styles route through `japanese-manga-style-selection.md`; quirky cartoon styles route through `quirky-cartoon-style-selection.md`; Rule-Bound Crude Doodle routes through `rule-bound-crude-doodle-style-selection.md`. Rule-Bound Crude Doodle is production-approved. Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事 routes through the Chinese nostalgic guide and `freehand-ink-wash-narrative.md`; it is a revision-2 candidate that must be validated with the initialized IP through Signal-Path Poster and Loose Technical Strip scenes before human-approved promotion.

Do not dump all six required decisions on the user at once. First ask for a short natural-language brief and show an example. Then map the user's brief to the six required decisions.

If a required decision is missing or ambiguous, ask one focused follow-up question at a time. Prefer multiple-choice options plus an optional custom answer.

Do not enter Visual Master Directions until the visual-master gate is satisfied:

- character subject is clear
- content domain is clear
- visual style is clear
- primary scenes are clear

IP type, audience, and personality should be collected or inferred before the summary, but they do not always need to block visual exploration if the summary makes the assumptions explicit and the user confirms them.

Before entering Visual Master Directions, summarize all collected decisions and ask the user to confirm or adjust them. Proceed only after confirmation or after the user provides edits that satisfy the visual-master gate.

## 2. Visual Master Directions

Generate 3-6 distinct visual master directions at once. Do not free-associate random variants. Read `references/ip/visual-master-directions.md` and build directions from a constrained direction matrix based on the confirmed brief.

Each direction must differ in long-term brand strategy, not only surface styling. Avoid making six versions that only vary clothing, color, pose, or illustration texture.

If generating images in this stage, create lightweight primary visual candidates only. Do not generate full character sheets, turnarounds, expression grids, or color palettes before the user selects a direction.

For each direction, include:

- Direction name.
- Strategic angle.
- Character appearance.
- Signature outfit or object.
- Palette.
- Temperament.
- Scene participation mode.
- Best-fit content scenarios.
- Risks or limitations.
- Why this direction differs from the others.

Ask the user to pick one direction before deep refinement.

When generating bitmap directions, read `references/image-generation-workflow.md`. If only one initial visual master is requested, still make it explicit that this is a first draft, not the final locked identity.

After images are generated, review them with `references/ip/visual-master-review.md` before updating the IP files.

## 3. Deep Refinement

After the user selects a visual master direction, do not restart broad exploration. Refine the selected direction into stable identity rules and generate a small validation set.

Deep Refinement should produce images for stability testing and identity locking. The preferred output is one refined character sheet for the selected direction. Do not generate another random batch of directions.

The character sheet may include:

- primary refined visual master
- front or three-quarter view
- side or back view if useful
- expression samples
- one or two core action poses
- signature props
- color palette

Generate extra separate validation images only when the character sheet does not sufficiently test action or scene participation.

Use these images to lock:

- face or head shape
- body proportion
- signature clothing
- signature object or visual motif
- line style and rendering
- palette or, for black-and-white rendering, grayscale identity mapping
- print/paint construction and composition grammar when the selected preset is a traditional New Year-picture rendering
- expression range
- action range
- allowed variation
- forbidden variation

Before persisting the final IP files, summarize:

- Must lock
- Flexible
- Do not lock

Ask the user to confirm or adjust this lock summary. Proceed only after confirmation.

## 4. Initial Asset Set

Create or request:

- front half-body
- full-body standing pose
- side or three-quarter pose
- thinking expression
- explaining action
- pointing action
- dissecting or organizing action
- diagnosing action

## 5. Persist the IP

Write the final files using templates:

- `templates/ip-profile-template.md`
- `templates/visual-spec-template.md`
- `templates/prompt-pack-template.md`
- `templates/action-library-template.md`

After persistence, future requests should skip this workflow unless the user asks for a new IP or revision.

If a generated image is accepted as the visual master, copy it into `reference-images/` and update `visual-spec.md` with:

- filename
- role, such as primary visual master, pose reference, expression reference, or action reference
- which identity traits it locks
- any traits that should not be copied into future images

Also save the accepted prompt as a reproducibility record beside the reference image when practical, for example:

- `reference-images/<ip-slug>-visual-master-v1.md`
- `reference-images/<ip-slug>-direction-sheet-v1.md`
