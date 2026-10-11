---
title: Lesson 1: Python basics
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-10-11
updated: 2026-10-11
---
# Lesson 1: Python basics

[Python](python.md) · [Practice](lesson-01-practice.md) · [Sources](../../../../05-sources/sources.md)

## Context and evidence

The owner supplied a Lesson 1 notebook on 2026-10-11.
The author, lecture date, and original notebook URL are unknown.
This note summarizes the material and separates corrections from source claims.
The vault does not retain the notebook or embedded images.

Stored outputs do not establish execution order.
Several outputs conflict with preceding assignments.
Agent checks use local Python 3.12.3, not the supplied Colab environment.
Official references were consulted on 2026-10-11.

## Notebook workflow

Colab provides hosted Jupyter notebooks. A notebook contains text cells and code cells.
Create your own copy before changes. Execute dependent cells in order.
Restart the kernel before a complete execution check.
A kernel retains names between cell executions.
Stored output can remain after code changes.
See [Colab FAQ](https://research.google.com/colaboratory/faq.html).

`print()` writes text. IPython can display the final expression of a code cell.
`display()` explicitly requests display output.
The IPython name `_` usually holds the last cached expression result.
A cell that only prints does not necessarily replace that result.
An assignment to `_` changes its behavior.
See [IPython output caching](https://ipython.readthedocs.io/en/stable/interactive/reference.html#output-caching-system).

```python
import sys
print(sys.version)
print("Ready")
```

## Versions and scope

The notebook reports Python 3.13.16. The agent did not verify its runtime.
Its claim that 3.12 and 3.13 are the newest versions is date-dependent.
Do not use its Python 3.9 minimum as current library guidance.
Check the required environment and library support before installation.
See [Python version status](https://devguide.python.org/versions/).

The notebook contains a GIL heading without an explanation.
Supplement: standard CPython uses a global interpreter lock for Python execution.
Python 3.13 also provides an optional experimental build without that lock.
See [free threading](https://docs.python.org/3.13/howto/free-threading-python.html).

## Objects, names, and types

A name refers to an object. An object has a type, value, and identity.
An assignment binds a name. It does not always create a new object.
Two names can refer to the same object.
A later assignment can refer to an object of another type.

`del` removes a name binding. Other references can keep the object reachable.
Garbage collection concerns unreachable objects, including references inside collections.
Do not assume immediate memory release.
The result of `gc.collect()` depends on the runtime state.
See [Python data model](https://docs.python.org/3.13/reference/datamodel.html#objects-values-and-types).

```python
first = [7]
second = first
first.append(8)
assert second == [7, 8]
first = "new value"
assert second == [7, 8]
```

## Types and literals

| Type | Meaning | Example |
| --- | --- | --- |
| `int` | Integer | `1_000` |
| `float` | Floating-point number | `2.5` |
| `complex` | Complex number | `3 + 4j` |
| `bool` | Boolean value | `True` |
| `str` | Unicode string | `"study"` |

Integers can grow within memory limits. Floating-point values can have rounding errors.
Binary, octal, and hexadecimal integer prefixes are `0b`, `0o`, and `0x`.
Scientific notation uses `e`: `65e-5` means $65 \times 10^{-5}$.
Its value is `0.00065`. The supplied exponent comment is incorrect.
See [numeric literals](https://docs.python.org/3.13/reference/lexical_analysis.html#numeric-literals).

Single and double quotes both define strings. Triple quotes permit multiple lines.
`\n` represents a newline. `\t` represents a tab. `\\` represents a backslash.
A raw string preserves backslashes but cannot end with an odd number of backslashes.
String `+` joins text. String `*` repeats text.
See [Python introduction](https://docs.python.org/3.13/tutorial/introduction.html#text).

An f-string inserts expression values inside braces.
Python 3.12 permits reuse of outer quotes inside those expressions.
Different quote styles also support earlier Python versions.
See [f-strings](https://docs.python.org/3.13/reference/lexical_analysis.html#f-strings).

```python
record = {"score": 9}
print(f"Score: {record['score']}")
```

## Collections

| Type | Main property | Example |
| --- | --- | --- |
| `list` | Ordered, mutable collection | `[3, "x"]` |
| `tuple` | Ordered collection with fixed item references | `(3, "x")` |
| `dict` | Mapping with unique, hashable keys | `{"score": 9}` |
| `set` | Unordered collection of distinct, hashable elements | `{3, 9}` |

A tuple can contain a mutable object.
An empty `{}` is a dictionary. Use `set()` for an empty set.
Dictionary access uses `record["score"]`, not `record.score`.
List `+` creates a joined list. List `*` repeats item references.
`append()` changes the list and returns `None`.
See [data structures](https://docs.python.org/3.13/tutorial/datastructures.html).

## Input, conversion, and names

`input()` returns a string. Convert numeric input with `int()` or `float()`.
`type()` identifies an object's type. `str()` creates a string representation.
`int("invalid")` raises `ValueError`. Adding an integer to a string raises `TypeError`.
See [built-in functions](https://docs.python.org/3.13/library/functions.html).

```python
age_text = "21"
age = int(age_text)
print(f"Age after ten years: {age + 10}")
```

Names cannot start with a digit or equal a reserved keyword.
Python permits Unicode identifiers, not only Latin letters.
Use `snake_case` for variables and functions. Use `CapWords` for classes.
The supplied class example is not lower camel case.
See [identifiers](https://docs.python.org/3.13/reference/lexical_analysis.html#identifiers) and [PEP 8](https://peps.python.org/pep-0008/#naming-conventions).

Avoid names such as `str` that hide built-in objects.
After `str = "text"`, `str(123)` raises `TypeError`.
After removal of that binding, the built-in `str` is available again.
An undefined name raises `NameError`.

## Arithmetic and comparison

| Operator | Purpose | Checked result |
| --- | --- | --- |
| `/` | Division | `9 / 3 == 3.0` |
| `//` | Floor division | `-7 // 3 == -3` |
| `%` | Remainder | `-7 % 3 == 2` |
| `**` | Power | `3 ** 2 == 9` |
| `^` | Bitwise exclusive OR | `3 ^ 2 == 1` |

`+`, `-`, and `*` provide addition, subtraction, and multiplication.
For integer operands, `/` returns a float.
Floor division rounds downward. A nonzero remainder has the divisor's sign.
`math.sqrt()` computes a square root.
See [Python arithmetic](https://docs.python.org/3.13/tutorial/introduction.html#numbers).

Comparison operators are `<`, `>`, `<=`, `>=`, `==`, and `!=`.
String ordering compares Unicode code points in sequence.
Complex numbers do not support order comparisons.
A comparison chain evaluates its middle expression once and can stop early.
Use `is None` for an identity check. Use `==` for value equality.
See [comparisons](https://docs.python.org/3.13/reference/expressions.html#comparisons).

## Boolean operations

Zero, `None`, and empty built-in collections have false truth values.
Nonempty `[False]` and `"0"` have true truth values.
Custom objects can define their own truth behavior.
`not` returns a Boolean value.
`and` returns the first false operand, or the final operand.
`or` returns the first true operand, or the final operand.
See [truth values](https://docs.python.org/3.13/library/stdtypes.html#truth-value-testing).

Both `and` and `or` stop when an earlier operand determines the result.
Their results need not have type `bool`.
Priority decreases from `not` to `and` to `or`.
Use parentheses when the intended grouping is unclear.
See [Boolean operations](https://docs.python.org/3.13/reference/expressions.html#boolean-operations).

```python
assert (0 and missing_name) == 0
assert ("ready" or missing_name) == "ready"
assert (4 and 12) == 12
assert (6 or 0 and not "x") == 6
```

`&`, `|`, `^`, and `~` operate on integer bits.
They do not provide Boolean short-circuit evaluation.
Examples: `6 & 5 == 4`, `6 | 5 == 7`, and `~5 == -6`.
See [bitwise operations](https://docs.python.org/3.13/library/stdtypes.html#bitwise-operations-on-integer-types).

A default expression such as `text or "missing"` replaces any value with a false truth value.
Whitespace alone remains a nonempty string.
The notebook's guarded average returns `False` when the count is zero.
A conditional expression can return `None` instead and preserve a distinct missing-value marker.

```python
total = 30.0
count = 0
average = total / count if count > 0 else None
assert average is None
```

## Conditional execution

An `if` statement selects a block from a condition's truth value.
Each condition line ends with a colon. Indentation defines its block.
Use four spaces for each indentation level.
`elif` checks another condition when earlier conditions are false.
`else` handles the remaining case and is optional.
See [control flow](https://docs.python.org/3.13/tutorial/controlflow.html#if-statements) and [PEP 8 indentation](https://peps.python.org/pep-0008/#indentation).

A conditional expression selects one value: `a if condition else b`.
Only the selected expression executes.
It does not replace every statement block.
See [conditional expressions](https://docs.python.org/3.13/reference/expressions.html#conditional-expressions).

## Corrections and limits

- Use $R^2$ in the disk test, not $R$.
- Use `**` for powers. Use `^` for bitwise exclusive OR.
- Convert bit diagrams to text or comments before execution.
- Replace the incomplete `????` expression before execution.
- Correct the missing colon after `else` in the explanatory example.
- Use a small exponent for integer demonstrations. The supplied enormous power requires substantial memory.
- Treat stored outputs as source examples, not fresh execution evidence.

## Recall questions

1. How does reassignment differ from a change to a shared list?
2. Why does `input()` require numeric conversion?
3. What does `-7 // 3` return?
4. Why can `and` return an integer?
5. Why does `[False]` have a true truth value?
6. How does `is` differ from `==`?
7. Which value belongs on the right side of the disk inequality?
8. What separates a condition line from its block?

Open questions: official course title, lecture date, notebook URL, and required runtime versions.
