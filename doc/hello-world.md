# Hello World (yep)

This short tutorial builds intuition for **yep** by creating the smallest possible pipeline.

The key idea: **your pipeline is just normal Python code**. yep *reflects* over that file to infer:

- **steps**: top-level public functions, in source order
- **vars (defaults)**: top-level string assignments

Then a **target** (like `local`) generates a wrapper that chains the steps.

## Prereqs

- Python 3.9+
- yep installed (editable install for local dev is fine)

From the repo root:

```bash
python -m pip install -e .
```

## 1) Create a new mini project

Make a fresh folder anywhere (this example uses `/tmp`).

```bash
mkdir -p /tmp/yep-hello
cd /tmp/yep-hello
```

Initialize the `.yep/` folder:

```bash
yep init
```

Create `.yep/project.toml`:

```toml
[project]
name = "yep-hello"
description = "Hello world pipeline"

[project.pipelines.hello]
file_path = "hello.py"
targets = ["local"]
```

## 2) Write the pipeline declaration (hello.py)

Create `hello.py`:

```python
"""Minimal yep pipeline.

Rules in today’s yep implementation:
- Top-level public functions are steps (in source order).
- Top-level string assignments become default vars.
"""

# Reflected default (strings only)
message = "Hello from yep"


def make_message(message: str) -> str:
    return message


def show(text: str) -> str:
    print(text)
    return text
```

What yep will infer:

- `vars = {"message": "Hello from yep"}`
- `tasks = [make_message(message), show(text)]`

## How yep wires steps together (the implicit rule)

Today’s `local` target uses a simple convention to build a linear call chain:

- Steps run in the order they appear in the file.
- The **first** step is called with values pulled from `vars` (defaults + CLI overrides).
- For every step after that, yep wires outputs to inputs by looking at the **next step’s signature**.

More concretely: for a step at position *i*, yep looks at the *next* step at position *i+1*.

- Let the next step’s parameter names be `[p1, p2, ...]`.
- The wrapper assigns the current step’s return value(s) into variables named `p1, p2, ...`.
- Then the next step is called with those variables.

That’s why this works:

```python
def make_message(message: str) -> str:
  return message


def show(text: str) -> str:
  print(text)
  return text
```

Because `show` has one parameter named `text`, yep generates a wrapper that (conceptually) does:

```python
defaults = {"message": "Hello from yep"}
vars = {**defaults, **(vars or {})}

# next step is show(text)  -> capture make_message output into variable named `text`
text = make_message(message=vars["message"])
return show(text)
```

If the next step had two parameters like `def show(prefix, text): ...`, then the previous step would need to return two values, and the wrapper would do `prefix, text = previous_step(...)`.

## 3) Generate the local wrapper

```bash
yep wrap --update
```

This writes a generated wrapper under:

- `.yep/targets/local/hello_wrapper.py`

Conceptually, that wrapper does:

```python
vars = {**defaults, **(vars or {})}
text = make_message(message=vars["message"])
return show(text)
```

## 4) Run it

Run with defaults:

```bash
yep run --target local
```

Override defaults at runtime:

```bash
yep run --target local --vars message:Hi
```

## Mental model (important constraints)

- **Linear chain only (today):** steps run in source order.
- **Data flows via return values:** the output of step *i* becomes the input(s) of step *i+1*.
  - If the next step declares N parameters, the current step should return N values (a single value for N=1).
- **Defaults are limited (today):** only top-level **string** assignments are reflected into `vars`.

For the bigger design rationale, see `doc/design.md`.
