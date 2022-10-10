from flex_dispatch import dispatcher


@dispatcher
def greet(*args):
    if len(args) == 0:
        return greet.Static('Hello!')
    if len(args) == 1:
        return 'name'
    if len(args) == 2:
        return 'message'


def test_static():
    assert 'Hello!' == greet()