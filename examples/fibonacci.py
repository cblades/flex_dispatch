"""Fibonacci implementation demonstrating the Inline and Static features of flex_dispatch.

If a dispatcher returns a Static object, the contained value will be returned directly instead of invoking any receiver function.

If a dispatcher returns an Inline object, the contained callable will be called.  This is purely a convenience to avoid implementing a
receiver and decorating it with map().
"""
from flex_dispatch import dispatcher


@dispatcher
def fib(n):
    """Calculates the nth fibonacci number."""
    if n <= 0:
        return fib.Static(0)
    if n in (1, 2):
        return fib.Static(1)
    else:
        return fib.Inline(lambda n: fib(n-1) + fib(n-2))


print(fib(6))