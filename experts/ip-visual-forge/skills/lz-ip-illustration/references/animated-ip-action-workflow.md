# Animated IP Action Workflow

Use this workflow when the user asks for an article illustration where the IP action should move, or when an accepted static article illustration should receive a lightweight motion version.

## Positioning

Animated IP action is the **lightweight motion-enhanced version of a static article illustration**.

It is not:

- image-to-video as the default path;
- a character animation short;
- a cinematic clip;
- a full skeletal/rigged animation system;
- a replacement for the static illustration workflow.

Default goal:

```text
static article illustration + one small cognitive action loop
```

## Default Output Contract

Use this as the first production tier unless the user explicitly asks for a richer animation pipeline:

- 3-6 keyframes;
- 1-2 seconds total duration;
- seamless loop;
- one cognitive action only;
- background mostly fixed;
- no camera move by default;
- no full-body performance unless required;
- preserve IP identity, palette, rendering style, and article-size readability;
- output GIF by default, with APNG or MP4 only when requested or platform-required.

This tier is intentionally modest. The animation should make the article's key action clearer, not become a video asset.

## When to Use

Use for:

- `让配图里的 IP 动起来`;
- `做一个文章动图`;
- `生成 GIF`;
- `让这个动作循环一下`;
- an accepted static article illustration with one action beat that benefits from motion;
- Chinese shadow-puppetry scenes where joint movement, light sweep, or restored light-path motion clarifies the idea.

Do not use when the user wants a full video, cinematic motion, full character acting, camera movement, talking avatar, or reusable rig. Those are later tiers and should not be silently substituted for this workflow.

## Required Inputs

Start from an initialized IP and one of these:

1. an accepted static article illustration; or
2. an accepted shot direction before image generation; or
3. a clear user-provided scene brief with one action beat.

If the static image has not been accepted yet, generate and approve the static illustration first. Do not animate a rejected or unstable identity frame.

## Motion Grammar

Choose one motion family per loop:

- **Joint micro-motion**: arm rotates, hand aligns a connector, head/gaze shifts slightly.
- **Light motion**: lantern glow sweeps, restored path brightens, screen backlight pulses.
- **Object motion**: tile/card/route piece slides into place.
- **State transition**: broken/dim state becomes connected/bright.
- **Attention cue**: small highlight pulse around the causal object.

Avoid mixing too many motions. A good article GIF usually has one primary motion and one optional secondary light cue.

## Motion Visibility Rule

Do not claim a motion family unless the pixels visibly support it. A light-only pulse is valid only as **light motion**. If the plan says **joint micro-motion**, at least one joint, hand, rod, or articulated guide must visibly change position or angle. If the plan says **repair**, a connector, tile, patch, knot, plug, or equivalent repair object must visibly move into place before the final restored state appears.

## Chinese Shadow-Puppetry Defaults

For Chinese shadow puppetry, prefer finite puppet-stage motion:

- one articulated arm rotates at the shoulder/elbow;
- a small connector is pushed into a gap;
- a lantern glow sweeps along the route;
- a dark route turns amber after repair;
- joint discs shift subtly;
- warm screen light flickers very slightly.

Keep the puppet silhouette, pierced cutout density, translucent color placement, and warm screen-light relationship stable. Do not turn the result into generic cartoon animation, paper-cut motion graphics, or a cinematic theatre shot.

## Workflow

1. **Load static context**
   - Load `ip-profile.md`, `visual-spec.md`, `prompt-pack.md`, accepted static image, and article/shot context.
   - Identify the one cognitive action that should move.

2. **Write an animation plan**
   - Use `templates/animated-action-plan-template.md`.
   - Define frame count, duration, loop type, moving elements, fixed elements, and success criteria.

3. **Choose frame strategy**
   - Prefer keyframe prompts when image generation can preserve identity from a reference image.
   - Prefer local compositing when the needed motion is just glow, light sweep, pulse, or small object translation.
   - Do not use image-to-video by default for this tier.

4. **Create keyframes**
   - Save one prompt per keyframe under `animation-runs/<scene-slug>/prompts/`.
   - Use `templates/animated-keyframe-prompt-template.md`.
   - Keep fixed identity, palette, style, and camera/composition identical across frames.

5. **Assemble loop**
   - Save frames under `animation-runs/<scene-slug>/frames/`.
   - Assemble GIF under `animation-runs/<scene-slug>/output/action-loop.gif`.
   - Optional: save APNG or MP4 if requested.

6. **QA before handoff**
   - Verify the file opens and loops.
   - Verify frame count, dimensions, duration, and file size.
   - Confirm motion clarifies one article idea.
   - Confirm identity does not drift frame-to-frame.

## Directory Layout

```text
ip-assets/<ip-slug>/animation-runs/<scene-slug>/
  source/
    static-source.png
  storyboard.md
  prompts/
    keyframe-01.md
    keyframe-02.md
    keyframe-03.md
  frames/
    01.png
    02.png
    03.png
  output/
    action-loop.gif
    action-loop.apng      # optional
    action-loop.mp4       # optional
  qa-notes.md
```

## QA Checklist

Accept only when:

- the same IP remains recognisable in every frame;
- the animation has one clear cognitive action;
- the motion improves explanation instead of adding decoration;
- the background and composition do not jitter distractingly;
- labels, if any, remain stable and readable;
- the loop feels intentional at article-reading size;
- the output file opens and loops in a normal viewer or browser.

Reject or revise when:

- the IP face, clothing, palette, rendering style, or body structure drifts;
- motion becomes a generic video effect rather than IP action;
- the action is too large for article reading;
- the loop distracts from the surrounding text;
- the file is too large for practical article use.
