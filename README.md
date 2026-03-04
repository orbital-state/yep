# yep

Yet another Engine for Pipelines

## Documentation

- [Hello World tutorial](doc/hello-world.md)
- [Design overview](doc/design.md)
- [Targets (direction + intent)](doc/targets.md)

## Installation

with pip:

    pip install yeplib

with poetry:

    poetry add git+https://orbital-state/yep.git

## Publish

    poetry publish --build


## License

Licensed under Apache License Version 2.0. See LICENSE for details.


## Developer

### Running yep

As developer you can run yep locally with poetry:

    poetry run yep --help

But you also have an option to fallback to `pip install --editable .` to simplify local 
development process.
