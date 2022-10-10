from flex_dispatch import dispatcher


@dispatcher
def greet(*args):
    if len(args) == 1:
        return greet.Inline(lambda name: f'Hello, {name}!')
    if len(args) == 2:
        return 'message'


def test_inline():
    assert 'Hello, Bob!' == greet('Bob')