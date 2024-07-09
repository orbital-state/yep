from yep.targets.factory import _registered_languages, get_target_cls, guess_programming_language


def test_can_guess_programming_language():
    assert guess_programming_language('test.py') == 'python'


def test_can_instantiate_targets():
    lang = 'python'
    targets = _registered_languages[lang]['targets']
    list_of_target_names = list(targets.keys())
    for target_name in list_of_target_names:
        target_class = get_target_cls(lang, target_name)
        assert target_class is not None
        assert hasattr(target_class, 'generate_wrapper')
        assert hasattr(target_class, 'reflect_pipeline')
