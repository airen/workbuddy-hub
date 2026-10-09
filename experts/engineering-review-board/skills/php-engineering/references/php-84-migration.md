# PHP 8.4 Migration Reference

Use this reference only for PHP 8.4 adoption, compatibility review, or migration. First establish the project’s declared PHP range, deployed extensions, and CI matrix. PHP 8.4 features are not a reason to raise a project’s minimum version without an explicit compatibility decision.

## Adoption Sequence

1. Read the target’s `composer.json` platform constraints, CI images, extension requirements, and supported deployment runtimes.
2. Run configured tests and static analysis on the declared support matrix before and after the change.
3. Search for deprecated and incompatible constructs, including implicit nullable parameters and `E_USER_ERROR` use through `trigger_error()`.
4. Migrate only where the new construct clarifies an existing contract; do not make an API change merely to use a feature.

## New Language And Library Surfaces

- **Property hooks:** a backed property has storage and may validate, normalize, or derive local behavior through hooks; a virtual property has hooks without backing storage. Constructor-promotion behavior and visibility must be reviewed deliberately. Hooks are incompatible with `readonly` properties. Keep hooks local: no hidden database, network, service lookup, logging, or other I/O.
- **Asymmetric property visibility:** use `public private(set)` or `public protected(set)` when public reads and constrained writes express the real contract. It controls property writes, not the mutability of objects referenced by that property.
- **Deprecation attribute:** use `#[\Deprecated]` when a declaration’s deprecation needs machine-readable metadata; preserve an existing `@deprecated` annotation only when human or tooling compatibility needs both.
- **Lazy objects:** Reflection APIs can create and manage lazy objects. Keep initialization behavior explicit and test lifetime, errors, and side effects.
- **Chained `new`:** `new MyClass()->method()` no longer requires wrapping constructor parentheses.
- **Array predicates:** `array_find()`, `array_find_key()`, `array_any()`, and `array_all()` express common search and predicate operations without manual loops.
- **Multibyte helpers:** `mb_trim()`, `mb_ltrim()`, `mb_rtrim()`, `mb_ucfirst()`, and `mb_lcfirst()` add Unicode-aware trimming and first-character case operations when `mbstring` is installed.
- **Math and dates:** `RoundingMode` makes rounding intent explicit; DateTime adds microsecond and timestamp helpers. Verify exact installed-version behavior before changing serialization or persisted values.
- **Request parsing and DOM:** `request_parse_body()` supports parsing request bodies outside normal form handling; `Dom\HTMLDocument` and the new DOM API provide modern HTML document parsing/manipulation. Validate input bounds and output encoding at these boundaries.
- **Numbers and drivers:** `BcMath\Number` offers object-oriented arbitrary-precision arithmetic. PDO adds driver-specific subclasses; code must not assume generic PDO behavior when it depends on a driver.
- **Extensions:** review extension availability and changed APIs, including `mysqli`, against the actual deployment image rather than assuming a development installation represents production.

## Before And After

### Accessors to a backed property hook

```php
// Before
final class TaxRate {
    private float $value;
    public function setValue(float $value): void { $this->value = max(0, $value); }
    public function value(): float { return $this->value; }
}

// PHP 8.4, when the project requires it
final class TaxRate {
    public float $value {
        set (float $value) => max(0, $value);
    }
}
```

### Public read, private write

```php
// Before
final class Order {
    private string $status = 'draft';
    public function status(): string { return $this->status; }
}

// PHP 8.4
final class Order {
    public private(set) string $status = 'draft';
}
```

### Explicit nullable parameter

```php
// Before: implicit nullable parameter is deprecated
function render(string $title = null): string { return $title ?? ''; }

// After
function render(?string $title = null): string { return $title ?? ''; }
```

### Predicate helpers

```php
// Before
$hasOverdue = false;
foreach ($invoices as $invoice) {
    if ($invoice->isOverdue()) { $hasOverdue = true; break; }
}

// After
$hasOverdue = array_any($invoices, fn (Invoice $invoice): bool => $invoice->isOverdue());
$firstOverdue = array_find($invoices, fn (Invoice $invoice): bool => $invoice->isOverdue());
```

Use `array_find_key()` when the matching key is needed, and `array_all()` when every element must satisfy a predicate. Preserve behavior for empty collections and callbacks before replacement.

## Compatibility Checklist

- Require a supported-version CI/runtime matrix before introducing PHP 8.4-only
  syntax, including deployed extensions and target PHP versions.
- Replace implicit nullable parameters with `?T` or `T|null`; do not retain `_`
  class names or depend on removed `E_STRICT`.
- Replace `trigger_error(..., E_USER_ERROR)` with an intentional exception or
  `exit()`/`die()` contract. Review `exit()`/`die()` behavior changes: they now
  follow normal type coercion and `strict_types`, and invalid types raise
  `TypeError`.
- Replace deprecated `mysqli_ping()`, `mysqli_kill()`, and `mysqli_refresh()`
  uses; remove references to legacy removed `mysqli` constants such as
  `MYSQLI_SET_CHARSET_DIR`, `MYSQLI_STMT_ATTR_PREFETCH_ROWS`,
  `MYSQLI_CURSOR_TYPE_FOR_UPDATE`, `MYSQLI_CURSOR_TYPE_SCROLLABLE`, and
  `MYSQLI_TYPE_INTERVAL`.
- Audit typed extension constants/properties, resource-to-object changes, and
  newly raised `ValueError` cases before relying on prior coercion, warning, or
  resource-check behavior.
- Review `readonly` combinations, visibility assumptions, constructor promotion,
  reflection use, extension availability, `mysqli`, and PDO driver behavior.
- Treat the migration guide as the canonical compatibility source; target-project
  policy decides whether a deprecated construct is removed now, version-gated,
  or scheduled.

## Official Sources

- <https://www.php.net/releases/8.4/en.php>
- <https://www.php.net/manual/en/migration84.php>
- <https://www.php.net/manual/en/language.oop5.property-hooks.php>
- <https://www.php.net/manual/en/language.oop5.visibility.php>
- <https://www.php.net/manual/en/migration84.deprecated.php>
- <https://www.php.net/manual/en/migration84.incompatible.php>
