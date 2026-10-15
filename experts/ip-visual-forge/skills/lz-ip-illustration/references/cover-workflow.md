# Article Cover Workflow

Use this workflow when an initialized IP exists and the user requests an article cover, social cover, thumbnail, hero image, or other first-view promotional image.

Do not reuse the inline article shot-list workflow. Inline illustrations explain cognitive anchors inside the article. A cover selects one communication proposition and turns it into a compact visual promise.

## 1. Load Inputs

Load available inputs:

- article title, subtitle, outline, or full text
- `ip-profile.md`
- `visual-spec.md`
- `prompt-pack.md`
- `action-library.md`
- `scene-rules.md`
- primary visual master image, when available
- target platform and aspect ratio, when supplied

The article title, subtitle, outline, and full text are alternatives, not a mandatory bundle. Do not require the user to provide all of them.

Minimum content rule:

- proceed when the available material is sufficient to infer one accurate communication proposition
- a specific title may be sufficient by itself
- a vague title such as "Some Thoughts" is not sufficient by itself
- a title plus a short summary, an outline, a representative excerpt, or the full text is normally sufficient
- if the user provides only a topic, ask for the intended thesis, reader tension, or promised payoff before proposing cover directions

Use progressive input collection:

1. Inspect the material already provided.
2. Infer every field that can be supported without guessing.
3. Ask only for the single most important missing item.
4. Continue once the communication proposition and content boundary are reliable.

Treat this list as a collection checklist, not a questionnaire. Do not ask the user to restate information already present in the article.

The primary visual master image is the default identity reference when the image generation tool supports image references. Use it to stabilize the IP's face, body proportions, signature clothing, palette, and rendering style. Do not use it as a mandatory composition reference, and do not copy its pose or background unless the selected cover direction calls for them.

If no platform is specified, use a neutral 16:9 composition. Do not invent platform-specific UI decoration. Read `references/text-as-visual-material.md` before planning any title, subtitle, label, or other text. Local text overlay/compositing is forbidden.

## 2. Compress the Article

Write a cover brief with five fields:

- `topic`: what the article is about
- `communication proposition`: the single idea the cover promises
- `reader tension`: the problem, uncertainty, desire, or conflict that creates interest
- `promised payoff`: what understanding, result, or transformation the reader expects
- `content boundary`: what the cover must not imply because the article does not support it

Use this pattern when useful:

`For [reader], this article reveals/shows/challenges [core idea], so they can understand/achieve/avoid [payoff].`

The communication proposition is not the article summary. It is the strongest accurate promise that can survive at thumbnail size.

## 3. Select One Visual Hook

The visual hook is an abstract communication device. It defines why the cover creates immediate interest, not the literal scene that will be drawn.

Choose one primary hook:

- `conflict`: two forces, choices, or states oppose each other
- `transformation`: a visible before-to-after change
- `obstacle`: a barrier is confronted, removed, crossed, or escaped
- `reveal`: a hidden mechanism, truth, or path is uncovered
- `choice`: routes, tools, or strategies are contrasted
- `scale`: one object or consequence is unexpectedly large or small
- `mechanism`: a system is activated, repaired, or inspected
- `identity`: the visual world embodies the reader's desired or feared state

Do not combine multiple hooks unless one is clearly dominant and the second only supports it.

## 4. Build the Cover Motif

The cover motif is the drawable physical expression of the selected hook. Convert the abstract hook into visible subjects, actions, objects, spatial relationships, and an integrated typography area only when text is requested.

Translate the hook into one physical scene:

- one dominant subject or visual event
- one primary object or opposing force
- optional secondary object only when needed
- clear foreground/background hierarchy
- a visual metaphor understandable without explanatory labels

Do not turn the cover into a literal collection of every article concept. A motif fails when it remains an abstract phrase such as "breaking conventions," "discovering truth," or "improving efficiency" without a drawable visual relationship.

## 5. Choose the IP Deployment Mode

A cover is not an inline explanation scene. Select the IP's contribution deliberately; do not automatically require a large causal action.

### A. Narrative actor

Use when the article's hook is best expressed through an IP action: diagnosing, building, confronting, choosing, repairing, transforming, or navigating.

- define role, one strong verb, visible object/opposing force, and dominant emotion
- the IP is a major subject
- removing the IP must break the central visual idea

### B. Scene guide

Use when the main motif carries the proposition but the IP helps readers orient, interpret, or emotionally enter the scene.

- define role, gesture/posture, gaze or spatial relationship to the motif, and emotion
- the IP need not cause the event
- it must improve reader guidance or emotional interpretation without competing with the motif

### C. Brand anchor

Use for title-led, conceptual, or recurring series covers where stable author recognition matters more than IP-led narrative.

- the primary visual proposition must work without the IP
- place the IP as a small, intentional presenter/observer anchor, normally near an edge or lower corner
- choose a theme-responsive expression, small gesture, or prop from the action library; do not reuse a blank sticker pose by default
- the IP must strengthen series recognition without blocking the headline, hook, or thumbnail hierarchy

Never use an undeclared decorative IP placement. Record the selected mode, purpose, scale, placement, posture/action, and emotion.

## 6. Select Constrained Visual Treatment

Use the following cover-specific choices to give each article an appropriate editorial treatment. They are subordinate to the fixed IP identity system in `visual-spec.md`.

### Cover expression mode

Choose one: `scene`, `metaphor`, `conceptual`, `minimal`, `hero`, or constrained `typography`.

- `typography` is allowed only when title lettering is part of the physical scene or visual event and does not reduce the IP to a detached mascot.
- the expression mode changes the communication method, not the IP rendering style.

### Text mode

Choose one: `none`, `integrated-title-only`, or `integrated-title-and-short-subtitle`.

- never use text-rich cover copy, paragraph text, tiny UI, or local post-production overlays
- all requested text must follow `references/text-as-visual-material.md`

### Mood

Choose one: `subtle`, `balanced`, or `bold`.

Mood may adjust composition tension, contrast, gesture amplitude, density, and use of whitespace. It must remain faithful to the article's reader tension and the IP's visual world.

### Contextual color emphasis

Do not select a new palette. The identity palette is inherited from `visual-spec.md`.

You may adjust only the balance, value, and situational use of existing IP colors: for example, heavier ink and a restrained warning accent for risk, or larger warm-paper whitespace for reflection. Do not introduce a new dominant palette, such as neon cyberpunk or macaron, when it conflicts with the established IP system.

### Rendering

Rendering is locked from `visual-spec.md`. Do not select or replace it during cover planning. A traditional Chinese lianhuanhua IP cannot be changed into flat-vector, 3D, pixel, or another incompatible rendering system merely to fit an article topic.

## 7. Produce Candidate Directions

Create 2-4 directions using `templates/cover-direction-template.md`.

Each direction must differ in its hook, motif, IP deployment mode, or cover expression mode. Changing only camera angle, color emphasis, or background does not create a new direction.

Each direction includes:

- direction name and communication proposition
- primary hook and one-sentence cover scene
- IP deployment mode, purpose, placement/scale, posture/action, and emotion
- dominant objects and composition
- cover expression mode, text mode, mood, and contextual color emphasis
- curiosity mechanism, content accuracy risk, and thumbnail success criterion

Present the directions for user confirmation before writing the final image prompt. If the user explicitly asks for immediate generation, select the strongest direction and record why.

## 8. Select the Direction

Prefer the direction that best balances:

1. content accuracy
2. thumbnail comprehension
3. visual curiosity
4. appropriate IP recognition and deployment mode
5. integrated text compatibility, if text is requested
6. fit between expression mode, mood, and article tone

Reject a direction when it:

- promises a result absent from the article
- requires paragraph-length text to make sense
- contains several competing scenes
- uses an undeclared or obstructive IP sticker placement
- duplicates the title literally without adding a visual idea
- depends on tiny interface details or unreadable labels
- changes the IP's locked palette or rendering system

Persist the accepted direction as `cover-direction.md` in the cover run directory.

## 9. Write and Save the Prompt

Use `templates/cover-prompt-template.md`.

Save the final prompt before generation:

`cover-runs/<article-slug>/prompts/cover-v1.md`

When regenerating, use `cover-v2.md`, `cover-v3.md`, and matching image names. Do not overwrite silently.

## 10. Generate and Review

When the image tool supports reference images, attach the accepted primary visual master as the identity reference. Use the selected cover direction, not the visual master, as the composition source. Keep identity, locked palette, rendering style, signature traits, selected IP deployment mode, and visual treatment explicit in the prompt.

Review at:

- thumbnail size for immediate recognition
- full size for identity, composition, artifacts, text treatment, and IP placement

Use `references/cover/cover-qa-checklist.md`. Save review notes to:

`cover-runs/<article-slug>/qa-notes.md`

## Output Contract

A completed cover planning pass produces:

- one article cover brief
- 2-4 distinct cover directions
- one accepted direction
- one saved final prompt
- one generated or generation-ready cover
- one cover-specific QA record
