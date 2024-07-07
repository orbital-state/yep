from yep.project import YepProject


def test_init_yep_project(tmp_path):
    project = YepProject(tmp_path)
    assert project.name == tmp_path.name
    assert project.yep_folder_path() == tmp_path / '.yep'
    assert project.yep_folder_path().exists() is False
    assert project.initialize() is True
    assert project.yep_folder_path().exists() is True
    # finally, test that we cannot initialize the project again
    assert project.initialize() is False
