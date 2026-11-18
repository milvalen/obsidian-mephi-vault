---
title: Java NIO
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-19
updated: 2026-11-19
---
# Java NIO

[Java Programming](java-programming.md) · [Networking](networking.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-19. It follows the [networking unit](networking.md).
Its module number, author, and URL are unknown. The text has no images.
The vault keeps an English summary, not the original text.

The agent ran the Java code below with OpenJDK 17.0.20.1 on macOS on 2026-11-19. The checks used local files and a local HTTP server. No external network request was made.

Sources for agent checks:

- [`java.nio.ByteBuffer`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/ByteBuffer.html)
- [`java.nio.channels.FileChannel`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/channels/FileChannel.html)
- [`java.nio.channels.Selector`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/channels/Selector.html)
- [`java.nio.channels.SocketChannel`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/channels/SocketChannel.html)
- [`java.nio.file.Path`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Path.html)
- [`java.nio.file.Files`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Files.html)
- [`java.net.http.HttpClient`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpClient.html)

## Skills for assessed work

| Skill | Verified example | Expected output |
| --- | --- | --- |
| Use a buffer | `ByteBuffer.allocate(16)`, `put`, `flip`, `get` | 3 bytes read as `abc` |
| Copy a file with channels | `FileChannel` and a loop with `read`, `flip`, `write`, `clear` | The target file is a byte copy |
| Copy without a loop | `inChannel.transferTo(0, inChannel.size(), outChannel)` | The same byte copy |
| Copy with `Files` | `Files.copy(source, target, REPLACE_EXISTING)` | The same byte copy |
| Use a non-blocking client | `SocketChannel` and `Selector` with `OP_CONNECT`, `OP_WRITE`, `OP_READ` | An HTTP response with status `200` |
| Send an async request | `HttpClient.sendAsync(...).join()` | Status `200` and the body |

## Materials

Videos, English:

1. [Socket Programming with Java NIO — Channels, Selectors, and Buffers](https://www.youtube.com/watch?v=h76n2R4HRts) — Will Tollefson, 2024-05-10. Channels, selectors, and buffers on sockets.
2. [Java NIO — Reading from and Writing to a file in Java](https://www.youtube.com/watch?v=_hN-m7qOn9Y) — Geekific, 2021-04-10. File channels and buffers.

A checked browser exercise for NIO does not exist on the public judges, because the sandbox does not expose a file system or sockets in the needed form. Use the local tasks below.

Local exercises:

1. Copy a file with `FileChannel` and a `ByteBuffer` loop. Compare the result with `cmp`.
2. Copy the same file with `transferTo` and with `Files.copy`. Compare all three files.
3. Read a text file with `Files.readAllLines` and print the number of lines.
4. Send an async request to a local HTTP server with `HttpClient.sendAsync`, then `join()`, and print the status and the body length.
5. Run the selector client from the lecture against a local server. Change `Connection: close` to `Connection: keep-alive` and observe that the read loop no longer stops at the server close.

## Java IO and Java NIO

Java IO is stream-oriented and blocking. Java NIO is buffer-oriented and supports non-blocking mode for selectable channels.

| Aspect | Java IO | Java NIO |
| --- | --- | --- |
| Data model | Stream of bytes or characters | `Buffer` plus `Channel` |
| Blocking | A read or write blocks the thread | Selectable channels can work in non-blocking mode |
| Many connections | One thread per connection is usual | One selector can watch many channels |
| Files | `File`, `FileInputStream`, `FileReader` | `Path`, `Files`, `FileChannel` |
| Complexity | Simple | More state: buffer position, limit, readiness |

NIO came in JDK 1.4. NIO.2 came in Java 7 with `java.nio.file`.

Important: only `SelectableChannel` types, such as sockets and pipes, support non-blocking mode. `FileChannel` and the `Files` methods are blocking.

Agent check: `FileChannel` is not a `SelectableChannel`, and `FileChannel` has no `configureBlocking` method. `File` is not annotated `@Deprecated` in JDK 17; it is legacy, and `Path` is the better choice.

## Buffers

A `ByteBuffer` has a position, a limit, and a capacity. `put` writes at the position and moves it. `get` reads at the position and moves it.

| Method | Effect |
| --- | --- |
| `allocate(n)` | Heap buffer with capacity `n` |
| `allocateDirect(n)` | Buffer outside the Java heap |
| `flip()` | `limit = position`, then `position = 0` |
| `clear()` | `position = 0`, `limit = capacity` |
| `compact()` | Copies the remaining bytes to the start |
| `hasRemaining()` | `position < limit` |

Agent checks:

- `allocate` gave `hasArray() = true`. `allocateDirect` gave `hasArray() = false`.
- After `put("abc")` on a 16-byte buffer, position and limit were `3/16`. After `flip()`, `0/3`. The read gave `abc`. After `clear()`, `0/16`.

Without `flip()`, a write starts at the current position and stops at the limit. A full buffer writes 0 bytes. A partially filled buffer writes the unfilled tail, usually zeros.

Agent check: a 16-byte buffer with 3 bytes wrote 13 bytes without `flip()`. A full 3-byte buffer wrote 0 bytes.

## Channels and file copy

`FileChannel.open` opens a channel with options such as `READ`, `WRITE`, `CREATE`, and `TRUNCATE_EXISTING`. A channel reads into a buffer and writes from a buffer.

```java
try (FileChannel in = FileChannel.open(source, StandardOpenOption.READ);
     FileChannel out = FileChannel.open(target, StandardOpenOption.CREATE,
             StandardOpenOption.WRITE, StandardOpenOption.TRUNCATE_EXISTING)) {
    ByteBuffer buffer = ByteBuffer.allocate(8192);
    while (in.read(buffer) != -1) {
        buffer.flip();
        while (buffer.hasRemaining()) {
            out.write(buffer);
        }
        buffer.clear();
    }
}
```

The loop must repeat `write` until the buffer has no remaining bytes. A channel can write only part of the buffer.

`transferTo` copies without a Java loop:

```java
in.transferTo(0, in.size(), out);
```

`Files.copy` does the same at the file level:

```java
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
```

Agent check: `transferTo` copied `1000` bytes. `Files.copy` made an identical file. Both files matched the source byte for byte.

`transferTo` may use an operating-system transfer, but zero-copy is not guaranteed.

## Non-blocking sockets and Selector

`SocketChannel` and `ServerSocketChannel` can work in non-blocking mode. A `Selector` reports which channels are ready.

| Key | Meaning |
| --- | --- |
| `OP_CONNECT` | The connection is ready to finish |
| `OP_WRITE` | The channel can accept bytes |
| `OP_READ` | The channel has bytes to read |

The example client registers `OP_CONNECT`, calls `finishConnect()`, writes the request, then reads the response. `read()` returns `0` when no data is ready, and `-1` when the server closes the connection. A `Connection: close` request makes the close the end marker.

Agent check: the client sent `GET / HTTP/1.1` to a local server and received `216` bytes with status `200`.

Non-blocking code must handle partial reads and writes. Keep the buffer state and change `interestOps` as the exchange moves from connect to write to read.

## Async HTTP client

`HttpClient.sendAsync` returns a `CompletableFuture`. `join()` waits for the result.

```java
HttpResponse<String> response = client
        .sendAsync(request, HttpResponse.BodyHandlers.ofString())
        .join();
```

Agent check: the async request to the local server returned status `200` and a body of `99` characters.

`HttpClient` does not decompress gzip responses automatically. The client must send `Accept-Encoding: gzip` and decode the body.

Agent check: the server sent a gzip body. The client received `30` bytes that started with `1F 8B`, the gzip magic number, and the `Content-Encoding` header stayed `gzip`.

## Source corrections

| Source statement | Correction |
| --- | --- |
| NIO offers non-blocking mode | Only `SelectableChannel` types support it. `FileChannel` and `Files` are blocking. Agent check: `FileChannel` is not a `SelectableChannel` and has no `configureBlocking` |
| Without `flip()`, `write(buffer)` writes nothing | A full buffer writes 0 bytes. A partially filled buffer writes the unfilled tail, usually zeros. Agent check: 16-byte buffer with 3 bytes wrote 13 bytes |
| `java.io.File` is deprecated | `File` is not annotated `@Deprecated` in JDK 17. It is legacy, and `Path` is preferred. Agent check: the annotation is absent |
| `transferTo` gives zero-copy | It may use an operating-system transfer, but zero-copy is not guaranteed |
| `HttpClient` supports automatic compression | It does not decompress gzip responses by default. Agent check: the body started with `1F 8B` and kept the `gzip` header |
| NIO is faster than IO | NIO scales better for many connections and large files. For simple sequential file work, the difference is small, and `Files.copy` or `transferTo` can use OS optimizations |
| NIO uses direct buffers | `ByteBuffer.allocate` creates a heap buffer. `allocateDirect` creates a direct buffer. Agent check: `hasArray()` was `true` and `false` |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `BufferOverflowException` | `put` after the limit | `clear()` or `compact()` |
| `BufferUnderflowException` | `get` after the limit | `flip()` before reading |
| The copied file has extra zero bytes | `write` without `flip()` | `flip()` after `read` |
| The copy is incomplete | One `write` call for a partial buffer | Loop while `hasRemaining()` |
| `NotBlocking` errors | Non-blocking call without a ready key | Register the channel and wait for the selector |
| `read()` returns `0` | No data is ready in non-blocking mode | Wait for the next `OP_READ` event |
| The selector loop spins | `select()` returns 0 | Use a timeout and a deadline |
| Garbled gzip body | No manual decompression | Wrap the body in `GZIPInputStream` |

## Recall questions

1. What is the difference between Java IO and Java NIO?
2. What does `flip()` do?
3. What does `clear()` do?
4. Why can a write without `flip()` write zeros?
5. Which channels support non-blocking mode?
6. What does `Selector` report?
7. What do `read()` values `0` and `-1` mean in non-blocking mode?
8. How does `transferTo` copy a file?
9. Why is `Path` preferred over `File`?
10. Does `HttpClient` decompress gzip automatically?

## Owner attempts

No attempts yet.

## Open questions

- The module number, the author, and the URL of the unit.
- The Java version used by the course.
- Whether the course expects the selector example or only `Files`.