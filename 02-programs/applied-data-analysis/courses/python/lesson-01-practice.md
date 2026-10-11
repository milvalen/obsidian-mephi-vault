---
title: Lesson 1 practice
type: problem
program: applied-data-analysis
course: Python
status: draft
created: 2026-10-11
updated: 2026-10-11
---
# Lesson 1 practice

[Lesson](lesson-01-python-basics.md) · [Python](python.md)

## Task and attempt status

Practice integer checks, geometric conditions, and conditional execution.
No student attempt was supplied for the incomplete tasks.
The following answers are agent-written examples, not assessed submissions.
Inputs must satisfy the stated conditions.

## Age threshold

Task: accept an integer age and compare it with a configured threshold.
The threshold below is an example value, not an external policy.

```python
threshold = 18
age = int(input("Age: "))
if age < 0:
    print("Invalid age")
elif age >= threshold:
    print("Welcome")
else:
    print("Access denied")
```

Check the boundary with ages `17`, `18`, and `19`.
Invalid numeric text raises `ValueError` before this block.

## Disk membership

Task: determine whether a point belongs to a disk, including its boundary.
Use the same length unit for both coordinates, center coordinates, and radius.
The radius must be nonnegative.

The squared distance must not exceed the squared radius:

$$ (x-c_x)^2 + (y-c_y)^2 \leq R^2. $$

```python
center_x, center_y = 0.0, 0.0
radius = 5.0
x, y = 14.0, 0.0
inside = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
assert inside is False
```

Reasoning: the point has squared distance `196`. The squared radius is `25`.
The point `(3, 4)` is on the boundary and passes the test.
At radius zero, only the center passes.
A floating-point boundary can require a task-specific rounding tolerance.

## Every thousandth customer

Task: offer a discount when a positive customer number is divisible by `1000`.
Zero is not a customer number.

```python
customer_number = 2000
if customer_number > 0 and customer_number % 1000 == 0:
    print("Discount available")
```

Check `999`, `1000`, `1001`, `2000`, and `0`.

## Parity and sign

Task: classify an integer as even or odd, then identify its sign.
The remainder test also works for negative integers.

```python
number = -4
parity = "even" if number % 2 == 0 else "odd"
if number > 0:
    sign = "positive"
elif number < 0:
    sign = "negative"
else:
    sign = "zero"
print(parity, sign)
```

Zero is even. Zero has neither a positive nor a negative sign.

## Pastry choice

Task: process yes, no, blank, and unexpected text.
The source does not specify a complete decision rule.
This example accepts English answers without case or surrounding-space differences.

```python
answer = input("Would you like a pastry? yes/no: ").strip().lower()
if answer == "yes":
    print("Pastry selected")
elif answer == "no":
    print("No pastry selected")
elif answer == "":
    print("No answer supplied")
else:
    print("Enter yes or no")
```

This example reports an invalid answer. It does not repeat the question.

## Answer checks and common errors

The agent executed the documented example blocks with controlled input on 2026-10-11.
The agent also checked boundary cases with local Python 3.12.3.
These checks do not establish execution in Colab or student completion.

Common errors include a missing colon, inconsistent indentation, an unsquared radius, and confusion between `^` and `**`.
A string input requires conversion before arithmetic.
An incomplete code cell can stop sequential notebook execution.

Try each task before you read its example.
Explain why the boundary cases produce their results.
