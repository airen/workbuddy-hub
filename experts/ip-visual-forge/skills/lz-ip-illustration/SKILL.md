---
name: lz-ip-illustration
description: Create, persist, and reuse a stable personal IP character for article covers, scene-based article illustrations, lightweight animated action loops, and Xiaohongshu/Green Book image-card series. Use when users want to design a reusable visual IP, build character specs and action libraries, create article cover images, parse articles into illustration shot lists, create short GIF/APNG action loops, create swipeable social card posts, or generate prompts where the IP actively participates in workflows, problem breakdowns, comparisons, diagnostics, routes, or conceptual scenes.
version: 0.3.29
category: content-creation
---

# Personal IP Illustration System


## Overview

Use this skill to build a reusable visual system for a personal IP character, then use that IP to create article covers, scene-based article illustrations, lightweight animated IP action loops, and Xiaohongshu/Green Book image-card series. Treat IP creation as a one-time initialization flow. Route each output type through its own repeatable workflow.

## Entry Router

Start every request by checking whether an IP asset folder already exists.

Default asset locations, in order:

1. A user-specified IP folder.
2. `ip-assets/<ip-slug>/` in the current project.
3. `ip-assets/` if the project has exactly one IP profile.

Hard gate: only these locations count as current project IP assets. Do not use `examples/`, demo assets, prior test assets, generated images from earlier conversations, or conversation history as substitutes for an initialized IP.

An IP is considered initialized when these minimum files exist:

- `ip-profile.md`
- `visual-spec.md`
- `prompt-pack.md`
- at least one reference image under `reference-images/` or a clear text-only reference in `visual-spec.md`

Route the work:

- If no initialized IP exists, run the IP creation workflow. Read `references/ip-creation-workflow.md`.
- If exactly one initialized IP exists, do not silently assume it should be used. Ask the user whether to use the existing IP or create a new IP, unless the user's request already clearly names the existing IP or explicitly says to continue with it.
- If multiple initialized IPs exist, ask the user which IP to use before continuing.
- If the user explicitly asks to revise an existing IP, load the existing files, preserve stable identity constraints, and update only the requested parts.

When a user asks for article illustrations but no initialized IP exists in the allowed locations, stop before parsing or generating article illustrations. Tell the user that an IP must first be created or explicitly specified. Then enter the brief-first IP creation workflow.

## Core Principles

- Keep the IP stable across scenarios: face, body proportions, signature clothing, palette, and rendering style must not drift.
- When the current image tool supports reference images, treat the accepted primary visual master as the default identity anchor for downstream image generation.
- Do not rely on reference images alone for palette consistency. Keep palette and rendering constraints explicit in text even when a visual master reference is attached.
- For article scene illustrations, make the IP a necessary actor, not decoration: if removing the IP leaves the explanation's core meaning intact, the image fails. Covers use their selected `narrative actor`, `scene guide`, or `brand anchor` deployment mode; Xiaohongshu cards use a separate content-first participation rule.
- Illustrate one cognitive anchor per image: one judgment, process, contrast, failure mode, route, state, or conceptual transformation. For article scene illustrations, each single-scene image must also carry one core structure and one primary IP action.
- Build each cover around one communication proposition and one dominant visual hook. Do not compress the whole article into the cover.
- Build each Xiaohongshu/Green Book series around one reader promise and an explicit story-led, information-led, visual-led, or hybrid strategy. During article analysis, extract 3-5 candidate **in-image feed-cover hooks** from the article's evidence-backed promise, then select one H1 and an optional support/proof line for Card 1; this is not the published SEO title and never takes over its optimization. Treat every card as a full-screen, independently consumable phone page. The first card is a feed cover that must stop scrolling through the selected hook plus a large title or an information-rich visual. For every card, have AI identify the content relationship first, dynamically choose one composition grammar that makes that relationship visible, and record why; then apply text hierarchy, functional color roles, safe-zone plan, and restrained semantic decorations. Content structure is primary; the IP stays small and may act, guide, react, or serve as a brand-memory anchor without being forced to cause the explanation on every card.
- Text is visual material, not a post-production patch. Never use local text overlay/compositing for covers, article illustrations, or Xiaohongshu cards. If Chinese text is needed, it must be generated as integrated in-image lettering that fits the composition, stays readable, does not deform, and does not weaken the IP action or central idea.
- Prefer reusable structure over fixed scene templates. For inline article scenes, select one structure type, one content-to-scene method, and one primary IP action. If an inline idea requires multiple actions, split it into multiple illustrations or mini-comic panels; for covers and Xiaohongshu cards, use their dedicated deployment or participation workflow.
- Keep article illustrations simple enough for repeated use: usually 16:9, clean background, short labels, strong whitespace, and one clear visual idea.

## Repeatable Content Routing

Hard route:

- For article cover, social cover, thumbnail, hero image, or first-view promotional image requests, read `references/cover-workflow.md`. Do not use the inline article shot-list workflow as a substitute.
- For images placed inside an article to explain sections or ideas, read `references/article-scene-workflow.md`.
- For lightweight moving article illustrations, animated IP action, short loop GIF/APNG, or requests to make the IP action move, read `references/animated-ip-action-workflow.md`. Treat this as an enhancement of an accepted static article illustration, not as image-to-video or a full animation pipeline.
- For Xiaohongshu, Little Red Book, Green Book, social image-card, carousel, or swipeable post requests, read `references/xhs-card-workflow.md`. Also read `references/xhs-content-density-ip-roles.md`, `references/xhs-visual-editorial-system.md`, and `references/text-as-visual-material.md` when cards must carry text. Do not use the cover or inline illustration workflow as a substitute.
- If the user requests both, complete the cover direction review separately from the inline shot-list review.

## Repeatable Article Illustration Flow

For an existing IP:

1. Load `ip-profile.md`, `visual-spec.md`, `prompt-pack.md`, and `action-library.md` if present.
2. Parse the article or topic into content types and cognitive anchors.
3. If the article source is a local file path, ask whether the user wants image insertion back into the article source before any write-back behavior.
4. Propose a shot list before generating images.
5. Keep the default shot list constrained to 3-5 high-value shots unless the user asks for broader coverage.
6. Show the shot list as a review table and get user confirmation before generating images.
7. For each shot, choose a composition pattern and a content-to-scene method.
8. Define the IP's required action before writing the image prompt.
9. When the image tool supports reference images, attach the accepted primary visual master by default as the identity reference for article illustrations and covers.
10. Generate or provide prompts one image at a time, keeping fixed identity, palette, and rendering constraints explicit in text even when a reference image is used.
11. Run QA against identity stability, scene participation, clarity, and reuse.

## Repeatable Animated IP Action Flow

For an existing IP and an accepted static article illustration or shot direction:

1. Load the available IP files, accepted static image, primary visual master, and article/shot context.
2. Read `references/animated-ip-action-workflow.md`.
3. Define one moving cognitive action only; do not add cinematic motion, full-body acting, or camera movement by default.
4. Produce an animation plan using `templates/animated-action-plan-template.md`.
5. Save the accepted plan as `animation-runs/<scene-slug>/storyboard.md`.
6. Create 3-6 keyframes or local compositing states while preserving the same IP identity, palette, rendering style, background, and labels.
7. Save one prompt per generated keyframe using `templates/animated-keyframe-prompt-template.md` when image generation is used.
8. Assemble a 1-2 second looping GIF by default; create APNG or MP4 only when requested or platform-required.
9. Run animation QA for frame count, dimensions, loop playback, file size, identity stability, and whether the motion clarifies one article idea.

## Repeatable Cover Flow

For an existing IP:

1. Load the available article material, stable IP files, and primary visual master.
2. Read `references/cover-workflow.md`.
3. Check whether the article material is sufficient to infer one accurate communication proposition. Ask only for the missing minimum information when it is not.
4. Compress the article into one communication proposition, reader tension, promised payoff, and content boundary.
5. Choose one abstract visual hook and convert it into one drawable physical cover motif.
6. Select the IP deployment mode (`narrative actor`, `scene guide`, or `brand anchor`) and define its mode-appropriate role, placement/scale, posture or action, and dominant emotion.
7. Produce 2-4 genuinely different cover directions using `templates/cover-direction-template.md`.
8. Get user confirmation on one direction before generating the final cover.
9. Write the final prompt using `templates/cover-prompt-template.md`.
10. Save the prompt before generation and use the primary visual master as the identity reference when supported.
11. Run `references/cover/cover-qa-checklist.md` at thumbnail size and full size before finalizing.

## Repeatable Xiaohongshu/Green Book Card Flow

For an existing IP:

1. Load the available source material, stable IP files, primary visual master, and target platform constraints.
2. Read `references/xhs-card-workflow.md`.
3. Analyze the article: extract one reader promise, target reader, evidence boundary, and CTA; then draft 3-5 article-backed candidate **in-image feed-cover hooks**. Select one hook type/H1, optional support or visual proof, and one-second understanding. Do not create, copy, or optimize the published SEO title.
4. Propose 2-3 series visual directions using `templates/xhs-series-style-template.md`.
5. Confirm one visual direction before planning cards, unless the user explicitly requests immediate generation.
6. Select a 3-6 card narrative arc using `templates/xhs-card-plan-template.md`.
7. Assign one readable point, card role, content density, text payload, IP role/scale, and text policy to each card.
8. Produce a card plan and get user confirmation before generation, unless the user explicitly requests an immediate smoke test or full run (for example, “实测一下”).
9. Write one final prompt per card using `templates/xhs-card-prompt-template.md`.
10. Save each prompt before generation and use the primary visual master as the identity reference when supported.
11. Generate cards in a consistent 3:4 vertical visual system unless the user specifies another format.
12. For medium/high-density Chinese cards, simplify the promise, split overloaded material into additional cards, or choose a clearer composition grammar; generate all titles, labels, and decorations as integrated in-image material. Save the generated image and a contact sheet for review; do not create local text-overlay variants or `text-overlays.md`.
13. Run `references/xhs-card/xhs-card-qa-checklist.md` on individual cards and the whole sequence before finalizing, and explicitly record whether the run is a pipeline smoke-test pass versus public-posting-ready visual approval.

Read the relevant references only when needed:

- `references/entry-router.md` when deciding whether to create, load, or reject an IP source.
- `references/ip-creation-workflow.md` for one-time IP initialization.
- `references/ip/brief-first-interview.md` when collecting or validating the initial IP brief.
- `references/ip/visual-master-directions.md` when creating 3-6 visual master directions from a confirmed brief.
- `references/ip/deep-refinement.md` after the user selects one visual master direction and the IP identity needs to be locked.
- `references/image-generation-workflow.md` when generating visual masters, reference images, covers, or article illustrations.
- `references/provider-pitfalls.md` when a generation fails with a timeout, content-policy rejection, or provider-specific error; contains known gpt-image-2 traps and workarounds.
- `references/ip/visual-master-review.md` when reviewing or selecting generated visual master directions.
- `references/article-scene-workflow.md` for parsing articles and making shot lists.
- `references/animated-ip-action-workflow.md` for turning an accepted static article illustration into a 3-6 frame lightweight action loop.
- `references/cover-workflow.md` for extracting a cover proposition, visual hook, motif, and candidate directions from an article.
- `references/xhs-card-workflow.md` for turning an article or topic into a Xiaohongshu/Green Book card sequence.
- `references/scene-methods.md` for content-to-scene methods and composition patterns.
- `references/ip/ip-action-rules.md` for hard constraints on IP participation.
- `references/article-scene/single-primary-action-rule.md` when planning or QA'ing inline article scenes that risk combining several conceptual actions into one frame.
- `references/prompt-template.md` for reusable prompt structure.
- `references/text-as-visual-material.md` when any output requires Chinese text, labels, titles, headings, captions, or UI-like lettering.
- `references/ip/styles/lianhuanhua-preset-validation.md` when adding or independently validating any locked Chinese narrative-illustration or folk-performance rendering preset.
- `references/ip/styles/lianhuanhua-style-selection.md` when selecting a locked rendering family or preserving boundaries between approved families.
- `references/ip/styles/chinese-shadow-puppetry.md` only when the user explicitly selects Chinese shadow puppetry for a new IP or explicitly revises an existing IP to that preset.
- `references/article-scene/qa-checklist.md` before finalizing images or prompts.
- `references/cover/cover-qa-checklist.md` before finalizing a cover direction, prompt, or generated cover.
- `references/xhs-card/xhs-card-qa-checklist.md` before finalizing a card plan, prompt, or generated card series.

## Style Atlas Documentation

When creating or revising a README style table with real example images, read `references/style-atlas-workflow.md`. It defines production-versus-candidate separation, benchmark-scene parity, batch generation, manifest/contact-sheet records, and bilingual README publication checks.

## Output Assets

Use a two-layer filesystem layout:

1. stable IP asset root for long-lived reusable identity files
2. per-article and per-cover run directories for analysis, prompts, generated images, QA notes, and optional source write-back copies

Default root:

- `ip-assets/<ip-slug>/`

Recommended layout:

```text
ip-assets/<ip-slug>/
  ip-profile.md
  visual-spec.md
  prompt-pack.md
  action-library.md
  scene-rules.md                  # optional
  reference-images/
    <ip-slug>-visual-master-v1.png
    <ip-slug>-visual-master-v1.md
    <ip-slug>-direction-sheet-v1.png
    <ip-slug>-direction-sheet-v1.md
  article-runs/
    <article-slug>/
      source/
        source-<article-slug>.<ext>
      analysis.md
      shot-list.md
      prompts/
        01-<anchor-slug>.md
        02-<anchor-slug>.md
      images/
        01-<anchor-slug>.png
        02-<anchor-slug>.png
      qa-notes.md
      article-with-images.<ext>   # only when the user asked for write-back
  animation-runs/
    <scene-slug>/
      source/
        static-source.png
      storyboard.md
      prompts/
        keyframe-01.md
        keyframe-02.md
      frames/
        01.png
        02.png
      output/
        action-loop.gif
        action-loop.apng             # optional
        action-loop.mp4              # optional
      qa-notes.md
  cover-runs/
    <article-slug>/
      prompts/
        cover-v1.md
      images/
        cover-v1.png
      qa-notes.md
  xhs-runs/
    <post-slug>/
      source/
        source-<post-slug>.<ext>
      analysis.md
      visual-system.md
      card-plan.md
      prompts/
        01-cover.md
        02-problem.md
      images/
        01-cover.png
        02-problem.png
      qa-notes.md
```

Slug rules:

- `ip-slug`: stable kebab-case identity name
- `article-slug`: kebab-case from article title or file stem
- if a distinct new run would collide with an existing directory, append timestamp `-YYYYMMDD-HHMMSS`

When creating a new IP, save or propose these files:

- `ip-profile.md`
- `visual-spec.md`
- `prompt-pack.md`
- `action-library.md`
- `scene-rules.md`
- `reference-images/`
- `templates/cover-direction-template.md`
- `templates/cover-prompt-template.md`
- `templates/xhs-card-plan-template.md`
- `templates/xhs-card-prompt-template.md`
- `templates/xhs-series-style-template.md`
- `templates/shot-list-template.md`
- `templates/animated-action-plan-template.md`
- `templates/animated-keyframe-prompt-template.md`

Use the templates in `templates/` when writing these files.

When an image is generated and accepted as a reference image, copy it into the relevant `reference-images/` folder and update `visual-spec.md` with the filename and role.

Prompt-file rule:

- before generating any reference image, article illustration, cover image, or animation keyframe, save the final prompt text to a dedicated prompt file in the corresponding directory
- the prompt file is the reproducibility record and should exist even if the backend only receives inline prompt text

Overwrite rule:

- do not silently overwrite an existing prompt or generated image
- when regenerating, either create a new versioned filename such as `v2` or rename the old file with a timestamped backup suffix before replacement

## Validating a New Locked Rendering Preset

When adding any new locked rendering preset, do not call it production-ready merely because a related preset passed. Validate it independently with a temporary IP using: (1) visual master, (2) action-driven explanation scene, and (3) diagnosis/repair scene. Save reproducible prompts, archive accepted images in the IP asset layout, and use the visual master as an identity reference for downstream scenes when supported. Before downstream image-to-image calls, create an optimized reference copy when practical: preserve the original PNG, then create `reference-images/optimized/<name>-ref-1024-q85.jpg` with long edge 1024px and JPEG quality 85. Human visual approval is required before marking the preset passed. Use `references/ip/styles/style-selection.md` to choose the family, then read the matching family validation protocol such as `lianhuanhua-preset-validation.md`, `japanese-manga-preset-validation.md`, or `quirky-cartoon-preset-validation.md`.

Before adding or reorganizing style families, read `references/style-taxonomy-maintenance.md`. Keep family-specific guides narrow: Chinese nostalgic styles stay in `lianhuanhua-style-selection.md`; Japanese manga / animation styles stay in `japanese-manga-style-selection.md`; rubber-hose, UPA-like, lowbrow, newspaper gag, heta-uma, and other oddball humor systems stay in `quirky-cartoon-style-selection.md` unless a deliberate split is made.

## Maintaining This Skill

When the request is to modify `lz-ip-illustration` itself, edit the installed Hermes skill package first, validate the change through the actual skill-loading path and a real smoke test, then synchronize the validated files back to the project repository. Do not start from the project copy and assume Hermes has picked it up. Read `references/skill-maintenance-workflow.md` before changing presets, routing, templates, QA rules, or validation status.

