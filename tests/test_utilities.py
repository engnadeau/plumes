import plumes.utilities as pu


def test_set_output(tmp_path):
    pu.set_output(fname="foo", path=tmp_path)


def test_get_user():
    pu.get_user()
    pu.get_user("EngNadeau")
    pu.get_user("SteveMartinToGo")
    pu.get_user("alyankovic")
    pu.get_user("ConanOBrien")
