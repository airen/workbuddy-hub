# Svelte and SvelteKit Design Patterns

Patterns that recur in production SvelteKit applications, with the mechanics
and the trade-off each one manages.

## Layout Composition

- Use nested `+layout.svelte` files to share chrome (nav, footer, providers)
  across a route subtree without repeating markup per page. Each layout wraps
  its child routes' rendered output via the layout's `{@render children()}` (or
  `<slot />` in Svelte 4 syntax).
- Use route groups — a directory named `(group)` — to apply a layout to a set
  of routes without adding a path segment to the URL. Common uses: an
  `(app)` group with an authenticated shell layout, and a separate
  `(marketing)` group with a public layout, both under `src/routes`.
- Break out of layout inheritance deliberately with `+layout@.svelte` (reset to
  the root layout) or `+page@.svelte`/`+layout@(group).svelte` (reset to a
  specific ancestor) for pages that need a fundamentally different shell (e.g.,
  a full-screen onboarding flow inside an otherwise chrome-heavy app).
- Keep layout `load` functions focused on data every child route actually
  needs (current user, navigation data); push page-specific data into that
  page's own `load` rather than over-fetching in a shared layout.

## Load Functions

- **Universal vs. server `load`:** use `+page.server.js`/`+layout.server.js`
  when the code needs server-only capabilities (database access, secrets,
  `cookies`, filesystem) or must guarantee it never runs in the browser. Use
  `+page.js`/`+layout.js` for data-fetching that's safe to run on the client
  too (e.g., calling a public API) and that benefits from running during
  client-side navigation without a server round-trip.
- **Parallel loading:** SvelteKit runs a page's and its ancestor layouts'
  `load` functions concurrently by default. Preserve that by not manually
  awaiting a parent's data inside a child `load` unless the child genuinely
  depends on it — access shared data via `await parent()` only when a real
  dependency exists.
- **Streaming slow data:** return a promise (not an awaited value) inside a
  `load`'s returned object to stream it in after the initial render:
  `return { critical: await fastCall(), streamed: { slow: slowCall() } }`. The
  page template then awaits `data.streamed.slow` inside `{#await}` so the shell
  and fast data render immediately.
- **Invalidation:** use `depends('app:key')` inside a `load` and call
  `invalidate('app:key')` (or `invalidateAll()`) after a mutation to re-run the
  affected `load` functions without a full navigation. Prefer targeted
  `invalidate` over `invalidateAll` when only specific data changed, to avoid
  re-fetching unrelated data.
- **Redirect and error from `load`:** use `redirect(303, '/login')` for
  auth-gated routes and `error(404, 'Not found')` for missing resources,
  rather than returning a sentinel value and branching in the template.

## Form Actions and Progressive Enhancement

- Define named actions (`export const actions = { create: async (event) => {...}, delete: async (event) => {...} }`)
  in `+page.server.js` for a page with multiple distinct mutations, and target
  them from markup with `<form method="POST" action="?/delete">`.
- Enhance forms with `use:enhance` to get SPA-like behavior (no full page
  reload, automatic `data`/`form` prop updates) while the form remains a real
  `<form>` that works with JavaScript disabled or before hydration completes —
  this is the core of SvelteKit's progressive-enhancement story.
- Return validation failures with `fail(400, { values, errors })` so the form
  re-renders with the user's input preserved and field-level errors available
  via the `form` prop, instead of losing state on a failed submission.
- Use a custom `use:enhance` callback only when you need to intercept the
  default behavior (optimistic UI, custom redirect handling, toast
  notifications on success); otherwise the default behavior already handles
  the common case correctly.
- For multi-step or wizard-style forms, keep step state in the URL (query
  params or route segments) or server-side session rather than only in
  component state, so back/forward navigation and page reloads behave
  correctly.

## Route-Level Data Patterns

- **Optional data via `+page.js` combined with `+page.server.js`:** a page can
  export `load` from both files; the server `load`'s return value is passed as
  input to the universal `load`, letting the universal `load` enrich or
  reshape server data with client-available context (e.g., `fetch` for a
  public third-party API) without exposing secrets.
- **Shared `fetch`:** use the `fetch` provided to `load` functions (not the
  global `fetch`) so SvelteKit can dedupe/cache the call during SSR and inline
  the response into the initial HTML for hydration, avoiding a duplicate
  client-side request.
- **Typed route params:** use `src/params/*.js` matcher functions to validate
  dynamic segments (e.g., `[id=integer]`) at the routing layer instead of
  parsing and validating the same param inside every `load`/action that uses
  it.

## State Sharing Patterns

- **Context-scoped stores for per-request/per-tree state:** create the
  store/`$state` object inside a component (commonly the root layout) and
  register it with `setContext` so it's fresh per component-tree instance —
  critical for SSR safety, since a module-level singleton would leak between
  requests.
- **`.svelte.js`/`.svelte.ts` modules for shared runes state:** export a
  `$state`-based object from a plain module when the state is genuinely
  global and safe to share (e.g., a client-only UI preference), understanding
  that on the server this module is still process-wide — do not put
  per-request data here.
- **Snapshot/URL-driven state:** for state that should survive a reload or be
  shareable via link (filters, pagination, selected tab), store it in the URL
  (`page.url.searchParams`) rather than only in component state, and read it
  back in `load` so SSR renders the correct initial view.

## Authentication and Session Patterns

- Populate `event.locals.user` in `hooks.server.js` by validating the session
  cookie once per request, then read `locals.user` from any `load`/action/
  `+server.js` — avoid re-validating the session independently in every route.
- Gate protected routes with a check in the nearest relevant `+layout.server.js`
  (or a route-group layout) that `redirect()`s unauthenticated requests, rather
  than repeating the check in every page.
- Keep the session/auth cookie `httpOnly`, `secure`, and `sameSite`-appropriate;
  never expose the raw session token to client-side JavaScript or `$state`.
