---
name: mcp-server-engineering
description: >-
  MCP server engineering guidance. Use when creating, updating, refactoring,
  testing, or reviewing Model Context Protocol servers, tools, resources,
  prompts, capability discovery, stdio transport, Streamable HTTP, or legacy
  HTTP+SSE compatibility. Do not use merely to operate an existing MCP server;
  use the applicable provider or service skill instead.
---

# MCP Server Engineering

Use this skill to build or change an MCP server without tying the design to one
language, SDK, host, or package. Inspect the target repository, dependency
policy, known clients, and current official MCP documentation before selecting
implementation details.

## Load the right detail

Keep this file for activation, ownership, project discovery, implementation, and
non-negotiable safety rules. Load a directly linked reference when its subject
is in scope:

| Need | Load |
| --- | --- |
| A dated wire rule, lifecycle, transport, authorization, MRTR, elicitation, or extension-negotiation decision | [Protocol baseline — 2026-07-28](references/protocol-2026-07-28.md) |
| SDK choice, MCP Apps, MCPB packaging, host policy, or a large fixed action surface | [SDK, extension, and package baseline](references/sdk-selection.md) |

The dated core specification governs core MCP. SDK releases, extension releases,
packages, registry rules, and host policy do not silently change that contract.

## Boundaries and required handoffs

- This skill owns MCP-facing contracts, capability composition, and server
  workflow. The repository's language skill owns SDK APIs, package setup, types,
  runtime mechanics, and test commands.
- Load [`api-design`](../api-design/SKILL.md) for material public compatibility,
  schema, error-contract, or versioning decisions.
- Route trust-boundary design—users, principals, tenants, assets, data flows,
  abuse cases, and residual risk—to
  [`threat-modeling`](../threat-modeling/SKILL.md). Load
  [`security-review`](../security-review/SKILL.md) and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) for
  implemented controls involving identity, secrets, external input, files,
  commands, network access, remote effects, or sensitive data.
- Load [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
  before adding or changing an SDK, transport library, generated code, package,
  lockfile, install script, bundle runtime, or registry publication.
- Do not install, execute, configure, operate, or mutate data through an
  existing server merely to develop its guidance or implementation unless that
  is separately authorized.

## Pre-implementation brief

Write this compact brief before selecting an SDK or exposing a capability:

1. **Target:** integration and deployment shape; intended users, principals,
   tenants, and trust boundaries.
2. **Effects:** local and remote effects, the upstream systems involved, and
   whose authorization governs each effect.
3. **Action surface:** qualitative pressure for a small curated surface versus a
   genuinely large fixed surface; do not use a numeric tool-count threshold.
4. **Interaction:** text, structured input, elicitation, and rich-UI needs.
5. **Compatibility:** intended clients, core revisions, separately negotiated
   extensions, and expected fallbacks.

Treat this as design input, not a permission grant. Revisit it when a new
principal, upstream, side effect, or host is introduced.

## Core design rules

### Primitives and contracts

- A **tool** is a named action with bounded schema-defined input and, when
  useful, structured output. A **resource** is retrievable context at a stable
  URI. A **prompt** is an explicit user-selected reusable message template; it
  is not hidden authority or a system-prompt-injection channel.
- Treat tool/resource/prompt arguments, client metadata, upstream data, and
  returned embedded content as untrusted. Canonicalize before authorization when
  representation ambiguity could bypass policy.
- Use a stable, specific name and description for each exposed primitive. State
  selection conditions, preconditions, effects, retry behavior, limits, and
  result meaning. Keep input objects closed where practical, validate schema and
  domain invariants server-side, and use opaque identifiers instead of internal
  paths or implementation objects.
- Return concise text for model use and structured content for machine use;
  validate declared structured output before returning it. Paginate or summarize
  large results rather than flooding context.
- Do not mirror credentials, tokens, API keys, personal data, or similarly
  sensitive schema fields into HTTP headers; intermediaries and logs commonly
  expose them. Keep prompt arguments and embedded resource content transparent,
  validated, and unable to smuggle authority or bypass host policy.
- Separate protocol/transport adapters from authorization-aware application
  operations and underlying infrastructure. Registration must be explicit and
  deterministic, not dependent on import order or transient connection state.
- Keep resources canonical, authorization-checked, and free of credentials.
  File-backed access needs a defined containment and symlink policy; route its
  race-resistant implementation and review to `security-review`.

### Capability and compatibility discipline

- Discover the selected core revision and declared client/server capabilities
  before use. Advertise only versions, primitives, notifications, subscriptions,
  extensions, and optional interactions that are implemented and tested.
- Choose optional behavior from declared capabilities, negotiated extensions,
  and the selected revision—not a client product name or version label. Never
  send an unsupported optional interaction.
- When an optional capability is absent, preserve semantics with a useful
  fallback where feasible; otherwise return the selected revision's applicable
  missing- or unsupported-capability error. Fallbacks are interoperability
  guidance, not universal protocol law.
- Treat changes to names, descriptions, schemas, URIs, capability declarations,
  error semantics, authorization scope, defaults, effects, transport, and
  supported revisions as externally observable contracts. Prefer additive
  optional changes, a new narrow primitive, or an explicit migration over an
  in-place break.

### Effects, errors, and cache safety

- Authorize every operation and referenced object at execution time. A tool
  name, client claim, connection, opaque handle, or host approval is not proof
  of authorization.
- Make reads side-effect free apart from bounded telemetry and caching. For a
  mutation, state idempotency and reconciliation behavior; bind idempotency
  records to the authenticated principal, operation, and relevant request
  digest. Provide preview/validate before high-impact apply where useful.
- Apply least-privilege credentials, rate limits, and resource budgets to every
  underlying system. Command-backed actions use a fixed executable allowlist and
  structured arguments without shell interpolation; constrain process
  environment, working directory, filesystem/network access, runtime, and
  privileges. Schema-valid input never makes an arbitrary command safe.
- Require explicit host/user approval for sensitive actions and recheck
  server-side authorization. Neither approval nor tool availability replaces the
  other control.
- Map malformed protocol requests and unknown methods to protocol errors; map
  recoverable execution outcomes to safe, actionable operation errors. Do not
  leak stack traces, private paths, tokens, SQL, or raw upstream responses.
- Cache only when the selected revision permits it. Partition private data by
  the authorization context, never use a cache label as access control, and do
  not cache multi-round input-required results or retries carrying returned
  state/input responses.

### MRTR state safety

Multi-round interactions need opaque state that is safe when a client returns
it. Treat returned state as attacker-controlled; integrity-protect state that
affects authorization, access, or logic; bind it to the authenticated principal,
short expiry, method, and security-relevant request digest; and verify every
binding on retry. For a replayable write or unsafe effect, atomically consume a
server-side nonce/state identifier. Test tampering, wrong-principal reuse,
expiry, request mismatch, and replay. The dated MRTR and elicitation lifecycle
is in the [protocol baseline](references/protocol-2026-07-28.md#mrtr-and-elicitation).

### Transport and runtime

- Use stdio for a client-launched local child process. Send only newline-delimited
  UTF-8 JSON-RPC on stdout; send sanitized diagnostics to stderr; do not rely on
  the launcher’s working directory or full shell environment.
- Use the selected current remote transport for independently deployed services.
  Keep one request's transport framing, authentication middleware, and startup
  outside domain operations; bound size, time, concurrency, cancellation, and
  cleanup. Validate Origin and use HTTPS outside explicitly bounded local
  development.
- Validate protocol metadata and any mirrored transport metadata, rejecting
  disagreement rather than silently choosing one. Keep authentication at the
  service boundary and repeat authorization for every operation/object.
- For remote upstream access, use least-privilege credentials issued for that
  upstream; never pass an MCP-client bearer token through to an upstream service.
  Defend URL-fetching and metadata discovery against SSRF, redirects, rebinding,
  and disallowed network targets according to deployment policy.

## Implementation workflow

1. **Inventory and brief.** Inspect repository conventions, existing discovery
   output, registrations, handlers, schemas, tests, client fixtures, deployment,
   and the pre-implementation brief. Load the dated protocol reference and
   relevant SDK/extension reference before choosing their behaviors.
2. **Choose the smallest coherent surface.** Select one transport and a narrow
   primitive. Define its authorization boundary, schemas, outputs, effects,
   error categories, limits, and compatibility/fallback behavior before adding
   dependencies.
3. **Implement thin adapters.** Decode/validate, authorize, invoke a
   transport-independent operation, map results, and clean up/cancel bounded
   work. Keep secrets out of source, schemas, descriptions, URIs, outputs,
   logs, fixtures, screenshots, and traces.
4. **Declare and compose deliberately.** Synchronize discovery, capability
   declarations, schemas, list ordering, notifications, documentation, and
   supported revisions. Treat core, extensions, packages, and host policy as
   separate decisions below.
5. **Compare and prove.** Capture a before/after contract for updates and
   refactors. Test every advertised revision, transport, capability, and
   intended host; report skipped coverage and sanitized residual risk.

## Core, extension, package, and vendor boundaries

- **Core MCP:** follows the selected dated specification.
- **MCP Apps:** an official optional extension, independently versioned and
  host-dependent. It requires extension negotiation and does not make UI support
  a core requirement.
- **MCPB:** portable MCP-project packaging outside core MCP. Its manifest,
  loader, and CLI behavior are package concerns, not wire-protocol rules.
- **SDKs:** Apps SDK and MCPB CLI mechanics are package-specific; select and
  validate them from target-repository evidence, never a fixed version here.
- **Vendors/hosts:** directory listings, callback URLs, screenshots, host limits,
  templates, and comparable requirements are vendor/host policy, not core MCP.
- **Apps delivery:** obtain current extension and intended-host evidence;
  negotiate the extension; retain meaningful text/structured fallbacks; include
  frontend/JavaScript/CSS/UX/security companion skills as their triggers apply;
  and test the intended host. Load the [SDK, extension, and package baseline](references/sdk-selection.md#official-extensions-packages-and-hosts).

## Validation

- Schema-check inputs and declared outputs; assert unique names, stable URIs,
  valid prompt arguments, bounded inputs, and deterministic unchanged lists.
- Test success, malformed/boundary input, authorization denial, missing objects,
  upstream failure, timeout, cancellation, partial failure, redaction,
  idempotent retry, and reconciliation as applicable.
- Exercise discovery, list, invoke/read/get, unknown names/URIs, pagination,
  transport metadata disagreement, selected cache behavior, and every declared
  capability. Confirm unsupported interactions are neither advertised nor sent.
- For stdio, prove clean stdout, stderr diagnostics, framing, unexpected working
  directory, missing configuration, and shutdown. For remote deployment, prove
  authentication, Origin policy, request limits, concurrent clients,
  cancellation, and proxy behavior as applicable.
- Use a protocol-aware inspector first, then the intended host. Confirm only
  implemented capabilities appear, errors are actionable and sanitized, and no
  hidden connection-local assumption survives restart.

## Explicit exclusions

Do not treat any of these as current core MCP guidance:

- pre-2026 session, initialization-handshake, or independent server-request
  examples; `logging/setLevel`; or new Roots, Sampling, or Logging adoption;
- a remote scaffold from official documentation as production-ready security
  code, or stale `2025-11-25`/`2026-03` ledgers as current authority;
- a directory character limit, vendor callback/auth/screenshot/payload/CIDR
  policy, or a Cloudflare scaffold as MCP law;
- “instructions as system prompt injection” framing;
- fixed SDK, framework, or package versions; Apps SDK mechanics as core MCP; or
  MCPB manifest/CLI behavior as core MCP;
- a fixed numeric tool-count threshold, an arbitrary command/endpoint/payload
  dispatcher, lexical path resolution as proof of symlink-safe containment, or
  large external code blocks copied verbatim.

## Completion evidence

Report changed MCP contracts and their compatibility class; tested revisions,
transports, capabilities, and intended hosts; schema/unit/integration/inspector
results; the baseline or fixtures compared; skipped checks; and sanitized
security, migration, and interoperability risk.

## Zod Adapter Routing

Zod is only a resolved TypeScript SDK or Standard Schema adapter; load [`zod-engineering`](../zod-engineering/SKILL.md) for mechanics. MCP JSON Schema dialect, capabilities, authorization, and conformance remain authoritative; test malformed inputs and schema bridges.
