# Style Atlas: README Example Images

## Goal

Add a durable, visual style atlas to `README.md` and `README.en.md`: every production rendering style gets one comparable, locally versioned example image under `examples/style-atlas/`.

The atlas must help a reader select a style from actual visual evidence, not only prose descriptions. It is a rendering benchmark, not an initialized production IP and not a substitute for a user’s own IP validation.

## Scope

- Include all **18 production styles**.
- Keep **Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事** out of the production atlas until its revision-2 validation is complete; list it as a clearly marked candidate without a published sample.
- Preserve the existing Chinese and English README split.
- Store prompts, output metadata, batch state, and QA notes beside the generated images so a partial run resumes without rediscovering choices.
- Add a narrow `.gitignore` exception for `examples/style-atlas/` so the intended documentation assets are versionable while other ad-hoc examples remain ignored.

## Canonical Article-Illustration Scene

**Name:** Signal Relay Recovery — annotated inline illustration

This is a complex **article inline illustration**, not a cover. One original, unbranded guide character works in a wide 16:9 scene. A visible route begins at a compact handheld source device, travels through three simple system elements, breaks at one clear fault, and is physically reconnected by the guide. A visible confirmation state closes the route.

The guide is active: detecting, tracing, reconnecting, then confirming. The scene contains five short Chinese labels as physical visual materials, not a headline or a pasted caption:

- `异常` — on the source-device alert tag;
- `追踪` — on a route flag or trace tab;
- `断点` — on the broken route’s fault tag;
- `修复` — on the guide’s active repair tag or tool label;
- `已恢复` — on the final confirmation node.

### Required semantic beats

1. Source / detection (`异常`).
2. Trace through a route and three deliberately simple system elements (`追踪`).
3. One visible break or blockage (`断点`).
4. Physical repair caused by the guide (`修复`).
5. Resolved / verification state (`已恢复`).

### Cross-style invariants

- Landscape 16:9 inline-article composition, not a cover layout.
- The five exact labels are generated as part of the scene. They must sit on physical carriers such as tags, tabs, module cards, route flags, tool labels, or node markers; no post-production overlay.
- No extra readable text, logos, watermarks, named characters, named artists, studios, or franchises.
- One original guide character; each style may translate the subject according to its own medium.
- No photorealism unless the style’s definition explicitly calls for semi-realistic treatment.
- The guide causes the repair; it cannot merely stand beside a completed diagram.
- The scene, label carriers, and causal route must remain understandable at README thumbnail scale.

### Why this scene

It demonstrates what users actually need from an article illustration: a complex explanatory scene that combines IP action, route/structure, short in-context Chinese labels, state change, and rendering-style differentiation. It maps naturally to Chinese narrative styles, cartoons, 3D/clay/pixel systems, and the rough-doodle system without forcing them to imitate one another.

**Selected direction:** C — 三个节点，各有职责，接力完成修复 (approved for the first atlas batch on 2026-07-15).

**Exact integrated labels:** `发现`, `定位`, `断点`, `接回`, `验证`.

The guide moves along a shallow diagonal relay route linking three distinct work stations. It carries the repair object, physically reconnects the central break, and visibly completes the chain. The five labels must appear on physical carriers: first-station tag, second-station tab, central broken-link marker, repair-object tag, and final-station plate. This is a complex inline article illustration — no headline, no local overlay, and no additional text.

## Scene Approval Gate

The scene gate is satisfied for **Direction C**. Generate only the selected first-batch styles — flat illustration, semi-realistic illustration, and 3D toy — before requesting user visual review. Do not begin the remaining 15 production styles until that review passes.

## Asset Layout

```text
examples/style-atlas/
  README.md                         # scope, scene contract, regeneration instructions
  manifest.json                     # all 18 style ids, status, filenames, prompts
  batch-status.md                   # append-only execution / retry record
  prompts/
    01-flat-illustration.md
    ...
  images/
    01-flat-illustration-v1.png
    ...
  qa-notes.md                       # per-image visual and technical checks
```

## README Table Contract

Both READMEs get a `Style Atlas / 风格示例图谱` section after the style-selection introduction.

Production row columns:

| Preview | Style | Best for | Boundary |

- `Preview` links to `examples/style-atlas/images/<slug>-v1.png`.
- Chinese and English use their own localized row descriptions but exactly the same image paths and style order.
- Candidate styles use a clearly labeled text row with no thumbnail until independently validated; they must never appear visually equivalent to production presets.

## Batches

Generate and review in these resumable batches, stopping after each batch for technical checks and a visual contact sheet:

1. **Basic systems (6):** flat illustration, semi-realistic illustration, 3D toy, clay, comic, pixel art.
2. **Modern / cartoon systems (5):** hand-drawn technical sketch, classic Japanese children’s manga-animation, Japanese gag-reaction manga-animation, modern color rubber-hose tech cartoon, Rule-Bound Crude Doodle.
3. **Chinese narrative systems A (4):** traditional Chinese baimiao realistic lianhuanhua, pen-and-ink realistic lianhuanhua, gongbi line-and-color realistic lianhuanhua, woodcut-print realistic lianhuanhua.
4. **Chinese narrative systems B (3):** late-20th-century Chinese realistic watercolor-and-gouache textbook illustration, Mianzhu woodblock New Year picture, Chinese shadow puppetry.

## Generation / QA Rules

- Use text-to-image for the atlas. The atlas demonstrates rendering systems, not cross-image identity stability, so it must not be blocked by the current image-to-image upstream timeout path.
- Generate each image as a single subject/scenario prompt; do not create multi-region sheets.
- Generate at most three independent images concurrently. If an upstream timeout occurs, record it in `batch-status.md`, retry only after changing a meaningful variable, and do not silently substitute a synthetic asset.
- For each successful asset: verify PNG decode, dimensions, RGB mode, filename, and prompt archive.
- Visual review checks: scene causality, style-family differentiation, active guide, no named-work imitation, no readable garbage text, and thumbnail legibility.
- Do not mark candidate styles production-approved merely because an atlas attempt exists.

## README Update Gate

Only add a production row after its image exists and decodes. A batch may be published incrementally, but rows must not use placeholders that pretend an image was generated.
