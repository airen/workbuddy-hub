# Lao Zhang Personal IP Illustration System

> A Hermes Skill for building a stable, reusable visual identity for a personal IP and applying it to article covers, in-article scene illustrations, and Xiaohongshu / Little Red Book card carousels.

[中文文档](README.md)

## Overview

One-off illustrations can look attractive but rarely become a durable, recognizable personal brand. This project packages visual identity definition, action design, prompt discipline, image generation, and output-specific production workflows into a reusable skill.

It is built around four ideas:

- **Build the IP before scaling content.** Lock identity, signature clothing and props, palette, rendering language, and variation boundaries.
- **Make the IP part of the narrative.** The character must explain, break down, diagnose, repair, build, or guide—not merely decorate a composition.
- **Use specialized workflows for different outputs.** Covers, inline illustrations, and Xiaohongshu cards serve different communication goals.
- **Keep work reproducible.** Prompts, plans, generated images, and QA notes are retained for each run so work can be reviewed, reused, and iterated.

The repository currently includes one example project IP: `wenren-agent`.

## Capabilities

| Use case | Main deliverables |
| --- | --- |
| Create or revise a personal IP | IP profile, visual specification, prompt pack, action library, primary visual reference |
| Article / social cover | Cover brief, multiple directions, final prompt, cover image, QA |
| In-article scene illustration | Content analysis, shot list, per-image prompts, images, QA |
| Xiaohongshu / carousel cards | Post brief, series visual system, card plan, card images, QA |
| Bitmap image generation | Tool selection, reference-image constraints, archiving, technical verification |

## Install and use

### Install in Hermes

Use the slash command in a Hermes conversation:

```text
/learn
```

Then select or import the `lz-ip-illustration` skill from this project to install it into the active Hermes profile. Start a fresh session or reload the skill after installation before using it.

### Choose a task entry point

- **Create a new personal IP:** start from a natural-language brief, then complete the interview, visual-direction exploration, and identity locking.
- **Create an article cover:** derive a communication proposition and visual hook from a title, summary, outline, or full article.
- **Create inline article illustrations:** extract high-value cognitive anchors and convert them into action-led scenes.
- **Create Xiaohongshu cards:** turn an article or topic into a phone-first card sequence with a clear swipe rhythm.

The skill checks for a usable current-project IP first. If none exists, it enters the IP-creation flow rather than silently using example assets.

## Workflow overview

```text
User request
   │
   ▼
Inspect / select an existing IP
   │
   ├─ No IP ──► brief-first interview ──► visual-master directions
   │                                      │
   │                                      ▼
   │                              refinement and identity locking
   │                                      │
   │                                      ▼
   │                                persist IP assets
   │
   └─ Existing IP ─► choose cover / article scenes / Xiaohongshu cards
                              │
                              ▼
                 plan directions, shot list, or card plan
                              │
                              ▼
                   save prompts → generate → QA → archive
```

## Core principles

1. **Identity stability comes first.** Face, body proportions, signature clothes, key props, palette, and rendering must not drift from scene to scene.
2. **The IP must cause a change.** If removing the character leaves the core meaning intact, the scene fails.
3. **One image serves one cognitive anchor.** Do not compress every concept in an article into a single scene.
4. **A cover is not an inline illustration.** It needs an accurate communication promise, thumbnail readability, a visual hook, and title-safe space.
5. **Cards are not sliced covers.** Each card needs its own reading beat and one clear visual anchor.
6. **Save prompts before generation.** Prompts are reproducibility records; regenerate with versioned filenames rather than silently overwriting assets.

## Rendering presets

Every rendering preset is a **locked visual system**, not an interchangeable one-off filter. Once selected, it should be fixed in the IP visual specification and prompt pack, and downstream scenes should be constrained by an accepted visual-master reference.

### Independently Validated Production Presets

The skill provides multiple **independently validated** production presets across Chinese nostalgic narrative, Japanese manga/animation, quirky-cartoon, and modern explanatory/doodle families. Each has a defined visual boundary and can serve as a long-term IP rendering system; do not switch them casually between articles. The authoritative router is [`references/ip/styles/style-selection.md`](references/ip/styles/style-selection.md). **Hand-drawn sketchnote technical draft and Rule-Bound Crude Doodle are modern styles, not Chinese nostalgic styles.**

`custom` is not a production preset. It is only an input option for collecting a user’s custom direction. A custom direction must define its visual boundaries, pass independent validation, and receive approval before it becomes a new locked rendering system.

### Article Illustration Style Atlas (reviewed examples)

The examples below share one complex inline-article scene: **three stations, one repair relay**. A guide moves along a relay path through three work stations, discovers a problem, isolates the fault, reconnects the broken route, and verifies recovery. The short Chinese labels `发现`, `定位`, `断点`, `接回`, and `验证` are generated on physical scene carriers, not added as a post-production overlay or cover title.

| Preview | Style | Status | What this article illustration demonstrates | Boundary |
| --- | --- | --- | --- | --- |
| <img src="examples/style-atlas/images/01-flat-illustration-annotated-v2.png" width="260" alt="Flat illustration: three-station relay repair inline article illustration"> | **Flat illustration** | Production-ready · example reviewed | Compresses a multi-node causal chain into a high-information, quick-to-scan explanatory illustration using clear shapes, routes, and physical labels | Do not turn it into a SaaS dashboard or reduce the IP to an icon |
| <img src="examples/style-atlas/images/02-semi-realistic-illustration-annotated-v2.png" width="260" alt="Semi-realistic illustration: three-station relay repair inline article illustration"> | **Semi-realistic illustration** | Production-ready · example reviewed | Uses credible figure, hand action, space, and material to show who repairs what and how the recovery happens | Do not drift into photo realism, game concept art, or cinematic spectacle |
| <img src="examples/style-atlas/images/03-3d-toy-annotated-v2.png" width="260" alt="3D toy: three-station relay repair inline article illustration"> | **3D toy** | Production-ready · example reviewed | Uses tactile work stations and dimensional action to make a complex route friendly, lightweight, and spatially legible | Do not become a static cute figurine or an empty product shot |
| <img src="examples/style-atlas/images/07-hand-drawn-technical-sketch-annotated-v1.png" width="260" alt="Hand-drawn technical sketch: three-station relay repair inline article illustration"> | **Hand-drawn technical sketch** | Production-ready · example reviewed | Organizes three stations, a relay route, and short physical labels into a visible paper-based reasoning process | Do not become a dense whiteboard, neat vector infographic, or random scribble |
| <img src="examples/style-atlas/images/08-classic-japanese-childrens-manga-animation-annotated-v1.png" width="260" alt="Classic Japanese children’s manga-animation: three-station relay repair inline article illustration"> | **Classic Japanese children’s manga-animation** | Production-ready · example reviewed | Uses a clean friendly action path and short causal beats to explain a multi-node repair process | Never imitate a specific animation, character, or studio; avoid glossy anime and passive characters |
| <img src="examples/style-atlas/images/09-japanese-gag-reaction-manga-animation-annotated-v1.png" width="260" alt="Japanese gag-reaction manga-animation: three-station relay repair inline article illustration"> | **Japanese gag-reaction manga-animation** | Production-ready · example reviewed | Uses shock, focus, repair, and relief beats to make a complex diagnosis memorable and readable | Do not become an emoji sticker sheet, dense manga page, or funny face with no technical action |
| <img src="examples/style-atlas/images/04-clay-annotated-v2.png" width="260" alt="Clay: three-station relay repair inline article illustration"> | **Clay** | Production-ready · example reviewed | Uses handmade volume, tactile work stations, and readable labels to make complex relay repair warm and spatial | Do not drift into plastic 3D, intricate miniature display, or a passive mascot |
| <img src="examples/style-atlas/images/05-comic-annotated-v2.png" width="260" alt="Comic: three-station relay repair inline article illustration"> | **Comic** | Production-ready · example reviewed | Uses rhythmic action, routes, and short physical labels to tell a compact multi-node fault-to-repair visual narrative | Do not become a dense panel page, dialogue page, or imitation of a specific comic |
| <img src="examples/style-atlas/images/06-pixel-art-annotated-v2.png" width="260" alt="Pixel art: three-station relay repair inline article illustration"> | **Pixel art** | Production-ready · example reviewed | Uses pixel routes, state nodes, and pixel-label carriers to show an interactive system recovery process | Do not hide action or text in blurry low resolution or imitate a named game |
| <img src="examples/style-atlas/images/10-modern-color-rubber-hose-tech-cartoon-annotated-v1.png" width="260" alt="Modern color rubber-hose tech cartoon: three-station relay repair inline article illustration"> | **Modern color rubber-hose tech cartoon** | Production-ready · example reviewed | Uses elastic limbs to make the physical act of pulling a broken route straight and reconnecting it intuitive and lively | Elastic action must explain failure and recovery, not become vintage-cartoon imitation |
| <img src="examples/style-atlas/images/11-rule-bound-crude-doodle-annotated-v2.png" width="260" alt="Rule-Bound Crude Doodle: three-station relay repair inline article illustration"> | **Rule-Bound Crude Doodle** | Production-ready · example reviewed | Uses minimum necessary marks, rough action hands, and physical labels to compress complex causality into an instantly readable sketch | Do not turn a detailed illustration into thick lines; delete details that do not change meaning |
| <img src="examples/style-atlas/images/12-traditional-chinese-baimiao-realistic-lianhuanhua-annotated-v1.png" width="260" alt="Traditional Chinese baimiao realistic lianhuanhua: three-station relay repair inline article illustration"> | **Traditional Chinese baimiao realistic lianhuanhua** | Production-ready · example reviewed | Uses restrained ink contour, hand gesture, and paper reserve to turn repair into an airy readable horizontal narrative | Do not drift into freehand ink wash, manga, or color-dependent identity |
| <img src="examples/style-atlas/images/13-pen-and-ink-realistic-lianhuanhua-annotated-v1.png" width="260" alt="Pen-and-ink realistic lianhuanhua: three-station relay repair inline article illustration"> | **Pen-and-ink realistic lianhuanhua** | Production-ready · example reviewed | Uses pen contour, hatching, and clear spatial hierarchy for structured diagnosis and repair | Do not become messy sketching, smooth grayscale, or a text-dense diagram |
| <img src="examples/style-atlas/images/14-gongbi-line-and-color-realistic-lianhuanhua-annotated-v1.png" width="260" alt="Gongbi line-and-color realistic lianhuanhua: three-station relay repair inline article illustration"> | **Gongbi line-and-color realistic lianhuanhua** | Production-ready · example reviewed | Uses precise line, restrained color, and stable order to express multi-node coordination and state change | Do not let thick paint, gold-red ornament, or fantasy aesthetics bury the repair causality |
| <img src="examples/style-atlas/images/15-woodcut-print-realistic-lianhuanhua-annotated-v1.png" width="260" alt="Woodcut-print realistic lianhuanhua: three-station relay repair inline article illustration"> | **Woodcut-print realistic lianhuanhua** | Production-ready · example reviewed | Uses black-white masses and directional carving marks to strengthen breaks, reconnection, routes, and action tension | Not a propaganda poster, rough stamp, or texture in place of readable action |
| <img src="examples/style-atlas/images/16-late-20th-century-chinese-realistic-watercolor-gouache-textbook-annotated-v1.png" width="260" alt="Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration: three-station relay repair inline article illustration"> | **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration** | Production-ready · example reviewed | Uses natural light, everyday objects, and instructional warmth to explain human-scale repair | Do not replace causality with nostalgia filtering, prop clutter, or cartoon treatment |
| <img src="examples/style-atlas/images/17-mianzhu-woodblock-new-year-picture-annotated-v1.png" width="260" alt="Mianzhu woodblock New Year picture: three-station relay repair inline article illustration"> | **Mianzhu woodblock New Year picture** | Production-ready · example reviewed | Uses printed line-blocks and hand color to make reconnection and recovery a complete, lively folk narrative | Not a red-gold ad, generic guochao, or static mascot display |
| <img src="examples/style-atlas/images/18-freehand-ink-wash-technical-narrative-annotated-v1.png" width="260" alt="Freehand Ink-Wash Technical Narrative: three-station relay repair inline article illustration"> | **Freehand Ink-Wash Technical Narrative** | Production-ready · example reviewed | Uses one route spine, brush hierarchy, scale shifts, and functional transparent color to carry complex technical narrative | Brush-and-ink serves route, fault, repair, and verification; never reduce it to a vague mood image |

All 18 production-style examples are now included under the same scene contract. Candidate presets appear here only after independent validation and approval.

### Independently Validated Production Presets

| Preset | Visual language | Best for | Boundary |
| --- | --- | --- | --- |
| **Traditional Chinese baimiao realistic lianhuanhua** | Fine monochrome ink contours, restrained hatching, paper reserve, and narrative framing; airy and line-led | Principle explanation, thoughtful characters, calm technical instruction, culturally grounded content | Not freehand ink wash, manga, or generic “retro Chinese style”; IP recognition cannot depend on color |
| **Pen-and-ink realistic lianhuanhua** | Crisp pen contours with hatching, cross-hatching, and stippling; stronger black-and-white structure | Tools, assembly, diagnosis, breakdowns, workflows, and technical structure | More structural and explicit in tone than baimiao; must not become messy sketching or digital grayscale |
| **Gongbi line-and-color realistic lianhuanhua** | Precise outlines containing restrained layered color; orderly, luminous, and detailed | Precise systems, culture-meets-technology concepts, and IPs needing stable color identity | Not heavy “Chinese fantasy,” game concept art, or thick painting; outlines must remain visible and ornament must not dominate information |
| **Woodcut-print realistic lianhuanhua** | Strong black-white masses, directional carving marks, tactile texture, bold silhouette | Connections, breaks, repair, routes, turning points, and high-energy action | Not propaganda poster art, political poster language, or rough stamp texture; faces, hands, and action must stay readable |
| **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration** | Low-saturation watercolor washes with selective gouache, gentle daylight, life observation, and educational warmth | Children, family, school, community, nature, and approachable teaching | This is textbook illustration rather than lianhuanhua; avoid yellowed filters, nostalgia-prop clutter, flat cartoons, and commercial-poster treatment |
| **Mianzhu woodblock New Year picture** | Deep ink line-block contours plus hand-painted color; bright but harmonious folk palette and balanced festive composition | Welcome, renewal, milestones, promises, shared values, celebrations, and auspicious transformation | Not a red-and-gold New Year advertisement, generic guochao, vector paper-cut, or another regional New Year-picture tradition; gold is a local accent only |
| **Chinese shadow puppetry** | Carved and pierced jointed figures on a backlit screen, controlled profile/three-quarter silhouettes, shallow stage space | Reveal, connection, transformation, guidance, and material cause-and-effect | Not paper-cut, flat red silhouette, or generic guochao; the stage action must show the IP causing the change |

#### Other modern and cartoon styles (selected)

| Preset | Visual language | Best for | Boundary |
| --- | --- | --- | --- |
| **Flat illustration** | Clear geometric shapes, simplified contours, limited color blocks, and strong information hierarchy | Product concepts, quick knowledge communication, diagrams, and lightweight social content | Do not turn the IP into a passive icon or pile on decorative UI |
| **Hand-drawn technical sketch** | Visible ink/pencil construction lines, paper-based reasoning traces, restrained watercolor annotations, and whitespace | Methodology, architecture, workflows, technical thinking, and diagnosis | Not careless doodling, generic retro-paper filtering, or a dense whiteboard screenshot |
| **Semi-realistic illustration** | Credible anatomy and materials, designed light, and controlled detail | Professional character presence, complex themes, and narrative covers | Avoid photorealism, game concept art, excessive cinematic lighting, or ornate materials |
| **3D toy** | Simplified toy-like volumes, soft forms, controlled materials, and spatial presence | Friendly product communication, lightweight concept demonstrations, and card visuals | Do not let plastic material overpower narrative or reduce the IP to a passive mascot |
| **Clay** | Hand-sculpted irregular volume, matte grain, and visible craft warmth | Warm, gentle, tactile explanations and family-oriented content | Not generic 3D, sticky material treatment, or cute expressions without causal action |
| **Comic** | Clear contours, rhythmic composition, expressive action, and optional panel-based storytelling | Conflict, comparison, before/after change, and short sequential explanation | Do not replicate a specific comic work, substitute dense dialogue for visual storytelling, or lose a single focal point |
| **Pixel art** | Grid-based contours, limited palettes, discrete pixel blocks, and retro-interactive feel | Gamified workflows, state changes, and tool/system metaphors | Low resolution must not hide information; keep characters, actions, and text readable at target size |
| **Classic Japanese children’s manga-animation** | Original rounded geometric character design, clean contours, controlled flat color, light cel shadows | Everyday problems, tests, comparison, sorting, and approachable technical explanation | Never imitate a named artist, studio, franchise, character, or signature prop; avoid modern glossy anime, chibi, and magical-gadget tropes |

| **Hand-drawn sketchnote technical draft** | White or light-gray paper ground, black/gray hand-drawn lines, visible draft construction marks, paper-based reasoning traces, and sparse yellow/light-blue/light-green annotations; reads as a visual note or low-fidelity infographic | Concept breakdowns, workflow comparisons, diagnosis paths, methodology cards, and knowledge posters for technical articles | Belongs to “other styles,” not nostalgic Chinese style, lianhuanhua, folk craft, or textbook nostalgia; also not careless doodling, dense whiteboard screenshots, or polished editorial illustration |
| **Rule-Bound Crude Doodle** | Thick marker, strongly uneven line weight, overshot endings, double contours, lopsided head/uneven eyes, and fixed awkward mitten hands; the crude rules stay stable while action stays clear | Independent personal-brand covers, diagnosis/repair/transformation scenes, opinion and maker-oriented content | Not polished journal doodling, sketchnote, cute cartoon, or random scribbling; must remain anti-cute and anti-polished while preserving readable identity and causality |

### Choosing a preset

- For **calm, rational, airy linework**: traditional baimiao realistic lianhuanhua.
- For **technical structure, breakdown, and diagnosis**: pen-and-ink realistic lianhuanhua.
- For **meticulous order and stable color identity**: gongbi line-and-color realistic lianhuanhua.
- For **force, recovery, turning points, and strong narrative silhouettes**: woodcut-print realistic lianhuanhua.
- For **warm, everyday, approachable educational scenes**: realistic watercolor-and-gouache textbook illustration.
- For **celebration, renewal, promise, and folk vitality**: Mianzhu woodblock New Year picture.
- For **stage-like causality, revelation, and traditional craft materiality**: Chinese shadow puppetry.
- For **clear, efficient, diagrammatic knowledge communication**: flat illustration.
- For **visible reasoning, technical methodology, and paper-based thought processes**: hand-drawn technical sketch.
- For **white-ground sketchnotes, low-fidelity infographics, and rough-draft knowledge posters**: hand-drawn sketchnote technical draft.
- For **professional narrative, credible characters, and richer material/spatial presence**: semi-realistic illustration.
- For **friendly, lightweight, dimensional product or concept communication**: 3D toy.
- For **warm handmade tactility and gentle emotion**: clay.
- For **conflict, change, or a short sequential narrative**: comic.
- For **gamified states and retro-interactive metaphors**: pixel art.
- For **lightweight, direct everyday problem → action → outcome storytelling**: classic Japanese children’s manga-animation.
- For a **rough, independent, anti-polished visual voice with instantly readable action and causality**: Rule-Bound Crude Doodle.

A new preset must be validated independently. A related preset passing validation does not make a new rendering system production-ready.

## Project contents

- [`SKILL.md`](SKILL.md): main skill entry point, routing, and cross-workflow rules.
- [`references/`](references/): IP creation, covers, article scenes, Xiaohongshu cards, and image-generation workflows.
- [`templates/`](templates/): reusable templates for IP assets, covers, shot lists, and social cards.
- [`examples/`](examples/): example IP and runs, for structure and writing reference only.
- [`ip-assets/`](ip-assets/): actual generated and accepted IP assets and outputs in this project.

## Version

Current skill version: `0.3.18` (see the `version` field in the [`SKILL.md`](SKILL.md) frontmatter).

### Recent updates

- `0.3.18`: Added and independently validated **Rule-Bound Crude Doodle**. Its stable grammar is thick marker work, overshot endings, double contours, lopsided/uneven eyes, awkward mitten hands, and inconsistent limbs: anti-cute and anti-polished, while preserving immediately readable action and causality. The original Direction 09 anchor and cross-topic validation assets are retained; the earlier, overly polished Freeform Doodle validation record is marked as a superseded adjacent direction.
- `0.3.14`: Reorganized style-family routing into Chinese nostalgic, Japanese manga/animation, and quirky-cartoon families; added and independently validated Japanese gag-reaction manga-animation and modern color rubber-hose tech cartoon. Downstream image-to-image generation now preserves the original PNG and uses an optimized 1024px-long-edge JPEG reference at quality 85 by default to reduce reference payload.
- `0.3.11`: Moved the version into Hermes-standard frontmatter; strengthened the inline-illustration rule of one core structure plus one primary IP action per single-scene image.
- `0.3.10`: Unified text handling across covers, inline illustrations, and Xiaohongshu cards; local text overlay is forbidden and text must be generated as part of the visual composition.
- `0.3.9`: Added Xiaohongshu card content-density, IP-role, and IP-scale rules.
