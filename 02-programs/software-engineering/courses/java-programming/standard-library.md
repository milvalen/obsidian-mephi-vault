---
title: Java standard library
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-12
updated: 2026-11-12
---
# Java standard library

[Java Programming](java-programming.md) · [Git merge conflicts](git-merge-conflicts.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-12. It starts a module about libraries.
Its module number, author, and URL are unknown. The text refers to three IDE screenshots and a screencast about source view. The owner did not supply them.
The vault keeps an English summary, not the original text or images.

The agent ran the Java code below with OpenJDK 17.0.20.1 and Oracle JDK 27 on macOS on 2026-11-12.
The agent read the `Math` and `StrictMath` source files in the `lib/src.zip` file of JDK 27.

Sources for agent checks:

- [`Math`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Math.html)
- [`java.base` module, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/module-summary.html)
- [IntelliJ IDEA: Libraries](https://www.jetbrains.com/help/idea/library.html)

## Skills for assessed work

1. Call a method of a standard class, for example `Math.hypot`.
2. Know the difference between a module, a package, and a class.
3. Use a class from a package other than `java.lang` with `import`.
4. Find a class and its source code in the IDE.

## Library

A library is code that other programmers wrote and tested. You call its methods, and you do not have to know how they operate.

```java
public class Test {
  public static void main(String[] args) {
    int a = 2;
    int b = 2;
    double c = Math.hypot(a, b);
    System.out.println(c);
  }
}
```

Agent check: the output is `2.8284271247461903`, the square root of 8.
`Math.hypot` takes `double` arguments. Java changes the `int` values to `double` automatically.

| Kind | Meaning | Example |
| --- | --- | --- |
| Standard library | Classes that come with the JDK | `java.lang.Math`, `java.util.Scanner` |
| External library | Classes that you add to a project, usually as a JAR file | A JSON library from a package repository |

## Module, package, and class

The path `java.base → java.lang → Math` has three different levels:

| Level | Example | Meaning |
| --- | --- | --- |
| Module | `java.base` | Group of packages. JDK 17 has 62 modules in the boot layer |
| Package | `java.lang` | Group of classes with one name prefix |
| Class | `Math` | Code with fields and methods |

Agent check: `Math.class.getModule().getName()` gives `java.base`. `Math.class.getPackageName()` gives `java.lang`.

Java imports the `java.lang` package automatically. Classes from other packages need `import`:

```java
import java.util.Scanner;
```

Agent check: without this line, `new Scanner(System.in)` gives the compile error `cannot find symbol`.

## Source code in IntelliJ IDEA

The Project tool window has the node External Libraries. It contains the JDK of the project.
To open the source of a method, put the cursor on its name and press Cmd+B on macOS or Ctrl+B on Windows and Linux. Cmd+click and Ctrl+click also operate.
If the JDK has no `src.zip` file, IntelliJ IDEA shows decompiled code without comments.

Agent check: in JDK 27, `Math.hypot(x, y)` only calls `StrictMath.hypot(x, y)`. That method calls `FdLibm.Hypot.compute(x, y)`.
Thus a source search can need two or three steps.

## Why use a library method

A library method often handles cases that a simple formula does not handle.
Agent check: for `a = b = 1e200`, `Math.sqrt(a * a + b * b)` gives `Infinity`, because `a * a` is too large for `double`.
`Math.hypot(a, b)` gives the correct value, `1.414213562373095E200`.

## Source corrections

| Source statement | Correction |
| --- | --- |
| `java.base → java.lang → Math` is called a library | `java.base` is a module, `java.lang` is a package, and `Math` is a class. The standard library is all modules of the JDK |
| The standard libraries "are in each project" | They come with the JDK of the project. A project with a different JDK version has a different set of classes |
| You only call a method, and you do not have to read about it | Read the API documentation for the argument types, the return type, and the special cases. For example, `Math.round` returns `long` for a `double` argument |
| No information about `import` | Only `java.lang` is available without `import` |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `cannot find symbol` for `Scanner` | No `import java.util.Scanner;` | Add the import, or let the IDE add it |
| Decompiled code without comments | The JDK has no source archive | Install a JDK with `src.zip`, or download sources in the IDE |
| `incompatible types: possible lossy conversion from double to int` | A `double` result goes into an `int` variable | Use `double`, or make the conversion explicit with `(int)` |

## Recall questions

1. What is the difference between a standard library and an external library?
2. Which levels are `java.base`, `java.lang`, and `Math`?
3. Why does `Math` operate without `import`, but `Scanner` does not?
4. What does `Math.hypot(2, 2)` give?
5. Why can `Math.sqrt(a * a + b * b)` give `Infinity` when `Math.hypot(a, b)` does not?
6. How do you open the source of a method in IntelliJ IDEA?

## Open questions

- The module number, the author, and the URL of the unit.
- The IDE and the JDK version that the course uses.
