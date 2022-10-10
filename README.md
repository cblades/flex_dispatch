flex_dispatch
==============================

A super flexible dynamic dispatch implementation for python, inspired by Clojure's multimethod.

Install with: `pip install flex-dispatch`

To use: `from flex_dispatch import Dispatcher` and annotate any callable with `@Dispatcher`

Example
------------
```
from flex_dispatch import Dispatcher


@Dispatcher
def greet(*args):
    if len(args) == 1:
        return '_just_name'
    elif len(args) == 2:
        return '_name_msg'


@greet.map('_just_name')
def say_hey(name):
    print(f'Hello, {name}!')


@greet.map('_name_msg')
def say_message(name, msg):
    print(f'{msg} {name}')


greet('Chris')
greet('Bob', 'Boo')

greet('b', 'b', 3)
```

Any callable decorated with @Dispatcher becomes a dispatcher function.  It should inspect its arguments and return a "dispatch value"; i.e., a value used
to determine which callable to dispatch the call to.  Callables decorated with `@<dispatcher>.map(<value>)` (like `@greet.map('_just_name')` above) register the decorated function as the dispatch target for the given value.

In other words, when `greet('Chris')` is called, first the `greet` function is called to return a dispatch value, in this case `'_just_name'`.  Since `say_hey` was decorated with `@greet.amp('_just_name')`, it was registered as the target function to call when `greet` returns the dispatch value `'_just_name'`.

