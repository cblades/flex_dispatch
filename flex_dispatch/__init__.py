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
        self.delegate = delegate
        self.method_mappings = []

    def __call__(self, *args, **kwargs):
        dispatch_value = self.delegate(*args, **kwargs)
        if not dispatch_value:
            raise DispatchError(
             f'Dispatch value could not be determined for function {self.delegate.__name__} for '
             f'arguments {args}, {kwargs}')

        for d, fn in self.method_mappings:
            if d == dispatch_value:
                return fn(*args, **kwargs)

        raise DispatchError(f'No function mapped to dispatch value {dispatch_value} for '
                                f'function {self.delegate.__name__}')

    def map(self, dispatch_value, fn = None):
        """Map callable to handle the given dispatch value.
        
        Can be used as a decorator or called directly and passed a callable.
        
        Examples:
            @greet.map('just_name')
            def say_hey(name: str):
                print(f'Hello, {name}!')

        Or:
            greet.map('just_name', say_hey)
        """
        if fn and callable(fn):
            self.method_mappings.append((dispatch_value, fn))
        else:
            def _decorator(fn):
                self.method_mappings.append((dispatch_value, fn))

                def _wrapper(*args, **kwargs):
                    return fn(*args, **kwargs)

            return _decorator


__all__ = [
    'DispatchError',
    'dispatcher'
]