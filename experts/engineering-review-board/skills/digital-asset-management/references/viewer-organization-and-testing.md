# Viewer, Organization, And Testing

Use this reference for media-browser interaction, tree views, smart collections,
and confidence planning across domain, persistence, and browser behavior.

## Viewer Behavior

- Define grid, list, filmstrip, timeline, and detail modes; use virtualization
  and appropriately sized thumbnails/proxies for large catalogs.
- Define progressive load, cancellation, placeholders, retry, unsupported-media,
  unavailable-original, stale-preview, and decode-failure states.
- Verify orientation and color-managed presentation. Do not use visual thumbnails
  as authoritative alt text or privacy-safe content.
- Define zoom, pan, fit/fill, comparison, single/multi/range selection, focus
  restoration, and keyboard navigation.
- For video, define poster-frame, load, play/pause, scrub/seek, captions, audio
  track, keyboard, and reduced-motion behavior.

## Tree And Collection Interaction

- Use a tree only when hierarchy navigation is the task; a filtered list may be
  clearer and less complex.
- Define expansion, selection, focus, arrow-key, Home/End, type-ahead, lazy-load,
  rename, delete, and move semantics.
- Preserve accessibility under virtualization. Provide keyboard-accessible moves
  in addition to drag/drop and report cycle/move failures clearly.
- Keep focus, selection, and expansion state distinct. Restore focus after a move
  or delete without silently changing the selected asset/collection.

## Smart Collections

- Expose only validated fields/operators. Define missing versus null metadata,
  text matching, collation, timezone, numeric units, deterministic sort, and
  schema/query-version evolution.
- Test membership changes after metadata edits, renders, imports, and deletion;
  test authorization filtering independently from query matching.

## Test Matrix

| Behavior | Suitable evidence |
| --- | --- |
| Asset/version/edit invariants | Unit or property tests |
| Metadata precedence and hierarchy cycles | Integration/property tests |
| Ingest, queries, caching, authorization | Storage/API integration tests |
| Viewer, tree, selection, playback controls | Browser or native UI E2E tests |
| Virtualized catalog and rendering throughput | Representative performance tests |

Include deterministic, sanitized fixtures for duplicate/perceptually similar
media, missing/conflicting metadata, orientation, profiles, malformed inputs,
sidecars, mislabeled/polyglot media, bounded resource-exhaustion cases, variable
frame rates, multiple streams, and large-catalog pagination. Include authorization
regressions for stale share capabilities, direct identifiers, indexes, workers,
and cached originals/renditions after ACL, privacy, tenant, or deletion changes.

## Behavior Examples

```gherkin
Scenario: Automatic white balance remains reproducible
  Given a photo has an immutable original and an edit recipe revision
  When automatic white balance is applied
  Then the resolved white-balance parameters and algorithm version are recorded
  And the original bytes remain unchanged

Scenario: A collection cannot become its own descendant
  Given a collection has a nested child collection
  When the parent is moved beneath its child
  Then the move is rejected
  And the hierarchy remains unchanged
```
