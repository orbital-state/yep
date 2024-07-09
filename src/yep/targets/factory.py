"""Factory for creating targets."""

_registered_languages = {
    'python': {
        'extension': 'py',
        'targets': {
            'local': 'yep.targets.python.local:LocalTarget',
        }
    }
}


def guess_programming_language(file_path: str):
    """Guess programming language from file path."""
    _, extension = file_path.rsplit('.', 1)
    for lang, lang_info in _registered_languages.items():
        if extension == lang_info['extension']:
            return lang
    raise ValueError(f"Programming language not registered for extension: {extension}")


def get_target_cls(lang: str, target: str):
    """Map target string to a target class."""
    assert lang in _registered_languages, f"Language '{lang}' not registered."
    targets = _registered_languages[lang]['targets']
    assert target in targets, f"Target '{target}' not registered."
    target_module, target_class = targets[target].rsplit(':', 1)
    module = __import__(target_module, fromlist=[target_class])
    return getattr(module, target_class)
