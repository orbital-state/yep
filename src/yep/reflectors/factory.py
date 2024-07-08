"""Factory for creating reflectors."""

_registered_reflectors = {
    'python': {
        'class_name': 'yep.reflectors.python_reflector:PythonReflector',
        'description': 'Python reflector implementation',
        'extension': 'py',
    }
}


def guess_reflector(pipeline_path: str):
    """Guess reflector based on pipeline file extension."""
    extension = pipeline_path.split('.')[-1]
    for reflector, info in _registered_reflectors.items():
        if extension == info['extension']:
            return reflector
    raise ValueError(f"No reflector registered for extension: {extension}")


def get_reflector(reflector: str):
    """Map reflector string to a reflector class."""
    assert reflector in _registered_reflectors, f"Reflector '{reflector}' not registered."
    reflector_module, reflector_class = _registered_reflectors[reflector]['class_name'].rsplit(':', 1)
    module = __import__(reflector_module, fromlist=[reflector_class])
    return getattr(module, reflector_class)
