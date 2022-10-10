class DispatchException(Exception):
    pass


class dispatcher:
    def __init__(self, delegate):
        self.delegate = delegate
        self.method_mappings = []

    def __call__(self, *args, **kwargs):
        dispatch_value = self.delegate(*args, **kwargs)
        if not dispatch_value:
            raise DispatchException(
             f'Dispatch value could not be determined for function {self.delegate.__name__} for '
             f'arguments {args}, {kwargs}')

        for d, fn in self.method_mappings:
            if d == dispatch_value:
                return fn(*args, **kwargs)

        raise DispatchException(f'No function mapped to dispatch value {dispatch_value} for '
                                f'function {self.delegate.__name__}')

    def map(self, dispatch_value: any):
        def _decorator(fn):
            self.method_mappings.append((dispatch_value, fn))

            def _wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

        return _decorator


__all__ = [
    'DispatchException',
    'Dispatcher'
]