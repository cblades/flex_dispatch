import pytest
from flex_dispatch import DispatchError, dispatcher

from functools import partial

class Greeter:
    @dispatcher
    def greet(self, name, msg=None):
        return 'just-name' if not msg else 'with-msg'

    @greet.map('just-name')
    def _just_name(self, name):
        return f'Hello, {name}!'

    @greet.map('with-msg')
    def _with_msg(self, name, msg):
        return f'{msg} {name}'

def test_methods():
    g = Greeter()
    assert 'Hello, Bob!' == g.greet('Bob')

    assert 'Foo Bar' == g.greet('Bar', 'Foo')
