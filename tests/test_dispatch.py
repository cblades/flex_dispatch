import pytest

from flex_dispatch import dispatcher, DispatchError


@dispatcher
def greet(*args):
    if len(args) == 1:
        return 'name'
    if len(args) == 2:
        return 'message'

@greet.map('name')
def say_hey(name):
    return f'Hello, {name}'


def test_happy_path():
    assert 'Hello, Chris' == greet('Chris')


def test_dispatch_errors():
    with pytest.raises(DispatchError): 
        greet('foo', 'bar')

    with pytest.raises(DispatchError):
        greet('foo', 'bar', 'bash')

    with pytest.raises(DispatchError):
        greet.map('name', lambda s: s)

def test_map():
    greet.map('message', lambda n, m: f'{m} {n}')
    assert 'Foo Bar' == greet('Bar', 'Foo')


