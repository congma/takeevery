"""every(iterable, n) yields lists of size at most n from iterable, until the
iterable is exhausted.

Example: taking every N elements from nothing -- nothing is taken.
>>> from six import advance_iterator
>>> import six.moves as sm
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
>>> advance_iterator(t)
[0, 1, 2]
>>> advance_iterator(t)
[3, 4, 5]

Example: taking nothing from an infinite generator -- nothing is ever taken.
>>> tp = every(integers(), 0)
>>> advance_iterator(tp)
Traceback (most recent call last):
    ...
StopIteration
>>> advance_iterator(tp)
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
>>> advance_iterator(tp)
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

from six import advance_iterator
import six.moves as sm


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
    toexit = False
    it = iter(iterable)
    while not toexit:
        batch = []
        for i in sm.range(n):
            try:
                batch.append(advance_iterator(it))
            except StopIteration:
                toexit = True
        if not batch:
            break
        yield batch


if __name__ == "__main__":
    import doctest
    doctest.testmod()
