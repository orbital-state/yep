# Capturing step outputs into `vars` (Python chain-wiring idea)

This note proposes a small Python-first “live annotations” mechanism for **capturing the result of a step under a stable variable name**, pushing it into a shared `vars` dictionary, so it can be used as input by *later* steps (not only the immediate next step).

This is a design note only — not implemented in this repo today.

## Problem (what hurts today)

The current `local` wrapper model is intentionally simple:

- Only the **first** step pulls from `vars` (defaults + CLI overrides).
- Every later step gets its arguments solely from the previous step’s outputs.

This makes linear pipelines easy, but it makes some common patterns awkward:

- A step computes a value that should be reused 2–3 steps later (e.g., a computed path, an auth token, a build artifact ID).
- You want to “name” a step output to make wiring more explicit.
- You want a later step to take a value from `vars` without having to thread it through every intermediate step.

## Desired behavior

Allow a step to *export* one or more outputs into `vars` under explicit names, e.g.:

- export the output of `build()` as `image_ref`
- export multiple outputs of `docker_build()` as `image_ref`, `image_repo`, etc.

Then later steps can declare parameters matching those names and have them resolved from `vars`.

## Key design choice: how later steps resolve inputs

Once `vars` can change over time, wiring becomes ambiguous unless we define a strict precedence rule.

A simple and predictable rule:

1. For each step call, build its kwargs by name.
2. For each parameter name `p` in the step signature:
   - If `p` exists in `vars`, use `vars[p]`.
   - Else, if `p` exists as a local variable produced by the immediately previous wiring, use that.
   - Else, error: missing input.

This shifts the model from “positional pass-through” toward “named dependency injection from a growing dict”.

### Why prefer `vars` first?

Because `vars` becomes the explicit shared state (defaults + CLI + exported outputs). If a value is exported under a name, it should be the authoritative value for that name.

### Collision policy

Exports can accidentally overwrite user-provided inputs (CLI vars). You need one of:

- **Strict**: disallow overwriting an existing `vars[key]` unless explicitly allowed.
- **Permissive**: allow overwriting (simple but can surprise).

Recommendation: strict-by-default.

## “Live annotation” mechanism options (Python)

There are a few ways to let users declare exports.

### Option A: decorator-based exports (recommended)

Provide a tiny Python runtime helper (hypothetical) that attaches metadata to the function object.

Single output:

```py
@yep.export("text")
def make_message(message: str) -> str:
    return message
```

Multiple outputs:

```py
@yep.export("image_ref", "image_repo", "publish_latest", "dry_run")
def docker_build(...) -> tuple[str, str, str, str]:
    ...
    return image_ref, image_repo, publish_latest, dry_run
```

Wrapper behavior (conceptually):

```py
image_ref, image_repo, publish_latest, dry_run = docker_build(...)
vars["image_ref"] = image_ref
vars["image_repo"] = image_repo
vars["publish_latest"] = publish_latest
vars["dry_run"] = dry_run
```

Pros:
- Very explicit at the step definition.
- Natural for Python.
- Doesn’t require changing function signatures.

Cons:
- The reflector must learn to read decorators (AST) or the wrapper must import the module to inspect function attributes.

### Option B: docstring tags (AST-only friendly)

Example:

```py
def docker_build(...):
    """yep: export=image_ref,image_repo"""
    ...
    return image_ref, image_repo
```

Pros:
- The reflector can read docstrings from AST without importing the module.

Cons:
- Less discoverable than decorators.
- Needs a mini syntax.

### Option C (ugly): explicit “ctx/state” object

This is the classic framework approach: add a reserved argument like `ctx`/`state`/`vars` and let steps mutate it.

```py
def docker_build(ctx, image_repo: str, image_tag: str):
  ctx["image_ref"] = f"{image_repo}:{image_tag}"
  return ctx["image_ref"]
```

Why it’s ugly (in a yep context):

- It makes the declaration less “just code”: every step now has to accept a framework parameter.
- It increases boilerplate and cognitive load (especially for simple pipelines).
- It couples step functions to yep’s execution model, which makes reuse/testing outside yep a bit less clean.

Why you might still keep it around:

- It is extremely explicit (no hidden exports).
- It’s flexible for advanced cases where you genuinely want shared mutable state.

In other words: it’s a workable fallback, but it’s not the ergonomic sweet spot for the “linear pipeline from ordinary code” vibe.

## How this interacts with the current chain-wiring

Today’s chain-wiring relies on the next step’s argument names to decide variable names.

With exports, you can keep the “linear” feel while enabling long-distance references:

- Step i returns output(s)
- Wrapper wires to next step as usual
- Wrapper also exports selected values into `vars`
- Later steps can pull by name from `vars`

This gives you a spectrum:

- quick pipelines: rely on immediate pass-through
- more complex pipelines: export named values to avoid threading

## Counterexample (where this can go wrong)

If a step exports `token` into `vars`, but the user also passes `--vars token:...` at runtime, then without a strict collision policy, it’s unclear which value is used.

That’s why the note recommends strict-by-default export semantics (no overwrite unless explicitly allowed).

## Minimal “version 1” scope (if implemented)

- Add an export annotation mechanism (decorator or docstring tag)
- Update wrapper generation to:
  - export annotated outputs into `vars`
  - resolve step inputs by name using the precedence rule
- Emit a “wiring report” during `yep wrap`:
  - inferred step list
  - exports per step
  - which vars each step consumes

---

Related notes:

- Type hints discussion: `doc/type-hinting.md`
- Overall design: `doc/design.md`
