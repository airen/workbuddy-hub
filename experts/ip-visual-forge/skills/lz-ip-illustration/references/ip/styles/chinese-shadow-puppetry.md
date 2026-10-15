# Chinese Shadow Puppetry Preset

Use this preset only when the user explicitly selects **Chinese shadow puppetry** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a locked **traditional folk-performance and craft visual rendering preset**. It is not a painting-school label, a generic Chinese-style filter, a paper-cut substitute, or a freely switchable article-level variant.

```text
IP visual = fixed character identity + Chinese shadow-puppetry rendering
```

Lock the character's side-profile or three-quarter silhouette, articulated-joint grammar, recurring prop shapes, pierced-cutout pattern density, translucent color placement, screen/light relationship, and stage-space rules in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as the identity reference for downstream scenes.

## What This Preset Is

Chinese shadow puppetry is a performance and craft language: carved, pierced, jointed figures appear through transmitted light on a pale screen. Its visual identity comes from the relationship between puppet, rod-operated action, cutout detail, translucent dyed material, and projected shadow--not from painterly realism or decorative nostalgia alone.

Use a regionally neutral Chinese shadow-puppetry interpretation unless the user explicitly asks for and provides constraints for a particular regional tradition. Do not claim a regional attribution from superficial styling.

## Visual Language

- **Figure grammar:** profile or controlled three-quarter reading; recognisable headwear/hair outline, nose/chin contour, torso, sleeves, and clear articulated joints. Do not make the figure a flat, unjointed sticker silhouette.
- **Material and line:** crisp carved perimeter and restrained pierced cutouts that describe garment, prop, or surface structure. Details must remain readable at article size; avoid indiscriminate lace-like perforation.
- **Color and light:** warm backlit screen, translucent dyed reds, ambers, greens, and blue-greens as role-based local color. The light passes through material; it is not opaque vector fill, metallic gold, neon glow, or a photo studio spotlight.
- **Action:** render physical puppet-stage causality through hands, rods, joint angles, prop direction, overlap, and a visible before/after state. Preserve the IP's active role even if control rods are omitted for compositional clarity.
- **Space:** shallow stage/screen space with one dominant figure and sparse supporting silhouette or prop layers. Prefer readable overlap and a short left-to-right or center-outward reading path over deep perspective.
- **Text:** normally no in-image text. If essential, use one or two short Chinese labels only, outside the main puppet silhouette.

## Identity Preservation Rules

Recognition must survive through the same:

- headwear/hair and profile silhouette;
- head-to-body proportion and articulated-joint pattern;
- signature costume cut and practical recurring prop;
- pierced-cutout motif family and controlled density;
- palette roles: warm screen neutral / main translucent garment color / secondary translucent color / dark carved contour / warm action accent / cool balance accent;
- stable backlight direction and shallow-screen composition;
- repeatable action vocabulary: connect, sort, inspect, test, repair, present, guide, transform.

## Best-Fit Use

Use for narrative moments where materiality, visible cause-and-effect, reveal, connection, transformation, guidance, or a story-within-a-screen can clarify an idea:

- explaining an invisible workflow as linked physical parts;
- diagnosing a break and restoring a connection;
- comparing blocked and restored states;
- showing a guide, operator, or maker causing a visible result;
- warm cultural covers where the central idea can be expressed through one decisive stage action.

It is less suitable for dense dashboards, exact UI anatomy, photorealistic portraits, highly nuanced facial emotion, heavy text explanation, or scenes requiring deep spatial realism.

## Base Style Prompt

```text
Chinese shadow-puppetry inspired original narrative illustration, traditional folk-performance and carved translucent-puppet visual language: a recognisable active character with a controlled side-profile or three-quarter silhouette, crisp carved perimeter, restrained pierced-cutout details, clearly articulated joints, role-based translucent dyed red, amber, mineral-green, and blue-green color, warm transmitted backlight through a pale stage screen, shallow layered stage space, one direct causal action and visible result, article-size readability, original character design only; no text.
```

## Avoid

```text
generic Chinese paper-cut, flat red silhouette, opaque vector icon, generic guochao collage, red-and-gold commercial festival poster, New Year-picture print-and-paint, ink wash, gongbi painting, lianhuanhua, woodcut, textile embroidery, opera-costume cosplay, Chinese fantasy game art, random palace scenery, dense ornamental perforation, fully frontal photorealistic face, 3D render, glossy plastic, metallic gold, neon, cinematic smoke, deep-perspective stage, dense UI, text-heavy infographic, passive character beside an already-complete diagram.
```

## Scene Rules

- The IP must cause the explanation. If removing the character leaves the causal reading intact, the scene fails.
- Write the action sentence before every prompt: `The IP is actively [verb] [object] so the reader understands [cognitive anchor].`
- Show one concrete friction and one visible result: disconnected jointed link -> align connector -> restored light path; mixed route tokens -> sort them by hand -> one illuminated route.
- Use the rods, joints, hand position, gaze, prop direction, and light path only when they clarify the action. They are not compulsory decoration.
- Preserve screen-like breathing room. Do not turn every background area into architectural, cloud, floral, or auspicious-symbol ornament.
- Keep the strongest light and color contrast at the action and state change; supporting layers remain quieter.
- Do not invent a regional school name or use a specific regional pattern system without an explicit user requirement and verified source constraints.

## Style QA Additions

Accept only when all are true:

- The IP remains recognisable across visual master and scenes through stable silhouette, articulated-joint grammar, costume/prop shape, cutout pattern family, palette placement, and screen-light relationship.
- The result reads as Chinese shadow-puppetry craft and performance--carved translucent figure plus transmitted screen light--not generic paper-cut, vector silhouette, New-Year poster, guochao collage, or an opaque flat illustration.
- Joint articulation, carved contour, pierced details, and props remain readable at article size; decorative perforation does not obscure the face, hands, action, or result.
- Translucent color is role-based and visibly backlit; it does not become blanket red-gold saturation, neon, metallic luxury styling, plastic gradients, or photorealistic lighting.
- The composition remains shallow, staged, and hierarchical, while the action is physically legible and the IP causes the explanatory transformation.
- The image does not falsely imitate or claim a specific regional shadow-puppetry school without explicit, verified constraints.

Reject or revise when the result becomes a flat paper-cut logo, generic festival graphic, ornate costume collage, a puppet without articulated action, an unrelated theatrical scene, or an image where the IP can be removed without harming the explanation.
