# Wrapper for local target
from hello import make_message, show


def run(vars):
    defaults = {'message': 'Hello from yep'}
    vars = {**defaults, **(vars or {})}
    __first_arg_names = ['message']
    __missing = [n for n in __first_arg_names if n not in vars]
    if __missing:
        raise KeyError(f"Missing required vars for first step: {__missing}")
    __first_args = {n: vars[n] for n in __first_arg_names}
    text = make_message(**__first_args)
    return show(text)


if __name__ == '__main__':
    print(run({}))
