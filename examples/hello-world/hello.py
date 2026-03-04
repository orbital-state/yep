"""Hello World pipeline for yep.

This file is the pipeline declaration.

Current yep rules (Python + local target):
- Top-level public functions are steps, in source order.
- Top-level string assignments become default vars.
"""

# Reflected default (strings only)
message = "Hello from yep"


def make_message(message: str) -> str:
    return message


def show(text: str) -> str:
    print(text)
    return text
