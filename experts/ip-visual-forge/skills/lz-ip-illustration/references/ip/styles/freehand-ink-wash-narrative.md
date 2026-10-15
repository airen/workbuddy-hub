# Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事

**Production-approved preset — revision 2.** This is a locked rendering system for reusable IP systems. It replaces the earlier single-event, near-monochrome “freehand ink-wash narrative” framing because that framing drifted away from the approved engineering-narrative anchors: Direction 06 **Signal-Path Poster** and Direction 08 **Loose Technical Strip**. The v1 validation images remain archived as superseded exploration.

## Intent and Boundary

Use this preset for technical article illustrations that make a causal workflow visible through expressive Chinese brush-and-ink rendering: failure → trace → diagnosis → reconnection → verification. The image may be rich, sequential, and system-like. “写意” controls how the visual system is rendered; it must not erase its technical narrative skeleton.

The target is:

> Preserve a strong signal-path composition and continuous action grammar; render the path, modules, failure, repair, and verification through purposeful brushwork, ink value, translucent color pools, and directed paper reserve.

It belongs to the Chinese nostalgic narrative family, while remaining distinct from:

- **Baimiao and pen-and-ink realistic lianhuanhua**: line construction and observed tonal modeling are primary there; here, brush energy, ink value, translucent color pools, and route motion share the structural load.
- **Gongbi**: no uniformly fine contour, enclosed decorative fill, or meticulous ornamental accumulation.
- **Watercolor-and-gouache textbook illustration**: no life-observed soft painting or broad opaque color modeling.
- **Woodcut and New Year picture**: no carved mass grammar, print hierarchy, festive symmetry, or folk-poster palette.
- **Chinese shadow puppetry**: no articulated cutout silhouette or backlit screen grammar.
- **Generic “Chinese style” / fantasy concept art**: no palace fantasy, misty mountain stock background, costume spectacle, calligraphy wallpaper, or ornamental seal decoration detached from the workflow.
- **SaaS infographic**: no neat dashboard grid, uniform icons, polished vector arrows, or data-card density.

## Narrative Grammar (Locked)

Choose one of two reusable compositional modes. Never collapse both into unrelated decorative vignettes.

### A. Signal-Path Poster

- One bold, looping or curving **flow/signal path** crosses the wide canvas and is the composition spine.
- It connects the selected IP’s source prop or source module, a compact system core, one small sharp fault/blockage marker, an active physical repair, and a resolved/verified node.
- The IP moves along, interrupts, or physically reconnects this path; the route must not read as a background ornament.
- Use 2–3 translucent color roles defined in the IP visual spec and large but directed negative space. The result is a handmade technical poster, not an infographic.

### B. Loose Technical Strip

- One unbordered continuous left-to-right or diagonal scene carries 3–4 linked action beats. It is not a comic grid.
- The IP can recur along the path at changing scale: catches the failure, follows the trace, crawls/leans into the system to repair, then verifies.
- Let the route and one or two enlarged props bridge the beats. Use spatial compression/expansion rather than panel borders.
- The image must read as one energized technical strip, not a collage or a sequence of isolated illustrations.

## Visual Language

- **Medium**: contemporary Chinese xieyi brush-and-ink technical storytelling on warm rice-paper or xuan-paper-like ground.
- **Brush and line**: thick-to-fine ink contour for the IP, tools, and important modules; loaded brush for route momentum; dry-brush breaks and fly-white only where they communicate direction, force, or material. Do not dissolve crucial paths into atmospheric wash.
- **Ink structure**: decisive near-black anchors for character, repair point, and system core; middle-gray brush bridges for the signal route and operational relationships; pale wash only as secondary environmental support; deliberate reserve around the cognitive focal action.
- **Functional palette**: fixed and sparse per IP, but not monochrome. Define three repeatable roles in that IP’s visual spec:
  - flow/path: trace, call path, system flow;
  - fault/blockage: defect, break, blocked handoff;
  - resolved/verified: restoration or confirmed handoff.
  The specific hues belong to the IP. Use no more than these roles plus that IP’s natural skin/clothing/material neutrals. Do not let accent colors become decorative confetti.
- **Figures and props**: preserve the selected IP’s own identifiable anatomy/shape language, pose, face, clothing or material treatment, signature props, and repair gesture. Tools and modules may be brush-simplified, but their causal relationship must remain legible. Do not prescribe another IP’s laptop, books, tools, or costume as a default.
- **Space**: asymmetrical, with one large readable field of reserve or quiet wash. Reserve directs the eye along the route; it is never blank space that severs the sequence.
- **Text**: normally none. If essential, use a short Chinese label only; never rely on generated calligraphy, poems, seals, or dense UI text.

## IP Independence and Identity Preservation

This is a rendering-and-narrative preset, not a character template. A new user may create an entirely new IP with its own subject, clothing, signature props, action vocabulary, and palette. The preset only requires that those IP-specific choices map to visible causal roles in the scene.

For every IP, lock:

1. its own head silhouette, body/shape language, and signature clothing or surface treatment;
2. its own recurring props; each must participate in trace, diagnosis, repair, handoff, or verification rather than decorate the margin;
3. its own functional color semantics: one role for flow/path, one for fault/blockage, and one for resolved/verified state;
4. its own route-interaction gesture vocabulary: trace, diagnose, intervene, reconnect, confirm;
5. stable dark-anchor placement around the character/subject and the causal repair point.

For an already initialized IP, use its approved visual master as the image reference. For a new IP, establish and approve that IP’s visual master first, then validate the preset through its own identity anchors. Record the chosen props, route-state mapping, paper ground, and color-role constraints in `visual-spec.md`. Do not borrow the validation IP’s clothing, props, or palette unless the user explicitly selects them.

## Current Revision-2 Validation Anchor (Non-Universal)

The revision-2 smoke test deliberately uses the existing **文人 Agent** and the visual richness target established by Direction 06 Signal-Path Poster and Direction 08 Loose Technical Strip:

- laptop and thread-bound *Analects* are its signature causal props;
- indigo → cinnabar → bamboo-green is its current flow → defect → verified mapping;
- failure → trace → physical reconnection → confirmation is its test workflow.

These are validation fixtures only. They prove whether the rendering grammar can preserve an established IP while supporting a rich technical narrative; they are not defaults imposed on future user IPs.

## Prompt Block

```text
Freehand ink-wash technical narrative illustration / 写意水墨技术叙事, preserve the supplied recurring IP identity exactly, including its own signature props and functional palette semantics. Wide handmade engineering narrative with one dominant path/flow spine; show a causally linked workflow of failure, trace, physical repair, and resolved verification. Contemporary Chinese xieyi brush-and-ink storytelling on warm absorbent xuan-paper-like ground: decisive near-black brush contour for the IP, its props, and system core; expressive loaded-brush route movement; dry-brush breaks and fly-white only where they show force and direction; controlled middle-gray bridges; 2–3 translucent functional color roles only — flow/path, defect/blockage, and verified restoration — using colors defined by this IP’s visual system; asymmetrical composition, directed paper reserve, technically legible modules, high article-size readability. Use either a single looping signal-path poster or an unbordered continuous loose technical strip with 3–4 linked action beats. No readable text.
```

## Negative Prompt Block

```text
Monochrome mood painting with no technical color code, generic misty ink landscape, detached abstract splashes, palace or wuxia fantasy, decorative calligraphy background, seals, poem text, ornate costume, meticulous gongbi line-and-color painting, baimiao contour drawing, pen-and-ink hatching, woodcut print, New Year picture, shadow puppet, generic guochao poster, clean SaaS infographic, polished vector arrows, dense dashboard, comic panel borders, glossy digital painting, watercolor textbook art, photorealism, 3D render, anime, passive mascot beside a completed diagram, imitation of any named artist, studio, character, or franchise.
```

## Scene Rules

- Start from a concrete technical causal chain, then choose Signal-Path Poster or Loose Technical Strip before rendering details.
- The IP must physically cause the change; its own signature props must participate in trace, diagnosis, repair, or verification rather than decorate the margin.
- Use the selected IP’s own flow/path → fault/blockage → resolved/verified state transition whenever the scene includes failure and recovery. The color assignment is defined in that IP’s visual spec, not inherited from a prior validation IP.
- Richness comes from a route, 2–4 linked beats, changing scale, one or two enlarged props, and brush hierarchy — not dense labels, UI cards, or unrelated ornaments.
- Keep one dominant route. Secondary strokes may support it but must not compete for the reading order.
- For covers, foreground the highest-tension route interruption or reconnection; for inline scenes, foreground the exact relation the paragraph needs the reader to understand.

## Candidate QA Additions

Accept a future validation set only when all are true:

- It reads as brush-and-ink **technical narrative**, not monochrome mood art, generic Chinese-style decoration, an ink landscape, gongbi, lianhuanhua, or a polished infographic.
- The selected IP remains recognizable across its visual master and article scenes through its own identity anchors and signature props.
- A viewer can trace the IP-defined flow/path, identify its fault/blockage state, see the IP physically resolve it, and find its resolved/verified state without reading text.
- Signal-Path Poster scenes have one strong route spine; Loose Technical Strip scenes have one continuous 3–4 beat action line without comic borders.
- Ink contour, gray bridge, translucent functional color, and reserve form a stable hierarchy rather than becoming muddy or decorative.
- The scene remains legible at article size and the visual complexity supports — rather than obscures — the cognitive action.
- No named artist, studio, character, franchise, or signature visual work is imitated.

Reject or revise when the palette loses state meaning, a route disappears into mist, the IP becomes a passive mascot, the sequence becomes a collage, paper reserve breaks the reading path, or “写意” reduces the technical system to a vague symbol.
