# Deep Refinement

Use this after the user selects one Visual Master Direction.

## Purpose

Turn a selected direction into a stable reusable IP identity. This step is not another broad exploration round.

## Should This Step Generate Images?

Yes. The main image for this step should be a refined character sheet, because the user has already selected the direction.

The goal is to test whether the chosen direction can remain stable across:

- neutral identity
- basic pose
- teaching/explaining action
- article-scene participation action

## Recommended Image Set

Preferred path: generate one complete character sheet image, then add separate validation images only if the sheet is missing important information.

The character sheet should include:

- main visual master
- front or three-quarter view
- side or back view if useful
- 2-4 expressions
- 1-2 core action poses if space allows
- signature props
- color palette

The refined sheet should also include:

- visible separators between major regions
- lightweight region labels
- enough labeling for orientation, not enough to become a text-heavy design

Minimum labeling expectation:

- main view
- support view
- expressions
- action poses
- palette

Optional extra validation images:

1. Refined visual master: clean character-first reference.
2. Neutral pose: confirms body proportion, outfit, silhouette.
3. Explaining pose: confirms teaching gesture and expression.
4. Scene-participation pose: confirms the IP can actively dissect, diagnose, organize, operate, or navigate.

If the visual master already contains a usable character sheet, generate fewer images and focus on the missing action validation.

Use the earlier visual master direction only as an identity starting point. The refinement output should be more user-readable and easier to review than the direction-stage sheet.

## Lock Summary

After reviewing the validation images, write three lists.

### Must Lock

Identity traits that should remain stable across all future images:

- character subject
- face or head shape
- body proportion
- signature clothing
- core palette
- rendering style
- signature object or motif

### Flexible

Traits that may vary by scene:

- expression
- pose
- background
- supporting props
- label text
- scene composition
- camera angle within the allowed range

### Do Not Lock

Accidental details that should not become part of the identity:

- exact whiteboard text
- accidental badge wording
- one-off card labels
- temporary background layout
- exact pose from a single generated image
- decorative props unrelated to the IP system

## User Confirmation

Ask the user to confirm the lock summary before writing final `visual-spec.md`, `prompt-pack.md`, and `action-library.md`.

The user is not choosing a new direction here. They are confirming what should be fixed, flexible, or excluded.
