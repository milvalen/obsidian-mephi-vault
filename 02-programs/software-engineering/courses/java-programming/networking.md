---
title: Java networking
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-18
updated: 2026-11-18
---
# Java networking

[Java Programming](java-programming.md) · [File streams](file-streams.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-18. It follows the [file streams unit](file-streams.md).
Its module number, author, and URL are unknown. The text refers to a TCP diagram from naukri.com. The owner did not supply the diagram.
The vault keeps an English summary, not the original text or images.

The agent ran the Java code below with OpenJDK 17.0.20.1 on macOS on 2026-11-18. The checks used only the local machine and a local HTTP server. No external network request was made.

Sources for agent checks:

- [`java.net.Socket`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/Socket.html)
- [`java.net.ServerSocket`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/ServerSocket.html)
- [`java.net.InetSocketAddress`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/InetSocketAddress.html)
- [`java.net.http.HttpClient`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpClient.html)
- [`java.net.http.HttpRequest`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpRequest.html)
- [`java.net.http.HttpResponse`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpResponse.html)
- [`java.net.HttpURLConnection`, Java SE 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/HttpURLConnection.html)

## Skills for assessed work

| Skill | Verified example | Expected output |
| --- | --- | --- |
| Open a server port | `new ServerSocket(0)` | A free port, for example `56437` |
| Accept one client | `server.accept()` | A `Socket` for that client |
| Exchange lines over TCP | `PrintWriter` and `BufferedReader` on the socket streams | Both sides read the line that the other side sent |
| Detect the end of the stream | `readLine()` after the other side closes | `null` |
| Handle a refused connection | `new Socket("localhost", closedPort)` | `ConnectException` |
| Send an HTTP GET request | `HttpClient.newHttpClient().send(...)` | Status `200` and the response body |
| Follow a redirect | `HttpClient.Redirect.NORMAL` | The final status `200` |

## Materials

Videos, English:

1. [Java Network Sockets + Virtual Threads = Cool!](https://www.youtube.com/watch?v=sFizpxHkIlI) — Will Tollefson, 2024-04-26. Basic client and server, then one thread per client.
2. [How To Call a REST API In Java - Simple Tutorial](https://www.youtube.com/watch?v=9oq7Y8n1t00) — Coding with John, 2022-06-06. HTTP request and the response body.
3. [How to call a Java REST API using JDK Http Client](https://www.youtube.com/watch?v=MAw5Ku1OVFA) — Dan Vega, 2024-01-29. `HttpClient` from Java 11.

Browser exercise: [HackerRank Java Exception Handling (Try-catch)](https://www.hackerrank.com/challenges/java-exception-handling-try-catch/problem). It practises the exception handling that network code needs. A public judge cannot open sockets, so a checked socket exercise does not exist.

Local exercises:

1. Echo server on port 0: print `getLocalPort()`, accept one client, send one line, read one line, close.
2. Multi-client server: a loop around `accept()`, one thread per client. Each client sends a name and gets a reply.
3. HTTP GET: call `https://example.com` with `HttpClient`, print the status and the body. Set a connect timeout.
4. Error cases: connect to a closed port and catch `ConnectException`. Set `setSoTimeout(500)` and catch `SocketTimeoutException`.

## Client, server, port, socket

A server listens on a port. A client connects to an address and a port. After the connection, both sides read and write bytes through the socket streams.

| Term | Meaning |
| --- | --- |
| IP address | Address of a computer on the network |
| port | Number that identifies a service on a computer, from 0 to 65535 |
| socket | End point of a connection, made of an address and a port |
| `Socket` | Client-side connection to a remote address and port |
| `ServerSocket` | Server-side object that listens on a port and accepts connections |

Ports 1 to 1023 are well-known ports. On Unix-like systems, a program needs administrator rights to bind them. Port 0 asks the operating system for a free port.

Agent check: `new ServerSocket(0).getLocalPort()` returned `56437`. The value changes at each run.

Common ports: 80 for HTTP, 443 for HTTPS, 21 for FTP. Use a port above 1023 for a test server, for example 8080.

## TCP connection

TCP is a stream protocol. It delivers bytes in order, but it does not keep message boundaries. Both sides must agree on a format, for example one line per message.

The server sequence:

1. Create a `ServerSocket` on a port.
2. Call `accept()`. This call blocks until a client connects.
3. Use the returned `Socket` for that client.
4. Close the socket and the server socket.

The client sequence:

1. Create a `Socket` with the server address and port.
2. Read and write through the socket streams.
3. Close the socket.

Agent check: the client read `hello client`, sent `hello server`, and then read `null` after the server closed. The server read `hello server`. A connection to a closed port threw `ConnectException`.

### Server example

```java
try (ServerSocket server = new ServerSocket(12345)) {
    try (Socket socket = server.accept()) {
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
        PrintWriter writer = new PrintWriter(
                new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true);
        writer.println("Hello. What is your name?");
        System.out.println("Client: " + reader.readLine());
    }
}
```

### Client example

```java
try (Socket socket = new Socket("localhost", 12345)) {
    BufferedReader reader = new BufferedReader(
            new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
    PrintWriter writer = new PrintWriter(
            new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true);
    System.out.println("Server: " + reader.readLine());
    writer.println("Hello, server.");
}
```

`PrintWriter` with `autoFlush = true` calls `flush()` after `println`, `printf`, and `format`. Without autoFlush, call `flush()` before the other side waits for the data.

Set the charset explicitly. `InputStreamReader` and `PrintWriter` use the default charset when no charset is given. Java 18 and later use UTF-8 by default.

### Close and errors

Closing a socket closes its streams. The other side then reads `null` from `readLine()` or `-1` from `read()`.

| Exception | Cause |
| --- | --- |
| `IOException` | General network or stream error |
| `UnknownHostException` | The host name has no IP address |
| `ConnectException` | The address is reachable, but no program listens on the port |
| `SocketTimeoutException` | A read or connect exceeded the timeout |

Use try-with-resources for sockets and streams. An unclosed socket keeps a file descriptor and a port.

## HTTP client in Java 11

`java.net.http.HttpClient` is the standard HTTP client from Java 11. It supports HTTP/1.1 and HTTP/2, synchronous and asynchronous requests, redirects, and WebSocket.

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://example.com"))
        .GET()
        .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.statusCode());
System.out.println(response.body());
```

Agent check: a local HTTP server returned status `200`, body `hello http`, and version `HTTP_1_1`. `HttpClient` did not follow a `302` redirect by default. With `HttpClient.Redirect.NORMAL`, the same request returned status `200` and the body of the target.

`HttpResponse` gives `statusCode()`, `headers()`, `body()`, `uri()`, and `version()`. `BodyHandlers.ofString()` reads the whole body as a `String`. Other handlers read bytes, a stream, or write to a file.

`HttpURLConnection` is the older API. It is not deprecated, but it supports only HTTP/1.1 and blocking calls. `HttpClient` is the better choice for new code.

## Source corrections

| Source statement | Correction |
| --- | --- |
| Ports 1 to 1023 need administrator rights | True on Unix-like systems. Windows does not enforce this rule in the same way. The range is still reserved for standard services |
| Port 0 makes the system choose a free port | True. Agent check: `getLocalPort()` returned `56437` |
| `accept()` blocks until a client connects | True. The call returns a new `Socket` for that client |
| Closing the output stream sends EOF to the other side | True for a socket. Agent check: after the server closed, the client `readLine()` returned `null` |
| `PrintWriter` with autoFlush flushes after each write | It flushes after `println`, `printf`, and `format`, not after every `write` |
| `InputStreamReader` and `PrintWriter` use the system charset | True without a charset argument. Java 18 and later use UTF-8 by default (JEP 400) |
| `HttpClient` appeared in Java 11 | True |
| `HttpClient` replaced `HttpURLConnection` | `HttpClient` is newer, but `HttpURLConnection` is not deprecated. It remains in the API |
| `HttpURLConnection` supports only HTTP/1.1 and blocking calls | True |
| `HttpClient` does not follow redirects by default | True. Agent check: a `302` response stayed `302` until `Redirect.NORMAL` was set |
| `HttpClient` supports HTTP/2 automatically | It requests HTTP/2 by default and falls back to HTTP/1.1 when the server does not support HTTP/2 |
| A missing server gives `ConnectException` | True when the host is reachable. A bad host name gives `UnknownHostException` |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `ConnectException: Connection refused` | No program listens on the port | Start the server first, or check the port |
| `BindException: Address already in use` | Another program uses the port | Use another port, or port 0 |
| `accept()` seems to hang | It waits for a client | Connect a client, or use a timeout |
| The client waits forever for a line | The server did not flush | Use `PrintWriter(..., true)` or call `flush()` |
| Garbled text | Different charsets on the two sides | Set `StandardCharsets.UTF_8` on both sides |
| `readLine()` returns `null` at once | The other side closed the socket | Check the order of close and read |
| The program does not exit | A socket or server socket is open | Use try-with-resources |
| `SocketTimeoutException` | The timeout is too short | Increase the timeout |

## Study advice in the source

The source recommends closing sockets, setting the charset, and handling network exceptions. These rules are correct. It also notes that a production server needs a loop or a thread per client. That is correct but outside this unit.

## Recall questions

1. What is the difference between `Socket` and `ServerSocket`?
2. What does `accept()` return?
3. What does port 0 mean?
4. Which ports need administrator rights on Unix?
5. Why must both sides agree on a message format?
6. What does `readLine()` return after the other side closes?
7. Why does `PrintWriter` need `autoFlush` or `flush()`?
8. Which exceptions occur for a bad host name and for a closed port?
9. Which Java version added `HttpClient`?
10. Does `HttpClient` follow redirects by default?

## Owner attempts

- [HackerRank Java Exception Handling (Try-catch)](https://www.hackerrank.com/challenges/java-exception-handling-try-catch/problem), solved in 10:41 (owner-reported, 2026-11-19). The task divides two integers and prints a message for a zero divisor or for an input outside the 32-bit range.
  The solution divides `sc.nextInt()` by `sc.nextInt()`, catches `ArithmeticException` with a fixed message, and catches `Exception` to print the canonical class name.

Agent check, 2026-11-19: the agent ran the solution with OpenJDK 17 on 7 inputs.
`10 3` gave `3`. `10 0` gave `java.lang.ArithmeticException: / by zero`. `2147483648 1`, `-2147483649 1`, and `1 2147483648` gave `java.util.InputMismatchException`. `5 -2` gave `-2`. One number alone gave `java.util.NoSuchElementException`, which the task does not ask for.
The result is correct for the task. The `ArithmeticException` message is hardcoded; `e.getMessage()` would give the same text without a fixed string. `sc.close()` runs only on the normal path, and the extra `;;` is unnecessary.

## Open questions

- The module number, the author, and the URL of the unit.
- The TCP diagram from naukri.com.
- The Java version used by the course.
- Whether the course requires a multi-client server.