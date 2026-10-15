# Xiaohongshu / Green Book Card QA Checklist

Review every card at feed thumbnail size, phone size, then as an ordered sequence.

## Feed-Cover Failures

Reject/redesign if card 1 cannot be understood in one second; lacks direct H1 or information-rich visual; is a large IP plus small mood title; has H1/key contrast/IP face-hands in top-right, bottom-right, or bottom 10%; or needs paragraphs to explain itself.

Also reject/redesign if the in-image H1 merely copies the published SEO title; its hook type and article-backed promise were not recorded; no alternatives were considered; its click promise is unsupported by the article; or a pain/curiosity hook leaves the topic/mechanism opaque without a support line or visual proof.

## General Failures

Reject/redesign if local text/decoration overlay exists; Chinese is garbled/tiny; labels exceed 10 Chinese characters; a dense card becomes paragraph/table wall; functional colors overwrite locked IP colors; decoration exceeds one emphasis + one container + one thematic family; IP is watermark-like; identity/rendering drifts.

## Relation -> Composition Checks

- Each card names one reader takeaway and one primary information relation.
- Plan records candidates, one selected composition grammar, and why it is clearer than alternatives.
- The rendered composition visibly expresses the named relation: contrast, hierarchy, category, space, progression, parallel tips, state change, or causal mechanism.
- AI did not reuse a previous grammar merely for series uniformity.
- Information budget fits the selected grammar.
- H1/H2/labels, safe zones, colors, decorations, and IP role support the relation rather than decorating it.

## Sequence Checks

- Strategy/hook/arc are coherent.
- Visual identity remains coherent, but composition changes whenever the content relation changes.
- Do not demand a preset layout rhythm; reject only filler or repeated title-plus-mascot posters without a narrative reason.

## Final Decision

Record `PASS`, `REVISE`, or `REJECT`; name failing layer: strategy, hook, relation analysis, composition selection, hierarchy, safe zone, color, decoration, IP, text, or identity.
