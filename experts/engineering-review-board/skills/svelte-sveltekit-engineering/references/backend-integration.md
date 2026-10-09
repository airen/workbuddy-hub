# Integrating SvelteKit With a Separate Backend

Use this reference when a SvelteKit app is the frontend for a backend owned by
a different language/framework, rather than doing all server-side work in
SvelteKit's own `+server.js`/`+page.server.js`. It covers the SvelteKit side of
the integration; route the backend's own implementation to its owning skill.

## Choosing a Topology

Three common topologies, in order of how much SvelteKit does:

1. **SvelteKit as pure static/SPA client, backend is the only server.** The
   SvelteKit app is built with `adapter-static` (or runs client-only) and talks
   to the backend's API directly from the browser via `fetch`. Simplest to
   deploy (static hosting/CDN for the frontend), but the browser must handle
   CORS, and any secret needed to call the backend cannot live in the frontend
   bundle. Use when the backend already exposes a public, browser-safe API
   (e.g., public read endpoints, or an API designed for first-party SPA
   clients with its own auth).
2. **SvelteKit as backend-for-frontend (BFF).** SvelteKit runs its own server
   (`adapter-node` or a platform adapter) and its `+page.server.js`/
   `+server.js` call the backend server-to-server, keeping backend credentials,
   internal URLs, and response shaping off the client. The browser only ever
   talks to SvelteKit. Use when the backend API isn't meant for direct browser
   use, needs a shared secret/service token, needs response aggregation from
   multiple backend calls, or when session cookies should be scoped to the
   SvelteKit origin rather than the backend's.
3. **Reverse-proxied single origin.** An edge proxy (nginx, Caddy, a cloud
   load balancer, or the platform's routing rules) puts SvelteKit and the
   backend behind the same origin (e.g., `/api/*` to the backend, everything
   else to SvelteKit). This avoids CORS entirely and lets cookies be
   first-party for both, at the cost of an extra infrastructure component to
   operate. Use when both sides need to share cookies/session without a BFF
   layer duplicating logic, or when the backend team owns its own deployment
   independently of the frontend.

Default to the BFF topology (option 2) for anything handling authentication,
secrets, or non-trivial data shaping — it keeps SvelteKit's existing
`load`/action model as the single integration point and avoids browser-side
CORS and credential exposure. Reach for the reverse-proxy topology when both
teams need independent deployments but still want same-origin cookies.

## API Communication

- Call the backend from `+page.server.js`, `+layout.server.js`, or
  `+server.js` using the platform's `fetch` (SvelteKit injects a `fetch` into
  `load`/action `event` that supports relative URLs and credential forwarding
  during SSR) — do not call the backend directly from a `.svelte` component or
  a universal `load` when the call requires a secret or internal-only URL.
- Centralize backend base URL, timeout, and auth-header construction in a
  single `$lib/server/api.ts`-style client module, so every route calls a
  typed function (`getOrder(id)`) instead of constructing fetch calls inline.
  This is the natural seam for retry/timeout policy and for swapping the
  backend implementation later.
- Model the backend's request/response shapes with explicit TypeScript types,
  generated from the backend's OpenAPI/schema when available rather than
  hand-transcribed, so contract drift surfaces as a type error. Route the
  contract shape itself to [`api-design`](../../api-design/SKILL.md) when it's
  still being decided jointly with the backend team.
- Propagate correlation/request IDs from SvelteKit hooks to backend calls so a
  single request can be traced across both systems; coordinate the header
  name and format with [`observability-engineering`](../../observability-engineering/SKILL.md).
- Handle backend errors explicitly: map backend error codes/status to
  SvelteKit's `error()`/`fail()` rather than letting a raw backend error object
  reach the template, so the frontend controls its own user-facing error
  messages independent of backend wording changes.

## Authentication Handoff

- **Session cookie owned by the backend, forwarded by SvelteKit (BFF):**
  SvelteKit's server calls the backend with the incoming request's session
  cookie (or a derived service token) attached, validates/refreshes it in
  `hooks.server.js`, and stores the resulting user on `event.locals`. The
  browser only ever sees the SvelteKit-issued cookie.
- **Session cookie owned by SvelteKit, backend trusts a signed token:**
  SvelteKit issues and manages its own session cookie, and calls the backend
  with a short-lived signed token (JWT or similar) that the backend verifies
  independently (shared secret or public key) without a shared session store.
  This decouples session lifecycle from the backend and scales well when the
  backend is called by multiple frontends.
- **Direct-to-API from the browser (SPA topology):** the backend issues and
  validates its own tokens (e.g., OAuth2/OIDC with PKCE) directly with the
  browser; SvelteKit does not sit in the auth path at all. Only viable when the
  backend's auth flow is designed for public clients and CORS is configured
  correctly.
- Whichever handoff is used, never forward a raw third-party API key or
  backend admin credential to the browser, and never store a backend session
  token in `localStorage`/non-`httpOnly` cookies where client-side JavaScript
  (and therefore any XSS) can read it.
- Treat every new auth handoff design as a
  [`threat-modeling`](../../threat-modeling/SKILL.md) trigger, and load
  [`security-review`](../../security-review/SKILL.md) for the implementation:
  CSRF exposure changes depending on whether cookies are same-origin
  (reverse-proxy) or cross-origin (direct SPA-to-API), and token storage
  location is a primary attack surface either way.

## Backend-Specific Notes

- **Rust/Axum:** Axum services typically expose JSON over HTTP; call them from
  SvelteKit's server-side `fetch` exactly like any other backend. If the same
  team owns both sides, prefer sharing the API contract via an OpenAPI spec or
  a generated TypeScript client rather than hand-syncing types across
  languages. Route Axum handler/middleware/auth implementation to
  [`rust-async-web`](../../rust-async-web/SKILL.md).
- **PHP:** a PHP backend (Laravel, Symfony, or plain PHP) commonly issues
  session cookies via `Set-Cookie` and expects them echoed back; when
  SvelteKit is a BFF in front of it, forward the `Cookie` header on
  server-to-server calls and keep `SameSite`/`secure` attributes consistent
  between what PHP sets and what SvelteKit's own cookies use. Route PHP-side
  implementation to [`php-engineering`](../../php-engineering/SKILL.md).
- **Python (FastAPI/Django):** FastAPI's typed Pydantic models and
  OpenAPI/JSON-schema output are a good source for generating the TypeScript
  types SvelteKit consumes — prefer generating over hand-transcribing. Django
  session/CSRF cookies (`csrftoken`, `sessionid`) require sending the CSRF
  token back on mutating requests if SvelteKit calls Django directly rather
  than through its own session layer; account for this explicitly in whichever
  topology is chosen. Route FastAPI/Django implementation to
  [`python-engineering`](../../python-engineering/SKILL.md).
- For any backend, treat its OpenAPI/schema (when available) as the source of
  truth for the SvelteKit-side types, and re-generate rather than diverge when
  the backend contract changes.

## Deployment Strategies

- **Separate services, separate deploys:** SvelteKit (Node/edge adapter) and
  the backend deploy independently, communicating over the network (private
  network/VPC when possible, otherwise authenticated HTTPS). Simplest to scale
  each side independently; requires explicit CORS or a proxy for browser
  calls that bypass the BFF.
- **Single reverse-proxied deploy:** both services run behind one ingress/load
  balancer or one container network, sharing an origin. Route the proxy/ingress
  and container topology to
  [`container-engineering`](../../container-engineering/SKILL.md); this skill
  only owns the SvelteKit adapter and route/API-path configuration on top of
  that topology.
- **Static frontend + API backend on a CDN/edge platform:** `adapter-static`
  output goes to a CDN, and the backend runs separately (its own server,
  serverless functions, or another provider). Fastest to serve, but every
  server-only SvelteKit feature (form actions, `+page.server.js`, `+server.js`)
  is unavailable — the backend must supply everything, including CSRF
  protection and cookie-based auth if used.
- Keep environment-specific backend URLs and secrets out of source; use
  SvelteKit's `$env/static/private` (server-only, statically replaced) and
  `$env/dynamic/private` for runtime-configured values, never `$env/*/public`
  for anything that must stay server-only.
