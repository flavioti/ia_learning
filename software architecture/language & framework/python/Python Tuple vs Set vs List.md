---
description: Comparison of Python's built-in collections tuple, set and list (mutability, order, duplicates, hashing and speed) and how to choose between them.
aliases:
  - tuple vs list vs set
  - Python collections comparison
tags:
  - python
  - data-structures
---

# Python Tuple vs Set vs List

All three store a group of items, but they make different promises. Pick the one whose promise matches what you need.

- **list**: ordered, mutable, allows duplicates. The default "sequence of things".
- **tuple**: ordered, **immutable**, allows duplicates. A fixed record.
- **set**: **unordered**, mutable, **unique** items only. Fast membership tests and math on groups.

## Comparison

| Feature                      | `list`       | `tuple`                        | `set`                            |
| ---------------------------- | ------------ | ------------------------------ | -------------------------------- |
| Syntax                       | `[1, 2, 3]`  | `(1, 2, 3)` or `1, 2, 3`       | `{1, 2, 3}` (`set()` for empty)  |
| Ordered / indexable          | Yes (`x[0]`) | Yes (`x[0]`)                   | No (no index, no slicing)        |
| Mutable                      | Yes          | No                             | Yes (but items must be hashable) |
| Duplicates                   | Allowed      | Allowed                        | Removed                          |
| Items must be hashable       | No           | No                             | Yes                              |
| Can be a dict key / set item | No           | Yes, if all items are hashable | No (use `frozenset`)             |
| `x in coll` cost             | O(n)         | O(n)                           | O(1) on average                  |
| Memory (3 ints, CPython)     | 88 bytes     | 72 bytes                       | 216 bytes                        |

Memory values were measured with `sys.getsizeof` on Python 3.14 and vary by version and platform. Treat them as a rough idea.

## Examples

```python
l = [1, 2, 3]
t = (1, 2, 3)
s = {1, 2, 3}

l.append(4)        # [1, 2, 3, 4]
t[0] = 9           # TypeError: 'tuple' object does not support item assignment
{1, 2, 2, 3}       # {1, 2, 3}  -> duplicates removed
```

### Set operations

```python
{1, 2} | {2, 3}    # union        -> {1, 2, 3}
{1, 2} & {2, 3}    # intersection -> {2}
{1, 2} - {2, 3}    # difference   -> {1}
{1, 2} ^ {2, 3}    # symmetric difference -> {1, 3}
```

### Tuple as a dict key

```python
{(1, 2): "ok"}     # works
{[1, 2]: 1}        # TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```

### Remove duplicates keeping order

A `set` loses order. Use `dict.fromkeys` when order matters:

```python
list(dict.fromkeys([3, 1, 3, 2, 1]))   # [3, 1, 2]
```

## When to use each

- **list**: a collection that grows, shrinks or is reordered (rows read from a file, a queue of tasks).
- **tuple**: a fixed group of values with meaning by position, such as `(lat, lon)`, a function returning several values, or a composite dict key.
- **set**: uniqueness, fast "is it in there?" checks, or comparing groups (what is in A but not in B).

## Pitfalls

- **Tuples are shallowly immutable.** The tuple cannot change which objects it holds, but a mutable object inside can still change:

  ```python
  a = (1, [2])
  a[1].append(3)   # a is now (1, [2, 3])
  ```

  This also means a tuple holding a list is not hashable.
- **One-item tuple needs a comma:** `(1,)` is a tuple, `(1)` is just the integer 1.
- **`{}` is an empty dict, not a set.** Use `set()`.
- **Do not rely on set order.** Sets are unordered, so never depend on the iteration order (unlike dicts, which keep insertion order).
- **`in` on a big list is slow.** Convert to a set first when you test membership many times.

## Interview questions

1. Why can a tuple be a dict key but a list cannot?
2. What is the average cost of `x in my_set` versus `x in my_list`?
3. How do you remove duplicates from a list and keep the original order?
4. Is `(1, [2])` really immutable? What happens on `a[1].append(3)`?

## Related

- [[software architecture/concepts/Big O Notation.md|Big O Notation]]: explains the O(1) and O(n) costs in the table above.
- `frozenset`: an immutable set, which can be used as a dict key or inside another set.
- `collections.namedtuple` and `typing.NamedTuple`: tuples with named fields.
- `collections.deque`: a list-like structure with fast appends and pops at both ends.
