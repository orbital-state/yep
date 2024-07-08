from yep.targets.factory import _registered_targets, get_target


def test_can_instantiate_targets():
    list_of_target_names = list(_registered_targets.keys())
    for target_name in list_of_target_names:
        target_class = get_target(target_name)
        assert target_class is not None
        assert hasattr(target_class, 'generate_wrapper')
        