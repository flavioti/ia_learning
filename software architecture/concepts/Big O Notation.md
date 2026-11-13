---
description: Big O notation, the way to describe how an algorithm's time or memory grows with input size, with the common classes (O(1), O(log n), O(n), O(n log n), O(n²)) and Python examples.
aliases:
  - Big O
  - Time complexity
  - Algorithm complexity
tags:
  - algorithms
  - complexity
---

# Big O Notation

Big O describes **how the cost of an algorithm grows as the input size `n` grows**. The cost is usually time (number of operations) or memory. It does not measure seconds, it measures the **growth rate**.

Big O usually describes the **worst case**, and it **ignores constants**: O(2n) and O(n) are the same class. So it tells you how an algorithm scales, not which one is faster on a small input.

![Growth of the common Big O classes](Big%20O%20Notation%20growth.png)

## Common classes

| Notation | Name | Meaning | Python example |
|---|---|---|---|
| O(1) | Constant | Cost does not depend on `n` | `x in my_set` (average), `my_list[0]` |
| O(log n) | Logarithmic | Each step cuts the problem in half | Binary search on a sorted list (`bisect`) |
| O(n) | Linear | Doubling `n` doubles the cost | `x in my_list`, `sum(my_list)` |
| O(n log n) | Linearithmic | Slightly worse than linear | `sorted(my_list)` |
| O(n²) | Quadratic | Doubling `n` quadruples the cost | Two nested loops over the same list |

## Examples

```python
# O(1): one step, no matter how big the list is
first = items[0]

# O(n): may look at every item
def contains(items, target):
    for item in items:
        if item == target:
            return True
    return False

# O(n²): for each item, loop over all items again
def has_duplicates(items):
    for i in items:
        for j in items:
            ...
```

A common fix is to trade memory for speed. The check `x in my_list` is O(n), but converting to a `set` once makes each lookup O(1) on average, because a set uses a hash table.

## Pitfalls

- **Average vs worst case.** `x in my_set` is O(1) on average, but can degrade to O(n) when many hash collisions happen (rare in practice).
- **Constants still matter for small `n`.** A list can beat a set on a handful of items.
- **Space complexity exists too.** The set above is faster but uses more memory than the list.
- **Nested loops are a hint, not a rule.** Two nested loops over *different* sizes are O(n·m), not O(n²).

## Related

- [[software architecture/language & framework/python/Python Tuple vs Set vs List.md|Python Tuple vs Set vs List]]: uses Big O to compare `in` on list, tuple and set.
