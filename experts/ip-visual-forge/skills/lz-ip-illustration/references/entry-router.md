# Entry Router

Use this reference at the start of every request.

## Allowed IP Sources

Only these sources count as initialized IP assets:

1. A user-specified IP folder.
2. `ip-assets/<ip-slug>/` in the current project.
3. `ip-assets/` in the current project, only when it contains exactly one initialized IP.

An initialized IP must include:

- `ip-profile.md`
- `visual-spec.md`
- `prompt-pack.md`
- at least one reference image under `reference-images/` or a clear text-only reference in `visual-spec.md`

## Forbidden Substitutes

Never use these as current project IP assets:

- `examples/`
- demo assets
- bundled sample IPs
- prior test assets
- images generated in earlier conversations
- conversation history
- model memory
- assets from unrelated projects

Demo assets are examples only. They can guide how to structure outputs, but they cannot satisfy the initialized-IP gate.

## Article Illustration Gate

If the user asks for article illustrations and no initialized IP exists in the allowed sources:

1. Stop before parsing the article into illustration prompts.
2. Tell the user no current project IP was found.
3. Ask the user either to specify an existing IP folder or create a new IP.
4. If creating a new IP, enter `references/ip/brief-first-interview.md`.

Do not silently choose an example IP.

## Existing IP Selection Gate

When initialized IP assets do exist:

- If there are zero initialized IPs, ask the user to specify an existing IP folder or create a new IP.
- If there is exactly one initialized IP, ask the user whether to use that IP or create a new one, unless the user already clearly indicated they want the existing one.
- If there are multiple initialized IPs, ask the user which IP to use or whether to create a new one.

Do not silently continue with an existing IP merely because it is the only one in the current project. The entry router should make the choice explicit unless the user's wording already made the choice explicit.
