# Hand-Drawn Sketchnote Technical Draft Preset

Use this preset only when the user explicitly selects **Hand-drawn sketchnote technical draft** / **手绘草稿信息图** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Validation Status

This preset is an **approved locked rendering preset**. It passed independent validation on 2026-07-12 with a temporary IP visual master, one explanation/orchestration scene, one diagnosis/repair scene, archived prompts/images, and human visual QA approval. Validation archive: `references/ip/styles/validation-runs/hand-drawn-sketchnote-technical-draft-20260712/`.


## Classification

This preset belongs to the **Other styles / modern explanatory styles** group. It must not be classified as a nostalgic Chinese visual system, lianhuanhua variant, folk-craft style, textbook nostalgia style, New Year picture, or shadow-puppetry style.

## Position in the IP System

This is a locked modern explanatory visual style, not an interchangeable article-level filter and not a request for messy doodles or generic whiteboard screenshots.

```text
IP visual = fixed character identity + hand-drawn sketchnote technical-draft rendering
```

Lock silhouette, head/body proportion, outfit/prop shapes, black-gray line hierarchy, accent-color placement, paper whitespace, label grammar, and action vocabulary in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as downstream identity reference after validation.

## What This Preset Is

This preset draws from hand-drawn visual notes, rough concept diagrams, low-fidelity technical infographics, and paper-based explanation sketches. It should feel like a deliberate thinking sketch captured before final polish: readable, structured, and human-made, with visible reasoning marks and enough imperfection to avoid a finished vector/poster look.

It is not casual doodling, a chaotic whiteboard dump, a retro-paper filter, pen-and-ink lianhuanhua, manga, UI wireframe screenshot, or polished editorial infographic.

## Visual Language

- **Ground:** white, off-white, or very light gray paper-like ground with generous breathing room; no heavy aged-paper filter or stained parchment effect.
- **Line:** black and gray loose-but-purposeful pencil/fineliner/marker strokes; visible construction marks, arrows, brackets, underlines, and rough diagram containers. Lines can wobble slightly but must remain readable.
- **Color:** mostly monochrome, with sparse accent annotations in warm yellow, pale blue, muted green, or soft beige. Accents highlight reasoning points, not decoration.
- **Composition:** sketchnote or low-fidelity infographic layout: compact panels, comparison blocks, route maps, callout clusters, and visible before/after or problem/action/result paths.
- **Text:** optional and minimal. Use short Chinese labels for Chinese articles; avoid paragraphs, fake UI text, English filler, or microcopy that cannot be read at article size.
- **Texture:** paper and hand pressure should be subtle; do not let grain, smudges, or scratch noise obscure the IP or explanation.

## Identity Preservation Rules

Recognition must survive despite the intentionally rough rendering:

- stable silhouette, clothing cut, and signature prop shape;
- repeated action vocabulary: sort, mark, connect, diagnose, compare, repair, annotate, route;
- stable dark/midtone/accent placement;
- consistent line density around face, hands, prop, and key action;
- predictable label and callout grammar around the IP.

## Best-Fit Use

Use for article covers or inline illustrations where the core value is visible thinking and fast comprehension:

- concept breakdowns and method cards;
- workflow, architecture, or route explanation;
- diagnosis and repair scenes;
- before/after comparison;
- tool selection or decision paths;
- knowledge posters that should feel human, provisional, and practical.

It is less suitable for emotional storytelling, premium polished branding, high-realism characters, folk/traditional craft atmosphere, or scenes where the IP needs rich material rendering.

## Base Style Prompt

```text
Hand-drawn sketchnote technical draft illustration: white paper background, loose but deliberate black and gray pencil/fineliner sketch lines, visible construction marks and reasoning traces, compact low-fidelity infographic layout, sparse yellow and pale-blue annotation accents, clear whitespace, short readable Chinese labels only when necessary, the IP actively sorting, connecting, diagnosing, marking, comparing, or repairing a concrete problem so the visual explanation is understandable at article size.
```

## Avoid

```text
careless doodle, chaotic whiteboard screenshot, dense unreadable text, fake UI paragraphs, polished vector infographic, glossy editorial illustration, retro parchment filter, sepia nostalgia filter, manga/anime, pen-and-ink lianhuanhua, cross-hatched realism, 3D render, photorealism, ornate icons, decorative gear clouds, passive mascot beside a completed diagram, excessive color, neon, heavy gradients, muddy paper texture, tiny unreadable labels.
```

## Scene Rules

- Write the action sentence before every prompt: `The IP is actively [verb] [object] so the reader understands [cognitive anchor].`
- The scene should explain one idea through one visible reasoning path; do not compress a full article into one image.
- The IP must alter the diagram: sorting cards, drawing a route, connecting nodes, marking a fault, repairing a link, comparing options, or moving a note from problem to solution.
- Use accents only on the key reasoning path, failure point, result marker, or priority decision.
- Keep labels large, sparse, and language-appropriate.
- Preserve enough whitespace around the IP and main action for article-size readability.

## Style QA Additions

Accept only when all are true:

- The image reads as deliberate hand-drawn sketchnote technical draft, not messy doodling, whiteboard dump, vector infographic, or polished illustration.
- The IP is recognisable through silhouette, clothing/prop shape, line-density placement, and repeated action vocabulary.
- One cognitive anchor is visible within three seconds: what problem is being diagnosed, what choice is being compared, or what path is being repaired.
- Text is short and readable; no dense paragraphs or fake UI copy.
- Accent colors are sparse and functional.
- The IP physically performs the reasoning action; removing it would break the explanation.

Reject or revise when the image becomes a decorative note wall, a passive character next to a finished diagram, a dense technical whiteboard, a retro paper texture effect, or a polished vector poster.
