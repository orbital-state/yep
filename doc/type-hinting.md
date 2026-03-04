# Type hinting for vars + chain wiring (design note)

This note captures a possible direction for making yep’s implicit wiring more explicit by using **type hints**.

It is **not implemented** in the current repo; today yep wires steps by **function order + next-step parameter names**, and only pulls `vars` into the **first** step.

## Current behavior (today)

### Vars (defaults)

The Python reflector currently extracts only **top-level string assignments** as default vars.

Example:

```py
# reflected
image_tag = "dev"   # string default

# not reflected today
publish_latest = False
retries = 3
```

### Step discovery

Steps are top-level public functions (module scope, not starting with `_`, not `main`), in source order.

### Wiring rule (local target)

- First step is called using a filtered subset of `vars`.
- For each step *i*, the wrapper looks at the **next step’s parameter names** and assigns step *i*’s return value(s) into variables with those names.

So if the next step is `show(text)`, the wrapper does:

```py
text = make_message(...)
show(text)
```

This is convenient but has two costs:

- Wiring is “magic” unless you’ve read the rule.
- Errors show up late (runtime) and can be confusing (arity mismatches, wrong shapes, etc.).

## What type hints could improve

Type hints could be used to provide **earlier feedback** and improve explainability, without forcing Python to behave like a static language.

Two separate (but related) areas:

1. **Vars typing:** validating that values pulled from `vars` match what the first step expects.
2. **Edge typing:** validating that step outputs match the next step’s expected input types.

## Proposed: optional type-hint-aware validation (Python)

### Goals

- Keep Python pipelines ergonomic: type checks should be **optional** and mostly produce **warnings**, not hard failures.
- Avoid importing arbitrary user code during reflection when possible.
- Keep the pipeline declaration “just code” (no separate YAML).

### Non-goals

- Full static type checking (mypy-equivalent) inside yep.
- Enforcing types at runtime for every step.

### 1) Vars typing: first step validation

Given:

```py
message: str = "Hello"  # (future) reflected default via AnnAssign

def make_message(message: str) -> str:
    return message
```

When a user runs:

```bash
yep run --vars message:123
```

Today, `message` arrives as a **string** from the CLI anyway. But type hints still help for:

- tooling / docs (“message is a string”)
- future non-string vars extraction (see below)

Potential validations (at wrap-time or run-time):

- If the first step parameter is annotated as `int`, warn that CLI vars are strings unless a coercion rule exists.
- If the first step parameter is annotated as `bool`, suggest accepted spellings (`true/false/1/0/yes/no`).

A pragmatic approach is to define a small set of **coercion rules** (opt-in):

- `str`: pass through
- `int`: `int(value)`
- `float`: `float(value)`
- `bool`: parse common true/false tokens
- `Path`: `Path(value)`

Then wrapper generation could include coercion for the first step only.

### 2) Edge typing: step-to-step checks

Given:

```py
def make_message(message: str) -> str:
    return message

def show(text: str) -> None:
    print(text)
```

The wrapper currently infers that `make_message` flows into `show(text)`.

Type hints could make this edge explainable:

- `make_message` returns `str`
- `show` expects `text: str`
- therefore `make_message -> show` is a compatible edge

If there is a mismatch:

```py
def make_number(message: str) -> int:
    return 123

def show(text: str) -> None:
    print(text)
```

Then yep could emit a warning during `yep wrap`:

- “Edge `make_number -> show(text)` looks incompatible: returns `int`, expects `str`.”

### Important caveat (Python reality)

Python annotations are not always reliable:

- functions may return different types at runtime
- annotations can be missing or use `Any`
- complex types (`Union`, generics) are hard to reason about with a small checker

So this should be presented as:

- **best-effort checks** for developer experience
- not a guarantee

## Extracting more than string defaults (future)

Today yep only reflects top-level string assignments.

To support typed defaults, the reflector could be expanded to parse:

```py
retries: int = 3
publish_latest: bool = False
input_path: Path = Path("data.txt")  # (might be too dynamic for AST-only)
```

The safest incremental step is supporting `AnnAssign` for simple constants:

- `x: int = 3`
- `x: bool = True`
- `x: float = 1.5`
- `x: str = "..."`

(Anything involving function calls like `Path("...")` is harder to support without importing/executing code.)

## Java: where type control *does* make sense

For Java (and other static languages), type-aware wiring is much more compelling because:

- step input/output types are explicit
- you can enforce compatibility during wrapper generation
- failures become compile-time errors or deterministic wrap-time validation errors

A Java reflector could extract:

- method parameter types
- return types
- possibly annotations for step metadata (retries, timeouts, etc.)

Then wiring can be:

- name-based (like today)
- type-checked (strict)
- or even type-driven (choose among overloads / adapters), if desired

## How to document this in the product

If/when implemented, it helps to expose it in three places:

- `yep wrap` output: print a short “wiring report” with inferred edges + (optional) type compatibility notes
- wrapper code comments: generated wrapper can include a compact summary of inferred edge contracts
- docs: show one good example + one counterexample warning

---

If you want, the next step is to turn this note into a concrete proposal under `doc/proposals/draft/` with a minimal, testable scope:

- Add AST support for `AnnAssign` constants as vars
- Add optional wrap-time warnings for edge type mismatches based on annotations
- (Optional) add first-step coercion rules behind a flag
