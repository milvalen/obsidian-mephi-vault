---
title: Java arrays
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-02
updated: 2026-11-06
---
# Java arrays

[Java Programming](java-programming.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this lecture text on 2026-11-02.
Its module number, author, and URL are unknown. The text says that strings are the next module.
The vault retains an English summary, not the original text or images.
The owner did not report attempts at the practice tasks.

Sources for agent checks, read on 2026-11-02:

- [Java Language Specification, SE 17, Chapter 10](https://docs.oracle.com/javase/specs/jls/se17/html/jls-10.html)
- [`java.util.Arrays`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Arrays.html)

## One-dimensional arrays

A Java array is an object with a fixed length. It keeps elements of one type.
An array of a primitive type keeps values. An array of a reference type keeps references.
Indexes start at 0. The last valid index is `length - 1`.
Access by index takes constant time, O(1).

`length` is a `final` field, not a method. Write `nums.length`, not `nums.length()`.
You cannot change the length of an array. To get a different length, create a new array.

| Element type | Default element value |
| --- | --- |
| numeric types | `0` or `0.0` |
| `boolean` | `false` |
| `char` | `'\u0000'` |
| reference types | `null` |

```java
int[] a = {1, 2, 3, 4, 5};  // Array initializer
int[] b = new int[10];      // Ten elements with the value 0
b[0] = 1;                   // Write
int first = b[0];           // Read
```

Agent addition: an array initializer without `new` is valid only in a declaration.
To assign a new array to an existing variable, write `nums = new int[]{1, 2};`.

## Index errors and exceptions

An index outside the array causes `ArrayIndexOutOfBoundsException`.
The usual cause is `i <= nums.length` as a loop condition. Use `i < nums.length`.

An exception is an object that reports an error or a special condition during execution.
It stops the usual program flow. Use `try`, `catch`, and `finally` to process it.

| Category | Classes |
| --- | --- |
| checked exception | `Exception` subclasses, other than `RuntimeException` and its subclasses |
| unchecked exception | `RuntimeException` and its subclasses |
| error | `Error` and its subclasses |

`ArrayIndexOutOfBoundsException` is an unchecked exception.

## Find a maximum and its index

Set the initial maximum to `nums[0]`, not to `0`.
With the values `{-5, -2, -9}`, an initial value of `0` gives an incorrect result of `0`.
The correct result is `-2`.

```java
int max = nums[0];
int maxIndex = 0;
for (int i = 1; i < nums.length; i++) {
    if (nums[i] > max) {
        max = nums[i];
        maxIndex = i;
    }
}
```

Agent addition: this code fails for an array with length 0, because `nums[0]` does not exist.
Check the length first if the input can be empty.

## Two-dimensional and jagged arrays

A two-dimensional array in Java is an array of references to arrays.
`a.length` gives the number of rows. `a[i].length` gives the number of columns in row `i`.
The index order is row, then column: `a[i][j]`.

```java
int[][] a = {{1, 2, 3}, {4, 5, 6}};
int[][] b = new int[3][4];          // Rectangular, all values 0
int[][] c = new int[3][];           // Rows are null at this step
c[0] = new int[1];
c[1] = new int[3];                  // Jagged: row lengths differ
```

Agent addition: with `new int[3][]`, each row is `null` until you assign it.
`c[2].length` then causes `NullPointerException`.

A for-each loop gives shorter code and has no index to make incorrect.

```java
for (int[] row : a) {
    for (int x : row) {
        System.out.print(x + " ");
    }
    System.out.println();
}
```

Agent addition: the loop variable is a copy of the element value.
An assignment to `x` does not change a value in the array. Use an index loop to write values.

To flatten a rectangular array row by row, use `flat[k++] = a[i][j]`.
To calculate the indexes again, use `i = k / cols` and `j = k % cols`.

The source recommends that the outer loop goes through rows, for better use of the processor cache.
Agent note: each row is a separate object. The JLS does not specify memory placement for rows.
Measure before you make a performance claim for a specific program.

## Copy and comparison

| Operation | Result for `int[][]` |
| --- | --- |
| `a.clone()` | Shallow copy: a new outer array with shared rows |
| `Arrays.copyOf(a[i], a[i].length)` for each row | Deep copy for `int[][]` |
| `a == b` | Compares references to outer arrays |
| `Arrays.equals(a, b)` | Compares row references, not row content |
| `Arrays.deepEquals(a, b)` | Compares the content of nested arrays |

## `java.util.Arrays` methods

| Method | Function | Agent addition |
| --- | --- | --- |
| `copyOf(array, length)` | Copies an array to a new length | A shorter length truncates. A longer length adds default values |
| `copyOfRange(array, from, to)` | Copies a range | `to` is exclusive and can be more than the length |
| `toString(array)` | Gives the elements as one string | For nested arrays, use `deepToString` |
| `sort(array)` | Sorts in ascending order | Changes the supplied array |
| `binarySearch(array, element)` | Gives the index of an element | See the conditions below |
| `fill(array, value)` | Sets all elements to one value | |
| `equals(a, b)` | Compares length and elements | For nested arrays, use `deepEquals` |

Agent additions for `binarySearch`:

- The array must be sorted. If not, the result is undefined.
- If a value occurs more than once, the API does not specify which index you get.
- If the value is not in the array, the result is `-(insertionPoint) - 1`.

Printing an array directly gives a type and hash text such as `[I@...`, not the elements.

## Practice tasks from the source

Change the maximum example to do these tasks. No attempts are reported.

1. Calculate the sum of the elements.
2. Count the even elements with `nums[i] % 2 == 0`.
3. Find the minimum element and its index.

## Owner attempts on CodingBat

On 2026-11-06 the owner reported two solved CodingBat problems.
Times are owner-reported. The CodingBat test results were not shown to the agent.

- [countEvens](https://codingbat.com/prob/p162010): solved in approximately 30 seconds. A for-each loop counts values with `num % 2 == 0`.
- [bigDiff](https://codingbat.com/prob/p196640): solved in 10:27.99. The solution sets `largest = 0` and `smallest = 1`. At the first loop step, `smallest > largest` causes initialization from `nums[0]` and `nums[1]`. A separate branch processes length 1.

Agent check, 2026-11-06: the agent ran the owner's `bigDiff` on 11 inputs, with negative values, equal values, and length 1.
All results agreed with a reference solution.
Agent comment: the result is correct, but the sentinel values make the code hard to read.
Initialize both values from `nums[0]`, as in the lecture's maximum example. Then length 1 needs no separate branch.

The owner then wrote a second `bigDiff` version in 01:36.85 (owner-reported) with initialization from `nums[0]`.
Its logic agrees with the code below. Only the argument order in `Math.min` and `Math.max` differs.

```java
int smallest = nums[0];
int largest = nums[0];
for (int num : nums) {
    smallest = Math.min(smallest, num);
    largest = Math.max(largest, num);
}
return largest - smallest;
```

## Common errors

- `i <= nums.length` as a loop condition.
- `nums.length()` instead of `nums.length`.
- `a[j][i]` instead of `a[i][j]`.
- An initial maximum of `0` when the values can be negative.
- `clone()` on a two-dimensional array when an independent copy is necessary.
- `binarySearch` on an unsorted array.

## Recall questions

1. What is the default element value in `new boolean[2]`, `new char[2]`, and `new String[2]`?
2. Why is the last valid index `length - 1`?
3. Which category of exception is `ArrayIndexOutOfBoundsException`?
4. Why is `max = nums[0]` better than `max = 0`?
5. What does `a[i].length` give, and why can it differ between rows?
6. After `int[][] b = a.clone(); b[0][0] = 99;`, what is the value of `a[0][0]`?
7. What does `Arrays.copyOfRange(new int[]{22, 4, 5, 6}, 1, 3)` give?
8. What does a negative result from `binarySearch` tell you?

## Verification limits

Agent check on 2026-11-02 with OpenJDK 17.0.20.1 on the owner's Mac:
the agent executed checks for default values, index errors, `new int[-1]`, empty and jagged arrays, `clone`, deep copy, `equals`, `deepEquals`, `copyOf`, `copyOfRange`, `binarySearch`, and for-each writes.
The observed results agree with this note. The check code is not stored in the vault.

The cache statement was not measured. The interactive `Scanner` programs from the source were not executed.
The note remains a draft because the course details are unknown.
