# Metadata And Interoperability

Use this reference for photo/video metadata extraction, catalog edits, sidecars,
color/orientation correctness, write-back, imports, exports, and sharing.

## Preserve, Normalize, And Attribute

Keep three separate concerns where interoperability matters:

1. Preserve raw embedded or sidecar content needed for fidelity.
2. Extract normalized searchable/displayable values.
3. Attribute each value to its source and extraction/write revision.

Do not make a normalized value appear authoritative when it was derived from a
different source or could be stale. Define field-level precedence for embedded
EXIF/IPTC/XMP, sidecars, catalog changes, and later filesystem imports. A catalog
edit to a caption must not overwrite unrelated camera or rights metadata.

## Photo Metadata Checklist

- EXIF: orientation, capture time, camera/lens data, GPS, and embedded thumbnail.
- IPTC/XMP: captions, keywords, ratings, people/places, rights, repeatable and
  namespaced fields.
- ICC: input/output profiles and the color transform used for display/export.
- Timestamps: stored instant, supplied offset/timezone, and local-time ambiguity.
- Encodings: legacy text encodings, malformed values, and lossless preservation.
- Sidecars: association identity, discovery, import/export, rename/move, and
  conflict behavior.

Orientation is presentation data. State whether geometry uses stored pixels or
orientation-normalized display coordinates, then apply that decision consistently
to viewer dimensions, crops, thumbnails, exports, and API responses.

## Video Metadata Checklist

- Model a container separately from video, audio, subtitle, and data streams.
- Extract only required facts: codec/profile, dimensions, duration, timebase,
  frame-rate mode, bitrate, rotation/display matrix, HDR/color transfer, audio
  channels/language, and keyframe locations.
- Define proxy/transcode selection, poster-frame policy, seeking limitations,
  stream-copy versus re-encode behavior, and metadata retention/stripping.

## Privacy And Write-Back

- Classify GPS, face/person labels, camera serials, timestamps, copyright/contact
  fields, captions, and audio as potentially sensitive. Decide what originals,
  previews, shared links, exports, search indexes, logs, and backups retain.
- Apply access control to original and each derivative. A lower-resolution
  thumbnail is not automatically safe to disclose.
- Treat sidecars/embedded metadata as untrusted file content. For XMP/XML, disable
  DTDs, external entities, and parser network resolution; bound document depth,
  node/field counts, and value sizes. Apply equivalent hardening to each parser
  format rather than assuming a field-name allowlist secures the parser.
- Treat filenames, captions, keywords, and all metadata values strictly as data.
  Use contextual output encoding in HTML/Markdown/UI, structured logging,
  parameterized query/index APIs, and spreadsheet-safe export rules. Do not
  interpolate values into SQL, search expressions, templates, logs, paths, or
  commands.
- Define write-back failure/conflict behavior. Do not claim catalog changes
  reached a file until write success is verified.
- Test malformed and deeply nested sidecars, entity declarations, external
  references, control characters, markup/script strings, formula-leading export
  values, and oversized/repeated fields without retaining raw sensitive fixtures.
