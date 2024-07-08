from yep.reflectors.factory import _registered_reflectors, get_reflector_cls, guess_reflection_language


def test_can_guess_reflectors():
    assert guess_reflection_language('pipeline.py') == 'python'

def test_can_instantiate_reflectors():
    list_of_reflector_names = list(_registered_reflectors.keys())
    for reflector_name in list_of_reflector_names:
        reflector_class = get_reflector_cls(reflector_name)
        assert reflector_class is not None
        assert hasattr(reflector_class, 'parse')
        assert hasattr(reflector_class, 'analyze')