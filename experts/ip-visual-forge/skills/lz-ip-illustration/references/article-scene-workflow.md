# Article Scene Workflow

Use this workflow when an initialized IP already exists and the user provides an article, outline, paragraph, topic, or content brief.

If the user provides a local article source path rather than a pasted excerpt or remote URL, detect that explicitly. Before any write-back behavior, ask whether the user wants the generated illustrations inserted into the article source.
When a local source file is used, copy it into the article run directory before further processing so the run remains self-contained.

## 1. Load IP Constraints

Read the available IP files:

- `ip-profile.md`
- `visual-spec.md`
- `prompt-pack.md`
- `action-library.md`
- `scene-rules.md`
- primary visual master image from `reference-images/`, when available

Respect identity stability before considering the article.

## 2. Parse Content Type

Classify each useful section as one or more types:

- judgment: a strong opinion or conclusion
- workflow: a sequence of steps
- breakdown: one object split into parts
- diagnosis: a problem and its causes
- comparison: old vs new, weak vs strong, before vs after
- route: movement from current state to target state
- state: emotional, cognitive, operational, or system condition
- mechanism: an internal system or causal chain

## 3. Extract Cognitive Anchors

Only illustrate high-value anchors:

- thesis
- turning point
- decision rule
- failure pattern
- key framework
- input-output chain
- before-after transformation
- common misconception
- method loop

Ignore generic explanation sentences unless they support a visual anchor.

## 4. Create Shot List

Before writing image prompts, propose a shot list.

Default shot-count rule:

- propose 3-5 high-value shots by default
- do not exceed 5 shots unless the user explicitly asks for broader coverage
- if the article is short or only has one strong anchor, propose 1-3 shots instead

Each shot must include:

- article placement
- cognitive anchor
- content type
- composition pattern
- content-to-scene method
- IP primary action
- main visual objects
- labels, if needed
- success criterion

Use `templates/shot-list-template.md`.

Present the shot list as a compact review table so the user can confirm the planned illustrations before image generation starts.

The table should make it easy to compare:

- what image will be drawn
- what part of the article it belongs to
- what content type it represents
- what scene method is being used
- what the IP is doing

Persist the accepted shot list as `shot-list.md` inside the article run directory.


## 4a. Single-Scene Action Rule

Each article scene illustration must explain one core structure or cognitive anchor. For a single-scene illustration, the IP may perform only one primary conceptual action.

Define the primary action as:

`The IP is actively [verb] [object] so the reader understands [cognitive anchor].`

Secondary gestures are allowed only when they support the primary action and do not create a second explanatory event. Do not combine diagnosis, repair, comparison, navigation, and explanation in one scene unless one is clearly primary and the others are passive supporting details.

If the idea requires multiple sequential actions, use multiple illustrations, a mini-comic composition with one action per panel, or a Xiaohongshu/Green Book card sequence. Do not force several conceptual actions into one single-scene image.

Use one primary composition pattern and one content-to-scene method per image. Keep main objects limited to the few objects required by the primary action; avoid dense object piles that turn the image into a full article summary.

## 5. Generate One Image Prompt at a Time

For each user-accepted shot:

1. Restate the image goal.
2. Save the final prompt to `article-runs/<article-slug>/prompts/NN-<anchor-slug>.md`.
3. Write the scene where the IP performs the required action.
4. Apply the IP identity constraints.
5. Apply the visual style and format.
6. Add short integrated Chinese labels only when image-only explanation is insufficient. Read `references/text-as-visual-material.md`; labels should usually be 5-10 Chinese characters, must be generated as part of the image, and must never be added locally after generation.
7. If the current image tool supports reference images, attach the accepted primary visual master by default as the identity reference.
8. Keep the fixed palette and rendering constraints explicit in the prompt text even when a reference image is attached.
9. Run QA before finalizing.

If generating images directly, read `references/image-generation-workflow.md`.

Hard rule:

- when the current tool supports image references, use the accepted primary visual master as the default identity reference
- do not drop text constraints for palette, rendering style, and signature identity traits just because a reference image is attached
- if image references are unavailable, repeat the fixed identity, palette, and rendering constraints from `visual-spec.md` and `prompt-pack.md` in every prompt


## Text Rule

Article illustrations prefer no text when the scene can carry the idea. When labels are necessary, text is part of the image composition: short, integrated, generated with the scene, and placed on physical carriers such as tags, tabs, module cards, route signs, sticky notes, or diagram nodes. Local text overlay/compositing is forbidden.
