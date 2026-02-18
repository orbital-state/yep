# yep design

## One-sentence idea
**yep is a pipeline engine that infers a runnable pipeline from ordinary source code**, instead of requiring a separate YAML/DSL pipeline definition.

You write a “declaration” file in a general-purpose language (currently Python is implemented) as a sequence of small routines. yep reflects over that code, deduces a call chain, then generates a target-specific wrapper (e.g. local execution) that runs the chain.

## What exists in this repo today
At a high level, yep is split into:

- **Project management**: a small `.yep/project.toml` config describing *where* a pipeline declaration file is and *which targets* to generate/run.
- **Reflectors**: language-specific analyzers that parse the declaration code and extract:
  - the **tasks** (pipeline steps)
  - the **vars** (simple runtime variables / defaults)
- **Targets**: runtime backends that take a reflected pipeline model and:
  - generate a runnable wrapper for that target (`yep wrap`)
  - execute the wrapper (`yep run`)

The current implementation is intentionally minimal:

- Implemented reflector(s): Python AST reflector.
- Implemented target(s): Python “local” target.

## Core terms

### Pipeline declaration
A source file (e.g. `word_count.py`) that contains:

- top-level step functions
- optional top-level “vars” (today: string constants)

The key design choice is that the declaration is *just code*.

### Reflected pipeline model
An in-memory model (`YepPipeline`) holding:

- `vars`: default values discovered in the declaration file
- `tasks`: the ordered step functions that form the pipeline

### Wrapper
Generated code placed under `.yep/targets/<target>/...` that wires the steps together and exposes a stable `run(vars)` entrypoint for execution.

## How yep deduces a pipeline (current algorithm)

### 1) Discover steps
The Python reflector (`PythonReflector`) parses the declaration file into an AST and walks it.

It collects **top-level function definitions** (functions defined at module scope):

- `def read_file(file_path): ...`
- `def map_words_to_counts(words): ...`
- `def reduce_word_counts(mapped_words): ...`
- `def print_word_counts(word_counts): ...`

These are stored as `tasks` in **source order**.

`main` is explicitly excluded from the task list.

### 2) Discover vars (defaults)
The Python reflector also collects top-level assignments that are string constants, for example:

```python
file_path = 'declaration.txt'
```

This becomes:

```python
vars = {"file_path": "declaration.txt"}
```

These defaults are used by generated wrappers.

### 3) Generate the call chain
The local target (`LocalTarget.generate_wrapper`) generates a wrapper that chains tasks.

The chaining is based on a simple convention:

- The *output* of step $i$ becomes the *input(s)* of step $i+1$.
- The names of the next step’s arguments are used as the variable names that capture the previous step’s output.

That is: if the next step is `map_words_to_counts(words)`, then the wrapper captures the previous output into `words`.

This works well for “linear” pipelines where each step returns exactly what the next step needs.

## Example: word count (Python)
The example in `examples/word-count-py/word_count.py` defines these steps:

1. `read_file(file_path)` → returns `words`
2. `map_words_to_counts(words)` → returns `mapped_words`
3. `reduce_word_counts(mapped_words)` → returns `word_counts`
4. `print_word_counts(word_counts)` → prints results

The generated local wrapper is conceptually:

```python
defaults = {"file_path": "declaration.txt"}
vars = {**defaults, **(vars or {})}

words = read_file(**vars)
mapped_words = map_words_to_counts(words)
word_counts = reduce_word_counts(mapped_words)
return print_word_counts(word_counts)
```

So the *pipeline definition* is inferred from:

- function order
- function signatures (argument names)
- simple variable defaults

## How the CLI maps to the architecture
The CLI is implemented in `src/yep/cli.py`.

### `yep init`
Creates a `.yep/` folder in the project directory (a marker that the directory is a yep project).

### `yep wrap`
- Reads `.yep/project.toml`
- For each configured pipeline, selects the appropriate target backend
- Reflects the declaration file into a `YepPipeline`
- Generates a wrapper into:

```
.yep/targets/<target>/<pipeline_name>_wrapper.py
```

### `yep run`
- Ensures a wrapper exists (you typically run `wrap` first)
- Loads and executes the wrapper module
- Calls `run(vars)` where `vars` comes from CLI `--vars key:value,...`

## The minimal configuration format
A project is configured via `.yep/project.toml`, for example (from the Python word count example):

```toml
[project]
name = "word-count-py"
description = "A simple word count pipeline in Python."

[project.pipelines.word_count_py]
file_path = "word_count.py"
targets = ["local"]
```

Notably, the config does **not** define steps or edges. It only points yep to the declaration file and desired execution targets.

## Design constraints and current limitations
The current implementation is deliberately small; these constraints are important to understand:

- **Linear pipelines only**: the generated wrapper assumes a single straight chain (no branching/join).
- **Source order matters**: tasks are executed in the order they appear in the file.
- **Signature convention**: step wiring is based on argument names of the *next* function.
- **Defaults are limited**: only top-level string assignments are reflected into `vars`.
- **Language/target support is small**: Python reflector + Python local target are registered; Java support is present only as an example at the moment.

## Why this approach (vs YAML)
The design goal is to reduce duplication:

- In many systems, you write code *and* a separate pipeline graph spec.
- With yep, the declaration file is the “single source of truth” for step names, signatures, and ordering.

That makes pipelines:

- easier to prototype (just write functions)
- easier to refactor (normal language tooling)
- less config-heavy (config points to the file; it doesn’t restate the logic)

## Likely future evolution
Based on the current structure (reflector/target factories), the intended growth path looks like:

- Add additional reflectors (e.g. Java AST/bytecode analysis) to extract step graphs.
- Add additional targets (containers, distributed backends, remote execution).
- Improve the pipeline model (`YepPipeline`) to represent non-linear graphs.
- Expand `vars` extraction beyond simple string constants.

---

If you want, I can also add a short “Architecture” section to the main README pointing to this file, but I kept this change strictly to the requested `doc/design.md` + a small correctness fix in wrapper generation.
