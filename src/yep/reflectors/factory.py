"""Factory for creating reflectors."""

_registered_reflectors = {
    'python': {
        'class_name': 'yep.reflectors.python_reflector:PythonReflector',
        'description': 'Python reflector implementation',
        'extension': 'py',
    }
}


def get_reflector_cls(programming_language: str):
    """Map reflector string (programming_language) to a reflector class."""
    assert programming_language in _registered_reflectors, f"Reflector '{programming_language}' not registered."
    reflector_module, reflector_class_name = _registered_reflectors[programming_language]['class_name'].rsplit(':', 1)
    module = __import__(reflector_module, fromlist=[reflector_class_name])
    return getattr(module, reflector_class_name)


def guess_reflection_language(pipeline_path: str):
    """Guess reflector based on pipeline file extension."""
    extension = pipeline_path.split('.')[-1]
    for programming_language, info in _registered_reflectors.items():
        if extension == info['extension']:
            return programming_language
    raise ValueError(f"No reflector (programming language) registered for extension: {extension}")
