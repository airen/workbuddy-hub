# Japanese Manga / Animation Rendering Presets: Selection and Validation

Use this guide only for **Japanese manga / animation style families** in reusable IP systems. These styles are parallel to Chinese nostalgic styles, not subtypes of lianhuanhua.

For the global style index, read `references/ip/styles/style-selection.md`.
For Chinese nostalgic styles, read `references/ip/styles/lianhuanhua-style-selection.md`.

A rendering preset is a **locked component of the IP visual system**, not an article-by-article filter. Do not imitate named artists, studios, series, characters, props, logos, or franchises.

## Rendering Families

- **Classic Japanese children’s manga-animation family**: original-character, rounded, everyday causal storytelling with clean contour lines and controlled flat color; never a named-franchise imitation or generic modern anime.
- **Japanese gag-reaction manga-animation family**: original-character comic reaction system for exaggerated expressions, elastic body acting, failed attempts, diagnosis, and recovery beats; never a named-franchise imitation, generic anime, emoji sticker sheet, or noisy manga page. When the user asks for 小众、诙谐、搞怪、夸张表情, also read `references/ip/styles/gag-style-candidate-research.md` before proposing or adding styles.

## Available Presets

| Preset | Best-fit IP role and article work | Identity locks | Do not confuse with |
|---|---|---|---|
| Classic Japanese children’s manga-animation | Friendly explainer, operator, diagnostician, coach, or companion; everyday problem solving, tool experiments, workflow explanation, before/after change | original rounded silhouette, face-feature grammar, signature practical prop, stable palette roles, clean contour plus controlled flat-color/cel-shadow relationship, short causal reading path | named-franchise imitation, generic modern anime, chibi/kawaii mascot, manga page, glossy digital illustration, or passive figure beside icons |
| Japanese gag-reaction manga-animation | Funny diagnostician, tester, operator, or self-mocking technical companion; bug panic, prompt backfire, tool-chain confusion, failed attempts, repair recovery, and visible relief | original rounded silhouette, stable reaction vocabulary, signature prop, palette roles, allowed squash-and-stretch range, clean contour plus flat color, 8-expression reaction sheet | named-franchise imitation, generic modern anime, emoji sticker sheet, chibi mascot-only pose, noisy manga page, glossy anime, or passive funny face without technical action |

## Preset-Specific Test Pattern

Every new Japanese manga / animation preset must pass independently. Do not reuse another preset's reference image, prompt block, or acceptance result.

General validation shape:

1. Create an independent temporary IP selected to stress the preset's strengths.
2. Generate one portrait visual master and archive its prompt beside it.
3. Use that master as an image-to-image identity reference for two landscape article scenes:
   - one orchestration / explanation scene;
   - one diagnosis / repair / transformation scene.
4. Archive all prompts, images, dimensions, and a `qa-notes.md` record.
5. Require human visual approval before marking the preset passed.
6. Keep the test IP temporary unless the user separately approves it as a production IP.

For **Japanese gag-reaction manga-animation**, add one required expression-sheet validation between the visual master and landscape scenes: 8 reactions covering normal explaining, shock, panic, speechless/deadpan, smug small win, defeated by bug, refocus/recover, and relieved after fix.

## Tested Pairings

- Classic Japanese children’s manga-animation: Route Tester sorting route cards into one next step and repairing a loose tabletop route connection; human visual QA approved on 2026-07-11. Test IP remains temporary.
- Japanese gag-reaction manga-animation: Bug Panic Mechanic testing exaggerated reactions, prompt backfire recovery, and loose connector repair; human visual QA approved on 2026-07-13. Test IP remains temporary. Validation archive: `references/ip/styles/validation-runs/japanese-gag-reaction-manga-animation-20260713/`.

These pairings demonstrate useful stress tests; they are not mandatory character choices for future production IPs.
