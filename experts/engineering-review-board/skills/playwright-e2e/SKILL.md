---
name: playwright-e2e
description: "Playwright browser E2E guidance. Use when adding, updating, running, or debugging checked-in Playwright tests, playwright.config files, browser test helpers, targeted test runs, traces, reports, cross-browser projects, or testing browser-visible behavior through checked-in Playwright tests. Do not use for non-browser domain logic, frontend implementation without a durable Playwright artifact, or generic manual browser automation."
---

# Playwright E2E

## Purpose

Use this skill for checked-in Playwright browser tests. The goal is fast,
targeted, behavior-readable evidence for browser-visible workflows, not broad
manual exploration or proof of backend/domain invariants.

Load [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
only when the work changes package scripts, Playwright or TypeScript config,
shared helpers, the JS/TS toolchain, lockfiles, or package-manager workflow.
Ordinary spec-only edits remain in this skill.

## When to Use

- Adding, updating, splitting, moving, or deleting Playwright specs.
- Debugging Playwright failures, flakes, traces, reports, browser projects, or
  web-server startup.
- Choosing between targeted, full-suite, cross-browser, mobile/responsive, and
  live-backend lanes.
- Testing browser-visible behavior: routing, forms, keyboard/focus behavior,
  visible validation/errors, accessibility-visible state, hydration/rendering,
  responsive layout, and browser API calls.

For photo/video catalog viewer, tree, selection, and playback behavior, compose
with [`digital-asset-management`](../digital-asset-management/SKILL.md); keep
domain invariants and media-processing contracts below the browser-test layer.

## When Not to Use

- Domain invariants, SQL/storage contracts, backend route/security contracts,
  config parsing, or pure state logic that can be tested faster below the
  browser.
- Ad hoc manual browser exploration, screenshots, or DOM inspection outside the
  checked-in Playwright test suite; use the appropriate browser automation skill
  or tool instead.
- Generic Playwright tutorial work that ignores the repository's package
  manager, scripts, config, support helpers, and artifact-safety rules.

## Required Repository Inspection

Before editing or recommending commands, inspect the current repository:

- package-manager files such as `package.json`, lockfiles, or workspace config;
- Playwright config files such as `playwright.config.ts` or
  `playwright.config.js`;
- command surfaces such as `just --list`, `make help`, package scripts, or CI
  workflows;
- existing spec directories such as `e2e/`, `tests/e2e/`, or
  `playwright/tests/`;
- support helpers, fixtures, route mocks, authentication setup, storage-state
  files, artifact-cleanup scripts, and test data builders;
- docs that explain test layers, browser support, package-manager policy,
  artifact handling, or live-backend restrictions.

Use a verified repository-provided script or recipe for setup, narrow iteration,
and final evidence. It is eligible only when repository evidence establishes
that it resolves Playwright from the expected package-local installed tree and
fails closed when that executable is unavailable, rather than using a
fetch-capable package runner.

## Test Organization and Boundaries

- Keep Playwright tests BDD-shaped: test titles should describe observable user
  or workflow behavior, not private implementation details.
- Prefer deterministic route mocks, fixtures, and seeded data for routine browser
  tests. Use live-backend tests only when the behavior cannot be proven with
  deterministic support helpers.
- Keep DDD boundaries clear: domain rules and persistence belong in lower-level
  tests; Playwright proves browser journeys and integration seams visible to the
  browser.
- Apply TDD when changing browser behavior: add or update the narrow failing spec
  first when practical, then implement the smallest source change.

## Command Strategy

Run from the repository root unless local docs specify otherwise.

Use only a repository-provided, lockfile-backed package script or
repository-owned recipe. Inspect its declaration, workspace ownership when
applicable, locked Playwright dependency, and its installed-tree resolution and
fail-closed contract before relying on it. A lockfile declaration, installed
dependency record, script name, or bare `playwright` token alone is insufficient:
npm script `PATH` prepends local bins but retains ambient entries, so a bare token
can fall through to an ambient or global executable when the local one is absent.
Do not prescribe a universal implementation check or package-manager filesystem
layout; the target repository must prove that its own script or recipe resolves
the expected package-local executable and fails closed if it is unavailable. If
repository evidence shows that npm owns a `test:e2e` script *and* this
installed-tree ownership and fail-closed behavior is verified, an npm invocation
may be:

```sh
npm run test:e2e -- <spec-or-filter>
```

Otherwise, substitute the documented repository command for
`<repository-e2e-script>` below and preserve its documented argument-forwarding
syntax.

Do not run or recommend direct package-runner commands. They cannot prove local
dependency or executable identity: an absent dependency can be fetched or
cache-resolved, and runners may assemble executable `PATH` entries from cache or
other local locations; neither the installed tree nor the executable owner is
fail-closed. Offline or non-interactive flags limit network or prompts, not that
identity ambiguity.

When no trustworthy repository script or recipe exists, use
[`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
and [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
to assess a proposed repository-owned command. Do not add a script, install a
dependency, or change a lockfile without separate authorization.

Useful focused options:

```sh
<repository-e2e-script> -- path/to/spec.ts
<repository-e2e-script> -- path/to/spec.ts:123
<repository-e2e-script> -- --grep "visible behavior title"
<repository-e2e-script> -- --project=chromium
<repository-e2e-script> -- --headed
<repository-e2e-script> -- --debug
<repository-e2e-script> -- --ui
```

Use `--headed`, `--debug`, or `--ui` only for focused local diagnosis, not as
routine handoff evidence.

## Lane Selection

Choose the narrowest lane that proves the behavior:

- **Targeted spec/filter** for iteration and regression reproduction.
- **Full default browser suite** before handoff when browser behavior changed.
- **Cross-browser lane** when changes touch browser APIs, rendering, downloads,
  media, storage, focus, dialogs, or compatibility-sensitive code.
- **Responsive/mobile lane** when layout, viewport, pointer/touch, or navigation
  shell behavior changed.
- **Live-backend lane** only when mocks cannot prove the contract and the
  repository documents setup, cleanup, and data isolation.

Prefer the repository's named recipe or CI lane for final evidence.

## Debugging, Traces, and Reports

1. Re-run the smallest failing filter first: spec path, `file:line`, or `--grep`.
2. Use `--list` to confirm a filter before starting browsers when supported.
3. Use `--workers=1` or `--repeat-each <N>` to diagnose ordering or flake
   hypotheses without broadening the suite.
4. Enable traces only as a narrow opt-in, for example
   `<repository-e2e-script> -- path/to/spec.ts --trace=retain-on-failure`.
5. Inspect traces with the repository-provided trace-viewing command when needed.
6. Keep raw screenshots, traces, videos, storage state, HAR/network dumps,
   downloads, and reports in ignored local artifact directories by default.
7. If an artifact must be shared or retained, create a sanitized derivative and
   do so only when documented repository policy or explicit approval allows it;
   capture [`security-review-evidence`](../security-review-evidence/SKILL.md)
   for redactions, access, retention, and cleanup.

Do not retain or share raw screenshots, videos, traces, network dumps, storage
state, cookies, CSRF/session values, credentialed URLs, local paths, `.env`
contents, reports, downloads, or live data.

## Verification Guidance

- Browser source or spec change: run the narrowest targeted script first, then
  the strongest relevant repository Playwright lane before handoff.
- Playwright config or helper-script change: run tests that cover config/helper
  contracts plus a targeted browser lane.
- Cross-browser or responsive risk: run the curated cross-browser or responsive
  lane instead of every browser combination by default.
- Documentation-only E2E guidance changes: run the repository's docs or drift
  checks if they exist; otherwise validate links and examples manually.

## Failure Triage

- Missing browser executable: use the repository's browser install/setup command
  only after separately authorizing its browser download and execution effects;
  do not substitute a fetch-capable package runner.
- Web server cannot start: check configured host, port, base URL, reuse-server
  policy, required env, and stale local processes.
- Unexpected API call: update route mocks or fixtures only if browser behavior is
  intentionally changing; otherwise fix the application call.
- Hydration/rendering failure: prefer a focused spec, console diagnostics, and a
  targeted render mode before broad browser matrices.
- Flake suspicion: use `--workers=1`, `--repeat-each`, and focused specs; do not
  hide nondeterminism with retries unless the lane's policy already owns them.

## Common Mistakes to Avoid

- Do not use Playwright as the only proof for domain invariants, storage
  constraints, auth/session security controls, CORS/CSRF policy, or config
  parsing.
- Do not add live-backend setup to deterministic mocked specs when support
  helpers can express the same browser contract.
- Do not promote cross-browser, responsive, live-backend, or slow visual lanes
  into default checks without explicit need or repository policy.
- Do not leave `test.only`, retained traces, screenshots, videos, HTML reports,
  downloads, raw browser artifacts, or sanitized artifacts without policy and
  security evidence in handoff evidence.
- Do not override repository evidence for pnpm, Yarn, Bun, or another
  documented workflow.
