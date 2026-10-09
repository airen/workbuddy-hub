# WebAssembly Target and Runtime Selection Evidence

**Purpose:** select a WebAssembly artifact form and a deployment runtime from
versioned, host-specific evidence. This is an evidence record and decision
procedure, **not** a static compatibility matrix. Runtime, engine backend,
operating-system, processor, component, and host-capability support must be
verified for the exact deployment candidate.

**Evidence retrieval date:** 2026-07-31. Sources were retrieved read-only from
their public canonical sites. No module, runtime, toolchain, generator, or
browser flow was downloaded, installed, executed, or mutated.

## Selection record required for each deployment

Record these fields before asserting that a target is supported:

1. **Artifact and ABI:** core module or component; core feature set; for a
   component, the Component Model release, Canonical ABI generation, and exact
   WIT package names, versions, and selected world.
2. **WASI profile:** no WASI, `wasi_snapshot_preview1`/WASI 0.1, WASI 0.2.x, or
   WASI 0.3.x; list every imported interface, including non-WASI imports.
3. **Host capability grant:** for each import, identify the host implementation,
   intended authority, scope, and limit. Examples include a preopened directory
   rather than the host filesystem, a bounded outbound-network policy rather
   than ambient networking, and explicit stdin/stdout rather than host process
   inheritance.
4. **Runtime evidence:** runtime name, exact released version, enabled backend
   and feature flags, host OS/CPU/ABI, and an official release or versioned-doc
   citation. A documentation page with no release number is not proof for an
   unspecified future runtime.
5. **Deployment constraints:** whether executable-memory/JIT is allowed; whether
   AOT is required; architecture and OS support tier; browser delivery
   requirements; resource limits; and whether untrusted code is in scope.
6. **Status and uncertainty:** classify every relied-on behavior using the
   labels below. Write `unresolved` rather than extrapolating from another
   runtime, a different backend, or a previous release.

## Status vocabulary

| Label | Meaning for a selection decision |
| --- | --- |
| **W3C Candidate Standard / Candidate Recommendation Draft** | The cited W3C publication status, not a W3C Recommendation. It is usable specification evidence for its stated revision, but still does not imply implementation by every runtime or host. |
| **Stable 0.x release / evolving specification** | A release line describes its APIs as stable for producers and consumers, but its underlying API proposals remain in the 0.x/standardization process. Pin the release and validate the chosen producer and consumer. |
| **Developer Preview / evolving specification** | A stable-for-tools release line whose underlying Component Model specification is still being incrementally standardized. Pin the release and validate the chosen producer and consumer. |
| **Proposal** | Not a portable deployment dependency until the exact host/runtime version explicitly documents and tests it. WASI proposal phase and Wasm proposal phase are distinct processes. |
| **Runtime extension** | Vendor/runtime behavior outside the cited common specification. Do not present it as WASI, WebAssembly core, or browser behavior. |
| **Unresolved** | Evidence does not establish support for the exact artifact, host capability, target, backend, or release. Block the compatibility claim or choose a documented fallback. |

## Applicable standards and specifications

### Core WebAssembly and Web embedding

- **Core:** W3C's current Core WebAssembly document at the persistent W3C
  shortname `wasm-core-2` describes **version 3.0 (2026-07-28)**. The `-2` in
  that URL is the W3C document shortname, **not** the Core-language revision;
  no `/TR/wasm-core-3/` publication exists at this retrieval date. It defines
  the virtual ISA, binary encoding, validation, execution semantics, and text
  representation, but explicitly does **not** define environment interaction or
  invocation. Core imports are therefore a host contract, not an
  operating-system capability claim. **Status:** W3C Candidate Standard for the
  cited Core 3.0 revision, not a W3C Recommendation. [C1]
- **JavaScript embedding:** the WebAssembly JavaScript Interface describes
  construction, instantiation, imports/exports, value exchange, and errors in
  JavaScript environments; it is not a general WASI or Component Model host
  contract. **Applicable revision:** WebAssembly JavaScript Interface 2.
  **Status:** W3C Candidate Recommendation Draft behavior only where the
  target's JS host implements this revision. [C2]
- **Web delivery:** the Web API defines streaming compilation/instantiation.
  `instantiateStreaming` requires an OK, CORS-same-origin response with exactly
  `Content-Type: application/wasm` (no parameters). The Web API also states that
  Wasm itself provides no integrity or privacy protection; delivery protection
  is external, such as HTTPS. **Applicable revision:** WebAssembly Web API 2.
  **Status:** W3C Candidate Recommendation Draft behavior, not a promise that a
  browser hosts WASI or components. [C3]

### Component Model, WIT, and Canonical ABI

- **Component Model:** the official `WebAssembly/component-model` repository is
  where the model is being standardized and says a formal specification and
  reference interpreter are future work. Its released Developer Preview lines
  are **0.2.0** (WIT, resources, linking) and **0.3.0** (native concurrency,
  `async`, `stream`, `future`, and additional ABI built-ins). **Status:**
  Developer Preview / evolving specification—not a claim that the Core 3.0
  specification or all web hosts implement components. [C4]
- **WIT:** WIT is an IDL for component imports and exports; WIT packages and
  worlds describe the contract, not guest behavior. A world identifies required
  imports and provided exports; a host must implement all imports selected by
  the world. **Applicable revision:** the exact Component Model release selected
  above and the exact WIT package versions. The moving `main` document is useful
  design evidence but must not substitute for a pinned release in deployment
  evidence. **Status:** 0.2.0/0.3.0 Developer Preview semantics as applicable;
  otherwise unresolved. [C5]
- **Canonical ABI:** this ABI converts Component Model values/functions to Core
  Wasm values/functions and specifies lifting/lowering through linear memory.
  A component binary is not interchangeable with a core-module ABI merely
  because both have a `.wasm` suffix. Producer, composer, and runtime must
  agree on the selected Component Model/Canonical ABI release and WIT world.
  **Status:** 0.2.0 baseline or 0.3.0 Developer Preview additions only when
  documented by the exact tools/runtime; otherwise unresolved. [C6]

### WASI

- **WASI host model:** WASI is a standards-track set of APIs under the WASI
  Subgroup in the W3C WebAssembly Community Group. A module/component begins
  without ambient authority and can act only through host-granted capabilities.
  This is a host policy and implementation responsibility: an import is not
  proof that access is safe, scoped, or available. [C7]
- **WASI 0.1 / Preview 1:** a legacy stable-release, POSIX-inspired *core-module*
  API identified by `wasi_snapshot_preview1`; it has broad existing deployment
  use. It is not a Component Model interface and cannot establish component
  portability. [C8]
- **WASI 0.2.x:** a stable 0.x Component Model/WIT release line, initially released
  in January 2024. It defines `wasi:cli/command` and `wasi:http/proxy` worlds
  and models asynchronous I/O through `wasi:io`. Pin the needed patch release;
  the cited release page lists through **0.2.12**. [C9]
- **WASI 0.3.0:** released 2026-06-11 and marked stable by the current WASI
  release documentation. It moves async into Component Model primitives,
  replaces 0.2 `wasi:io`, and changes the HTTP worlds to `wasi:http/service`
  and `wasi:http/middleware`. It is not ABI-compatible merely by changing a
  version label; pin the producer, WIT, and runtime release together. [C10]
- **Proposal qualification:** the WASI release index says all WASI APIs proceed
  through the WASI Subgroup phase process and remain 0.x until Phase 5
  standardization. A release described as *stable* is usable release evidence,
  but is not evidence that every individual API has completed a separate final
  standards process or that a chosen runtime supports it. Treat APIs outside
  the pinned release, and proposal-specific interfaces such as TLS, KV, NN,
  crypto, or threads, as **proposal/unresolved** until exact runtime evidence is
  recorded. [C9]

## Host capability model and security boundary

1. Start from an empty capability set. Derive required imports from the core
   module or selected WIT world, then grant only the named filesystem,
   environment, clock, random, socket, HTTP, process, or custom-host capability
   with explicit bounds.
2. Record the capability *implementation*, not only its WIT/interface name:
   allowed paths, symlink policy, network destinations/protocols, request/response
   limits, inherited handles, environment allowlist, clock/random source, and
   resource quotas are host-specific deployment facts.
3. Do not infer a security sandbox from Wasm validation, WASI naming, or a
   capability-shaped API. The Core specification assigns imported capabilities
   and security policy to the embedder. [C1]
4. If executing untrusted code, require runtime-specific sandbox evidence for
   the exact release and capability implementation. Node's documented WASI host
   is an explicit counterexample: Node 26.5.1 labels `node:wasi` experimental,
   supports only `unstable` and `preview1`, and says its filesystem capabilities
   do not form a secure sandbox. **Status:** Node WASI sandboxing is unsuitable
   for untrusted-code claims on this evidence. [C11]

## Runtime and deployment evidence (examples, not a matrix)

### Wasmtime / Bytecode Alliance

Wasmtime identifies itself as a Bytecode Alliance runtime for Wasm, WASI, and
the Component Model. Its support documentation makes support a joint property
of runtime feature, compiler/backend, target, and OS—not a property of the
`.wasm` file alone. Its tier page currently lists the Component Model as Tier 1
but identifies some Wasm and WASI facilities as lower tier or unsupported.
Use the exact Wasmtime release's feature documentation and tier state when
making a deployment claim. The cited pages are current, unversioned
documentation; therefore **the exact Wasmtime release for a new deployment is
unresolved until recorded**. [C12] [C13]

Deployment constraints established by Wasmtime's current platform documentation:

- Cranelift supports `x86_64`, `aarch64`, `s390x`, and `riscv64`; no 32-bit
  compiler target is currently supported. [C12]
- JIT-capable Cranelift/Winch needs an OS that permits dynamically created
  executable memory. AOT and JIT are distinct delivery choices. [C12]
- `#![no_std]` use supports only a feature subset and requires AOT; the custom
  platform header API is not stable. [C12]
- Tier labels are runtime-maintainer confidence statements, not a cross-runtime
  compatibility guarantee. Validate the exact backend/feature/architecture
  combination rather than transposing a tier from another target. [C13]

### Node.js and Wasmer examples of non-portable host behavior

- **Node.js 26.5.1:** documented `node:wasi` support is experimental and only
  `unstable`/`preview1` (WASI 0.1 shapes). Its `preopens`, environment, standard
  streams, and exit behavior are Node host configuration, not general WASI 0.2/
  0.3 or Component Model support. [C11]
- **Wasmer/WASIX:** Wasmer says a browser's built-in `WebAssembly` API runs bare
  modules and that its Browser backend supplies an operating-system layer named
  **WASIX**. Classify WASIX as a **runtime extension**, not a standardized WASI
  capability. Select it only with Wasmer version/backend/platform evidence and
  an explicit portability fallback. [C14]

## Decision procedure

1. **Choose the artifact boundary.** Use a core module when the target's
   documented module embedding and import ABI are sufficient. Choose a component
   only when the chosen runtime/host documents the selected Component Model and
   Canonical ABI release and the WIT world supplies the desired contract.
2. **Choose a released interface line.** Use WASI 0.1 only when a Preview-1
   core-module host is the intended boundary. For component deployments, choose
   a pinned WASI 0.2.x or 0.3.x world; do not silently rewrite worlds or async
   semantics across the boundary.
3. **Design the authority surface.** Minimize imports and define concrete host
   grants/limits. A component whose world excludes an interface cannot obtain it
   through the component boundary, but the host embedding still needs its own
   security evidence.
4. **Narrow to the actual runtime release.** Gather official evidence for the
   exact runtime version, backend/flags, OS, CPU, artifact form, feature set,
   WIT/Canonical ABI generation, and all imported capabilities. Do not use this
   reference as proof of any unlisted runtime.
5. **Resolve deployment constraints.** For browsers, check the Web API delivery
   requirements and separately establish the component/WASI host. For native
   runtimes, check executable-memory policy, AOT availability, target tier, and
   resource/security controls. For constrained or `no_std` targets, record the
   required AOT/custom-platform conditions.
6. **Classify gaps.** Mark unsupported or undocumented combinations
   `unresolved`; either change the artifact/profile/runtime or obtain current
   official evidence and validate in the intended deployment environment.

## Evidence ledger and citations

| ID | Authority and source | Exact applicable revision/status recorded | Retrieved |
| --- | --- | --- | --- |
| C1 | W3C WebAssembly Community Group, [WebAssembly Core Specification](https://www.w3.org/TR/wasm-core-2/) | **W3C Candidate Standard**; Core **3.0 (2026-07-28)**. The canonical persistent shortname is `wasm-core-2`, whose suffix is not the Core revision; `/TR/wasm-core-3/` was not published at retrieval. Core ISA only. | 2026-07-31 |
| C2 | W3C, [WebAssembly JavaScript Interface](https://www.w3.org/TR/wasm-js-api-2/) | **W3C Candidate Recommendation Draft**; JavaScript Interface **2**; JS embedding scope. | 2026-07-31 |
| C3 | W3C, [WebAssembly Web API](https://www.w3.org/TR/wasm-web-api-2/) | **W3C Candidate Recommendation Draft**; Web API **2**; browser streaming, MIME, CORS, and delivery scope. | 2026-07-31 |
| C4 | W3C WebAssembly Community Group, [Component Model repository](https://github.com/WebAssembly/component-model) | Repository `main` at retrieval; Developer Preview **0.2.0** and **0.3.0**; incremental standardization, formal spec future work. Not a pinned release URL. | 2026-07-31 |
| C5 | W3C WebAssembly Community Group, [WIT specification source](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md) | Moving `main` specification source retrieved at date; pin **0.2.0** or **0.3.0** separately for deployment. | 2026-07-31 |
| C6 | W3C WebAssembly Community Group, [Canonical ABI specification source](https://github.com/WebAssembly/component-model/blob/main/design/mvp/CanonicalABI.md) | Moving `main` ABI source retrieved at date; 0.3 additions are feature-gated in the Component Model release line. | 2026-07-31 |
| C7 | WASI Subgroup / W3C WebAssembly Community Group, [WASI introduction](https://wasi.dev/) | Current standards-track description; capability-based host model. | 2026-07-31 |
| C8 | WASI Subgroup / W3C WebAssembly Community Group, [WASI 0.1](https://wasi.dev/releases/wasi-p1) | Legacy stable **WASI 0.1 / Preview 1** core-module ABI. | 2026-07-31 |
| C9 | WASI Subgroup / W3C WebAssembly Community Group, [WASI releases](https://wasi.dev/releases) and [WASI 0.2](https://wasi.dev/releases/wasi-p2) | Stable 0.x **WASI 0.2.x**, patch list through **0.2.12**; release/proposal phase qualifications. The 0.2 page's "most recent" wording is stale relative to C10. | 2026-07-31 |
| C10 | WASI Subgroup / W3C WebAssembly Community Group, [WASI 0.3](https://wasi.dev/releases/wasi-p3) | Stable **WASI 0.3.0**, released **2026-06-11**; native async / changed worlds. | 2026-07-31 |
| C11 | Node.js project, [Node.js v26.5.1 WASI documentation](https://nodejs.org/download/release/v26.5.1/docs/api/wasi.html) | Version-pinned runtime **v26.5.1**; Stability 1 experimental; only `unstable` and `preview1`; documented sandbox limitation. | 2026-07-31 |
| C12 | Bytecode Alliance, [Wasmtime platform support](https://docs.wasmtime.dev/stability-platform-support.html) | Current unversioned runtime documentation; exact runtime release must be pinned by the deploying project. | 2026-07-31 |
| C13 | Bytecode Alliance, [Wasmtime support tiers](https://docs.wasmtime.dev/stability-tiers.html) | Current unversioned tier/feature/target evidence; exact runtime release/backend remains required. | 2026-07-31 |
| C14 | Wasmer, [Wasmer Runtime Features](https://docs.wasmer.io/runtime/features/) | Current unversioned runtime documentation; WASIX described as Wasmer's operating-system layer, not a common standard. | 2026-07-31 |
| C15 | Bytecode Alliance, [Component Model introduction](https://component-model.bytecodealliance.org/) | Current unversioned documentation says WASI **0.2.0** is current stable; retained as conflicting/stale status evidence. | 2026-07-31 |

## Recorded uncertainty and source reconciliation

- **C1 URL/revision correction:** `https://www.w3.org/TR/wasm-core-2/` is the
  published W3C shortname for the Core document that identifies itself as Core
  **3.0 (2026-07-28)**. The shortname suffix must not be reported as the
  language revision. The plausible-looking `/TR/wasm-core-3/` URL returned 404
  on 2026-07-31, so C1 now cites the canonical published document URL and
  records the document's own revision and W3C Candidate Standard status.
- **Ledger URL/revision scan:** C2 and C3 use their matching W3C `-2`
  publication shortnames and are Candidate Recommendation Drafts, not final
  W3C Recommendations. C4--C6 and C12--C15 are intentionally unversioned
  current documentation or moving repository sources and are labelled as such;
  they are not release-pinned deployment evidence. C11 now uses Node's
  version-pinned v26.5.1 archive instead of the moving `nodejs.org/api` URL.
- Bytecode Alliance's Component Model introduction still calls WASI 0.2.0 the
  current stable release, while the later, dedicated WASI release documentation
  calls WASI 0.3.0 stable and records its 2026-06-11 release. This reference
  relies on C10 for current WASI release status and preserves the conflict as a
  signal to verify the intended runtime/toolchain, rather than treating either
  page as universal support evidence. [C15]
- The WASI 0.2 page in C9 also calls 0.2 the "most recent stable" release, in
  conflict with the release index and C10. C9 supports the 0.2 interface and
  patch history only; C10 controls the current 0.3 release-status claim.
- Core 3.0, the JavaScript Interface, and the Web API do not establish a
  standardized browser component host or a browser WASI authority model.
  Browser component/WASI support is **unresolved** absent the intended browser
  or host's official versioned documentation.
- This record does not assert a universal WIT registry, component composer,
  language binding, engine feature, operating-system, CPU, AOT artifact, or
  proposal support claim. Each is **unresolved** until the exact selected
  implementation and deployment target provide official evidence.
