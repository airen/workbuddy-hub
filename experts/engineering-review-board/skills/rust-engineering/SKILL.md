---
name: rust-engineering
description: Core Rust engineering guidance. Use when adding or changing Rust crates, modules, public APIs, domain logic, ownership and lifetime structure, traits, generics, error types, feature flags, workspaces, refactors, design patterns, or declarative/procedural macros. Do not use for checked-in hosted CI/release-provider or Docker/OCI/Compose configuration except the Rust commands they invoke; use ci-release-engineering or container-engineering. Use api-design for public service/SDK/CLI contracts, observability-engineering for telemetry/logging signal design, rust-testing-quality for test and CI lanes, rust-async-web for Tokio/Axum/Leptos work, rust-desktop-gui for native desktop GUI frameworks and delivery, rust-persistence-sql for SQLx, SeaQuery, and database adapter work, and rust-code-review for requested reviews.
---

# Rust Engineering

Use this skill for project-neutral Rust implementation and refactoring. Keep the
guidance grounded in the repository's existing architecture, toolchain, and
public contracts.

## MCP SDK Composition

For MCP implementation, load
[`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) and its dated
[SDK selection record](../mcp-server-engineering/references/sdk-selection.md).
The selection record is the canonical source for the selected Rust lane's
retrieval-time authority, package/version, tier, core-revision, transport, and
conformance caveats. It is not a target-repository pin or local test result.

## MCP Rust Mechanics

Use this section only after loading
[`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) and its dated
[SDK selection record](../mcp-server-engineering/references/sdk-selection.md).
The parent owns MCP revision, capability, and transport rules; this section owns
Cargo, Rust API, Tokio, schema, shutdown, and test mechanics.

- **Discover and resolve the crate deliberately:** inspect workspace dependency
  declarations, `Cargo.lock`, feature flags, `rust-toolchain`, target support,
  and CI before adding or selecting `rmcp`. Resolve the exact crate version and
  enabled transport/runtime features through the repository's Cargo graph, then
  read that release's docs. Do not infer unqualified support, enable every
  feature, or add a crate merely to explore its API.
- **Keep service and transport adapters separate:** implement the SDK's resolved
  service/handler traits over typed application operations, then construct the
  SDK server/client and chosen transport in `main`, a dedicated adapter module,
  or the runtime composition root. Keep SDK sessions, transport handles, and
  generated request types outside domain APIs; let conversion code be explicit
  and small.
- **Use Tokio ownership and cancellation idiomatically:** make task ownership
  visible, propagate cancellation through owned work, retain/join spawned task
  handles, and drive the selected SDK's documented `waiting()`/`cancel()` or
  equivalent close path from the application shutdown owner. Never detach an
  SDK transport task and assume Tokio runtime drop or process exit performs
  orderly cleanup; confirm selected-feature and transport behavior in its docs.
- **Derive, then validate schemas:** express handler data with concrete Rust
  types and the resolved SDK's supported generated-schema/derive path. Validate
  untrusted values at conversion boundaries and test derived/declared schemas,
  serialization, optional fields, and invalid nested inputs. A Rust type or
  generated schema does not substitute for boundary validation.
- **Test the qualified adapter surface:** use configured Rust test lanes and
  `#[tokio::test]` only when the repository/runtime requires it. Unit-test
  transport-independent services with fakes; integration-test the resolved SDK
  service/transport adapter, generated schemas, cancellation, and shutdown with
  an SDK-supported local fixture when available. Treat conformance or real
  transport results as target-specific evidence, and report skipped checks.

## Workflow

1. Inspect the local shape first: `Cargo.toml`, workspace members, crate
   boundaries, feature flags, `rust-toolchain`, CI recipes, README/AGENTS docs,
   and nearby modules.
   Use local code navigation, direct reads, and search for symbols, references,
   implementations, exact strings, docs, config, logs, fixtures, generated
   assets, and macro-generated surprises; use repository commands for tests,
   builds, and other validation.
2. State the behavior or domain change in concrete terms. Use BDD-style
   examples for user-visible behavior and DDD language for boundaries,
   invariants, and aggregate-like rules.
3. Choose the smallest crate/module/API boundary that can own the behavior.
   Keep framework, database, and transport concerns outside core domain logic
   unless the crate is explicitly an adapter. Load
   [`hexagonal-architecture`](../hexagonal-architecture/SKILL.md) for
   ports/adapters and external actors, [`clean-architecture`](../clean-architecture/SKILL.md)
   for use-case and interface-adapter boundaries, or
   [`onion-architecture`](../onion-architecture/SKILL.md) for domain/application
   rings.
4. Design the API before filling in code: visibility, ownership, lifetimes,
   trait bounds, error type, feature gating, and caller obligations.
5. Implement in small steps. Prefer clear safe Rust, narrow mutation, explicit
   invariants, and tests close to the behavior.
6. Refactor after tests pass: simplify ownership, collapse accidental
   abstraction, remove duplicated conversions, and make invalid states harder to
   express.
7. Verify with the repository recipe or an appropriately scoped Cargo lane.

Use [`ci-release-engineering`](../ci-release-engineering/SKILL.md) for hosted
pipeline and automated release configuration, and
[`container-engineering`](../container-engineering/SKILL.md) for Dockerfile, OCI
image, and Compose behavior. Keep Cargo build and packaging mechanics here.

## Core Rust Checklist

- Ownership expresses real responsibility. Use `&T`, `&mut T`, owned values,
  `Cow`, `Rc`, or `Arc` deliberately; do not add clones to satisfy the compiler
  without checking allocation, aliasing, and lifetime implications.
- Lifetimes describe relationships already present in the data model. Avoid
  over-generalized lifetimes, self-referential structures, and references stored
  where owned values would simplify the design.
- Traits and generics buy reuse, substitution, or testability. Keep bounds close
  to the item that needs them and avoid generic APIs when one concrete type is
  the honest contract.
- Error handling distinguishes caller errors, domain errors, I/O failures, and
  programmer bugs. Library-like crates should expose typed errors; application
  edges may add context and convert to user-facing responses.
- Keep core domain APIs synchronous unless the domain behavior itself requires
  asynchrony. Push async I/O, Tokio runtime details, channels, and task handles
  to application services, ports, adapters, or process wiring.
- Modules reveal boundaries. Public modules should be stable enough for callers;
  private modules can optimize for clarity and local cohesion.
- Collections and iterators match the semantics: ordering, uniqueness, lookup
  cost, allocation, and borrowing behavior should be intentional.
- Smart pointers have a reason: `Box` for indirection or trait objects, `Rc` for
  single-threaded sharing, `Arc` for cross-thread sharing, `Mutex/RwLock` for
  mutation behind sharing, and `Pin` only when pinning invariants matter.
- `unsafe` is isolated, justified, documented with safety invariants, and tested
  with risk-appropriate tools.

## Project Setup

- Prefer one crate until independent release, feature, dependency, or compile
  boundaries justify a workspace member.
- Use workspace dependencies and lints when they reduce drift. Do not introduce
  workspace-wide policy for a local experiment.
- Feature flags should be additive. Keep defaults intentional, avoid mutually
  exclusive features unless the crate already has a clear policy, and test the
  feature combinations CI claims to support.
- Keep dependencies narrow. Inspect direct and transitive impact with
  `cargo tree` before adding broad crates for small needs.
- Put generated code, build scripts, FFI bindings, examples, benches, and tests
  in conventional locations unless the repository already documents otherwise.

## Desktop GUI Routing

Use [`rust-desktop-gui`](../rust-desktop-gui/SKILL.md) when Rust work primarily
changes a native desktop GUI framework, widget tree, event loop, window lifecycle,
platform integration, or desktop bundle requirements. This skill retains Cargo,
ownership, types, errors, workspace, and dependency mechanics. Before adding or
changing a desktop framework dependency, inspect its resolved version, features,
renderer or backend, native prerequisites, assets, and supported OS targets; use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
when dependency provenance, native crates, build scripts, or installers matter.

Useful inspection commands:

```sh
cargo metadata --no-deps
cargo tree -p <package>
cargo check -p <package> --all-targets
cargo fmt
```

## Pattern Routing

- Load [`rust-design-patterns`](../rust-design-patterns/SKILL.md) when the Rust
  change needs a deliberate pattern choice: newtypes, enums, builders, RAII
  guards, traits as ports, compose-structs, contained unsafe modules, custom
  traits for complex bounds, or macros.
- Load [`rust-antipatterns`](../rust-antipatterns/SKILL.md) when reviewing or
  refactoring generated-code smells: clone-to-satisfy-borrow-checker,
  reflexive `Arc<Mutex<_>>`, deref polymorphism, panic at trust boundaries,
   async overuse, framework leakage, or brittle Rust tests.

## Local CPU Parallelism Routing

Compose with [`parallelism-engineering`](../parallelism-engineering/SKILL.md)
when a local CPU-bound Rust workload needs data or task decomposition, partition
sizing, bounded executor design, deterministic reduction, cancellation, or
nested-parallelism control. That skill owns the cross-language parallel design;
this skill owns Rust ownership, thread/task API, crate, and test mechanics.

Do not route ordinary Tokio, async I/O, channels, request concurrency, or
event-loop/runtime behavior to `parallelism-engineering`; use
[`rust-async-web`](../rust-async-web/SKILL.md) when that async/runtime surface is
primary. Spark/PySpark execution remains with
[`data-platform-engineering`](../data-platform-engineering/SKILL.md), not local
parallelism engineering.

## WebAssembly Routing

Compose with [`webassembly-engineering`](../webassembly-engineering/SKILL.md)
when Rust work includes a general WebAssembly decision: a WAT or `.wasm`
artifact, WASI or WIT, the Component Model, host/guest contract, runtime or
target selection, capability grants, or Wasm packaging and deployment. That
skill owns those Wasm boundary and compatibility decisions. This skill retains
Rust source, Cargo, compiler and target mechanics, `wasm-bindgen` and generated
Rust binding mechanics, and Rust tests; the Wasm skill does not establish Rust
toolchain, target, or binding-generator support. Keep Leptos and other Rust web
framework mechanics with [`rust-async-web`](../rust-async-web/SKILL.md).

## API and Observability Routing

- Load [`api-design`](../api-design/SKILL.md) when Rust changes define or alter a
  public service, SDK, CLI, serialization, error, pagination, webhook/event, or
  generated-client contract. Keep this skill focused on ownership, types,
  modules, and implementation mechanics.
- Load [`observability-engineering`](../observability-engineering/SKILL.md) when
  Rust changes add or change durable logs, metrics, traces, request/correlation
  IDs, instrumentation fields, or operator-facing diagnostics.

## Security Review Routing

Load [`security-review`](../security-review/SKILL.md) when Rust changes touch
implemented auth or session handling, crypto/randomness, credentials, secrets or
`.env`, filesystem paths, command/process execution, `unsafe`, FFI, plugin
boundaries, HTTP clients, SQL binding, or other trust boundaries. Use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for Cargo dependency bumps, `Cargo.lock` churn, `build.rs`, proc macros, native
crates, toolchain/bootstrap pins, provenance, or advisory questions. Use
[`threat-modeling`](../threat-modeling/SKILL.md) before or during new auth,
service-to-service, FFI/plugin, unsafe, external-client, or sensitive data-flow
boundaries. Pair security-sensitive reviews with
[`security-review-evidence`](../security-review-evidence/SKILL.md) for sanitized
logs, telemetry, build artifacts, dependency reports, or test output.

## Refactoring Guidance

- Protect current behavior first with focused tests, characterization tests, or
  BDD-style acceptance criteria.
- Separate mechanical moves from semantic changes when possible.
- Decide whether the refactor is defensive or simplifying. Add types and
  adapters to protect real invariants; delete indirection when it only forwards
  parameters or preserves obsolete paths.
- Move code toward domain language: named value types, explicit state
  transitions, and constructors that enforce invariants.
- Simplify ownership by changing data flow before adding lifetimes, reference
  cycles, or interior mutability.
- Simplify errors by removing duplicate variants, preserving actionable context,
  and keeping conversion points near adapter boundaries.
- Replace groups of mutually exclusive `Option<T>` fields with enums when only
  one mode is valid.
- Remove dead feature flags completely: call sites, `cfg`s, conditional return
  types, monitoring scaffolding, docs, tests, and dependency gates.
- Move tests with code during module splits, and keep intermediate states
  compiling.
- For performance refactors, measure or reproduce the bottleneck before changing
  algorithms, allocation patterns, locking, or async task structure.

## Macros

- Prefer functions, traits, derives, builders, or generics before macros.
- Use `macro_rules!` for small syntax/repetition patterns with predictable
  expansion. Keep patterns minimal and diagnostics readable.
- Use procedural macros only when compile-time code generation materially
  improves the caller experience. Keep parsing, validation, and generated code
  covered by tests.
- Review macro hygiene, spans, error messages, generated visibility, feature
  gates, and compile-time cost.
- Test caller-facing macro behavior with ordinary tests, doctests,
  `compile_fail` examples, or a compile-test harness when the failure mode is a
  type-system contract.

## Common Crate Guidance

- `serde` / `serde_json`: keep serialization formats explicit at API, storage,
  and message boundaries. Use derives for stable data shapes, custom serializers
  only when the wire contract requires them, and tests for compatibility-sensitive
  JSON.
- `anyhow`: appropriate at application edges, CLIs, and task orchestration where
  context matters more than typed recovery. Library-like crates and domain APIs
  should expose typed errors callers can handle.
- `tokio`: use `rust-async-web` for runtime, task, cancellation, backpressure,
  Axum, and Leptos details. Introduce async deliberately for I/O-bound or
  high-concurrency work; do not hide blocking work inside async functions.
- `reqwest`: keep HTTP clients at adapter boundaries, configure timeouts, handle
  status codes deliberately, avoid logging secrets, and test request/response
  mapping without real network calls when practical.
- `rand` and ID crates: use
  [`random-data-identifiers`](../random-data-identifiers/SKILL.md) for secure
  randomness, deterministic seeds, UUIDs, and collision-resistant identifiers.

## Anti-Patterns

- Fighting borrow errors by cloning, leaking, boxing, or adding `Arc<Mutex<_>>`
  before revisiting ownership.
- Adding abstractions because they are common in other languages rather than
  because this code has multiple real implementations.
- Exposing framework, SQL, HTTP, or serialization types from core domain APIs
  without a deliberate adapter boundary.
- Making feature flags subtractive or environment-sensitive.
- Treating Clippy suggestions, design patterns, or public docs as substitutes
  for behavior tests and explicit contracts.

## Acceptance Criteria

Successful Rust engineering work has:

- a clear behavior or domain reason for the change;
- crate/module/API boundaries that match repository conventions;
- ownership, lifetimes, traits, errors, and features chosen intentionally;
- tests or examples covering the changed behavior or invariant;
- relevant Cargo verification run or a clear explanation of what could not run.

## TypeScript Zod Interoperability

For a real TypeScript/backend JSON crossing, load [`zod-engineering`](../zod-engineering/SKILL.md). Rust retains native validation, DTO/domain conversion, stable serialization/errors, and shared-fixture parity.
