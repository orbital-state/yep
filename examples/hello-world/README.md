# hello-world (example)

This example demonstrates the smallest runnable yep pipeline.

## Run

From the repo root:

```bash
python -m pip install -e .
cd examples/hello-world

# Generate the local wrapper under .yep/targets/local/
yep wrap --update

# Run with defaults
yep run --target local

# Override defaults
yep run --target local --vars message:Hi
```

## What yep infers

From `hello.py` yep infers:

- defaults (`vars`): `message = "Hello from yep"`
- steps (`tasks`): `make_message(...)` then `show(...)`

The `local` target generates a wrapper that calls the steps in order and passes outputs forward.
