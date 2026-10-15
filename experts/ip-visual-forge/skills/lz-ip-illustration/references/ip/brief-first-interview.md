# Brief-First Interview

Use this protocol when no initialized IP exists and the user needs to create one.

## Goal

Reduce user friction. Do not start with a six-field questionnaire. Ask for a natural-language brief, infer what is obvious, identify gaps, and ask one focused follow-up at a time.

## Opening Message

Tell the user that no reusable IP profile was found, so the IP must be created first. Ask for a short brief and provide a copyable example in the user's language.

Example content to include:

```text
No reusable IP profile was found. We need to create one first; future article illustrations will reuse it.

Describe the IP in one sentence or short paragraph. For example:
"I want a chubby hippo IP that shares high-quality image generation prompts. It acts like a patient prompt coach for AI image creators. The style is clean 2D editorial illustration, mainly for article covers and inline article illustrations."
```

## Required Decisions

Track these six fields internally:

1. IP type: expert, companion, observer, host, coach, critic, storyteller, operator.
2. Audience: creators, designers, developers, operators, entrepreneurs, students, general readers, or custom.
3. Content domain: prompts, AI tools, writing, career, product, design, business, education, or custom.
4. Personality: rational, warm, sharp, playful, calm, absurd, premium, practical.
5. Visual style: **flat illustration**, **hand-drawn technical sketch**, **semi-realistic illustration**, **3D toy**, **clay**, **comic**, **pixel art**, **Classic Japanese children’s manga-animation**, **Japanese gag-reaction manga-animation**, **Modern color rubber-hose tech cartoon**, **Traditional Chinese baimiao realistic lianhuanhua**, **Pen-and-ink realistic lianhuanhua**, **Gongbi line-and-color realistic lianhuanhua**, **Woodcut-print realistic lianhuanhua**, **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration**, **Mianzhu woodblock New Year picture**, **Chinese shadow puppetry**, **Rule-Bound Crude Doodle / 规则化粗糙涂鸦**, **Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事** (candidate revision 2; not yet production-approved), or custom. The 18 bold styles are production presets; Freehand Ink-Wash Technical Narrative is a selectable candidate under independent validation; `custom` is an input option, not a production preset. Every named rendering preset is a locked component of the IP visual system, not a freely switchable per-article filter; when selected, read its matching preset under `references`.
6. Primary scenes: article covers, article inline illustrations, social posts, slides, video covers, course assets. **Rule-Bound Crude Doodle / 规则化粗糙涂鸦** is production-approved; **Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事** is a revision-2 candidate and must not be called production-approved before its own visual QA.

When a named rendering preset is selected, first read `references/ip/styles/style-selection.md`, then the matching family guide and preset file. Examples: Chinese nostalgic styles route through `lianhuanhua-style-selection.md`; Japanese manga / animation styles route through `japanese-manga-style-selection.md`; quirky cartoon styles route through `quirky-cartoon-style-selection.md`; Rule-Bound Crude Doodle routes through `rule-bound-crude-doodle-style-selection.md`.

## Visual Master Gate

Do not use fixed numbered gate fields. Decide gates by whether the missing information would materially change visual master directions.

The minimum information needed before Visual Master Directions is:

- Character subject: what the IP visually is, such as a person, animal, object, mascot, or abstract figure.
- Content domain: what the IP repeatedly explains or represents.
- Visual style: the rendering family, such as 2D editorial illustration, hand-drawn sketch, 3D toy, clay, comic, or semi-realistic illustration.
- Primary scenes: where the IP will be used first, because cover-first, inline-illustration-first, video-first, and social-card-first IPs need different visual strategies.

These fields are usually required but may be inferred and confirmed in the pre-visual-master summary:

- IP type: affects posture, authority, expression, and props.
- Audience: affects tone, complexity, and polish.
- Personality: affects facial expression, gesture vocabulary, color, and shape language.

If character subject, content domain, visual style, or primary scenes are missing or ambiguous, ask follow-up questions before Visual Master Directions. If IP type, audience, or personality are only lightly ambiguous, infer them, label them as inferred, and ask the user to confirm in the summary.

## Gap Analysis

After receiving the brief:

1. Extract all six required decisions plus character subject.
2. Mark each field as confirmed, inferred, ambiguous, or missing.
3. Determine whether any visual-master gate field is missing or ambiguous.
4. Ask exactly one follow-up question for the most important blocking gap.
5. Prefer options. Add "or describe your own answer" when the options may not fit.

Follow-up priority:

1. Character subject.
2. Content domain.
3. Visual style.
4. Primary scenes.
5. IP type.
6. Audience.
7. Personality.

## One-Question Rule

Ask only one question per turn unless the user explicitly asks to speed through setup.

Good:

```text
I need to confirm the visual style before creating visual master directions. Which direction fits best?
A. Clean 2D editorial illustration
B. Hand-drawn sketch style
C. Soft 3D toy style
D. Comic style
Or describe your own style.
```

Avoid:

```text
Please answer IP type, audience, content domain, personality, visual style, and primary scenes.
```

## Pre-Visual-Master Summary

Before generating visual master directions, summarize the collected decisions and ask for confirmation.

Use this shape in the user's language:

```text
Here is the IP creation brief I have collected:

- Character subject: [...]
- IP type: [...]
- Audience: [...]
- Content domain: [...]
- Personality: [...]
- Visual style: [...]
- Primary scenes: [...]

If this is correct, I will generate 3-6 visual master directions next. If you want changes, tell me which item to adjust.
```

Proceed to Visual Master Directions only after the user confirms, or after they provide edits that make all visual-master gate fields clear.

## Inference Rules

Be willing to infer obvious fields from the user's brief, but label them as inferred in the summary.

Examples:

- "shares high-quality image generation prompts" implies content domain: prompts / AI image generation.
- "chubby hippo" confirms character subject and body direction, but not visual style.
- "like a teacher who explains clearly" implies expert or coach, but ask if the distinction matters.
- "for article covers and inline article illustrations" confirms primary scenes.

Do not infer visual style unless the user gives style words such as 2D illustration, hand-drawn, 3D, clay, comic, or similar.
