---
title: Lesson 2 practice
type: problem
program: applied-data-analysis
course: Python
status: draft
created: 2026-10-11
updated: 2026-10-11
---
# Lesson 2 practice

[Lesson](lesson-02-loops-and-functions.md) · [Python](python.md)

## Task and attempt status

Practice loop termination, sequence calculations, function calls, and scope.
The owner supplied course examples, not a separate student attempt.
The solutions below are agent-written corrections and answer checks.
Try each task before you read its answer.

## Sequence and loop completion

Task: collect the integers from zero through seven.
The source starts at ten, which does not satisfy this task.

```python
numbers = []
counter = 0
while counter <= 7:
    numbers.append(counter)
    counter += 1
else:
    completed = True
assert numbers == list(range(8))
assert completed is True
```

Check zero iterations and an early exit separately.

```python
events = []
for item in []:
    events.append(item)
else:
    events.append("complete")
assert events == ["complete"]

for item in range(3):
    break
else:
    events.append("unexpected")
assert events == ["complete"]
```

## Sentinel sum

Task: add integers until the first zero. Exclude that zero from the sum.
Negative values are permitted. Immediate zero gives a sum of zero.

```python
def read_total():
    """Read integers until zero and return their sum."""
    total = 0
    while True:
        number = int(input("Integer, or zero to finish: "))
        if number == 0:
            return total
        total += number
```

Check inputs `10, 20, 30, 45, 0`: the answer is `105`.
Check inputs `-3, 8, 0`: the answer is `5`.
Invalid numeric text raises `ValueError`. The example does not retry that input.

## Pastry limit

Task: accept no more than twenty pastries, even when an offered portion exceeds the remaining capacity.
Assumption: stop at twenty accepted pastries. The source wording does not specify another stopping choice.
Counts have units of pastries. Offered portions must be positive integers.

```python
def accept_portions(portions, limit=20):
    """Return accepted pastries without exceeding the limit."""
    if limit < 0:
        raise ValueError("Negative limit")
    accepted = 0
    for portion in portions:
        if accepted == limit:
            break
        if portion <= 0:
            raise ValueError("Portion must be positive")
        accepted += min(portion, limit - accepted)
    return accepted

assert accept_portions([100]) == 20
assert accept_portions([8, 9, 7]) == 20
assert accept_portions([4, 3]) == 7
```

A finite supply can finish below the limit.
The original accumulation loop can exceed twenty and does not reject negative additions.
This example uses supplied portions. It does not claim random generation or actual consumption.

## Progressions and iteration counts

Task: compute the positions after ten jumps from position one, with a step of three.
Include the initial position only when the task asks for all visited positions.

```python
visited = []
for jump in range(11):
    visited.append(1 + 3 * jump)
assert visited == list(range(1, 32, 3))
assert visited[-1] == 31
assert len(visited[1:]) == 10
```

Task: add seven daily counts, starting at two and increasing by one daily.

```python
total = 0
for day in range(7):
    total += 2 + day
assert total == 35
```

| Range | Iterations |
| --- | --- |
| `range(4, 5)` | 1 |
| `range(1, 4, 4)` | 1 |
| `range(1, 10, -1)` | 0 |
| `range(10, 0, -1)` | 10 |

## Discount function

Task: compute a discounted price, with five extra percentage points for VIP customers.
Policy choice: reject a total discount outside zero through one hundred.
The source does not supply this validation policy.
Use one consistent currency unit for input and output.
The float result demonstrates arithmetic, not a currency-rounding policy.

```python
def final_price(price: float, discount: float, is_vip: bool = False) -> float:
    """Return the price after a validated percentage discount."""
    total_discount = discount + (5 if is_vip else 0)
    if price < 0 or not 0 <= discount <= 100:
        raise ValueError("Invalid price or discount")
    if not 0 <= total_discount <= 100:
        raise ValueError("Invalid total discount")
    return price * (100 - total_discount) / 100

assert final_price(100, 5) == 95.0
assert final_price(10, 5, True) == 9.0
assert final_price(discount=10, price=100, is_vip=True) == 85.0
```

The source's unvalidated formula gives `-0.5` for price ten, discount one hundred, and VIP status.
The corrected function rejects this case.
Annotations do not replace input checks. This example assumes finite numeric inputs and a Boolean VIP flag.

## Scope and returned functions

Task: preserve the outer and module values when an inner function uses its own local name.

```python
value = 0

def outer():
    value = 1
    def inner():
        value = 2
        return value
    return inner(), value

assert outer() == (2, 1)
assert value == 0
```

Task: return a nested function that uses its enclosing parameter.

```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

triple = make_multiplier(3)
assert triple(7) == 21
```

## Verification and common errors

The agent executed all Python example blocks in these two notes on 2026-10-11 with Python 3.12.3.
Separate checks cover sentinel input, rejected discounts, range boundaries, and invalid call syntax.
The agent did not execute an infinite loop or reproduce the supplied timings.
These results do not confirm Colab execution or student completion.

Common errors include an incorrect initial counter, an excluded range endpoint, and confusion between `break` and `continue`.
A positional argument after an ordinary keyword argument is invalid syntax.
Repeated use of an exhausted iterator produces no further items.
