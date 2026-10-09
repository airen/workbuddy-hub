# Catalog, Persistence, And Organization

Use this reference when a DAM change affects asset identity, database schema,
search, collection membership, or hierarchy behavior. Use the SQL skills for
database-specific implementation and migration mechanics.

## Model Independent Facts

Do not use a single `file` record to mean all of the following. They change at
different times and need different retention and authorization behavior.

| Fact | Typical responsibility |
| --- | --- |
| Logical asset | Stable user-facing identity and lifecycle |
| Media file | Stored bytes, URI, hash, size, MIME type, provenance |
| Original | Immutable import source and preservation policy |
| Rendition | Generated thumbnail, preview, proxy, or export |
| Edit recipe | Ordered, reproducible operation parameters |
| Asset version | Restorable user-visible revision or branch |
| Metadata value | Raw/normalized value, source, extraction revision |

Use names that preserve the distinction in the target domain. The following is a
conceptual relationship map, not a required schema:

```text
asset -> media_file(role: original | imported_copy)
asset -> asset_version -> edit_recipe -> edit_operation
asset_version -> rendition(role: thumbnail | preview | proxy | export)
asset -> metadata_value(source: embedded | sidecar | catalog)
asset <-> tag
collection <-> asset
collection -> parent_collection
smart_collection -> validated_query
```

## Schema And Invariants

- Give persistent identities stable primary keys. Record byte hashes separately
  from filenames and paths; a rename must not create an unrelated asset.
- Use foreign keys and constraints for required lifecycle relationships. Define
  source deletion, soft deletion, retention expiry, rendition garbage collection,
  and restore behavior.
- Keep many-to-many tags/manual collection memberships relational. Do not use
  arrays or JSON blobs when membership requires integrity, ordering, metadata, or
  authorization checks.
- Store semi-structured raw metadata only when needed for fidelity; promote
  routinely filtered facts to normalized columns or indexes.
- Create indexes from browse/search paths: asset ordering, membership, tag
  filters, capture/import time, ratings, and selected metadata. Verify plans at
  representative catalog sizes.
- Store a smart collection's query-language version with its expression. Validate
  it before persistence; never treat it as arbitrary client-supplied SQL.

## Ingest And Duplicate Semantics

| Input condition | Decision to specify |
| --- | --- |
| Same byte hash | Reuse, reject, another import record, or another asset |
| Perceptually similar image | Candidate only, automatic duplicate, or no deduplication |
| Same source path changed | New original, replacement, or external-change conflict |
| Retry after partial import | Idempotency key, cleanup, and visible job state |
| Extractor failure | Asset visibility, error state, retry, and source preservation |

Content identity and perceptual similarity must not be silently conflated. A
perceptual hash can aid search; it does not prove byte identity or ownership.

## Collections, Tags, And Hierarchies

- Specify whether folders model physical locations, a user-facing hierarchy, or
  both. A manual collection is normally membership, not a filesystem directory.
- Specify whether tags can nest, whether child implies parent, and whether a
  resource may have several parents. Do not infer this from the UI.
- Enforce no self-parent or descendant-parent moves. Make subtree moves atomic
  enough that concurrent moves cannot create a cycle.
- Define root behavior, sibling-name uniqueness, ordering, move, delete, detach,
  reparent, and parent-authorization rules.
- Define whether a smart collection is live or snapshot. For live membership,
  apply authorization before results are returned and define metadata/edit/delete
  updates.

## Persistence Tests

- Test idempotent imports, duplicate classification, failed extraction, and
  original preservation against real storage/database boundaries.
- Property-test hierarchy acyclicity and concurrent move conflict behavior.
- Test metadata precedence and smart-query validation/evolution with fixed,
  sanitized fixtures.
- Test rendition invalidation after source, recipe, orientation, color, or
  authorization changes.
