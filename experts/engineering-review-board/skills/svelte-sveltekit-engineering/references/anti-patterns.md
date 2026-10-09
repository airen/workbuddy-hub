# Svelte and SvelteKit Anti-Patterns

Each entry names the anti-pattern, why it causes real problems, and the
correct alternative. Use this list during review or before implementing new
Svelte/SvelteKit code; do not treat it as exhaustive — apply the same
reasoning (does this break SSR, leak state across requests, or duplicate
framework-provided behavior?) to unfamiliar code.

## Data Loading

**Fetching in `onMount` or a component-level `$effect` instead of `load`.**
Why it's a problem: the page renders empty first, then re-renders once the
fetch resolves — this breaks SSR (the server sends an empty shell), hurts
perceived performance, and forces the component to hand-roll loading/error
states that `load` already gives you via `+page.svelte`'s `data`/`form` props
and `+error.svelte`. It also means the fetch re-runs on every component mount
rather than being cached/invalidated by SvelteKit's navigation lifecycle.
Alternative: fetch in `+page.js`/`+page.server.js` `load`, and use `await`
inside the returned object's promises (with `streamed`) if the page shell
should render before slow data arrives.

**Calling a database or secret-bearing API from a universal `load` (`+page.js`).**
Why it's a problem: universal `load` functions run on both server and client
(e.g., on client-side navigation). Any credential, connection string, or
private API key referenced there ships to the browser bundle or executes with
browser-available credentials, exposing secrets.
Alternative: move the code to `+page.server.js`/`+layout.server.js`, which runs
only on the server, and pass the derived (non-secret) result down through
`data`.

**Waterfalling independent `load` calls.**
Why it's a problem: awaiting one fetch before starting an unrelated second
fetch inside the same `load` function serializes latency that could be
parallel.
Alternative: start independent fetches without awaiting immediately, then
`await Promise.all([...])`, or rely on SvelteKit's parallel `load` execution
across `+layout` and `+page` boundaries (which already run in parallel;
sequential dependency should exist only when one call's input depends on
another's output).

## State Management

**Module-level mutable state on the server.**
Why it's a problem: a `.js`/`.ts` module is instantiated once per server
process, not once per request. A `writable`/`$state` value at module scope
that stores per-user or per-request data (current user, cart contents, request
locale) is shared across every concurrent request the server handles, leaking
one user's data into another's response — a serious correctness and privacy
bug that will not show up in single-user local testing.
Alternative: derive per-request data in `load`/hooks and pass it through
`event.locals` or the `data` prop; use context (`setContext`/`getContext`)
scoped to a component tree for per-render shared state, never a module-level
singleton, for anything request- or session-specific.

**One global "app store" holding unrelated state.**
Why it's a problem: a single store/`$state` object accumulating auth, UI
theme, form drafts, and feature flags becomes an untyped god-object every
component depends on, making changes risky and testing hard — any component
can read or write any part of global state.
Alternative: scope stores/runes modules to the feature or route that owns
them; expose narrow, purpose-specific stores (`authStore`, `themeStore`)
instead of one shared blob.

**Manual `.subscribe()` without unsubscribing.**
Why it's a problem: calling `store.subscribe(cb)` directly inside component
setup without storing and calling the returned unsubscribe function leaks the
subscription after the component is destroyed, keeping the callback (and
whatever it closes over) alive indefinitely.
Alternative: use the `$store` auto-subscription syntax in a `.svelte` file,
which Svelte compiles into a properly-cleaned-up subscription; reserve manual
`.subscribe()` for non-component `.ts` code, where the caller must call the
returned unsubscribe explicitly (e.g., in an `$effect` teardown).

**Using `$effect` to mirror one state into another.**
Why it's a problem: `$effect(() => { total = price * qty })` is push-based and
introduces an extra render pass and ordering ambiguity versus a pull-based
computation; it also cannot be used outside a component/effect root as easily
as a plain derived value, and multiplies re-run surface as more effects depend
on `total`.
Alternative: `let total = $derived(price * qty)`. Reserve `$effect` for actual
side effects (DOM measurement, subscriptions, analytics calls, syncing to
storage).

## Components

**Boolean-prop explosion instead of composition.**
Why it's a problem: a component with `compact`, `bordered`, `withIcon`,
`withFooter`, `variant`, etc., grows an internal branching mess and forces
every consumer to read the prop list to guess the rendered output.
Alternative: use slots/snippets or separate composed components
(`<Card><CardHeader/><CardFooter/></Card>`) so structure is visible at the
call site.

**Overusing `bind:` for parent/child communication.**
Why it's a problem: pervasive two-way binding makes data flow hard to trace —
any child can silently mutate a parent's state, which is fine for genuine
form-control-like components but becomes unmanageable when used as the default
communication style for arbitrary components.
Alternative: pass data down via props, communicate up via callback props;
reserve `bind:`/`$bindable` for components that behave like native form
controls (an editable field, a custom `<select>`-like widget).

**Deep prop-drilling instead of context.**
Why it's a problem: threading a value through five layers of components that
don't use it themselves just to reach a deeply nested consumer couples every
intermediate component to a concern it doesn't own, and makes refactors touch
unrelated files.
Alternative: use `setContext`/`getContext` at the point the value is produced
and consumed, keeping intermediate components free of the pass-through prop.

## Rendering and Markup

**Unnecessary `{@html ...}`.**
Why it's a problem: `{@html}` injects raw HTML with no sanitization, and is a
direct XSS vector if the content includes any user-controlled or
externally-sourced string.
Alternative: render structured data with normal Svelte markup; if raw HTML is
genuinely required (e.g., rendering sanitized Markdown output), sanitize
server-side with a vetted library and treat this as a
[`security-review`](../../security-review/SKILL.md) trigger.

**Suppressing compiler accessibility warnings by default.**
Why it's a problem: `<!-- svelte-ignore a11y-click-events-have-key-events -->`
and similar directives silence a real signal that the markup is not usable via
keyboard or assistive technology; reflexively adding these to make warnings
disappear ships inaccessible UI.
Alternative: fix the underlying markup (use a `<button>` instead of a `<div>`
with a click handler, add the missing `alt`/label); only suppress with a
comment explaining the specific, reviewed reason it doesn't apply.

## Forms and Actions

**Hand-rolled `fetch` + `preventDefault` instead of form actions.**
Why it's a problem: reimplementing submission with client-side `fetch`
duplicates validation, loses progressive enhancement (the form stops working
if JavaScript fails to load or execute), and bypasses SvelteKit's built-in
handling of redirects, cookies, and `fail()`-based validation state.
Alternative: use a `+page.server.js` form action with a native `<form method="POST">`,
enhanced with `use:enhance` for a SPA-like experience that still works without
JavaScript.

**Throwing raw errors from actions instead of `fail()`.**
Why it's a problem: throwing an exception for a validation failure loses the
submitted form values and triggers the nearest error boundary instead of
re-rendering the form with field-level errors — a jarring UX for something as
routine as "email is required."
Alternative: `return fail(400, { errors, values })` for expected validation
failures; reserve thrown `error()`/uncaught exceptions for truly exceptional
conditions.

## Deployment

**Assuming server-only routes work under `adapter-static`.**
Why it's a problem: a fully static/prerendered deployment has no server
runtime at request time; `+page.server.js` data loading, form actions, and
`+server.js` endpoints that aren't prerendered will not function, causing
silent 404s or build failures that surface late.
Alternative: check `svelte.config.js` for the configured adapter before adding
server-only routes, and use a server-capable adapter (`adapter-node`, a
platform adapter) when the app needs live server behavior.
