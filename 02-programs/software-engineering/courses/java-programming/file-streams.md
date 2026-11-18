---
title: Java file streams
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-18
updated: 2026-11-18
---
# Java file streams

[Java Programming](java-programming.md) · [Character streams](character-streams.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-18. It follows the [character streams unit](character-streams.md). The next unit is about buffered streams.
Its module number, author, and URL are unknown. The text refers to a diagram from javaskool.com. The owner did not supply the diagram.
The vault keeps an English summary, not the original text or images.

The agent ran the Java code below with OpenJDK 17.0.20.1 on macOS on 2026-11-18. The default charset was UTF-8. The agent also ran the same code with `LC_ALL=ru_RU.CP1251`.

Sources for agent checks:

- [`java.io.FileInputStream`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileInputStream.html)
- [`java.io.FileOutputStream`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileOutputStream.html)
- [`java.io.FileReader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileReader.html)
- [`java.io.FileWriter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileWriter.html)
- [`java.io.BufferedReader`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedReader.html)
- [`java.util.zip.ZipInputStream`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/zip/ZipInputStream.html)
- [`java.util.zip.ZipOutputStream`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/zip/ZipOutputStream.html)
- [`java.util.zip.ZipEntry`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/zip/ZipEntry.html)
- [`java.io.PrintStream`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintStream.html)
- [`java.io.PrintWriter`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/PrintWriter.html)
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)

## Skills for assessed work

| Skill | Verified example | Expected output |
| --- | --- | --- |
| Choose a byte stream or a character stream | A ZIP entry with binary data uses `FileInputStream`. A text file uses `FileReader` | The binary data stays byte values. The text becomes characters |
| Read a file byte by byte | `FileInputStream.read()` on `Hello` | `72 101 108 108 111`, then `-1` |
| Write bytes and append | `FileOutputStream` without `true`, then with `true` | The first write replaces the file. The second adds bytes |
| Copy a file | `FileInputStream` and `FileOutputStream` in one loop | The output file is a byte copy of the input |
| Read text lines | `BufferedReader.readLine()` | Each line without its terminator, then `null` |
| Read a ZIP entry | `ZipInputStream.getNextEntry()` and `closeEntry()` | Each entry name and its content |
| Create a ZIP archive | `ZipOutputStream.putNextEntry()` and `closeEntry()` | An archive with the named entries |
| Write formatted text | `PrintWriter.println(123)` | The text `123` and a newline |

## File streams and byte streams

A file stream connects a program to a file. Java represents it with `FileInputStream` for reading and `FileOutputStream` for writing.

`FileInputStream` extends `InputStream`. `FileOutputStream` extends `OutputStream`. Both operate on bytes.

| Class | Superclass | Purpose |
| --- | --- | --- |
| `FileInputStream` | `InputStream` | Read bytes from a file |
| `FileOutputStream` | `OutputStream` | Write bytes to a file |

Agent check: `FileInputStream.class.getSuperclass()` is `java.io.InputStream`. `FileOutputStream.class.getSuperclass()` is `java.io.OutputStream`.

### Read bytes

```java
try (FileInputStream in = new FileInputStream("input.bin")) {
    int b;
    while ((b = in.read()) != -1) {
        System.out.print((char) b);
    }
}
```

Agent checks:

- The file `Hello` gave the values `[72, 101, 108, 108, 111]`, then `-1`.
- A missing input file throws `FileNotFoundException`.
- `read()` returns a value from 0 to 255, or `-1` at the end of the file.

### Write bytes

```java
try (FileOutputStream out = new FileOutputStream("output.bin")) {
    out.write('H');
    out.write('i');
    out.write('!');
}
```

Agent checks:

- `write(0x1FF)` wrote one byte, `FF`. The method writes the low 8 bits.
- `FileOutputStream` without `true` overwrites the file. The content changed from `AB` to `C`.
- `FileOutputStream` with `true` appends. The content was `AB`.
- A missing output file is created.

`FileOutputStream` does not have a Java-level buffer. Its `flush()` method is inherited from `OutputStream` and does nothing. Buffering requires `BufferedOutputStream`.

Agent check: `FileOutputStream.flush` is declared by `java.io.OutputStream`.

### Copy a file

```java
try (FileInputStream in = new FileInputStream("data.bin");
     FileOutputStream out = new FileOutputStream("copy.bin")) {
    int b;
    while ((b = in.read()) != -1) {
        out.write(b);
    }
}
```

The output file is an exact byte copy of the input file.

Reading one byte at a time is slow for large files. Read a block into a `byte[]` with `read(byte[])` and write it with `write(byte[], int, int)`.

## Character file streams

`FileReader` and `FileWriter` work with characters. They decode bytes to characters and encode characters to bytes.

| Class | Superclass | Purpose |
| --- | --- | --- |
| `FileReader` | `InputStreamReader` | Read characters from a file |
| `FileWriter` | `OutputStreamWriter` | Write characters to a file |

Agent check: `FileWriter.class.getSuperclass()` is `java.io.OutputStreamWriter`.

```java
try (FileReader reader = new FileReader("text.txt");
     FileWriter writer = new FileWriter("text_copy.txt")) {
    int ch;
    while ((ch = reader.read()) != -1) {
        writer.write(ch);
    }
}
```

`FileWriter` with `true` appends. `write(String)` writes a whole string.

Agent check: two writes, without and with `true`, gave the content `onetwo`.

### Read lines

`BufferedReader.readLine()` returns a line without its terminator, or `null` at the end of the file.

```java
try (BufferedReader br = new BufferedReader(new FileReader("text.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}
```

Agent check: the file `a\nb\n` gave the lines `[a, b]`, then `null`.

### Byte-wise reading of UTF-8 text

A byte-wise read does not decode UTF-8. Each byte becomes one `char`.

Agent check: the UTF-8 bytes of `Привет` read with `FileInputStream` gave `U+00D0 U+009F U+00D1 U+0080 ...`, not the letters. `FileReader` with UTF-8 gave `Привет`.

Use a character stream for text.

## ZIP archives

The `java.util.zip` package reads and writes ZIP archives on top of file streams. Each file in an archive is a `ZipEntry`.

```java
try (ZipInputStream zis = new ZipInputStream(new FileInputStream("example.zip"))) {
    ZipEntry entry;
    while ((entry = zis.getNextEntry()) != null) {
        System.out.println(entry.getName());
        zis.closeEntry();
    }
}
```

```java
try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream("archive.zip"))) {
    zos.putNextEntry(new ZipEntry("hello.txt"));
    zos.write("Привет".getBytes(StandardCharsets.UTF_8));
    zos.closeEntry();
}
```

Agent checks:

- A ZIP file with two entries gave the names `one.txt` and `two.txt` and the correct content for each entry.
- An entry name with Cyrillic characters, `привет.txt`, came back unchanged.
- `ZipInputStream.read()` returns `-1` at the end of the current entry. Call `closeEntry()` before `getNextEntry()`.

Set the charset for entry content. `getBytes()` and `new InputStreamReader(zis)` use the default charset. Use `StandardCharsets.UTF_8` when the entry contains UTF-8 text.

## PrintStream and PrintWriter

`PrintStream` writes bytes and has `print`, `println`, and `printf`. `PrintWriter` writes characters and has the same methods.

Agent check: `PrintStream.class.getSuperclass()` is `java.io.FilterOutputStream`. `PrintWriter.class.getSuperclass()` is `java.io.Writer`.

Both classes have a `Charset` constructor since Java 10. `println(123)` wrote the bytes `31 32 33 0A` in both classes.

`new PrintStream("out.txt")` and `new PrintWriter("out.txt")` use the default charset. Set the charset explicitly for text files.

## Source corrections

| Source statement | Correction |
| --- | --- |
| A file stream may keep data in an internal buffer, and `flush()` writes it | `FileOutputStream` has no Java-level buffer. Its `flush()` is inherited from `OutputStream` and does nothing. Buffering needs `BufferedOutputStream` |
| If you do not close the stream, the file may stay locked | A lock depends on the operating system. On Windows an open file can stay locked. On Unix the file can be removed while it is open. The resource leak is real in both cases |
| `FileReader` and `FileWriter` use the platform charset, often UTF-8 | True before Java 18. Java 18 and later use UTF-8 by default (JEP 400). Agent check: JDK 17 with `LC_ALL=ru_RU.CP1251` wrote `CF F0 E8 E2 E5 F2` for `Привет`, which is windows-1251 |
| A byte-wise read with `(char) byteData` prints a text file | Only for a single-byte charset. Agent check: UTF-8 `Привет` gave `U+00D0 U+009F ...`. Use `FileReader` for UTF-8 text |
| ZIP entry text can be read with `new InputStreamReader(zis)` | The constructor uses the default charset. Set `StandardCharsets.UTF_8` when the entry is UTF-8 text |
| `zos.write(content.getBytes())` writes text to the archive | `getBytes()` uses the default charset. Use `content.getBytes(StandardCharsets.UTF_8)` |
| `PrintStream` works with bytes and `PrintWriter` with characters | True. Both have `Charset` constructors since Java 10. Agent check: both wrote `31 32 33 0A` |
| Reading and writing one byte at a time is slow for large files | True. Use `BufferedInputStream`, `BufferedOutputStream`, or block reads and writes |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `FileNotFoundException` on read | The path is wrong or the file is missing | Check the path. Relative paths start at the working directory |
| The file content disappeared | `FileOutputStream` or `FileWriter` without `true` | Use the append constructor |
| The loop does not end | `read()` is not compared with `-1` | Compare the result with `-1` |
| `write("H")` does not compile | `write(int)` takes one byte, not a string | Use `write('H')`, or `write("H".getBytes())` |
| Russian text is garbled | A byte-wise read of UTF-8, or the wrong charset | Use `FileReader` and set the charset |
| `NullPointerException` after `readLine()` | `readLine()` returned `null` at the end of the file | Check for `null` before you use the line |
| ZIP content is garbled | The entry content charset is not set | Use `StandardCharsets.UTF_8` |
| The archive has no entries | `putNextEntry()` or `closeEntry()` is missing | Add the entry, write, then close the entry |
| Data is missing after a write | The stream is not closed | Use try-with-resources |

## Study advice in the source

The source recommends try-with-resources and closing streams. It also recommends block reads and buffered streams for large files. These rules are correct.

## Recall questions

1. What is the difference between `FileInputStream` and `FileReader`?
2. What does `read()` return at the end of a file?
3. What does `write(int)` write to the file?
4. How do you append to a file with `FileOutputStream` and `FileWriter`?
5. Why does a byte-wise read of UTF-8 text give wrong characters?
6. What does `BufferedReader.readLine()` return at the end of a file?
7. How do you read one entry of a ZIP archive?
8. Why must you set the charset for ZIP entry content?
9. What is the difference between `PrintStream` and `PrintWriter`?
10. What does `flush()` do for `FileOutputStream`?

## Owner attempts

Exercism [Word Count](https://exercism.org/tracks/java/exercises/word-count), solved in 34:32 (owner-reported, 2026-11-18). The task counts words in a sentence, lower-cased, with punctuation stripped and apostrophes inside words kept.
  The solution splits with the regex `[\p{Punct}\s&&[^']]|(?<!\p{L})'|'(?!\p{L})` and counts into a `HashMap` with `getOrDefault`.

Agent check, 2026-11-18: the agent ran the solution against all 15 cases of the official `canonical-data.json` of the exercise. All 15 passed.
Two observations. `word == "'"` compares references; it should be `word.equals("'")`. It is harmless here because a lone apostrophe token does not survive the split. `\p{Punct}` covers only ASCII punctuation; non-ASCII punctuation (for example `«`, `—`, `¡`) would stay inside a word token.

- Refined version in 05:39 (owner-reported, 2026-11-18). The owner removed the `word == "'"` check and replaced `getOrDefault` with `merge(lower, 1, Integer::sum)`.

Agent check, 2026-11-18: the agent ran the refined version against the same 15 canonical cases. All 15 passed. Edge inputs `''` and `a '' b` produced no lone apostrophe token, so the removed check was dead code.
A variant with `[\p{P}\p{S}\s&&[^']]` in place of `[\p{Punct}\s&&[^']]` also passed all 15 cases. It splits `¡Sí!`, `«word»`, and `a—b` correctly, while `\p{Punct}` keeps those punctuation marks inside the token.

## Open questions

- The module number, the author, and the URL of the unit.
- The diagram from javaskool.com.
- The Java version used by the course.
- The next unit about buffered streams.