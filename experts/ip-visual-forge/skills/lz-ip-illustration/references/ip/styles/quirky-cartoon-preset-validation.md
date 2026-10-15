# Quirky Cartoon Preset Validation Protocol

Use this protocol to validate a newly added locked quirky cartoon rendering preset before calling it production-ready.

## Scope

A rendering preset is independently validated. Passing a different humor/cartoon preset does not validate this one, especially when the body mechanics, expression grammar, deformation range, or article role differs.

Current validated test shape:

1. **Visual master** — creates the reusable character identity and tests silhouette, feature grammar, clothing/prop shapes, palette roles, and line/color treatment.
2. **Action or expression vocabulary** — required when the preset depends on reusable physical acting or reaction grammar.
3. **Explanation scene** — tests whether the IP actively makes one technical relationship understandable.
4. **Diagnosis / repair scene** — tests whether the IP can inspect, manipulate, and visibly transform a failed workflow.

## Test-IP Selection

Choose a character whose physical vocabulary stresses the target rendering style.

- For **Modern color rubber-hose tech cartoon**, prefer a funny operator, workflow untangler, bug catcher, tool-chain repairer, or cable mechanic whose identity can survive elastic limb deformation. Define the original rounded silhouette, feature grammar, main/secondary garment colors, dark contour, warm action accent, cool result accent, skin range, tube-limb deformation, and reusable elastic action symbols. Test an elastic action sheet before article scenes: neutral explaining, arm stretched to grab a loose connector, body recoiling from a bad button, tangled in cable/workflow line, pulling a knot straight, catching a small bug pest, springing back into balance, and proudly presenting a restored route. Then test one explanation scene and one diagnosis/repair/recovery scene where the elastic gag clarifies a real technical failure mode instead of becoming decorative stretchy limbs.

Treat the generated character as a temporary test IP unless the user separately approves it as a production IP.

## Required Records

Before generating, save:

- test brief with role, audience, and identity anchors;
- visual-master prompt beside the reference image path;
- action/expression-vocabulary prompt when required by the preset;
- one prompt per article scene beside its target output path;
- QA handoff record beside the run.

After each successful generation:

- copy accepted output from the image cache to the defined validation run directory;
- verify that the saved PNG decodes and that visual-master and article-scene formats match intended portrait/landscape roles where possible;
- preserve the original visual-master PNG, then create an optimized downstream reference when practical: long edge 1024px, JPEG quality 85, saved under `reference-images/optimized/`;
- use the optimized visual master as the image-to-image identity reference for downstream scenes when supported, while keeping the original PNG as the archive source.

## Human Acceptance Gate

Do not claim a style preset has passed visual QA without human inspection. Ask for review against:

- identity stability across visual master, action vocabulary, and scenes;
- target style differentiation from adjacent quirky, Japanese, and generic cartoon styles;
- article-size legibility and causal readability;
- action necessity: the IP must cause the explanatory transformation rather than decorate an already-complete diagram;
- for rubber-hose styles: elastic body mechanics, technical metaphor clarity, and separation from named vintage franchise imitation.

When the user approves, record the result as a passed preset test while keeping the test IP temporary unless separately approved.
