from stuff.thing import Thing

def test_thing():
    t = Thing()
    assert t.method() == 2
