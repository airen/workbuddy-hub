# Zod 4.5 Baseline

Dated source record for Zod 4.5. Target repositories may use another version;
inspect the installed package and migration evidence before applying this record.

## Parsing And Validation

`.parse()` returns a deep-cloned typed output or throws; safe parsing returns a
discriminated result; async refinements/transforms require async parsing.
`z.validate()` and `z.validateAsync()` answer validity without producing
normalized output or diagnostics, so they must not replace parsing when
coercion, transforms, defaults, or error details matter.

## Compilation

`z.compile()` compiles the final schema, not an intermediate; derived schemas
are uncompiled. Invalid inputs still fall back to the normal parser. Async,
recursive, coercion, `z.xor()`, custom-`when`, and callback-`.catch()` cases
are unsupported or partially fall back; use `{ strict: true }` to surface the
refusal instead of returning the runtime schema. Global `import "zod/compile"`
is application-only. Generated `new Function` code requires a CSP/security
decision and a local benchmark.

## Performance

Zod 4.5's reported speedups, faster safe-failure path, and schema-memory
reduction are upstream measurements, not target-repository performance evidence.
Benchmark representative valid, invalid-with-diagnostics, boolean-validation,
schema-construction/reuse, transformation, depth, and async workloads first.

## Upgrade And Migration Checks

Before a 4.5 upgrade, fixture seconds in offset/`Z` datetimes, Unicode-code-point
string lengths, record/intersection behavior, stricter string formats, and
unconditional stripping of `__proto__`. For Zod 3-to-4, audit the unified
`error` parameter, deprecated string-format instance helpers, `z.nativeEnum`,
`z.promise`, error-formatting APIs, record exhaustiveness, defaults inside
optionals, unknown-key behavior, and input/output/JSON-Schema parity. Remove
obsolete aliases rather than retaining dual-era examples.

## Official Sources

- [Zod 4.5 announcement](https://zod.dev/blog/zod-4-5)
- [Basic usage](https://zod.dev/basics)
- [Schema API](https://zod.dev/api)
- [Error customization](https://zod.dev/error-customization)
- [Error formatting](https://zod.dev/error-formatting)
- [JSON Schema conversion](https://zod.dev/json-schema)
- [AOT compilation](https://zod.dev/compile)
- [Zod 4 migration guide](https://zod.dev/v4/changelog)
