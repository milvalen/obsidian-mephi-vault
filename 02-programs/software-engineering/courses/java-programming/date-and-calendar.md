---
title: Java Date and Calendar
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-16
updated: 2026-11-16
---
# Java Date and Calendar

[Java Programming](java-programming.md) · [Standard library](standard-library.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-16. It follows the [standard library unit](standard-library.md). The next unit is about classes for files.
Its module number, author, and URL are unknown. The text refers to five screenshots of console output and to a page with the format pattern letters. The owner did not supply them.
The vault keeps an English summary, not the original text or images.

The agent ran the Java code below with OpenJDK 17.0.20.1 on macOS on 2026-11-16. The default time zone was `Europe/Moscow`.
The examples use the fixed date 2026-11-16 09:05:03, not the current time, so that the output is the same at each run.

Sources for agent checks:

- [`java.util.Date`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Date.html)
- [`java.util.Calendar`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Calendar.html)
- [`java.text.SimpleDateFormat`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/text/SimpleDateFormat.html)
- [`java.time` package, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/package-summary.html)
- [`DateTimeFormatter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/format/DateTimeFormatter.html)

## Skills for assessed work

1. Make a `Date` from a number of milliseconds and compare two dates.
2. Get and change the fields of a `Calendar`. Remember that `MONTH` starts at 0.
3. Format a date with a pattern, a locale, and a time zone.
4. Do the same operations with the `java.time` classes, which new code uses.

## Unix time

Java keeps a moment as the number of milliseconds after 1970-01-01 00:00:00 UTC. This start point is the Unix epoch.
`System.currentTimeMillis()` gives this number for the current moment.

`Date` has only this number. It has no time zone.
`System.out.println(date)` calls `toString()`, and `toString()` uses the default time zone of the JVM.

Agent check: `new Date(11111111111L)` gave `Sat May 09 17:25:11 MSK 1970` with the time zone `Europe/Moscow`, and `Sat May 09 14:25:11 UTC 1970` with UTC.
The number was the same. Only the text was different.

## Date

| Method | Result | Agent check |
| --- | --- | --- |
| `new Date()` | The current moment | |
| `new Date(long ms)` | The moment `ms` milliseconds after the epoch | See "Unix time" |
| `a.after(b)`, `a.before(b)` | `true` if `a` is later, or earlier, than `b` | `new Date(1).before(new Date(2))` is `true` |
| `a.compareTo(b)` | Negative, 0, or positive | Agent check: −1, 0, or 1. The API promises only the sign |
| `getTime()`, `setTime(long)` | Get or set the number of milliseconds | |

Agent check: `Date` in JDK 17 has 6 public constructors. The constructors with year, month, and day numbers, and `Date(String)`, are deprecated.
The methods `getYear`, `getMonth`, `getHours`, and similar methods are deprecated. The methods in the table above are not deprecated.

## Calendar

`Calendar.getInstance()` gives a calendar for the current moment, the default time zone, and the default locale.
`calendar.get(Calendar.FIELD)` gives one field.

| Field | Values | Agent check for 2026-11-16 09:05:03 |
| --- | --- | --- |
| `YEAR` | Year | 2026 |
| `MONTH` | 0 for January to 11 for December | 10 |
| `DAY_OF_MONTH` | 1 to 31 | 16 |
| `DAY_OF_WEEK` | 1 for Sunday to 7 for Saturday | 2, Monday |
| `HOUR` | 0 to 11 | 9 |
| `HOUR_OF_DAY` | 0 to 23 | 9 |
| `MINUTE`, `SECOND`, `MILLISECOND` | Parts of the time | 5, 3 |
| `ERA` | 0 for BC, 1 for AD in the Gregorian calendar | 1 |

| Method | Result |
| --- | --- |
| `add(field, value)` | Adds `value` to the field. Larger fields change when necessary |
| `set(field, value)` | Sets the field |
| `clear()` | Sets all fields to undefined. The moment becomes the epoch in the default time zone |
| `getTime()` | Gives a `Date` for the same moment |
| `after(Object)`, `before(Object)` | Compare with a different `Calendar` |

Agent checks:

- `add(Calendar.HOUR_OF_DAY, 2)` at 23:00 on 2026-11-16 gave 01:00 on 2026-11-17.
- `add(Calendar.MONTH, 1)` on 2026-01-31 gave 2026-02-28.
- `set(Calendar.MONTH, 12)` gave January of the next year. The calendar does not refuse a value outside the range.
- After `clear()`, `getTimeInMillis()` gave `-10800000`: 00:00 in Moscow is 21:00 UTC on 1969-12-31.

## Format a date

`SimpleDateFormat` changes a `Date` to text with a pattern:

```java
Calendar calendar = Calendar.getInstance();
SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy MMM dd HH:mm:ss", Locale.ENGLISH);
dateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
System.out.println(dateFormat.format(calendar.getTime()));
```

Agent check: for 09:05:03 in Moscow, the output was `2026 Nov 16 06:05:03`. The time zone of the format changed the hour.

| Letter | Meaning | Note |
| --- | --- | --- |
| `yyyy` | Year | |
| `YYYY` | Week year | Agent check: 2024-12-30 gave `2025-12-30` |
| `MM`, `MMM` | Month as a number, as a short name | |
| `mm` | Minute | Agent check: `yyyy-mm-dd` gave `2026-05-16`, with the minute in place of the month |
| `dd` | Day of the month | |
| `HH` | Hour, 0 to 23 | |
| `hh` | Hour, 1 to 12 | Agent check: 01:00 at night and 13:00 both give `01` |
| `ss` | Second | |

The full list is in the [`SimpleDateFormat` API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/text/SimpleDateFormat.html).

## java.time

Java 8 added the package `java.time`. The `Date` and `Calendar` API documentation does not deprecate the classes, but new code uses `java.time`.

| Old class | `java.time` class | Difference |
| --- | --- | --- |
| `Date` | `Instant` | A moment on the UTC time line |
| `Calendar` | `LocalDate`, `LocalDateTime`, `ZonedDateTime` | Months start at 1. Objects do not change: each operation gives a new object |
| `SimpleDateFormat` | `DateTimeFormatter` | Safe for many threads |

```java
LocalDateTime now = LocalDateTime.now();
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy MMM dd HH:mm:ss", Locale.ENGLISH);
System.out.println(formatter.format(now));
```

Agent checks:

- `LocalDateTime.of(2026, 11, 16, 9, 5, 3)` with this pattern gave `2026 Nov 16 09:05:03`. `getMonthValue()` gave 11. `getDayOfWeek()` gave `MONDAY`.
- `LocalDate.of(2026, 1, 31).plusMonths(1)` gave `2026-02-28`.
- `LocalDate.of(2026, 13, 1)` gave `DateTimeException`. `Calendar` accepted month 12 and moved to the next year.
- `Instant.ofEpochMilli(11111111111L)` gave `1970-05-09T14:25:11.111Z`. `date.toInstant()` changes an old `Date` to an `Instant`.

## Source corrections

| Source statement | Correction |
| --- | --- |
| Most methods and constructors of `Date` are deprecated | Agent check: 22 of 36 public methods and constructors are deprecated. The constructors `Date()` and `Date(long)` and all methods in the source table are not deprecated |
| `Calendar` is the more modern class | `Calendar` came in Java 1.1. The modern API is `java.time`, from Java 8 |
| `Date` and `Calendar` are in `java.util` | Correct. `SimpleDateFormat` is in `java.text`, and needs a different `import` |
| `compareTo` gives −1 | The API promises only a negative value. Agent check: JDK 17 gives −1 |
| The manual string gives the current time | Agent check: 09:05 became `9:5`. The code does not add zeros. Use a format pattern |
| A `Calendar` cannot be formatted | Correct. Agent check: `format(calendar)` gave `IllegalArgumentException: Cannot format given Object as a Date`. A `Long` number of milliseconds is accepted |
| `Calendar.getInstance()` gives the current date | It gives a calendar for the default locale. Agent check: for the locale `th_TH`, Java gave a `BuddhistCalendar` with the year 2569 |
| The era is not necessary | For a Buddhist or Japanese calendar, the era and the year are different from the Gregorian ones |
| `clear()` sets the time fields to 0 | It clears all fields. The date also becomes 1970-01-01 |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| The month is one less than expected | `Calendar.MONTH` starts at 0 | Add 1, or use `LocalDate.getMonthValue()` |
| The year is wrong at the end of December | `YYYY` in the pattern | Use `yyyy` |
| The month is a number from 0 to 59 | `mm` in place of `MM` | `MM` is the month, `mm` is the minute |
| The time is 3 hours different | The output used a different time zone | Set the time zone of the format, or use `ZonedDateTime` |
| Wrong dates in a program with threads | One `SimpleDateFormat` object in many threads. Agent check: 1738 of 2000 parse operations on 8 threads gave a wrong result or an exception | Use `DateTimeFormatter` |
| `cannot find symbol` for `SimpleDateFormat` | No `import java.text.SimpleDateFormat;` | Add the import |

## Study advice in the source

The unit ends with advice from a methodologist: study a little each day, and repeat new material on several days in sequence.
The text gives numbers about sleep and memory, but no source for them. The agent did not check these numbers.
The practical rule is useful for this course: repeat the recall questions of a unit on the next days, not only on the day of the lecture.

## Recall questions

1. What does the number in `new Date(11111111111L)` mean?
2. Why does one `Date` show different text on two computers?
3. Which value does `calendar.get(Calendar.MONTH)` give for November?
4. What is the difference between `HOUR` and `HOUR_OF_DAY`?
5. What do `MM`, `mm`, `yyyy`, and `YYYY` mean in a pattern?
6. Why must you call `getTime()` before you format a `Calendar`?
7. What happens after `add(Calendar.MONTH, 1)` on 31 January?
8. Which `java.time` classes replace `Date`, `Calendar`, and `SimpleDateFormat`?

## Owner attempts

- [Codewars Unlucky Days (Java)](https://www.codewars.com/kata/56eb0be52caf798c630013c0), 7 kyu: count the Fridays on the 13th day of the months of a year. Solved in 16:22.57 (owner-reported, 2026-11-16).
  The solution sets day 13 of each month with `Calendar.set(year, month, 13)`, with months 0 to 11, and compares `DAY_OF_WEEK` with `Calendar.FRIDAY`.
  The first compile failed: no `import java.util.Calendar;`, the loop variable `month` with the condition on `i`, and a call of `get` on the result of `set`, which returns `void`.
- Second form of the same task, 13:37.19 (owner-reported, 2026-11-16). The owner read the top solution on Codewars and then wrote it again.
  It uses `java.time`: a stream of `Month.values()`, `LocalDate.of(year, month, 13)`, `getDayOfWeek()`, and a count of `DayOfWeek.FRIDAY`.

Agent check, 2026-11-16: the agent compared both forms with Zeller's congruence for the Gregorian calendar. Both gave 3 for 2015 and 1 for 1986.
For the years 1583 to 3000, both forms gave the correct result in all 1418 years.
For the years 1 to 1582, the `Calendar` form gave a different result in 908 of 1582 years. `GregorianCalendar` uses the Julian calendar before 15 October 1582. `LocalDate` uses the Gregorian rules for all years.
The second form uses streams, method references, and a lambda. The course has not shown them yet.

## Open questions

- The module number, the author, and the URL of the unit.
- The page with the pattern letters that the source refers to.
