# Zod Patterns And Examples

## Core Concepts

Zod is a runtime schema library: a schema parses `unknown` into output. `z.infer<S>` is output; `z.input<S>` is accepted input; `z.output<S>` makes transformation divergence explicit. `.parse()` returns output or throws, `.safeParse()` returns `{ success, data | error }`, and async refinements/transforms require `.parseAsync()` or `.safeParseAsync()`. Use `.refine()` for a local predicate and object `.superRefine()` to assign cross-field issues.

## Selection

| Situation | Choice |
| --- | --- |
| Internal compile-time-only shape | Plain TypeScript type |
| Existing runtime validator or Standard Schema adapter | Preserve it; do not add Zod absent an explicit migration |
| Existing io-ts or Yup contract | Preserve its conventions and migration evidence |
| New selected JS/TS ingress/egress boundary | Zod schema |
| Small closed-format rule | Explicit validation may be clearer |

Use schema-first `z.infer` when Zod owns the boundary. For type-first compatibility use `z.toZod<T>()` only where the installed version supports it. Never duplicate a hand-maintained interface and schema.

## Composition

Use object spread or `.safeExtend()` instead of long chained `.extend()` calls. Use ordered unions only where ordering is meaningful. Use `z.discriminatedUnion()` for events and intents, strict branch shapes when overlapping branches could both match, and object getters for recursive objects. Use `z.lazy()` for deferred non-object or mutually recursive shapes.

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const UserInput = z.object({ displayName: z.string().trim().min(1).max(80), email: z.email() }).strict();
type UserInput = z.infer<typeof UserInput>;
const value: UserInput = UserInput.parse({ displayName: " Ada ", email: "ada@example.com" });
if (value.displayName !== "Ada") throw new Error("normalization failed");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Address = z.object({ country: z.string().length(2), postalCode: z.string().min(1).max(20) }).strict();
const Profile = z.object({ id: z.uuid(), address: Address }).strict();
if (!Profile.safeParse({ id: "00000000-0000-4000-8000-000000000000", address: { country: "US", postalCode: "1" } }).success) throw new Error("profile");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Intent = z.discriminatedUnion("kind", [z.object({ kind: z.literal("search"), query: z.string().min(1) }).strict(), z.object({ kind: z.literal("open"), resourceId: z.uuid() }).strict()]);
if (Intent.safeParse({ kind: "search", query: "zod", resourceId: "x" }).success) throw new Error("strict branch");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Pagination = z.object({ cursor: z.string().optional(), limit: z.coerce.number().int().min(1).max(100).default(20) }).strict();
if (Pagination.parse({ limit: "1" }).limit !== 1 || Pagination.parse({}).limit !== 20) throw new Error("pagination");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Range = z.object({ start: z.iso.datetime({ offset: true }), end: z.iso.datetime({ offset: true }) }).transform(({ start, end }) => ({ start: new Date(start), end: new Date(end) })).superRefine(({ start, end }, ctx) => { if (end < start) ctx.addIssue({ code: "custom", path: ["end"], message: "end before start" }); });
if (!Range.safeParse({ start: "2026-01-01T00:00:00Z", end: "2026-01-01T00:00:00Z" }).success) throw new Error("range");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Category: z.ZodType<{ name: string; children: unknown[] }> = z.object({ name: z.string(), get children() { return z.array(Category); } });
const Node: z.ZodType<{ value: string; next?: unknown }> = z.lazy(() => z.object({ value: z.string(), next: Node.optional() }));
if (!Category.safeParse({ name: "root", children: [] }).success || !Node.safeParse({ value: "n" }).success) throw new Error("recursion");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Available = z.string().refine(async (name) => name !== "admin", { error: "unavailable" });
void Available.parseAsync("ada").then((name) => { if (!name) throw new Error("async parse"); });
```

## Errors And JSON Schema

Normalize structured issue codes and bounded paths into a stable envelope. Translate only at the adapter/render layer; default library wording is not public API. Keep `reportInput` off without an explicit sanitized policy. Use `z.treeifyError()` and `z.flattenError()` only in presentation adapters.

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Schema = z.object({ id: z.uuid() }); const result = Schema.safeParse({});
if (result.success) throw new Error("expected rejection");
const problem = { code: "invalid_input", issues: result.error.issues.map((issue) => ({ code: issue.code, path: issue.path.slice(0, 8) })) };
if (problem.code !== "invalid_input") throw new Error("mapping");
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Schema = z.object({ id: z.uuid() }).strict();
const jsonSchema = z.toJSONSchema(Schema, { io: "input" });
if (jsonSchema.type !== "object") throw new Error("json schema");
```

<!-- illustrative:unsafe-before -->
```ts
const payload = await response.json() as Payload;
```

<!-- runnable:zod-4.5 -->
```ts
import { z } from "zod";
const Payload = z.object({ id: z.uuid() }).strict();
const response = new Response(JSON.stringify({ id: "00000000-0000-4000-8000-000000000000" }));
void response.json().then((value) => {
  const payload = Payload.parse(value);
  if (!payload.id) throw new Error("boundary parse");
});
```

## Cross-Language Interop

Use `unknown JSON/IPC → Zod boundary schema → plain wire DTO → backend-native deserializer/validator → backend domain type`; reverse through `domain result/error → backend wire serializer → stable JSON envelope → Zod parse → UI/application type`. Specify JSON representations for missing/null, safe integers versus decimal strings, RFC 3339 timestamps, bytes, enum evolution, discriminators, and unknown fields. Use OpenAPI, JSON Schema, protobuf, or versioned JSON fixtures as shared contract; make Zod authoritative only when the repository explicitly chooses and tests generation.

| Concern | Wire representation | Compatibility and validation rule |
| --- | --- | --- |
| Missing / `null` | Omitted field versus JSON `null` | Specify each independently; never silently coerce one to the other. |
| Integers / decimals | JSON safe integer; decimal string when precision exceeds it | Reject unsafe numeric representations and parse decimal strings explicitly. |
| Timestamps | RFC 3339 string with offset | Parse as an instant; retain fractional-second policy in fixtures. |
| Bytes | Base64 or base64url string | State alphabet, padding, maximum decoded size, and decode ownership. |
| Enum evolution | Stable string discriminator/value | Define unknown-value forward-compatibility policy and test it. |
| Discriminators | Required named string field | Use strict, discriminated branch DTOs and exhaustive backend mapping. |
| Unknown fields | Explicit strip, pass-through, or reject rule | Match the public compatibility policy at both boundaries. |

## Tests And Anti-Patterns

Test accepted/rejected boundaries, optional/null/unknown keys, transforms and input/output divergence, sync/async paths, stable mapped errors, JSON Schema parity, and bounded properties only with an existing generator. Reject validation after side effects, repeated parsing, broad coercion, `z.any()`, unsafe assertions, forward-compatibility-breaking strictness, throwing refinements, sync parsing of async schemas, hidden structural refinements, exposed `ZodError`, validator leakage into the core, circular imports, lossless generated-schema claims, and unmeasured compilation.
