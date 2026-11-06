---
title: Java strings
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-06
updated: 2026-11-06
---
# Java strings

[Java Programming](java-programming.md) · [Java arrays](arrays.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this lecture text on 2026-11-06. It follows the [arrays lecture](arrays.md).
Its module number, author, and URL are unknown.
The text refers to two screencasts, about string storage and formatting. The owner did not supply them.
The vault retains an English summary, not the original text or images.

Source for agent checks: [`String`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html).

## Strings and concatenation

A string is a sequence of characters. In Java, `String` is a class, not a primitive type.
The `+` operator joins strings. This operation is concatenation.

```java
String a = "2";
String b = "2";
System.out.println(a + b);       // 22, not 4
System.out.println("Total: " + 22); // The number becomes text
```

Concatenation operates from left to right. The order of operands changes the result.
Agent check: `1 + 2 + "s"` gives `3s`. `"s" + 1 + 2` gives `s12`.

`String` is immutable. Each operation that "changes" a string makes a new string.
For many changes in a loop, use `StringBuilder`.

## Length and characters

`length()` is a method on a string. On an array, `length` is a field.
`charAt(i)` gives the character at index `i`. Indexes start at 0.
`charAt(s.length())` causes `StringIndexOutOfBoundsException`.

Agent addition: a string is not a `char[]`. `length()` counts UTF-16 code units, not visible characters.
An emoji such as `😀` has `length()` 2 but only one code point.
For such text, use `codePoints()` or `codePointCount`.

## Comparison

`==` compares references. `equals` compares content. Use `equals` for strings.
`equalsIgnoreCase` compares content and ignores letter case.

Agent check: two literals `"22"` give `true` with `==`, because Java keeps one shared copy of equal literals.
A string from `new String("22")` or from `Scanner` input gives `false` with `==`.
Thus a test with literals can hide an incorrect `==` comparison.

## Common methods

| Method | Result | Agent addition |
| --- | --- | --- |
| `charAt(i)` | Character at index `i` | |
| `concat(s)` | Joined string | |
| `equals(o)` / `equalsIgnoreCase(s)` | `true` if equal | `equals` accepts any `Object` |
| `indexOf(...)` / `lastIndexOf(...)` | Index of the first or last match | `-1` if there is no match |
| `length()` | Number of UTF-16 code units | |
| `replace(old, new)` | All matches replaced | Literal text, not a regular expression |
| `replaceAll(regex, s)` / `replaceFirst(regex, s)` | All or the first match replaced | The first argument is a regular expression |
| `split(regex)` | Array of parts | The argument is a regular expression |
| `substring(begin)` / `substring(begin, end)` | Part of the string | `end` is exclusive |
| `toLowerCase()` / `toUpperCase()` | Changed letter case | Depends on the locale. See below |
| `trim()` | Text without leading and trailing characters up to U+0020 | `strip()` also removes Unicode whitespace |
| `String.valueOf(x)` | Text form of `x` | |

Agent checks on regular expressions:

- `"a.b".split(".")` gives an empty array, because `.` matches any character. Use `split("\\.")`.
- `"a.b".replaceAll(".", "x")` gives `xxx`. `"a.b".replace(".", "x")` gives `axb`.
- `"a,b,,".split(",")` gives `[a, b]`. Empty parts at the end are removed.

To check for empty or space-only text, use `s == null || s.isBlank()` (Java 11 and later).

## Locale and letter case

Letter case rules depend on the locale.
Agent check: `"TITLE".toLowerCase(new Locale("tr"))` gives `tıtle` with a dotless `ı`.
For program identifiers and comparison keys, use `toLowerCase(Locale.ROOT)`.

## Palindrome check

A palindrome reads the same from left to right and from right to left.
The source program uses two indexes that move toward the center.
It ignores letter case and skips characters that are not letters or digits.
Its time is O(n).

The source also finds the longest palindromic substring by expansion from each center.
It checks an odd center `(i, i)` and an even center `(i, i + 1)`. Its time is O(n²) in the worst case.
This search ignores letter case but keeps spaces and punctuation.

Read the full line with `nextLine()`. The `next()` method stops at whitespace.

Agent check: the phrase "А роза упала на лапу Азора" is a palindrome for the first method.
The longest palindromic substring with spaces is only `ала`.

## Formatting

`String.format` puts values into a template. `System.out.printf` prints the same result.

| Specifier | Function | Example result |
| --- | --- | --- |
| `%s`, `%d`, `%f` | String, integer, floating-point number | |
| `%10s` / `%-10s` | Width 10, right or left alignment | `     right` |
| `%05d` | Width 5 with leading zeros | `00042` |
| `%.3f` | Three digits after the decimal separator | `3.142` |
| `%,d` | Group separators from the locale | `1,234,567` for `Locale.US` |
| `%2$s` | Argument by position | |
| `%%` | Percent sign | `%` |

The default locale is `Locale.getDefault()`. Specify a locale for a fixed result.
Agent check: `Locale.GERMANY` gives `1234,56`. The `ru` locale gives `1 234 567` and `1,50`.
A specifier that does not agree with the argument type causes `IllegalFormatConversionException`.

## Practice tasks from the source

No attempts are reported.

1. Put the comma variable `d` into `a + b + c` to make the phrase "Kaznit' nelzya pomilovat'" have a clear meaning.
2. Correct the argument order in a `String.format` call, so that the name, age, and status go in the correct positions.

## Owner attempts on CodingBat

On 2026-11-06 the owner reported two solved CodingBat problems.
Times are owner-reported. The CodingBat test results were not shown to the agent.

- [countHi](https://codingbat.com/prob/p147448): solved in 12:40.30, with a hint at approximately 10 minutes.
  A loop with `i < str.length() - 1` compares `str.substring(i, i + 2)` with `"hi"`.
  The owner then wrote the same logic again in 06:45.09 with a shorter `if` statement.
- [endOther](https://codingbat.com/prob/p126880): solved in 24:28.53.
  The solution selects the longer string, cuts its end with `substring`, and compares the two parts in lowercase.

Agent check, 2026-11-06: the agent ran both solutions on 24 inputs, with empty strings, equal lengths, and overlapping `"hi"`.
All results agreed with a reference solution.
Agent comment: `endOther` is correct. The `endsWith` method gives shorter code with the same result:

```java
a = a.toLowerCase();
b = b.toLowerCase();
return a.endsWith(b) || b.endsWith(a);
```

The owner then wrote this `endsWith` version of `endOther` in 01:28.0 (owner-reported). The code is the same as the code above.

## Common errors

- `==` instead of `equals`.
- `charAt(s.length())`.
- A regular expression character such as `.` in `split` or `replaceAll` without `\\`.
- `+` in a long loop instead of `StringBuilder`.
- Letter case change without a locale for program identifiers.
- Format arguments in an incorrect order or with an incorrect type.

## Recall questions

1. What does `"2" + "2"` give, and why?
2. What do `1 + 2 + "s"` and `"s" + 1 + 2` give?
3. Why can `==` give `true` for two strings with the same text?
4. Why does `"a.b".split(".")` give an empty array?
5. What is the difference between `replace` and `replaceAll`?
6. Why can `length()` be 2 for one emoji?
7. When do you use `StringBuilder`?
8. What does `%-10s` do?

## Verification limits

Agent check on 2026-11-06 with OpenJDK 17.0.20.1 on the owner's Mac.
The agent executed the palindrome methods and checks for `==`, concatenation order, `length()`, `charAt`, `split`, `replaceAll`, `trim`, `strip`, letter case, and formatting.
The results agree with this note. The check code is not stored in the vault.
The agent did not see the screencasts. The note remains a draft because the course details are unknown.
