# Chinese Narrative Illustration Preset Validation Protocol

Use this protocol to validate a newly added locked Chinese narrative-illustration or traditional folk-performance rendering preset before calling it production-ready. It covers Chinese lianhuanhua, textbook illustration, region-specific traditional New Year-picture, and Chinese shadow-puppetry presets.

## Scope

A rendering preset is independently validated. Passing a different preset does not validate this one, including when both belong to Chinese narrative illustration but differ in medium, palette, or audience tone.

Current validated test shape:

1. **Visual master** — creates the reusable character identity and tests the preset-appropriate recognition system: silhouette plus light/midtone/dark mapping for black-and-white presets, or silhouette plus palette roles, color placement, and value hierarchy for color presets.
2. **Explanation scene** — tests whether the IP actively makes one technical relationship understandable.
3. **Diagnosis / repair scene** — tests whether the IP can inspect, manipulate, and visibly transform a failed workflow.

## Test-IP Selection

Choose a character whose physical vocabulary stresses the target rendering style.

- For **Traditional Chinese baimiao realistic lianhuanhua**, a restrained scholar/teacher can test calm explanation, clothing folds, and narrative clarity.
- For **Pen-and-ink realistic lianhuanhua**, prefer a technician, maintenance worker, operator, or builder. This tests tool material, workwear seams, cable/module structure, hands, working postures, hatching, cross-hatching, and white-paper reserve.
- For **Gongbi line-and-color realistic lianhuanhua**, prefer a meticulous craft engineer, organizer, designer, restorer, or similar role with precise hand actions and a small set of recurring props. Define palette roles before generation: neutral background, main garment, secondary garment, dark contour anchor, signature-prop accents, and restrained skin-tone range. Test whether fine outlines remain visible around layered color and whether the palette remains stable across all three images without becoming glossy fantasy art or ornamental costume imagery.
- For **Woodcut-print realistic lianhuanhua**, prefer a field repairer, link builder, emergency operator, or other role with an unmistakable working silhouette, clear physical connection/break/recovery actions, and signature tools. Define the black-white mass map and a no-propaganda composition guardrail before generation. Test face, hands, tools, and action readability through white reserve and ensure carved marks follow form rather than becoming generic texture.
- For **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration**, prefer a child, parent, teacher, community helper, young maker, or similar everyday role with warm life-observed gestures and approachable props. Define palette roles before generation: paper neutral, main and secondary garments, warm/cool accents, signature-prop accent, skin-tone range, and environmental support colors. Test gentle natural light, watercolor transparency, selective matte gouache, open composition, stable palette placement, and explanatory action without drifting into flat cartoon, lianhuanhua line art, glossy digital nostalgia, or a decorative memory collage.
- For **Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事**, validate with an initialized IP chosen for that test — it may be an existing approved IP or a newly created temporary test IP. Never prescribe another IP’s character, clothing, props, or colors. First lock that IP’s own signature props and its own three functional color roles: flow/path, fault/blockage, and resolved/verified state. Generate one wide **Signal-Path Poster** scene with a dominant route spine and one wide **Loose Technical Strip** scene with a continuous 3–4 beat workflow. Before promotion, verify that the supplied visual master was serialized into the provider request as an image input; then test whether the route, fault, physical repair, and verification remain readable at article size without drifting into monochrome mood ink wash, generic ink landscape, palace/wuxia fantasy, decorative calligraphy, gongbi, line-led lianhuanhua, clean SaaS infographic, or a disconnected collage. The current 文人 Agent + laptop + thread-bound *Analects* + indigo/cinnabar/bamboo-green run is one validation fixture, not a production default.
- For **Mianzhu woodblock New Year picture**, prefer an active host, maker, organizer, messenger, or celebrant with an unmistakable silhouette, a small set of practical signature props, and an action that can carry welcome, renewal, a milestone, shared value, or auspicious transformation. Define a warm paper neutral, main/secondary subject colors, deep line anchor, warm vermilion/brick-red accent, cool mineral-green/blue-green balance, skin range, environmental supports, and an optional single local gold role. Test visible deep-ink line-block contour plus hand-painted color, complete balanced hierarchy, bright-but-harmonious color, and an IP-caused action without drifting into a generic red-gold commercial poster, papercut vector art, static guardian symmetry, another regional New Year-picture tradition, or an ornamental collage.
- For **Chinese shadow puppetry**, prefer a guide, maker, operator, diagnostician, or storyteller with an unmistakable profile or three-quarter silhouette, readable articulated joints, a small set of practical signature props, and an action involving reveal, connection, sorting, repair, or transformation. Define a warm screen neutral, main/secondary translucent dyed colors, dark carved contour, warm action accent, cool balance accent, pierced-cutout motif family, and stable transmitted-light direction. Test carved perimeter plus restrained cutouts, articulated action, translucent material under backlight, shallow screen-space hierarchy, and IP-caused explanation without drifting into generic paper-cut, opaque vector silhouette, New-Year poster, generic guochao, deep-perspective theatre, or decorative puppet collage.

Treat the generated character as a temporary test IP unless the user separately approves it as a production IP.

## Required Records

Before generating, save:

- test brief with role, audience, and identity anchors;
- visual-master prompt beside the reference image path;
- one prompt per article scene beside its target output path;
- QA handoff record beside the run.

After each successful generation:

- copy accepted output from the image cache to the defined `ip-assets/<ip-slug>/` run directory;
- verify that the saved PNG decodes and that visual-master and article-scene formats match their intended portrait/landscape roles;
- use the accepted visual master as the image-to-image identity reference for downstream scenes when supported.

## Human Acceptance Gate

Do not claim a style preset has passed visual QA without human inspection. Ask for review against:

- identity stability across all three images;
- for black-and-white presets: recognition through silhouette and intentional light/midtone/dark anchors; for color presets: recognition through silhouette plus stable palette roles, color placement, and value hierarchy;
- target style differentiation from adjacent presets;
- article-size legibility, including line density and white-space hierarchy;
- action necessity: the IP must cause the explanatory transformation rather than decorate an already-complete diagram;
- scene-specific cognitive clarity.

When the user approves, record the result as a passed preset test while keeping the test IP temporary unless separately approved.
