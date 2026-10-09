import { z } from "zod";

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

export const UserInputSchema = z.object({
  displayName: z.string().trim().min(1).max(80),
  email: z.email(),
}).strict();
export type UserInput = z.output<typeof UserInputSchema>;
export function parseUserInput(input: unknown): UserInput { return UserInputSchema.parse(input); }

export const ProfileSchema = UserInputSchema.safeExtend({
  id: z.uuid(),
  address: z.object({ country: z.string().length(2), postalCode: z.string().min(1).max(20) }).strict(),
});
const SearchIntentSchema = z.object({ kind: z.literal("search"), query: z.string().min(1) }).strict();
const OpenIntentSchema = z.object({ kind: z.literal("open"), resourceId: z.uuid() }).strict();
export const IntentSchema = z.discriminatedUnion("kind", [SearchIntentSchema, OpenIntentSchema]);
export const PaginationSchema = z.object({ cursor: z.string().min(1).optional(), limit: z.coerce.number().int().min(1).max(100).default(20) }).strict();
export const DateRangeSchema = z.object({ start: z.iso.datetime({ offset: true }), end: z.iso.datetime({ offset: true }) })
  .transform(({ start, end }) => ({ start: new Date(start), end: new Date(end) }))
  .superRefine(({ start, end }, context) => { if (end.getTime() < start.getTime()) context.addIssue({ code: "custom", path: ["end"], message: "end precedes start" }); });

export const CategorySchema: z.ZodType<{ name: string; children: unknown[] }> = z.object({
  name: z.string().min(1),
  get children() { return z.array(CategorySchema); },
});
export const LazyNodeSchema: z.ZodType<{ value: string; next?: unknown }> = z.lazy(() => z.object({ value: z.string(), next: LazyNodeSchema.optional() }).strict());
const unavailableUsernames = new Set(["admin", "root"]);
export const AvailableUsernameSchema = z.string().min(3).refine(async (name) => !unavailableUsernames.has(name.toLowerCase()), { error: "unavailable username" });

export type ValidationProblem = { code: "invalid_input"; issues: Array<{ code: string; path: Array<string | number> }> };
export function toValidationProblem(error: z.ZodError): ValidationProblem {
  return { code: "invalid_input", issues: error.issues.map((issue) => ({ code: issue.code, path: issue.path.slice(0, 8).map((part) => typeof part === "string" || typeof part === "number" ? part : String(part)) })) };
}
type CategoryInput = { name: unknown; children: unknown };
function preflightCategory(input: unknown): void {
  const pending: Array<{ value: unknown; depth: number }> = [{ value: input, depth: 1 }]; let nodes = 0;
  while (pending.length) {
    const current = pending.pop()!;
    if (!current.value || typeof current.value !== "object" || Array.isArray(current.value)) throw new Error("category node shape");
    const node = current.value as CategoryInput;
    if (typeof node.name !== "string" || !Array.isArray(node.children)) throw new Error("category node fields");
    if (++nodes > 1_000) throw new Error("category node limit");
    if (current.depth > 8) throw new Error("category depth limit");
    if (node.children.length > 100) throw new Error("category child limit");
    for (const child of node.children) pending.push({ value: child, depth: current.depth + 1 });
  }
}
export function parseCategoryInput(input: unknown): z.output<typeof CategorySchema> { preflightCategory(input); return CategorySchema.parse(input); }
function rejects(operation: () => unknown): boolean { try { operation(); return false; } catch { return true; } }

async function main(): Promise<void> {
  const base = { displayName: " Ada ", email: "ada@example.com" };
  assert(parseUserInput(base).displayName === "Ada", "trimmed name");
  assert(UserInputSchema.safeParse({ ...base, displayName: "😀".repeat(80) }).success, "80 code points");
  assert(!UserInputSchema.safeParse({ ...base, displayName: "😀".repeat(81) }).success, "81 code points");
  const profile = { ...base, id: "00000000-0000-4000-8000-000000000000", address: { country: "US", postalCode: "1" } };
  assert(ProfileSchema.safeParse(profile).success, "profile");
  assert(!ProfileSchema.safeParse({ ...profile, address: { country: "U", postalCode: "1" } }).success, "country short");
  assert(!ProfileSchema.safeParse({ ...profile, address: { country: "USA", postalCode: "1" } }).success, "country long");
  assert(ProfileSchema.safeParse({ ...profile, address: { country: "US", postalCode: "x".repeat(20) } }).success, "postal upper");
  assert(!ProfileSchema.safeParse({ ...profile, address: { country: "US", postalCode: "" } }).success, "postal empty");
  assert(!ProfileSchema.safeParse({ ...profile, address: { country: "US", postalCode: "x".repeat(21) } }).success, "postal long");
  assert(IntentSchema.safeParse({ kind: "search", query: "zod" }).success, "search"); assert(IntentSchema.safeParse({ kind: "open", resourceId: profile.id }).success, "open");
  assert(!IntentSchema.safeParse({ kind: "search", query: "zod", resourceId: profile.id }).success, "strict search"); assert(!IntentSchema.safeParse({ kind: "open", resourceId: profile.id, query: "zod" }).success, "strict open");
  const paginationInput: z.input<typeof PaginationSchema> = { limit: "1" }; const paginationOutput: z.output<typeof PaginationSchema> = PaginationSchema.parse(paginationInput);
  assert(paginationInput.limit === "1" && paginationOutput.limit === 1, "input output divergence"); assert(PaginationSchema.parse({}).limit === 20, "default"); assert(PaginationSchema.parse({ limit: "100" }).limit === 100, "upper");
  for (const invalid of [0, 101, 1.5]) assert(!PaginationSchema.safeParse({ limit: invalid }).success, "pagination boundary");
  assert(DateRangeSchema.safeParse({ start: "2026-01-01T00:00:00Z", end: "2026-01-01T00:00:00Z" }).success, "equal");
  assert(DateRangeSchema.safeParse({ start: "2026-01-01T00:00:00.500Z", end: "2025-12-31T19:00:00.500-05:00" }).success, "fractional offsets");
  const invalidRange = DateRangeSchema.safeParse({ start: "2026-01-01T01:00:00+01:00", end: "2025-12-31T23:59:59Z" }); assert(!invalidRange.success && invalidRange.error.issues.some((i) => i.path.join(".") === "end"), "end issue");
  const leaf = { name: "leaf", children: [] }; assert(parseCategoryInput(leaf).name === "leaf", "category");
  const hundred = { name: "root", children: Array.from({ length: 100 }, (_, i) => ({ name: String(i), children: [] })) }; assert(parseCategoryInput(hundred).children.length === 100, "child limit"); assert(rejects(() => parseCategoryInput({ ...hundred, children: [...hundred.children, leaf] })), "child over");
  let deep: unknown = leaf; for (let i = 0; i < 7; i++) deep = { name: String(i), children: [deep] }; assert(parseCategoryInput(deep).name === "6", "depth limit"); let tooDeep: unknown = leaf; for (let i = 0; i < 8; i++) tooDeep = { name: String(i), children: [tooDeep] }; assert(rejects(() => parseCategoryInput(tooDeep)), "depth over");
  const nodes = { name: "root", children: Array.from({ length: 100 }, (_, index) => ({ name: "branch", children: Array.from({ length: index < 99 ? 9 : 8 }, () => leaf) })) }; assert(parseCategoryInput(nodes).name === "root", "node limit"); const tooManyNodes = { name: "root", children: Array.from({ length: 100 }, () => ({ name: "branch", children: Array.from({ length: 10 }, () => leaf) })) }; assert(rejects(() => parseCategoryInput(tooManyNodes)), "node over"); let adversarial: unknown = leaf; for (let i = 0; i < 10_000; i++) adversarial = { name: "deep", children: [adversarial] }; assert(rejects(() => parseCategoryInput(adversarial)), "iterative deep preflight");
  assert(LazyNodeSchema.safeParse({ value: "one", next: { value: "two" } }).success, "lazy"); assert((await AvailableUsernameSchema.safeParseAsync("candidate")).success, "async valid"); assert(!(await AvailableUsernameSchema.safeParseAsync("admin")).success, "async invalid");
  const rejected = UserInputSchema.safeParse({}); assert(!rejected.success && toValidationProblem(rejected.error).code === "invalid_input", "normalized error"); assert(z.toJSONSchema(UserInputSchema, { io: "input" }).type === "object", "json schema");
  assert(z.validate(UserInputSchema, base), "validate"); assert(await z.validateAsync(AvailableUsernameSchema, "candidate"), "validate async");
  const compiled = z.compile(UserInputSchema); for (const sample of [base, { ...base, displayName: "" }]) assert(compiled.safeParse(sample).success === UserInputSchema.safeParse(sample).success, "compiled parity"); const derived = UserInputSchema.safeExtend({ role: z.literal("member") }); assert(z.compile(derived).safeParse({ ...base, role: "member" }).success, "derived compile"); assert(rejects(() => z.compile(AvailableUsernameSchema, { strict: true })), "async compile rejected");
  console.log("Zod 4.5 examples passed");
}
void main();
