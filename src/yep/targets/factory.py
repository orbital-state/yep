"""Factory for creating targets."""

_registered_targets = {
    'local': 'yep.targets.local:LocalTarget',
}

def get_target_cls(target: str):
    """Map target string to a target class."""
    assert target in _registered_targets, f"Target '{target}' not registered."
    target_module, target_class = _registered_targets[target].rsplit(':', 1)
    module = __import__(target_module, fromlist=[target_class])
    return getattr(module, target_class)
