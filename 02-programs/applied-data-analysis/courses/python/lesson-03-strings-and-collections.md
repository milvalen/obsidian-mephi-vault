---
title: "Lesson 3: strings and collections"
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-06
updated: 2026-11-06
---
# Lesson 3: strings and collections

[Python](python.md) · [Lesson 2](lesson-02-loops-and-functions.md)

## Context and evidence

The owner supplied the Lesson 3 notebook on 2026-11-06. Its file name ends in `_empty`.
The author, lecture date, and original notebook URL are unknown.
Notebook metadata reports Python 3.9.7. Metadata does not verify the active runtime.
The notebook has stored outputs. Its answers to the Part I recall questions and to Exercises 1–7 and 9 are present.
The notebook does not identify the author of these answers.
The agent checked examples with local Python 3.9.6 on 2026-11-06.
The vault does not retain the notebook, original text, or images.

Main reference: [built-in types](https://docs.python.org/3/library/stdtypes.html).

## Collection types

| Type | Mutable | Ordered | Unique items | Typical use |
| --- | --- | --- | --- | --- |
| `str` | No | Yes | No | Text |
| `list` | Yes | Yes | No | Items that you add, change, or remove |
| `tuple` | No | Yes | No | A fixed group, for example point coordinates |
| `set` | Yes | No | Yes | Unique values and set operations |
| `dict` | Yes | Insertion order | Unique keys | Fast access to a value by its key |

Since Python 3.7, a dictionary keeps the insertion order of its keys.

## Strings

A string is an immutable sequence of characters.
An assignment such as `s[0] = "A"` causes `TypeError`. Each string method returns a new string.

### Indexes and slices

Index 0 is the first character. Index -1 is the last character.
A slice `s[start:stop:step]` includes `start` and excludes `stop`.

| Slice | Result |
| --- | --- |
| `s[:2]` | The first two characters |
| `s[8:]` | From index 8 to the end |
| `s[::2]` / `s[1::2]` | Characters at even or odd indexes |
| `s[::-1]` | The reversed string |
| `s[:228]` | The full string. A slice bound out of range does not cause an error |

### Methods

| Method | Result | Note |
| --- | --- | --- |
| `len(s)` | Number of characters | `len("\n")` is 1 |
| `s.split(sep)` | List of parts | `split()` with no argument splits on any whitespace and removes empty parts |
| `sep.join(items)` | One string | All items must be strings |
| `s.find(sub, start)` | Index of the first match | `-1` if there is no match |
| `s.replace(old, new)` | String with all matches replaced | Literal text, not a pattern |
| `s.count(sub)` | Number of matches that do not overlap | |
| `s.strip()` | String without leading and trailing whitespace | |
| `sub in s` / `sub not in s` | `True` or `False` | Substring check |

To remove repeated spaces, use `" ".join(s.split())`.

## Lists

A list is a mutable sequence of references to objects. Indexes and slices operate as for strings.
A slice assignment can change the list length: `colors[2:4] = ["x"]` replaces two items with one item.
The list identity does not change.

| Method | Effect | Error case |
| --- | --- | --- |
| `append(x)` | Adds one item at the end. Returns `None` | `append(1, 2, 3)` causes `TypeError` |
| `extend(items)` | Adds each item of an iterable | |
| `insert(i, x)` | Inserts before index `i` | An index past the end adds at the end, without an error |
| `pop(i)` | Removes and returns the item at `i` | An empty list or bad index causes `IndexError` |
| `remove(x)` | Removes the first item equal to `x` | No such item causes `ValueError` |
| `index(x, start)` | Index of the first match | No such item causes `ValueError` |
| `count(x)` | Number of equal items | |

`append([1, 2, 3])` adds one item, the list. `extend([1, 2, 3])` adds three items.

`ls.sort()` sorts the list in place and returns `None`. `sorted(ls)` returns a new list.
Thus `print(ls.sort())` prints `None`.

Functions for lists: `len`, `min`, `max`, `sum`, `sorted`, `all`, and `any`.
`all([])` gives `True`. `any([])` gives `False`.

### List comprehensions

A list comprehension makes a list in one expression.

```python
squares = [x * x for x in range(10)]
odd_squares = [x * x for x in range(10) if x % 2]
cells = [col + str(row) for row in range(1, 9) for col in "abcdefgh"]
```

The `for` clauses go in the same order as nested loops.

### Copies

`b = a` makes a second name for the same list. `a.copy()` and `a[:]` make a shallow copy.
A shallow copy shares nested objects. For nested lists, use `copy.deepcopy`.

## Tuples

A tuple is an immutable sequence. The comma makes a tuple, not the parentheses.
`(3,)` is a tuple with one item. `(3)` is the integer 3.
A tuple can contain a list. You cannot replace that list in the tuple, but you can change the list.

## Sets

A set contains unique hashable items. It has no indexes and no slices.
`{}` makes an empty dictionary, not a set. Use `set()` for an empty set.
`frozenset` is an immutable set. It can be an item of another set or a dictionary key.

| Operation | Operator | Method |
| --- | --- | --- |
| Intersection | `a & b` | `a.intersection(b)` |
| Union | Vertical bar operator | `a.union(b)` |
| Difference | `a - b` | `a.difference(b)` |
| Symmetric difference | `a ^ b` | `a.symmetric_difference(b)` |
| Subset | `a <= b` | `a.issubset(b)` |

These methods return a new set. `add`, `discard`, `remove`, `pop`, `clear`, and the `*_update` methods change the set.
`remove(x)` causes `KeyError` if `x` is not in the set. `discard(x)` does not.
`pop()` removes an arbitrary item, not a "first" item.

## Dictionaries

A dictionary maps unique hashable keys to values. A list cannot be a key. A tuple of immutable items can be a key.

| Operation | Result |
| --- | --- |
| `d[key]` | Value, or `KeyError` if the key is missing |
| `d.get(key, default)` | Value, or `default` if the key is missing |
| `d[key] = value` | Adds or changes a value |
| `del d[key]` | Removes a key, or `KeyError` |
| `key in d` | Checks keys, not values |
| `d.keys()`, `d.values()`, `d.items()` | Views of keys, values, and pairs |

`dict(zip(keys, values))` stops at the shorter input.
`dict2 = dict1` does not copy. `dict1.copy()` is a shallow copy: a list value stays shared.

Sort by keys: `sorted(d)`. Sort keys by values: `sorted(d, key=d.get)`.
Swap keys and values: `{v: k for k, v in d.items()}`. Equal values then lose keys.

## Source corrections

The agent ran each case below with Python 3.9.6.

| Source example | Correction or limit |
| --- | --- |
| A word is long with "not less than 7 letters", but the code uses `len(word) > 7` | Use `>= 7`. With `>`, a 7-letter word prints without the warning |
| `len(s.strip().split(" "))` counts words | Repeated spaces give empty parts. The example gives 6, not 3. Use `len(s.split())` |
| `S.split([",", ";"])` | `TypeError`. `split` accepts one separator string. Use `re.split` for several separators |
| `tmp = copy(example)` | Only `deepcopy` is imported. A fresh run causes `NameError`. A string needs no copy |
| `A in B`, with `frozenset([1, 2, 3])` in `B` | Gives `True` because `B` contains that frozenset as an item. It is not a subset test. Use `A <= B` |
| `set.pop()` removes "the first" item | It removes an arbitrary item |
| Exercise 4: `v * 1.10` | Gives `55.00000000000001`. Use `round(v * 1.1, 2)` |
| Exercise 5: four punctuation characters | Other characters, such as `:` or `;`, stay. Use `string.punctuation` |

## Exercises from the source

| Exercise | Checked answer |
| --- | --- |
| 1. Remove duplicates and sort | `sorted(set(numbers))`. `list(...)` is not necessary |
| 2. Print tuple items by index | `for i, item in enumerate(data)` |
| 3. Students in both, only math, only CS | `&`, `math - cs`, `cs - math` |
| 4. Prices plus 10% | `{k: round(v * 1.1, 2) for k, v in prices.items()}` |
| 5. Unique words in alphabetical order | Remove punctuation, `lower()`, `split()`, then `sorted(set(words))` |
| 6. Merge sales and add equal keys | `total[k] = total.get(k, 0) + v` for each item of the second dictionary |
| 7. Points in the square from (0, 0) to (5, 5) | `0 <= x <= 5 and 0 <= y <= 5`. Boundary points are inside |
| 8. Students on both courses or on one course | `set(c1) & set(c2)` gives Anna and Maria. `set(c1) ^ set(c2)` gives Dmitry, Ivan, Pyotr, and Sergey |
| 9. Word frequency | `collections.Counter(words)` or a `get` loop |

Exercise 8 has no answer in the notebook. The answer above is agent-written and checked.
The Exercise 9 answer in the notebook calls `words.count` once for each unique word. Its time is O(n·k). `Counter` makes one pass.

## Recall questions

1. Which collection types are mutable?
2. Does a slice change the source string or list?
3. Why does `s.split(" ")` give empty parts?
4. What is the difference between `append` and `extend`?
5. Why does `print(ls.sort())` print `None`?
6. How do you make a tuple with one item?
7. How do you make an empty set?
8. Which set method removes an item safely?
9. How do you check that `A` is a subset of `B`?
10. What does `zip` do with inputs of different lengths?
11. Why does `dict.copy()` not protect a nested list?

Open questions: official course title, lecture date, and required runtime.
