"""every(iterable, n) yields lists of size at most n from iterable, until the
iterable is exhausted.

Example: taking every N elements from nothing -- nothing is taken.
>>> for t in every([], 11):
...     print(t)

Example: taking every N elements from an unending generator -- can always take
more.
>>> def integers():
...     i = 0
...     while True:
...         yield i
...         i += 1
>>> t = every(integers(), 3)
>>> next(t)
[0, 1, 2]
>>> next(t)
[3, 4, 5]

Example: taking nothing from an infinite generator -- nothing is ever taken.
>>> tp = every(integers(), 0)
>>> next(tp)
Traceback (most recent call last):
    ...
StopIteration
>>> next(tp)
Traceback (most recent call last):
    ...
StopIteration

Example: taking nothing from a finite sequence -- nothing is ever taken.
>>> for item in every([0, 1], 0):
...     print(item)

Example: taking more than what is available -- exhausts everything.
>>> for item in every([0, 1], 10):
...     print(item)
[0, 1]

Example: taking nothing from nothing -- nothing is taken.
>>> tp = every([], 0)
>>> next(tp)
Traceback (most recent call last):
    ...
StopIteration

Example: composite taking -- inner generator takes first.
>>> a = sm.range(11)
>>> t = every(every(a, 2), 3)
>>> for item in t:
...     print(item)
[[0, 1], [2, 3], [4, 5]]
[[6, 7], [8, 9], [10]]
>>> a = sm.range(7)
>>> t = every(every(a, 3), 2)
>>> for item in t:
...     print(item)
[[0, 1, 2], [3, 4, 5]]
[[6]]

Example: taking from heterogeneous sequence -- nothing special.
>>> for item in every((0, 1, [2], [], None, [5, 6], [[[]]], [8]), 3):
...     print(item)
[0, 1, [2]]
[[], None, [5, 6]]
[[[[]]], [8]]
"""


from itertools import chain, islice
import six.moves as sm


def ievery(iterable, n):
    """ievery(iterable, n) generates "sub-iterator" objects.

    Each generated sub-iterator object can be exhausted by at most n
    iterations, and the first sub-iterable yields the first n (or all) elements
    from "iterable", and so on.

    Notice that apart from a look-ahead of size one to determine whether the
    "ievery" generator object should reach the stopped state as early as it
    can, this generator does not exhaust the original iterable.  The
    sub-iterators yielded by "ievery" only define a pattern of iteration to be
    applied to the original iterable.  The actual consumption of the original
    iterable must be done by starting the sub-iterators.

    A consequence is that during the consumption of sub-iterators, if the
    iteration stops early, without exhausting the current sub-iterator, the
    next sub-iterator will resume from the place next to the last stop.

    Example: using a series of sub-iterators to take every 3 elements from an
    integer sequence.
    >>> import six
    >>> for subiter in ievery(range(5), 3):
    ...     for item in subiter:
    ...         six.print_(item, end=" ")
    ...     six.print_()
    0 1 2 
    3 4 

    Example: early break.
    >>> for i, b in enumerate(ievery(range(13), 3)):
    ...     for j, t in enumerate(b):
    ...         six.print_(t, end=" ")
    ...         if i == 1 and j == 0:
    ...            break
    ...     six.print_()
    0 1 2 
    3 
    4 5 6 
    7 8 9 
    10 11 12 
    """
    it = iter(iterable)
    while True:
        raw_batch = islice(it, n)
        try:
            head = next(raw_batch)
        except StopIteration:
            break
        yield chain((head,), raw_batch)


def every(iterable, n):
    """every(ABCDEFG, 2) --> [AB] [CD] [EF] [G]
    >>> a = range(5)
    >>> s = every(a, 2)
    >>> for batch in s:
    ...     print(batch)
    [0, 1]
    [2, 3]
    [4]
    """
    for batch_iter in ievery(iterable, n):
        yield list(batch_iter)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
