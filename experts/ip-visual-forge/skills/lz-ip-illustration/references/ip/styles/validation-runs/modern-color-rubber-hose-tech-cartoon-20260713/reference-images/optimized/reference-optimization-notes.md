# Reference Optimization Notes

The original visual master was preserved as PNG. A separate optimized JPEG reference was generated for image-to-image calls.

Settings:

- Long edge: 1024px
- Format: JPEG
- Quality: 85
- Optimize: true
- Progressive: true

Observed result:

- Original PNG: 1024×1536, 1.773 MB
- Optimized reference: 683×1024, 0.079 MB
- Reduction: about 95.5%

Outcome during this validation:

- Action sheet generation with optimized reference succeeded.
- Workflow-knot scene with optimized reference succeeded.
- Connector/bug scene timed out twice even with optimized reference; simplified connector-only scene succeeded.

Interpretation: reference optimization greatly reduces upload/reference payload size, but it does not eliminate generation-side timeout risk when prompts are complex.
