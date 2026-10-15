# Xiaohongshu Content-Relation Composition System

Use this reference with `xhs-card-workflow.md`. It adapts infographic composition knowledge without weakening a reusable IP's locked identity, rendering style, identity palette, primary visual master, or no-local-overlay rule.

## 1. What Is Fixed vs Dynamic

### Fixed IP visual language

These are fixed after IP initialization: character identity, silhouette, clothing, signature prop, rendering style, identity palette placement, accepted visual master, and compatible title/decoration material language.

### Dynamic per-card composition

These must be selected from the source content, not inherited as a fixed series template: narrative role, information relation, visual anchor, title position, content structure, composition grammar, IP placement/pose, and supporting objects.

A series direction may set **compatibility constraints** (for example, warm textbook-watercolor should avoid cold UI tables and noisy sticker walls). It must not pre-assign every card to a visual motherboard, title position, or layout sequence.

## 2. Strategy and Feed-Cover Hook

During article analysis, extract the article's evidence-backed content promise, draft 3-5 candidate **in-image cover hooks**, and select one. This is a feed-creative decision only: do not copy, optimize, or keyword-stuff the published SEO title, which belongs to a separate workflow.

Choose a series strategy: `story-led`, `information-led`, `visual-led`, or `hybrid`. Evaluate candidate hook types: `pain`, `benefit`, `contrast`, `counterintuitive`, `number`, `identity`, or `curiosity`. Record selected H1, optional support/proof line, strength (1-5), and why it wins at thumbnail size over the nearest candidate. The hook must be specific, truthful to the article, and paired with a support line or visual proof when the hook alone does not reveal the topic/mechanism.

Strategy shapes reading order; it does not dictate the composition of each card.

## 3. Feed Cover and Safe Zones

Card 1 chooses `big-title`, `information-rich`, or `visual-first` and passes a one-second feed test.

- Keep H1, CTA, decisive comparison, key label, and IP face/hands out of top-right platform controls, bottom-right, and bottom 10% overlay zone.
- Keep strong outer margins. AI chooses the title/IP position from the actual composition, not a preset corner.
- Reject a cover that is only a large IP plus a small atmosphere title.

## 4. AI Content-Relation -> Composition Selection

For **every card**, AI must perform this sequence before prompting:

1. Write the `reader takeaway`.
2. Name one primary `information relation`.
3. Select one `composition grammar` that makes that relation visible.
4. State `why this composition`, including why a competing grammar is weaker.
5. Set an information budget, title hierarchy, safe-zone plan, IP role, and decoration budget.

Use this mapping as decision support, not as a fixed template library:

| Information relation | Typical composition grammar | When it fits |
|---|---|---|
| one strong judgment / pain / claim | sparse proposition or title-led visual metaphor | one message must stop scrolling |
| before vs after / wrong vs right / two alternatives | comparison | reader must see contrast directly |
| several concepts and their category/hierarchy relation | mindmap, modular relationship map, or quadrant | category/structure matters more than sequence |
| one topic mapped to real spaces | spatial map, quadrant, cutaway | task belongs to rooms/locations |
| ordered steps / cause-to-result / time progression | flow, route, timeline | progression is the message |
| parallel tips / repeated rules / ranked items | list or balanced repeated modules | items are independent and similarly weighted |
| four bounded dimensions / classifications | quadrant | four-way relation is meaningful |
| many compact facts with one central framework | dense modular information graphic | only when labels remain legible and no paragraph wall is needed |
| emotional state or experience change | state contrast, light scene, or mini sequence | reader must feel a shift, not inspect a framework |
| one causal mechanism | mechanism diagram or one action scene | one cause produces a visible result |

Do not choose a grammar because it was used on the prior card, because it is fashionable, or because a series direction named it. When two grammars are plausible, choose the simpler one that preserves the primary relation.

## 5. Composition Grammar Budgets

| Grammar | Information budget | Whitespace | Non-negotiable |
|---|---:|---:|---|
| sparse proposition | 1-2 points | 60-70% | one dominant hook |
| balanced modules | 3-4 points | 40-50% | readable hierarchy |
| dense modular graphic | 4-6 compact modules | 20-30% | no paragraphs/tiny tables |
| list | 3-5 parallel items | 30-40% | repeated rhythm |
| comparison | 2 states | 40-50% | decisive contrast divider |
| flow / route | 3-5 nodes | 35-45% | clear direction and progression |
| mindmap / relation map | 3-6 branches | 30-40% | central relation visible |
| quadrant / spatial map | 4 regions | 30-40% | meaningful region labels |
| state scene / action scene | one event | 45-60% | visible emotional or causal change |

`Dense` means compact visual modules only. Never use it for long generated paragraphs, full tables, or unreadable bullet walls.

## 6. Typography and Color

Use H1 100%, H2 70-80%, key labels 50-60%, support labels 35-45%, CTA 30-40%. H1 is largest in big-title covers.

Use generated integrated lettering only. Per series, choose at most one title treatment and one support treatment compatible with the locked IP material language. Low-risk options include soft outline, subtle painted shadow, highlighter stroke, hand-drawn underline, rounded pill, ribbon, pointer label, or circled number.

Keep fixed IP colors fixed. Derive functional roles from them: background, primary text, secondary text, problem/warning, solution/completion, structure/neutral, reward/accent. This is semantic allocation, not a per-post palette swap.

## 7. Semantic Decoration

Decoration must clarify reading. Per card choose at most one emphasis family + one container family + one thematic family.

| Element | Semantic job |
|---|---|
| circle / highlighter / underline | emphasis |
| arrow / pointer | direction |
| checkmark / cross | completion / avoid |
| circled number | sequence |
| star / badge | reward / milestone |
| rounded card / tab / pill | task/category container |
| dashed divider | separation |
| tape / clip | practical note |
| route node | progression |

All decoration is generated in-image. No post-generation sticker, crop, or text patch.

## 8. Series Coherence Without Fixed Layouts

A series keeps coherent IP identity, material language, functional colors, safe zones, title treatment, and decoration semantics. It may vary composition grammar, title position, dominant object, and IP pose whenever the content relation changes.

QA should reject repeated title-plus-mascot posters, but should not force an arbitrary cover -> overview -> comparison -> flow sequence. The sequence emerges from the source narrative and selected card relations.

## 9. Prompt / QA Requirement

Every plan and prompt states: strategy, hook type/strength, reader takeaway, information relation, selected composition grammar, why it fits, information budget, hierarchy, safe zones, functional colors, decoration budget, IP participation, and cover one-second understanding when applicable.
