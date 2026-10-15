# Xiaohongshu / Green Book Card Workflow

Use this workflow for Xiaohongshu, Little Red Book, Green Book, swipeable social posts, or image-card carousels. Treat every card as a full-screen, independently consumable phone page.

Read `references/xhs-content-density-ip-roles.md`, `references/xhs-visual-editorial-system.md`, and `references/text-as-visual-material.md`. The visual editorial reference gives AI a content-relation composition process; it does not impose fixed visual motherboards.

## 1. Load Inputs

Load source material, initialized IP files, primary visual master, platform, and fixed brand/title/CTA requirements. Default is 3:4 vertical.

## 2. Analyze the Article and Extract the Feed-Cover Hook

Before visual direction, analyze the source article for the **single content promise** that Card 1 can truthfully make to a passive feed reader. This step owns the in-image feed-cover title only; it does **not** create, copy, optimize, or validate the note's published SEO title.

1. Record reader, reader promise, core takeaway, evidence boundary, CTA, strategy, feed-cover mode, and one-second feed understanding.
2. Extract the cover-hook source: concrete pain, desired benefit, meaningful contrast, counterintuitive insight, identity cue, number, or curiosity gap supported by the article.
3. Draft 3-5 short candidate cover hooks across plausible hook types: `pain`, `benefit`, `contrast`, `counterintuitive`, `identity`, `number`, or `curiosity`.
4. Select one hook for the first-card H1; record its type, strength (1-5), and why it is more thumb-stopping and clearer than the closest alternative.
5. Write a short cover-support line or visual proof when needed so the reader can identify the topic/mechanism without relying on the SEO title. The hook and support must preserve the same article promise; reject unsupported outcomes, vague hype, and title-copying.

## 3. Select a Series Visual Direction

Propose 2-3 directions using `templates/xhs-series-style-template.md`. Each direction sets only:

- reader feeling and strategy/hook
- locked-IP constraints and compatible editorial material language
- functional color roles, title treatment, safe-zone/margin rules
- permitted decoration semantics and visual incompatibilities
- IP continuity policy

Do **not** lock a card-by-card layout recipe. The actual composition is chosen after each content unit is analyzed.

## 4. Select Narrative Arc, Then Analyze Each Card

Choose a strategy-appropriate arc (story-led, information-led, visual-led, or hybrid). For each candidate card:

1. write one takeaway;
2. identify its information relation;
3. select one composition grammar;
4. state why it makes the relation clearer than alternatives;
5. set budget, hierarchy, safe-zone, IP participation, and decoration plan.

Use 3-6 cards by default. Content determines composition; do not reuse a prior grammar without a content reason.

## 5. Plan Cards

Use `templates/xhs-card-plan-template.md`. Every card needs one role, one takeaway, one information relation, one selected composition grammar and rationale, budget, visual anchor, integrated text hierarchy, safe-zone plan, functional colors, decoration budget, IP participation, and swipe reason.

Roles: `feed-cover`, `problem`, `reframe`, `method`, `proof`, `summary`, `CTA`.

## 6. Feed Cover and IP Participation

Card 1 chooses `big-title`, `information-rich`, or `visual-first`; it must pass the one-second thumbnail test. Big-title: H1 is largest/high-contrast/direct. Information-rich: decisive structure/relation explains the topic without long text. Visual-first: an emotional/story visual communicates topic, not generic mood.

Small IP is default: 10-25%. Participation may be actor, guide, brand anchor, emotion anchor, or comparison anchor. The IP needs intentional pose/placement but causal action only when it improves comprehension. Evaluate continuity at series level.

## 7. Text and Generation

Text and decorations are integrated generated material; local overlay/compositing is forbidden. Non-header/footer labels are <=10 Chinese characters and scene-attached. Dense means compact modules, not paragraphs/tiny tables. Respect safe zones and locked IP rendering. Attach primary visual master when supported; do not substitute image 1 for a confirmed IP master. Preserve failures and retry with a new prompt/image path.

## Output Contract

A completed run produces: post brief; visual directions; accepted visual system; card plan with relation -> composition reasoning; prompts; generated in-image text cards; no post-generation compositing; sequence QA.
