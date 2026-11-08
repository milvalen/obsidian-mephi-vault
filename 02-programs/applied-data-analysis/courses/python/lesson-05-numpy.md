---
title: "Lesson 5: NumPy"
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-08
updated: 2026-11-08
---
# Lesson 5: NumPy

[Python](python.md) · [Lesson 4](lesson-04-object-oriented-programming.md)

## Context and evidence

The owner supplied the Lesson 5 notebook on 2026-11-08.
The author, lecture date, and original notebook URL are unknown.
Notebook metadata reports Python 3.9.7. Its stored outputs have the `np.int64(...)` display form, which comes from NumPy 2. Metadata does not verify the active runtime.
The agent checked the additions below with NumPy 2.0.2 on local Python 3.9.6 on 2026-11-08.
The vault does not retain the notebook, original text, or images.

Main reference: [NumPy documentation](https://numpy.org/doc/stable/).

## Why NumPy

NumPy keeps numbers in a compact form and does calculations in optimized low-level code.
Thus array operations are usually faster than Python loops on lists.

The stored results in the source are 80 times for vector addition and 33 times for a sum.
These are source observations on one machine, not a general ratio. The agent did not measure them again.

## Arrays

The main object is `np.ndarray`. It can be a vector, a matrix, or a tensor.
All elements usually have one type. NumPy changes mixed input to a common type:

| Input | `dtype` |
| --- | --- |
| `[1, 2, 3]` | `int64` |
| `[1, 2, 3, 4.0]` | `float64` |
| `[1, 2, 3, 4.0, "5"]` | `<U32`, a string type |

Rows of different lengths cause `ValueError`. With `dtype=object`, the result is a one-dimensional array of lists.

| Attribute | Meaning | `np.zeros((3, 2))` |
| --- | --- | --- |
| `ndim` | Number of axes | `2` |
| `shape` | Number of elements on each axis | `(3, 2)` |
| `size` | Total number of elements | `6` |
| `dtype` | Type of the elements | `float64` |

`ndim` is not the dimension of a vector space in linear algebra.

### Make arrays

| Function | Result | Note |
| --- | --- | --- |
| `np.zeros(shape)`, `np.ones(shape)` | Zeros or ones | The type is `float64` |
| `np.full(shape, value)` | One value in all elements | |
| `np.eye(n)` | Identity matrix | `np.eye(2, 3)` gives a matrix that is not square |
| `np.random.random(shape)` | Random values | From 0, up to but not including 1 |
| `np.random.randint(low, high, size=shape)` | Random integers | `high` is excluded |
| `np.arange(start, stop, step)` | Values with a step | `step` can be a fraction, unlike `range` |
| `np.linspace(start, stop, num=n)` | `n` values | `stop` is included |

Agent check: with a fractional step, the length of `np.arange` can be unexpected.
`np.arange(1, 1.3, 0.1)` has 4 values. Use `linspace` when the number of values is important.

`np.random.seed(n)` makes random results that you can reproduce.

## Vector operations

For arrays, `+`, `-`, `*`, `/`, and `**` operate element by element.
For lists, `[6, 2] + [6, 2]` joins the lists and `[6, 2] * 5` repeats the list.

| Group | Functions |
| --- | --- |
| Rounding | `np.round`, `np.floor`, `np.ceil`, `np.abs` |
| Trigonometry | `np.sin`, `np.cos`, `np.tan`, `np.pi` |
| Exponents and logarithms | `np.exp`, `np.log`, `np.log10`, `np.log2` |
| Aggregation | `np.sum`, `np.prod`, `np.mean`, `np.median`, `np.var`, `np.std`, `np.min`, `np.max` |
| Other | `np.sqrt`, `np.power`, `np.unique` |

Floating-point results can be not exact. `np.cos(np.pi / 2)` gives `6.1e-17`, not 0.
There is no general logarithm function. For base 4, use `np.log(3) / np.log(4)`.

### The axis parameter

`axis` tells which axis the aggregation removes.
For a matrix, `axis=0` gives one result for each column. `axis=1` gives one result for each row.

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
assert np.sum(m, axis=0).tolist() == [5, 7, 9]
assert np.sum(m, axis=1).tolist() == [6, 15]
```

Agent addition: `np.std` and `np.var` use `ddof=0`, the population formula, by default.
For `[1, 2, 3, 4, 5]`, `ddof=0` gives 1.414 and `ddof=1` gives 1.581.

## Matrix operations

`*` is element-by-element multiplication. `@` is matrix multiplication.
For `A @ B`, shapes `(m, k)` and `(k, l)` give `(m, l)`. Other shapes cause `ValueError`.

| Operation | Function | Note |
| --- | --- | --- |
| Transpose | `A.T` or `np.transpose(A)` | No effect on a one-dimensional array |
| Inverse | `np.linalg.inv(A)` | A singular matrix causes `LinAlgError` |
| Pseudoinverse | `np.linalg.pinv(A)` | Also for singular matrices and matrices that are not square |
| Linear system | `np.linalg.solve(A, b)` | Solves `Ax = b` for a square `A` |
| Least squares | `np.linalg.lstsq(A, b)` | For systems with more equations than unknowns |

Agent addition: `solve` and `lstsq` are usually a better choice than a calculation with `inv`.

Agent check: rounding can hide a singular matrix. The source stores `LinAlgError` for `inv` of `[[9, 8, 7], [6, 5, 4], [3, 2, 1]]`.
With NumPy 2.0.2 on the owner's Mac, the same call gave a result and no error. Do not use this error as the only singularity check.

## Shape changes and selection

`arr.reshape(2, 6)` changes the shape. The number of elements must stay the same.
`np.concatenate((a, b), axis=0)` adds rows. `axis=1` adds columns. The other axis must have the same length.

Slices operate as for lists, with one rule for each axis: `arr[start_row:end_row, start_col:end_col]`.
`A[1, 1]` and `A[1][1]` give the same element.

| Selection | Example | Result |
| --- | --- | --- |
| Boolean mask | `arr[arr > 15]` | Elements that agree with the condition |
| Indexes from a condition | `np.where(arr > 15)` | Tuple with an index array for each axis |
| Choice of two values | `np.where(arr > 15, 1, 0)` | New array with the same shape |
| Index list | `arr[[1, 4]]` | Elements at these indexes |

`arr[arr > 15]` is shorter than the source form `arr[np.where(arr > 15)]`.

### Views and copies

Agent addition: this difference from lists is not in the source.
A NumPy slice and `reshape` give a view of the same data. A list slice gives a copy.

```python
a = np.arange(6)
view = a[1:3]
view[0] = 99
assert a[1] == 99

copy = a[1:3].copy()
copy[0] = 0
assert a[1] == 99
```

A boolean mask and an index list give a copy.

## Sales series analysis

The source generates 180 days of data: a linear trend, weekly seasonality, and random noise.
It uses `np.random.seed(42)`. The agent got the same outliers and lowest days with NumPy 2.0.2.

| Purpose | Code | Source result |
| --- | --- | --- |
| Moving average, 7 days | `np.convolve(sales, np.ones(7) / 7, mode="valid")` | 174 values, thus 6 fewer than the input |
| Outliers | `np.where(sales > mean + 2 * std)[0]` | Days 156, 177, 179 |
| Five lowest days | `np.argsort(sales)[:5]` | Days 13, 19, 5, 26, 14 |
| Five highest days | `np.argsort(sales)[:-6:-1]` | Days 177, 179, 156, 162, 176 |

Agent note: this series has a rising trend. Thus the source threshold selects only late days, and the lowest days are all early.
To find days that are unusual for their period, first remove the trend, for example by a comparison with the moving average.

## Source corrections

| Source example | Correction or limit |
| --- | --- |
| `.dtype` is called a method | It is an attribute |
| `np.ones(shape=(3,))` is called a 1x3 vector | The shape is `(3,)`, one axis. A 1x3 matrix has the shape `(1, 3)` |
| Comment on `np.log2`: `[0. 0.301 1.]` | This is the `log10` result. `log2` gives `[0, 1, 3.32]` |
| Comment "3x4" on `arr.reshape(2, 6)` | The shape is 2x6 |
| Sales comment: 01.01.2026 to 01.07.2026 | 180 days from 01.01.2026 end on 29.06.2026 |
| Answer to Task 1.2 uses `seed(10)` and does not print the shape | The task specifies seed 0 and asks for the shape |
| Answer cell for Task 3.2 | It does not define the task `X` and `y`. In a full run, it uses `X` from an earlier cell, a zero matrix with shape (100, 5) |
| Cells with only `numeric python` or `2*x + y = 1` | These are notes, not code. They cause `SyntaxError` |

## Practice tasks from the source

The notebook has answers for Tasks 1.1, 1.2, 2.1, 2.2, and 3.2 only. It does not identify their author.
The other tasks have no attempts. The vault does not store answers for them yet.

| Task | Summary |
| --- | --- |
| 1.1 | Feature matrix of zeros with 100 objects and 5 features, target vector of ones |
| 1.2 | Random embedding matrix for 6 products with 4 features, seed 0 |
| 2.1 | Min-max normalization of `[10, 20, 30, 40, 50]` |
| 2.2 | Standardization of `[4, 8, 15, 16, 23, 42]` |
| 2.3 | RMSE of `[3, 5, 2, 7]` and `[2.5, 5.5, 2, 8]` |
| 2.4 | Cosine similarity of `[1, 2, 3]` and `[2, 4, 6]` |
| 2.5 | Sigmoid of `[-2, 0, 2]` |
| 2.6 | Softmax of `[2.0, 1.0, 0.1]`. Subtract the maximum before the exponent |
| 3.1 | Linear layer `XW + b`: shapes (4, 3) and (3, 2), result (4, 2) |
| 3.2 | Normal equation for `X = [[1, 1], [1, 2], [1, 3]]` and `y = [1, 2, 3]` |
| 3.3 | Similarity matrix `E E^T` for 5 products with 3 features, after row normalization |
| 4.1 | Class labels from probabilities with `np.where` and a limit of 0.5 |
| 4.2 | One-hot encoding of `[0, 2, 1, 2]` for 3 classes through `np.eye` |
| 4.3 | Min-max normalization for each column of a matrix |
| 4.4 | Train and test split of 10 rows into 8 and 2 with `np.random.permutation` |
| 4.5 | Vector from a random 8x8 image |
| 5.1 | Percentage of days with sales above the mean, through a boolean mask |
| 5.2 | Min-max normalization of the sales series |

## Owner attempts

On 2026-11-08 the owner reported one solved HackerRank problem.
The time is owner-reported. The HackerRank test results were not shown to the agent.

- [Min and Max](https://www.hackerrank.com/challenges/np-min-and-max/problem): solved in 48:42.27.
  The first attempt waited for an empty input line and stopped with `EOFError`. The agent then supplied code that reads `n` lines. The final solution has this code in a shorter form.

Agent check, 2026-11-08: the agent ran the final solution on one input, with the result 3.
Agent comment: `_` is the usual name for a value that the code does not use. Input has no empty line at the end, so use the count from the first line.

## Recall questions

1. What does NumPy do with `[1, 2.0, "3"]`?
2. What is the difference between `ndim`, `shape`, and `size`?
3. What is the difference between the shapes `(3,)` and `(1, 3)`?
4. What is the difference between `arange` and `linspace`?
5. What does `axis=0` give for a matrix?
6. What is the difference between `A * B` and `A @ B`?
7. Which shapes does `A @ B` permit?
8. What does `np.where` return with one argument, and with three?
9. Why can a change to a slice change the source array?
10. Why does a rising trend change the result of the outlier search?

Open questions: official course title, lecture date, required runtime, and whether these tasks are assessed.
