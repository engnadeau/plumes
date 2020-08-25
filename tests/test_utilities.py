import plumes.utilities as pu


def test_set_output(tmp_path):
    pu.set_output(fname="foo", path=tmp_path)


def test_get_user():
    api = pu.get_api()
    pu.get_user()
    pu.get_user("EngNadeau")
