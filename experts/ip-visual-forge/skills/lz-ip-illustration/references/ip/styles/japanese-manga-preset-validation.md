# Japanese Manga / Animation Preset Validation Protocol

Use this protocol to validate a newly added locked Japanese manga / animation rendering preset before calling it production-ready.

## Scope

A rendering preset is independently validated. Passing a different Japanese manga preset does not validate this one, especially when the expression grammar, deformation range, or article role differs.

Current validated test shape:

1. **Visual master** — creates the reusable character identity and tests silhouette, feature grammar, clothing/prop shapes, palette roles, and line/color treatment.
2. **Expression or action vocabulary** — required when the preset depends on reusable reactions or special body acting.
3. **Explanation scene** — tests whether the IP actively makes one technical relationship understandable.
4. **Diagnosis / repair scene** — tests whether the IP can inspect, manipulate, and visibly transform a failed workflow.

## Test-IP Selection

Choose a character whose physical vocabulary stresses the target rendering style.

- For **Classic Japanese children’s manga-animation**, prefer a friendly explainer, practical operator, diagnostician, coach, or companion who can make a small everyday problem and visible solution legible through hands, posture, and one recurring practical prop. Define the original rounded silhouette, feature grammar, main/secondary garment colors, dark contour, warm action accent, cool balance accent, skin range, and controlled flat-fill/cel-shadow relationship. Test clean contour stability, article-size causal readability, low-detail expressive posture, and original-character separation from named franchises, generic modern anime, chibi/kawaii mascot design, manga-page conventions, or glossy digital art.
- For **Japanese gag-reaction manga-animation**, prefer a funny diagnostician, tester, operator, or self-mocking technical companion whose identity can survive exaggerated reactions. Define the original rounded silhouette, feature grammar, main/secondary garment colors, dark contour, reaction accent, action-result accent, skin range, allowed squash-and-stretch deformation, and reusable reaction symbols. Test an 8-expression sheet before article scenes: normal explaining, shock, panic/scramble, speechless/deadpan, smug small win, defeated by bug, refocus/recover, and relieved after fix. Then test one explanation scene and one diagnosis/repair/recovery scene where the gag clarifies a real technical failure mode instead of becoming a decorative funny face.

Treat the generated character as a temporary test IP unless the user separately approves it as a production IP.

## Required Records

Before generating, save:

- test brief with role, audience, and identity anchors;
- visual-master prompt beside the reference image path;
- expression/action-vocabulary prompt when required by the preset;
- one prompt per article scene beside its target output path;
- QA handoff record beside the run.

After each successful generation:

- copy accepted output from the image cache to the defined validation run directory;
- verify that the saved PNG decodes and that visual-master and article-scene formats match intended portrait/landscape roles where possible;
- preserve the original visual-master PNG, then create an optimized downstream reference when practical: long edge 1024px, JPEG quality 85, saved under `reference-images/optimized/`;
- use the optimized visual master as the image-to-image identity reference for downstream scenes when supported, while keeping the original PNG as the archive source.

## Human Acceptance Gate

Do not claim a style preset has passed visual QA without human inspection. Ask for review against:

- identity stability across visual master, expression/action vocabulary, and scenes;
- target style differentiation from adjacent Japanese styles;
- article-size legibility and causal readability;
- action necessity: the IP must cause the explanatory transformation rather than decorate an already-complete diagram;
- for gag styles: reaction strength, reaction reuse, and whether the funny expression supports diagnosis/action/result.

When the user approves, record the result as a passed preset test while keeping the test IP temporary unless separately approved.
