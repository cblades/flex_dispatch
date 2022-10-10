from functools import partial, update_wrapper
from typing import Callable, Union

class DispatchError(Exception):
    """Error arising while trying to dispatch a call."""
    pass


class dispatcher:
    """Decorator that turns a callable into a dispatcher for flex-dispatcher. 
    
    A dispatcher inspects its arguments and returns a "dispatch value", which can be anything.
    The dispatcher method can then be used to decorate other functions as receivers for a call
    resulting in a given dispatch value.

    Example:
        from flex_dispatch import dispatcher

        @dispatcher
        def greet(*args):
            if len(args) == 0:
                return 'just_name'
            elif len(args) == 2:
                return 'message'
            
        
        @greet.map('just_name')
        def say_hey(name: str):
            print(f'Hello, {name}!')

        @greet.map('message')
        def say_message(name, msg):
            print(f'{msg} {name}')

        greet('Frank')  # will dispatch to say_hey and print "Hello, Frank!"
    """
    def __init__(self, delegate):
        update_wrapper(self, delegate)
        self.delegate = delegate
        self.method_mappings = []
        self.extensions = []

    def __get__(self, obj, objtype=None): 
        """Capture receiving obj when we've decorated a method."""    
        if obj:      
            return partial(self.__call__, obj)
        return self

    def __call__(self, *args, **kwargs):
        for extension in self.extensions:
            dispatch_value = extension(*args, **kwargs)
            if dispatch_value:
                break
        else:
            dispatch_value = self.delegate(*args, **kwargs)
            
        if not dispatch_value:
            raise DispatchError(
             f'Dispatch value could not be determined for function {self.delegate.__name__} for '
             f'arguments {args}, {kwargs}')

        if type(dispatch_value) == dispatcher.Static:
            return dispatch_value.value
        if type(dispatch_value) == dispatcher.Inline:
            return dispatch_value.fn(*args, **kwargs)

        receiver = self._get_receiver_for_dispatch_value(dispatch_value)
        if not receiver:
            raise DispatchError(f'No function mapped to dispatch value {dispatch_value} for '
                                f'function {self.delegate.__name__}')

        return receiver(*args, **kwargs)
    
    def extend(self, fn: Callable):
        self.extensions.append(fn)

    def map(self, dispatch_value, fn = None) -> Union[Callable[[Callable], Callable], None]:
        """Map callable to handle the given dispatch value.
        
        Can be used as a decorator or called directly and passed a callable.
        
        Examples:
            @greet.map('just_name')
            def say_hey(name: str):
                print(f'Hello, {name}!')

        Or:
            greet.map('just_name', say_hey)
        """
        if self._get_receiver_for_dispatch_value(dispatch_value):
            raise DispatchError(
                f'Reciever already mapped for dispatch value {dispatch_value} '
                f'({self._get_receiver_for_dispatch_value((dispatch_value))}).')

        if fn and callable(fn):
            self.method_mappings.append((dispatch_value, fn))
        else:
            def _decorator(fn):
                self.method_mappings.append((dispatch_value, fn))

                def _wrapper(*args, **kwargs):
                    return fn(*args, **kwargs)

            return _decorator

    def _get_receiver_for_dispatch_value(self, dispatch_value):
        return next(
            map(lambda m: m[1], filter(lambda m: m[0] == dispatch_value, self.method_mappings)), 
            None)

    class Static:
        def __init__(self, value: any) -> None:
            self.value = value

    class Inline:
        def __init__(self, fn: Callable) -> None:
            self.fn = fn

__all__ = [
    'DispatchError',
    'dispatcher'
]