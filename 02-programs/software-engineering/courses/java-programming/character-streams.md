---
title: Java character streams
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-18
updated: 2026-11-18
---
# Java character streams

[Java Programming](java-programming.md) · [Date and Calendar](date-and-calendar.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-18. It follows the [Date and Calendar unit](date-and-calendar.md). The next unit is about the `java.nio` API.
Its module number, author, and URL are unknown. The text refers to several images: a diagram of streams, a mojibake example, and two "русификация" screenshots. The owner did not supply them.
The vault keeps an English summary, not the original text or images.

The agent ran the Java code below with OpenJDK 17.0.20.1 and Oracle JDK 27 on macOS on 2026-11-18. The default charset was UTF-8. The agent also ran JDK 17 with `LC_ALL=ru_RU.CP1251` and with `-Dfile.encoding=windows-1251`.

Sources for agent checks:

- [`java.io.Reader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Reader.html)
- [`java.io.Writer`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Writer.html)
- [`java.io.InputStreamReader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/InputStreamReader.html)
- [`java.io.OutputStreamWriter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/OutputStreamWriter.html)
- [`java.io.FileReader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileReader.html)
- [`java.io.FileWriter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileWriter.html)
- [`java.io.BufferedReader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedReader.html)
- [`java.io.BufferedWriter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedWriter.html)
- [`java.nio.charset.Charset`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/charset/Charset.html)
- [`java.nio.charset.StandardCharsets`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/charset/StandardCharsets.html)
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)

## Skills for assessed work

| Skill | Verified example | Expected output |
| --- | --- | --- |
| Choose a byte stream or a character stream | A PNG file needs a byte stream. A text file needs a character stream | The PNG bytes stay binary. The text becomes characters |
| Read and write a text file | `FileWriter` writes "Привет". `FileReader` reads it | The file has 12 bytes in UTF-8. The reader returns the same text |
| Read lines | `BufferedReader.readLine()` on `one\r\ntwo\rthree\nfour` | `[one, two, three, four]` |
| Set the charset | `new FileReader(file, StandardCharsets.UTF_8)` | The reader uses UTF-8, not the default charset |
| Close streams | try-with-resources around `FileWriter` | The file has all bytes after the block |

## Byte streams and character streams

A byte stream reads and writes bytes. A character stream reads and writes characters. A character stream decodes bytes to characters and encodes characters to bytes.

| Stream type | Base classes | Data | Use |
| --- | --- | --- | --- |
| Byte stream | `InputStream`, `OutputStream` | 8-bit bytes | Binary data: images, audio, archives |
| Character stream | `Reader`, `Writer` | 16-bit UTF-16 code units | Text |

The source calls a character stream "символьный поток". In English, use "character stream".

A character stream is not a byte stream with a different name. It adds a charset. If you read a binary file as text, the decoder replaces malformed bytes with U+FFFD. You lose data. Use a byte stream for binary data.

## Reader and Writer

`Reader` and `Writer` are the base classes for character streams. They are analogous to `InputStream` and `OutputStream`.

| Class | Superclass | Purpose |
| --- | --- | --- |
| `FileReader` | `InputStreamReader` | Read a text file |
| `FileWriter` | `OutputStreamWriter` | Write a text file |
| `BufferedReader` | `Reader` | Buffer characters and read lines |
| `BufferedWriter` | `Writer` | Buffer characters and write lines |
| `InputStreamReader` | `Reader` | Bridge from a byte stream to a character stream |
| `OutputStreamWriter` | `Writer` | Bridge from a character stream to a byte stream |

Agent check: `FileWriter.class.getSuperclass()` is `java.io.OutputStreamWriter`. `FileReader.class.getSuperclass()` is `java.io.InputStreamReader`.

### FileReader and FileWriter

```java
try (FileWriter writer = new FileWriter("output.txt")) {
    writer.write("Hello, Привет!\n");
}
try (FileReader reader = new FileReader("output.txt")) {
    int ch;
    while ((ch = reader.read()) != -1) {
        System.out.print((char) ch);
    }
}
```

Agent checks:

- `FileWriter` without `close()`: the file size was 0 before close and 12 after close. The bytes were the UTF-8 form of "Привет".
- `FileWriter` with `true` appends. The content was "ab".
- `FileReader` on a missing file throws `FileNotFoundException`.
- `read()` returns 0 to 65535, or -1 at the end. The first code unit of "Привет" was 1055 (U+041F).
- `write(int)` writes the low 16 bits. `write(0x1F600)` wrote `EF 98 80`, which is U+F600, not the emoji.
- `FileWriter` without a charset uses the default charset. Under `LC_ALL=ru_RU.CP1251`, JDK 17 wrote 6 bytes in windows-1251. Under JDK 27, it wrote 12 bytes in UTF-8.

## BufferedReader and BufferedWriter

`BufferedReader.readLine()` reads a line. It removes the line terminator. It accepts `\n`, `\r\n`, and `\r`.

Agent check: the file `one\r\ntwo\rthree\nfour` gave `[one, two, three, four]`.

`BufferedWriter.newLine()` writes the platform line separator. On macOS and Linux, it is `\n`.

Agent check: `a`, `newLine()`, `b` gave the bytes `61 0A 62`.

Closing the outer stream closes the inner streams. Agent check: after `outer.close()`, `inner.write("y")` threw `IOException: Stream closed`.

## Charset and encoding

A charset is a mapping between characters and bytes. UTF-8, UTF-16, US-ASCII, and windows-1251 are charsets.

Java `String` uses UTF-16. A `char` is a 16-bit code unit. A supplementary character needs two `char` values.

Agent check: `"😀".length()` is 2. `codePointCount(0, 2)` is 1. `"A".codePointAt(0)` is 65. `"А".codePointAt(0)` is 1040.

The default charset depends on the Java version and the locale:

- JDK 17 uses the locale. On macOS with `LC_ALL=ru_RU.CP1251`, the default charset was `windows-1251`.
- JDK 18 and later use UTF-8 by default (JEP 400). JDK 27 with `LC_ALL=ru_RU.CP1251` still used UTF-8.
- `-Dfile.encoding=COMPAT` restores the locale behavior. JDK 27 with `COMPAT` used `windows-1251`.

Agent check: `FileReader.getEncoding()` returned `UTF8` under the UTF-8 default and `Cp1251` under the windows-1251 default.

### Explicit charset

Before Java 11, `FileReader` and `FileWriter` had no charset constructor. They used the default charset. Java 11 added `Charset` constructors. Without a charset argument, they still use the default charset.

```java
try (Reader reader = new FileReader("input.txt", StandardCharsets.UTF_8)) {
    // ...
}
try (Writer writer = new FileWriter("output.txt", StandardCharsets.UTF_8)) {
    writer.write("Привет");
}
```

Agent check: `FileReader` has no `(String, String)` constructor. It has a `Charset` constructor. `FileWriter` has a `Charset` constructor.

To set a charset on a byte stream, use the bridge classes:

```java
Reader reader = new InputStreamReader(new FileInputStream("input.txt"), StandardCharsets.UTF_8);
Writer writer = new OutputStreamWriter(new FileOutputStream("output.txt"), StandardCharsets.UTF_8);
```

An unknown charset name gives `UnsupportedEncodingException` for `InputStreamReader` and `OutputStreamWriter`. `Charset.forName` gives the unchecked `UnsupportedCharsetException`.

Agent check: `Charset.forName("NOPE")` gave `UnsupportedCharsetException`. `new InputStreamReader(..., "NOPE")` gave `UnsupportedEncodingException`.

### Mojibake

If you decode bytes with the wrong charset, you get mojibake. The bytes of "Привет" in UTF-8 are `D0 9F D1 80 D0 B8 D0 B2 D0 B5 D1 82`.

| Decoding charset | Result |
| --- | --- |
| windows-1251 | `РџСЂРёРІРµС‚` |
| ISO-8859-1 | `ÐŸÑ€Ð¸Ð²ÐµÑ‚` |
| US-ASCII | `????????????` |

The source's `Ð?Ñ?Ð¸Ð²ÐµÑ?` is UTF-8 read as ISO-8859-1 with control characters shown as `?`. It is not windows-1251.

### Malformed input

The default decoder replaces malformed bytes with U+FFFD. It does not throw an exception.

Agent check: the bytes `FF FE 41` read as UTF-8 gave `U+FFFD U+FFFD U+0041`.

## Other character streams

| Class | Purpose |
| --- | --- |
| `PrintWriter` | Write text with `print` and `println`. It has a `Charset` constructor since Java 10 |
| `CharArrayReader`, `CharArrayWriter` | Read and write a `char` array in memory |
| `StringReader`, `StringWriter` | Read from a `String` or write to a `String` |
| `PushbackReader` | Return a read character to the stream |
| `LineNumberReader` | A `BufferedReader` that counts lines |

Agent checks:

- `PrintWriter` with `StandardCharsets.UTF_8` wrote the UTF-8 bytes of "Привет" and a newline.
- `StringWriter` and `CharArrayWriter` returned "abc".
- `PushbackReader` returned the same character after `unread`.
- `LineNumberReader.getLineNumber()` was 0 before the first read and 1 after the first line.

## Wrapper chains

You can combine streams. For example:

```java
try (PrintWriter out = new PrintWriter(
        new BufferedWriter(
            new OutputStreamWriter(
                new FileOutputStream("output.txt"), StandardCharsets.UTF_8)))) {
    out.println("Привет");
}
```

Closing the outer stream closes all inner streams. Agent check: after `PrintWriter.close()`, a write to the inner `FileOutputStream` threw `IOException: Stream Closed`.

## Source corrections

| Source statement | Correction |
| --- | --- |
| A character stream works with text characters or bytes | A character stream works with characters. A byte stream works with bytes. Choose the stream for the data |
| Java character streams operate on 16-bit Unicode symbols | Java uses UTF-16 code units. A supplementary character needs two `char` values. Agent check: `"😀".length()` is 2 |
| `FileReader` uses `FileInputStream` inside | `FileReader` extends `InputStreamReader`. Its constructors create a `FileInputStream`. Agent check: the superclass is `InputStreamReader` |
| `FileWriter` converts characters to bytes and sends them to `FileOutputStream` | `FileWriter` extends `OutputStreamWriter`. Its constructors create a `FileOutputStream`. Agent check: the superclass is `OutputStreamWriter` |
| Reading one character at a time is slow | True. Buffering reduces the number of calls |
| `readLine()` reads up to `\n` | It also accepts `\r\n` and `\r`. Agent check: `one\r\ntwo\rthree\nfour` gave four lines |
| Before Java 11, `FileReader` and `FileWriter` use the default charset and cannot set another | Before Java 11, they had no charset constructor. Java 11 added `Charset` constructors. Without a charset argument, they still use the default charset |
| On Russian Windows, the default charset is windows-1251 | True for Java 17 and earlier. Java 18 and later use UTF-8 by default (JEP 400). Agent check: JDK 27 with `LC_ALL=ru_RU.CP1251` used UTF-8 |
| `FileReader` and `FileWriter` hard-code the platform default charset | Since Java 11, they accept a `Charset`. Without one, they use the default charset |
| The comment `// Запись в Windows-1251` matches `StandardCharsets.UTF_8` | The comment is wrong. The code writes UTF-8 |
| Reading a binary file as text causes conversion errors | The default decoder replaces malformed bytes with U+FFFD. It does not throw. You lose data |
| An unknown charset gives `UnsupportedEncodingException` | True for `InputStreamReader` and `OutputStreamWriter` with a `String` charset name. `Charset.forName` throws the unchecked `UnsupportedCharsetException`. `FileReader` has no `String` charset constructor |
| The mojibake `Ð?Ñ?Ð¸Ð²ÐµÑ?` is UTF-8 read as windows-1251 | windows-1251 gives `РџСЂРёРІРµС‚`. The `Ð?` form is UTF-8 read as ISO-8859-1 with control characters shown as `?` |
| `write(int c)` writes one character | It writes the low 16 bits. Agent check: `write(0x1F600)` wrote U+F600, not the emoji. Use `write(String)` for supplementary characters |
| Closing the outer stream closes all inner streams | True. Agent check: a write to the inner stream after close threw `IOException: Stream closed` |
| `PrintWriter` can set a charset through `OutputStreamWriter` | True. Since Java 10, `PrintWriter` also has `Charset` constructors. Agent check: the constructor exists |
| `LineNumberReader.getLineNumber()` gives the line number | It starts at 0. After the first line, it is 1. Agent check: 0 before the first read, 1 after the first line |
| UTF-16 is an encoding | True. Java's `UTF-16` charset writes a byte order mark. Agent check: the first bytes were `FE FF` |
| A character stream decodes data as the given charset | True. The charset is set at construction. The default decoder replaces malformed input |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `cannot find symbol` for `FileReader` | No `import java.io.FileReader;` | Add the import |
| `cannot find symbol` for `StandardCharsets` | No `import java.nio.charset.StandardCharsets;` | Add the import |
| Cyrillic text is garbled | The charset is wrong | Set the charset explicitly |
| `UnsupportedEncodingException` | The charset name is unknown | Use `StandardCharsets` |
| Data is missing after a write | The stream is not closed or flushed | Use try-with-resources |
| `Stream closed` | A write to an inner stream after the outer stream closed | Write before you close the outer stream |
| `readLine()` returns `null` | The end of the file | Check for `null` |
| `write(0x1F600)` writes the wrong character | `int` is truncated to 16 bits | Use `write(String)` |
| The file is empty after the program ends | The stream was not closed | Close the stream or use try-with-resources |

## Study advice in the source

The source says to use character streams for text and byte streams for binary data. It also says to close streams. These rules are correct.

## Recall questions

1. What is the difference between a byte stream and a character stream?
2. Which classes are the base of character input and output?
3. What does `FileReader` use inside?
4. Why does `FileWriter` need `close()` or `flush()`?
5. What does `readLine()` return at the end of a file?
6. Which line endings does `readLine()` accept?
7. What is a charset? Give three examples.
8. What is the default charset in Java 18 and later? What was it before?
9. How do you set UTF-8 explicitly for reading a file?
10. What happens when you read malformed UTF-8 with the default decoder?
11. Why does `write(0x1F600)` not write the emoji?
12. What does closing the outer stream do to the inner streams?

## Owner attempts

Owner reported completing the Exercism [Grep](https://exercism.org/tracks/java/exercises/grep) exercise on 2026-11-18. The exercise asks for a simplified `grep` that reads files and returns matching lines. The owner did not supply the code or the time.

- [HackerRank Java End-of-file](https://www.hackerrank.com/challenges/java-end-of-file/problem), solved in 03:37 (owner-reported, 2026-11-18). The task reads lines until end of file and prints each line with its number.
  The solution uses `Scanner`, `hasNextLine()`, and `nextLine()`, with the counter `i` starting at 1. The output line is `System.out.println(i++ + " " + sc.nextLine());`.

Agent check, 2026-11-18: the agent ran the solution with OpenJDK 17 on 5 inputs made by the agent.
Three lines of text gave `1 Hello world`, `2 I am a file`, `3 Read me until end-of-file.`. Empty input gave no output. A blank line in the middle was numbered as an empty line. Text without a final newline was numbered correctly. Windows line endings (`\r\n`) were numbered correctly.
The numbering starts at 1: `i++` returns the current value and then increments. The earlier concern that the code starts at 2 was wrong; the run showed the first line numbered 1.
`Scanner` is correct here but slower than `BufferedReader` for large input, because `Scanner` parses and buffers internally. For this task the size is small, so the choice is fine.

## Open questions

- The module number, the author, and the URL of the unit.
- The images and the "русификация" screenshots.
- The Java version used by the course.
