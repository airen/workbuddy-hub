# MCP SDK, Extension, and Package Baseline

**Retrieved:** 2026-08-01 UTC. This dated evidence record separates the
`2026-07-28` core protocol from independently versioned official SDKs,
extensions, packages, registries, and host policy. It neither authorizes package
installation nor selects a dependency for a target repository. Recheck the
official SDK index and the target repository's resolved dependency before use.

## Selection and evidence discipline

Use an official SDK appropriate to the target language, then verify its declared
core revision, extension, transport, lifecycle, and shutdown support against the
target repository's manifest, lockfile, supported clients, and test policy. The
official SDK index is authoritative for its *retrieval-time* tier assignment;
the tier policy explains what that assignment commits to ([S1], [S2]). It is not
a package pin, a feature-by-feature product matrix, or an execution record.

- Select behavior that explicitly supports core revision `2026-07-28`; an SDK
  upgrade does not by itself change wire behavior ([S3]). Language SDK releases
  and core protocol revisions have independent cadences.
- Core schema authority remains the dated specification: its TypeScript schema is
  the source of truth; generated JSON Schema is for tooling; implementations
  must support JSON Schema 2020-12 when `$schema` is absent ([S4]). Standard
  bindings are stdio and Streamable HTTP; protocol cancellation and
  transport/process shutdown are distinct responsibilities ([S5]).
- The official conformance repository provides trace/schema validation, client
  and server scenarios, and saved `checks.json` results; no test was run for
  this baseline ([S6]). A tier assignment is not a locally reproduced result.
- Record the resolved dependency in the target repository, not here. A dual-era
  implementation is an explicit compatibility choice; test every advertised
  revision ([S3], [S7]).

## Selected language lanes

The following are deliberately dated selection records, not a mutable support
matrix. “Documented” means the cited official project material describes the
surface; it does not establish compatibility with an arbitrary target, extension,
host, runtime, or prior protocol revision.

### C# — include as a Tier 1 implementation lane

- **Authority, retrieval, and tier:** The official MCP SDK index retrieved
  2026-08-01 lists `modelcontextprotocol/csharp-sdk` as **Tier 1** ([S1]); the
  project repository and releases are first-party SDK sources ([S8], [S9]).
- **Exact package, status, and protocol:** NuGet records the
  `ModelContextProtocol` **2.0.0** release ([S10]); its official 2.0.0 release
  calls it stable alignment with MCP **2026-07-28**, not a prerelease ([S9]).
- **Documented support:** the repository identifies Core, hosting, ASP.NET Core,
  Apps, and Tasks packages ([S8]); the stable release documents
  discovery-first negotiation, stateless-by-default HTTP, standard headers, and
  JSON Schema 2020-12 output schemas ([S9]). Use resolved-version API docs for
  exact transport setup, disposal/cancellation, and shutdown; they were not
  independently executed here.
- **Conformance, uncertainty, and rationale:** Tier 1 has the policy's 100%
  conformance and maintenance commitment ([S2]), but no C# fixture or result was
  run or imported. Verify the package, .NET target, stdio or Streamable-HTTP
  shutdown path, schemas, and project test/conformance fixture. **Include C#:**
  current authoritative tier and stable 2026 release retain the substantive lane.

### Python — include as a Tier 1 implementation lane

- **Authority, retrieval, and tier:** The official index retrieved 2026-08-01
  lists `modelcontextprotocol/python-sdk` as **Tier 1** ([S1]); its repository
  and release page are first-party SDK evidence ([S11], [S12]).
- **Exact package, status, and protocol:** PyPI records the `mcp` **2.0.0**
  release ([S13]); the official 2.0.0 release is stable, supports
  **2026-07-28** and earlier revisions, while 1.x is security-fixes-only
  maintenance ([S12]).
- **Documented support:** stdio, Streamable HTTP, SSE, typed schema generation,
  URL/stdio/custom/in-memory client targets, and in-memory test support are
  documented ([S11]). The release documents stateless discovery and both
  protocol eras ([S12]). Use the resolved version's async context/lifespan docs
  for cleanup; no standalone shutdown guarantee was inferred from an example.
- **Conformance, uncertainty, and rationale:** Tier 1 has the policy's 100%
  conformance and maintenance commitment ([S2]); no Python test or conformance
  result was run. Verify `mcp`/`mcp-types` lockstep resolution, schema dialect,
  selected transport cleanup, and target fixture. **Include Python:** current
  official evidence retains the substantive lane.

### TypeScript — include as a Tier 1 implementation lane

- **Authority, retrieval, and tier:** The official index retrieved 2026-08-01
  lists `modelcontextprotocol/typescript-sdk` as **Tier 1** ([S1]); its
  repository and release notes are first-party SDK sources ([S14], [S15]).
- **Exact package, status, and protocol:** select the split v2 packages
  `@modelcontextprotocol/server` **2.0.0** and
  `@modelcontextprotocol/client` **2.0.0** ([S15]), the stable v2 line for
  **2026-07-28** ([S14]). Do not substitute legacy
   `@modelcontextprotocol/sdk` **1.30.0** merely because that v1 release is
   published ([S16]); it is a different v1 line.
- **Documented support:** v2 documents stdio, Streamable HTTP, client transports,
  runnable examples, and Standard Schema input/prompt adapters ([S14]); release
  notes document final versioned wire schemas and an end-to-end test suite
  ([S15]). Resolve close/abort behavior from the selected package API and test
  it; `connect()` is not proof of process shutdown ownership.
- **Conformance, uncertainty, and rationale:** Tier 1 has the policy's 100%
  conformance and maintenance commitment ([S2]); no package, fixture, or
  conformance run occurred. Verify v2 package lockstep, runtime (Node/Bun/Deno),
  schema adapter, and chosen transport cleanup. **Include TypeScript:** current
  official evidence retains the substantive lane.

### Rust — include only as a qualified Tier 2 implementation lane

- **Authority, retrieval, and tier:** The official index retrieved 2026-08-01
  lists `modelcontextprotocol/rust-sdk` as **Tier 2** ([S1]); the project
  repository and releases are first-party SDK sources ([S17], [S18]).
- **Exact package, status, and protocol:** the latest listed stable release is
  `rmcp` **3.1.0** ([S18]); the 3.0 stable release added MCP **2026-07-28**
  support, while the repository documents compatibility with prior releases
  ([S17], [S18]). The package is stable; **Tier 2 remains a limitation**, not
  evidence of Tier 1 completeness.
- **Documented support:** the SDK documents stdio, Streamable HTTP,
  protocol/lifecycle negotiation, JSON Schema 2020-12, generated schemas, and
  explicit `waiting()`/`cancel()` shutdown behavior ([S17]). Its 3.0 release
  records conformance-oriented tests and full-conformance CI, but no per-target
  result is claimed here ([S18]).
- **Conformance, uncertainty, and rationale:** Tier 2 means active work toward
  full support, at least 80% policy conformance, a stable release, and a roadmap;
  it is not a 100% guarantee ([S2]). Verify exact crate version, feature flags,
  Tokio/runtime, lifecycle mode, transport shutdown, schemas, and the target
  fixture. **Include Rust only with this qualification:** the planned lane remains
  valid and does not expand.

### Ruby — routing-only while Tier 3

- **Authority, retrieval, and tier:** The official index retrieved 2026-08-01
  lists `modelcontextprotocol/ruby-sdk` as **Tier 3** ([S1]); the repository,
  release page, and RubyGems record are official project/package evidence
  ([S19], [S20], [S21]).
- **Exact package, status, and protocol:** `mcp` **1.0.0** is a non-prerelease,
  first-stable API release ([S20], [S21]). Its README documents stdio and
  Streamable HTTP/SSE, JSON Schema 2020-12 output schemas, cancellation, and
  legacy/session and draft discovery material ([S19]). That does **not** prove
  that `mcp` 1.0.0 fully implements final core revision 2026-07-28.
- **Lifecycle, test uncertainty, and rationale:** the docs describe HTTP
  `DELETE` session termination and stdio frame close limits ([S19]), but no
  retrieved official conformance result or target-neutral shutdown/test contract
  establishes Tier 1 or Tier 2 coverage. **Tier 3 limitation:** it has no minimum
  conformance, stable-release, or update-timeline requirement ([S2]); a stable
  gem API does not override that limitation. **Defer Ruby** as an implementation
  lane; retain `ruby-engineering` only for routing/ordinary Ruby mechanics.

## Official extensions, packages, and hosts

| Surface | Boundary and required decision |
| --- | --- |
| Core MCP | Follows the dated core specification and independent capability/version negotiation ([S3]). |
| MCP Apps | An official optional extension, `io.modelcontextprotocol/ui`, whose immutable commit records the stable `2026-01-26` specification ([S22]). Its UI lifecycle is negotiated separately and does not become core lifecycle law ([S22], [S23]). |
| Apps SDK and hosts | Implementation support and rendering/permission policy are package- and host-specific. Obtain current extension and intended-host evidence; retain useful text/structured fallback. |
| Other extensions | Official status does not make an extension core-mandatory. Tasks, for example, requires its own negotiation/version evidence ([S24]). |
| MCPB | Portable MCP-project packaging outside the core wire protocol. Bundle manifest, loader, CLI, registry, and distribution are package/host/supply-chain decisions ([S25], [S26], [S27]). |

For MCP Apps work: obtain current extension and intended-host evidence; negotiate
the extension; keep useful text and structured outputs when rich UI is absent;
add frontend, JavaScript, CSS, UX/accessibility, and security companions when
their triggers apply; and test the intended host. Do not treat a directory rule,
callback URL, screenshots, host limits, or a vendor template as core MCP.

MCPB is appropriate only when local-server packaging/distribution is explicit. It
does not replace stdio/Streamable HTTP conformance. Review bundle runtime,
provenance, registry, install, and publication decisions with the appropriate
supply-chain and security skills before acting.

## Large fixed action surfaces

Use searchable discovery plus execution by stable action ID only for a genuinely
large, fixed action surface where a curated ordinary tool list no longer provides
usable discovery. No universal numeric threshold decides that question.

- Discovery returns stable action IDs and enough safe metadata to choose an
  action. Execution accepts an ID only, not arbitrary command text, endpoints,
  or opaque payload dispatch.
- Each action retains its own schema, authorization, consent/confirmation,
  auditability, side-effect/retry/reconciliation semantics, and actionable
  errors. Validate the selected action and arguments at execution time.
- Keep the surface fixed or governed by an explicit reviewed registry. Do not turn
  this pattern into a universal dispatcher for arbitrary code, endpoints, or
  payloads.

## Example and plugin rule

The official development-skills documentation describes a reference
`mcp-server-dev` plugin and examples ([S28]). Those materials, installed
plugins, and host/vendor examples are non-authoritative for core protocol facts.
This baseline did not install or execute a plugin, package, server, App, MCPB
tool, browser flow, or filesystem-effect example.

## Sources

All sources were retrieved 2026-08-01. `modelcontextprotocol.io` and the
`modelcontextprotocol` GitHub organization are official MCP project authorities;
package registries are primary package metadata, not tier or protocol authority.

- [S1] [Official SDK index](https://modelcontextprotocol.io/docs/2026-07-28/sdk) — official retrieval-time SDK tier assignments and repositories.
- [S2] [SDK Tiering System](https://modelcontextprotocol.io/community/sdk-tiers) — official tier, stable-release, conformance, maintenance, and relegation policy.
- [S3] [Core versioning and compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning) — normative core revision `2026-07-28`.
- [S4] [Core specification overview and schema](https://modelcontextprotocol.io/specification/2026-07-28/basic) — normative schema authority and JSON Schema dialect.
- [S5] [Core transport bindings](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) — normative stdio, Streamable HTTP, and cancellation boundaries.
- [S6] [Official conformance repository](https://github.com/modelcontextprotocol/conformance) — official test harness, trace/schema checks, results, and SDK runner.
- [S7] [TypeScript SDK 2026-07-28 migration](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28.html) — official SDK compatibility guidance.
- [S8] [C# SDK repository](https://github.com/modelcontextprotocol/csharp-sdk) — official C# package/documentation authority.
- [S9] [C# SDK v2.0.0 release](https://github.com/modelcontextprotocol/csharp-sdk/releases/tag/v2.0.0) — official stable release and 2026-07-28 support record.
- [S10] [NuGet: ModelContextProtocol 2.0.0](https://www.nuget.org/packages/ModelContextProtocol/2.0.0) — primary package metadata.
- [S11] [Python SDK repository](https://github.com/modelcontextprotocol/python-sdk) — official Python SDK/documentation authority.
- [S12] [Python SDK v2.0.0 release](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0) — official stable release, revision, maintenance, and known-gaps record.
- [S13] [PyPI: mcp 2.0.0](https://pypi.org/project/mcp/2.0.0/) — primary package metadata.
- [S14] [TypeScript SDK repository](https://github.com/modelcontextprotocol/typescript-sdk) — official v2 docs, status, transports, schemas, and examples.
- [S15] [TypeScript SDK v2.0.0 release](https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/%40modelcontextprotocol%2Fserver%402.0.0) — official package/revision/test record.
- [S16] [npm: @modelcontextprotocol/sdk 1.30.0](https://www.npmjs.com/package/@modelcontextprotocol/sdk/v/1.30.0) — primary legacy v1 release metadata.
- [S17] [Rust SDK repository](https://github.com/modelcontextprotocol/rust-sdk) — official RMCP docs, protocol, transport, schema, and shutdown record.
- [S18] [Rust SDK releases](https://github.com/modelcontextprotocol/rust-sdk/releases) — official RMCP stable-release and conformance/CI record.
- [S19] [Ruby SDK repository](https://github.com/modelcontextprotocol/ruby-sdk) — official Ruby transport, schema, and lifecycle documentation.
- [S20] [Ruby SDK releases](https://github.com/modelcontextprotocol/ruby-sdk/releases) — official first-stable release record.
- [S21] [RubyGems: mcp 1.0.0](https://rubygems.org/gems/mcp/versions/1.0.0) — primary gem metadata.
- [S22] [MCP Apps 2026-01-26 specification, immutable v1.0.0 commit](https://github.com/modelcontextprotocol/ext-apps/blob/298e884ec3f02daba085acdb02042d73bd00b355/specification/2026-01-26/apps.mdx) — official stable extension specification; the commit records the `2026-01-26` stable release.
- [S23] [MCP Apps repository](https://github.com/modelcontextprotocol/ext-apps) — official extension support boundary.
- [S24] [Core changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — normative core/extension boundary.
- [S25] [MCPB adoption announcement](https://blog.modelcontextprotocol.io/posts/2025-11-20-adopting-mcpb/) — official project communication.
- [S26] [MCPB repository](https://github.com/modelcontextprotocol/mcpb) — official project packaging repository.
- [S27] [MCP Registry package types](https://modelcontextprotocol.io/registry/package-types) — official registry preview policy.
- [S28] [Build with Agent Skills](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-with-agent-skills) — official guidance/example, not normative core or package specification.
