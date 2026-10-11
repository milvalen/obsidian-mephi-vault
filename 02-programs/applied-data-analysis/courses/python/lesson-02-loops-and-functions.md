---
title: Lesson 2: loops and functions
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-10-11
updated: 2026-10-11
---
# Lesson 2: loops and functions

[Python](python.md) · [Lesson 1](lesson-01-python-basics.md) · [Practice](lesson-02-practice.md)

## Context and evidence

The owner supplied Lesson 2 on 2026-10-11.
The author, lecture date, and original notebook URL are unknown.
Notebook metadata reports Python 3.9.7. Metadata does not verify the active runtime.
The agent checked examples with local Python 3.12.3.
Official references were consulted on 2026-10-11.
The vault does not retain the notebook, original text, or images.

## Conditional practice

The lesson repeats parity, age thresholds, disk membership, customer discounts, and sign checks.
See [Lesson 1 practice](lesson-01-practice.md) for these conditions and their boundaries.
A disk test includes its boundary and requires a nonnegative radius.
The distance and radius must use the same length unit.

Normalize an answer before a membership check: `answer.strip().lower()`.
Then compare it with the accepted answers using `in`.
An unexpected answer needs a separate response.
Whitespace removal and case conversion do not validate numeric input.
See [string methods and membership](https://docs.python.org/3.13/library/stdtypes.html).

The supplied `%%timeit` results differ even for identical code.
They do not establish a general performance ranking.
`%%timeit` measures repeated cell execution in IPython. It is not ordinary Python syntax.
See [IPython timing commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit).

## While loops

`while` checks its condition before each iteration.
An initially false condition causes zero iterations.
Update the state so the loop can terminate.
A nonempty list such as `[0]` has a true truth value.
A constant true condition without an exit produces an infinite loop.

`break` exits the nearest loop. `continue` skips its remaining iteration statements.
For `while`, `continue` returns control to the condition check.
Put a necessary counter update before `continue`.
See [while statements](https://docs.python.org/3.13/reference/compound_stmts.html#the-while-statement).

```python
counter = 0
odds = []
while counter < 10:
    counter += 1
    if counter % 2 == 0:
        continue
    odds.append(counter)
assert odds == [1, 3, 5, 7, 9]
```

A sentinel marks the end of input. The lesson uses integer zero.
Initialize the accumulator before input. Add each non-sentinel value, then obtain the next input.
Negative integers also count unless the task prohibits them.
Invalid numeric text raises `ValueError`.
See [sentinel practice](lesson-02-practice.md#sentinel-sum).

`+=`, `*=`, `/=`, and `%=` combine an operation with assignment.
For simple numeric variables, `value += 1` adds one and assigns the result.
Augmented assignment can change a mutable object in place.
Do not assume complete equivalence with ordinary assignment for every object.
See [augmented assignment](https://docs.python.org/3.13/reference/simple_stmts.html#augmented-assignment-statements).

## For loops and range

`for` consumes items from an iterable. The total iteration count need not be known beforehand.
A string supplies characters. A dictionary supplies keys.
`range` is an immutable integer sequence, not a list or an iterator.
It stores the progression parameters instead of every element.

`range(stop)` starts at zero with step one.
`range(start, stop, step)` includes the start and excludes the stop.
The step must be nonzero. Its direction determines whether the range is empty.
See [range](https://docs.python.org/3.13/library/stdtypes.html#ranges) and [for statements](https://docs.python.org/3.13/reference/compound_stmts.html#the-for-statement).

```python
assert list(range(5, 41, 5)) == [5, 10, 15, 20, 25, 30, 35, 40]
assert list(range(10, 1, -2)) == [10, 8, 6, 4, 2]
assert list(range(1, 10, -1)) == []
```

`zip()` produces an iterator of paired items.
By default, it stops at the shortest input. Equal five-item inputs produce five pairs.
An exhausted zip iterator does not restart.
Use `strict=True` when unequal lengths must raise an error. This option requires Python 3.10 or later.
See [zip](https://docs.python.org/3.13/library/functions.html#zip).

```python
pairs = zip([2, 6, 9], ["two", "six", "nine"])
assert list(pairs) == [(2, "two"), (6, "six"), (9, "nine")]
assert list(pairs) == []
```

Both loop types support `break`, `continue`, and `else`.
Loop `else` runs after normal completion, including zero iterations.
A `break`, function return, or escaping exception prevents that completion.
`pass` performs no action when syntax requires a statement.
The name `_` conventionally marks an unused loop value. It remains an ordinary assignment target here.
See [loop control](https://docs.python.org/3.13/tutorial/controlflow.html#break-and-continue-statements).

## Functions and calls

`def` creates a function object when execution reaches the definition.
The body executes when the function is called.
A parameter names an input in a definition. An argument supplies a value in a call.
`return` ends the call and supplies its result.
A missing result or bare `return` supplies `None`.
A function can return another function.
See [function definitions](https://docs.python.org/3.13/reference/compound_stmts.html#function-definitions).

Ordinary positional arguments precede keyword arguments.
Keyword arguments use parameter names and can change their order.
Duplicate assignment to a parameter raises `TypeError`.
For positional parameters, required parameters precede parameters with defaults.
Required keyword-only parameters can follow defaulted parameters.
See [calls](https://docs.python.org/3.13/reference/expressions.html#calls).

Defaults are evaluated at function definition, not at each call.
A mutable default can retain changes between calls.
Use `None` and create a new collection inside the body when each call needs a fresh collection.
Type annotations describe intended types. They do not enforce them during ordinary execution.
See [function parameters](https://docs.python.org/3.13/tutorial/controlflow.html#more-on-defining-functions).

## Argument unpacking

In a call, `*items` supplies positional arguments from an iterable.
`**options` supplies keyword arguments from a mapping with string keys.
`*dictionary` supplies its keys, not its values.
A list without `*` remains one argument.
A standalone `*items` is not a valid expression statement.
See [call unpacking](https://docs.python.org/3.13/reference/expressions.html#calls).

```python
def describe(a, b, c, ending="!"):
    return a, b, c, ending

assert describe(*[1, 2, 3]) == (1, 2, 3, "!")
assert describe(1, 2, **{"c": 8, "ending": "done"}) == (1, 2, 8, "done")
```

In a definition, `*args` collects extra positional arguments into a tuple.
`**kwargs` collects extra keyword arguments into a dictionary.
A comma-separated return such as `return low, high` returns one tuple object.
Unpacking assigns its elements to separate names.
See [arbitrary argument lists](https://docs.python.org/3.13/tutorial/controlflow.html#arbitrary-argument-lists).

```python
def collect(*args, **kwargs):
    return args, kwargs

values, options = collect(4, 7, enabled=True)
assert values == (4, 7)
assert options == {"enabled": True}
```

## Documentation and lambda

A docstring is the first string statement inside a function definition.
Document the result, parameter names, restrictions, and important effects.
PEP 257 specifies docstring conventions. Parameter markup is a separate documentation choice.
The supplied discount docstring names a nonexistent `discount_percent` parameter.
See [PEP 257](https://peps.python.org/pep-0257/).

A lambda body contains one expression, not an arbitrary statement.
The function returns that expression's value.
Use `def` when the function needs several statements or a clearer name.
See [lambda expressions](https://docs.python.org/3.13/tutorial/controlflow.html#lambda-expressions).

```python
assert (lambda number: number ** 3 + 1)(10) == 1001
```

## Scope and name resolution

For ordinary function names, LEGB describes local, enclosing function, global, and built-in lookup.
An `if`, `while`, or `for` block does not create a separate local scope.
Global names belong to a module, not automatically to every program module.
An assignment inside a function normally makes that name local throughout the function body.
Reading it before assignment can raise `UnboundLocalError`.

`global` selects the module binding. `nonlocal` selects an existing enclosing function binding.
A nested function is not directly available by its local name outside its enclosing function.
Returning it can make the function object available to the caller.
See [execution model](https://docs.python.org/3.13/reference/executionmodel.html).

A function call needs an available function binding when the call executes.
A function body can reference another function defined later, if that definition executes before the call.
Recursion means that a function calls itself. It needs a terminating case.
See [name resolution](https://docs.python.org/3.13/reference/executionmodel.html#resolution-of-names).

`__name__` identifies the module context. Direct script execution commonly sets it to `"__main__"`.
An imported module normally uses its module name.
See [top-level environment](https://docs.python.org/3.13/library/__main__.html).

## Source corrections

| Source example | Correction or limit |
| --- | --- |
| Start at `10`, then test `<= 7` | Zero iterations, not the requested sequence from zero |
| Start at `10` inside `while True` | Prints ten once, then breaks |
| Five-item inputs to `zip` with four output lines | The code produces five pairs in a fresh execution |
| Pastry total can exceed twenty | This contradicts the stated maximum of twenty |
| VIP addition described as five percent | The formula adds five percentage points to the discount |
| Discount of 100 with VIP bonus | The source formula produces a negative price |
| Local scope attributed to every block | Ordinary conditional and loop blocks do not create scopes |

See [practice](lesson-02-practice.md) for corrected examples and boundary checks.
Stored timings and outputs remain source observations, not new agent measurements.

## Recall questions

1. When can a `while` body execute zero times?
2. Which state update can `continue` accidentally skip?
3. When does loop `else` execute?
4. Why is a range different from an iterator?
5. What happens when `zip` inputs have different lengths?
6. How do parameters differ from arguments?
7. When does Python evaluate a default value?
8. How do `*` and `**` differ in calls and definitions?
9. Does an `if` block create a local scope?
10. Can a returned nested function still be called?

Open questions: official course title, lecture date, required runtime, and the intended pastry stopping rule.
