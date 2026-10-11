# Technical terms

[Study note standard](documentation-standard.md) · [Home](../README.md)

These terms name computing concepts used in this vault.
They are subject-field terms, not additions to the official STE dictionary.
Use the noun and verb forms only with the meanings specified here.
Add every new technical term in the same change that first uses it. Define its meaning and permitted form. Do not use a new term to hide unclear prose.

## Study and evidence terms

| Term | Meaning |
| --- | --- |
| study program | A named course of study that leads to a qualification |
| professional development | Study intended to extend professional knowledge or skills |
| graph color group | An Obsidian search group that assigns a color to matching notes |
| vault | The collection of Obsidian study notes |
| source reference | Data that identifies a source without a copy of its text |
| draft | A note with facts or course details that need a check |
| checked | A note supported by the stated source or calculation checks |
| example | A proposed case or procedure, without an execution claim |
| owner-reported observation | A result that the owner supplied |
| agent check | A check that the agent actually executed |
| recall question | A question to answer from memory before a source check |

## Computing nouns

| Term | Meaning |
| --- | --- |
| binary package | Prepared software and package-manager metadata |
| repository | A package source or an image store, as identified by context |
| dependency | A required program, library, or capability |
| metadata | Data that describes a resource or its contents |
| image | Immutable container content and runtime configuration |
| container | An instance of a container image |
| writable layer | Container-specific filesystem changes |
| volume | A Docker data store or an LVM storage object, as identified by context |
| registry | A service that stores and distributes container images |
| tag | A readable image reference that can change |
| digest | A content identifier calculated from a hash |
| loop device | A block device backed by a file |
| RAID array | A block device formed from multiple member devices |
| physical volume (PV) | A storage device prepared for LVM |
| volume group (VG) | A pool of LVM storage extents |
| logical volume (LV) | An LVM block device allocated from a VG |
| filesystem | The structure used to store and find files on storage |
| namespace | An isolated view of a class of Linux resources |
| listener | A socket that accepts incoming connections |
| loopback address | An address for the local network context |
| wildcard bind address | An address value that selects all local addresses in its address family |
| reverse proxy | A server that accepts requests and passes them to an upstream |
| upstream | An application or server to which a proxy sends requests |
| certificate | A signed document that binds an identity to a public key |
| unit | A systemd object that describes a service or another managed resource |
| journal | Structured log records stored by journald |
| log entry | One recorded event or request |
| metric | A measured value used to describe system or service state |
| WAF | A web application firewall that inspects HTTP transactions |
| anomaly score | A total from detection rules used for a policy decision |
| threshold | A value at which a configured decision applies |

## Computing verbs

| Verb | Technical action |
| --- | --- |
| authenticate | Check the identity claimed by a participant |
| bind | Assign a local address and port to a socket |
| execute | Carry out a computer command or instruction |
| verify | Check a digital signature or a specified computing constraint |
| run | Start or operate a program |
| compile | Convert source code into executable code |
| decrypt / encrypt | Convert between readable and protected data with a cryptographic key |
| format | Create a filesystem structure on a device |
| mount / unmount | Attach or detach a filesystem at a mount point |
| reload | Read and apply configuration without a full service stop |
| resolve | Obtain an address or another DNS record from a name |
| resize | Change the size of a storage object or filesystem |
| sign | Create a digital signature with a private key |
| synchronize | Make replicas consistent |
| validate | Check specified syntax, constraints, or identity rules |

Keep case-sensitive identifiers as written in commands and output.
Do not change names such as `proxy_pass`, `colorGroups`, or `Restart=on-failure` to match prose rules.
Official interface labels and code punctuation remain exact.
The Windows profile path contains Cyrillic characters. Keep that actual path unchanged.

## Python and mathematics terms

| Term | Meaning and permitted form |
| --- | --- |
| Python | Programming language used by the supplied lesson. Noun unless specified otherwise |
| CPython | Python implementation written mainly in C. Noun unless specified otherwise |
| Colab | Google service for hosted notebooks. Noun unless specified otherwise |
| Jupyter notebook | Document with executable code cells and text cells. Noun unless specified otherwise |
| IPython | Interactive Python environment with display and result caching. Noun unless specified otherwise |
| kernel | Process that executes notebook code and retains runtime state. Noun unless specified otherwise |
| code cell | Notebook section with executable code. Noun unless specified otherwise |
| text cell | Notebook section with formatted text. Noun unless specified otherwise |
| runtime | Environment and state used during program execution. Noun unless specified otherwise |
| object | Python data entity with a type, identity, and value. Noun unless specified otherwise |
| name binding | Association between a name and an object. Noun unless specified otherwise |
| assignment | Statement that associates a target with a value. Noun unless specified otherwise |
| reference | Association that permits access to an object. Noun unless specified otherwise |
| identity | Property that distinguishes one object from another. Noun unless specified otherwise |
| type | Classification that determines supported object operations. Noun unless specified otherwise |
| mutable | Adjective for an object that permits changes. Noun unless specified otherwise |
| immutable | Adjective for an object that prohibits changes to its own contents. Noun unless specified otherwise |
| garbage collection | Automatic management of unreachable objects. Noun unless specified otherwise |
| GIL | Global interpreter lock in standard CPython. Noun unless specified otherwise |
| free threading | Python execution without the global interpreter lock. Noun unless specified otherwise |
| integer | Number without a fractional part. Noun unless specified otherwise |
| floating-point number | Finite-precision numeric representation with an exponent. Noun unless specified otherwise |
| complex number | Number with real and imaginary parts. Noun unless specified otherwise |
| Boolean value | One of the logical values True and False. Noun unless specified otherwise |
| Unicode | Standard that assigns code points to characters. Noun unless specified otherwise |
| code point | Integer assigned to a character by a character standard. Noun unless specified otherwise |
| identifier | Name permitted by programming-language syntax. Noun unless specified otherwise |
| literal | Code notation that directly specifies a value. Noun unless specified otherwise |
| scientific notation | Numeric notation with a decimal exponent. Noun unless specified otherwise |
| binary | Adjective for base-two representation. Noun unless specified otherwise |
| octal | Adjective for base-eight representation. Noun unless specified otherwise |
| hexadecimal | Adjective for base-sixteen representation. Noun unless specified otherwise |
| string | Ordered sequence of text characters. Noun unless specified otherwise |
| raw string | String literal that preserves backslashes with specified syntax restrictions. Noun unless specified otherwise |
| f-string | String literal with embedded expressions. Noun unless specified otherwise |
| newline | Character that starts a new text line. Noun unless specified otherwise |
| backslash | Character used in escape sequences and specified syntax. Noun unless specified otherwise |
| list | Mutable ordered collection of item references. Noun unless specified otherwise |
| tuple | Ordered collection with fixed item references. Noun unless specified otherwise |
| dictionary | Mapping from unique hashable keys to values. Noun unless specified otherwise |
| mapping | Association between keys and values. Noun unless specified otherwise |
| hashable | Adjective for an object with a stable hash and compatible equality. Noun unless specified otherwise |
| set | Unordered collection of distinct hashable elements. Noun unless specified otherwise |
| built-in object | Object provided by the language environment. Noun unless specified otherwise |
| keyword | Word reserved by programming-language syntax. Noun unless specified otherwise |
| snake_case | Naming style with lowercase words separated by underscores. Noun unless specified otherwise |
| CapWords | Naming style with capitalized words for Python classes. Noun unless specified otherwise |
| camel case | Naming style that separates words with capital letters. Noun unless specified otherwise |
| function | Callable unit that performs an operation. Noun unless specified otherwise |
| class | Definition of an object type. Noun unless specified otherwise |
| expression | Code that produces a value. Noun unless specified otherwise |
| operand | Value on which an operator acts. Noun unless specified otherwise |
| operator | Syntax element that specifies an operation. Noun unless specified otherwise |
| floor division | Division that rounds the quotient downward. Noun unless specified otherwise |
| remainder | Value left after floor division and multiplication by the divisor. Noun unless specified otherwise |
| bitwise operation | Operation on the bits of integer values. Noun unless specified otherwise |
| exclusive OR | Operation whose output bit is one when the input bits differ. Noun unless specified otherwise |
| short-circuit evaluation | Evaluation that stops when an earlier operand determines the result. Noun unless specified otherwise |
| comparison chain | Sequence of comparisons with shared middle expressions. Noun unless specified otherwise |
| truth value | Logical interpretation of an object. Noun unless specified otherwise |
| conditional expression | Expression that selects one value from a condition. Noun unless specified otherwise |
| block | Group of statements with the same structural indentation. Noun unless specified otherwise |
| indentation | Leading whitespace that indicates code structure. Noun unless specified otherwise |
| control flow | Order in which a program executes instructions. Noun unless specified otherwise |
| parity | Classification of an integer as even or odd. Noun unless specified otherwise |
| disk | Set of points within a specified radius, including the boundary. Noun unless specified otherwise |
| radius | Distance from a center to a circle boundary. Noun unless specified otherwise |
| coordinate | Value that locates a point along an axis. Noun unless specified otherwise |
| squared distance | Sum of squared coordinate differences. Noun unless specified otherwise |
| rounding tolerance | Permitted difference for a numerical boundary check. Noun unless specified otherwise |

Python verb use: `bind` also means to associate a name with an object.
Python verb use: `display` means to present an object through an interactive output interface.

## Loop and function terms

| Term | Meaning and permitted form |
| --- | --- |
| loop | Repeated execution controlled by a condition or an iterable. Noun |
| iteration | One execution of a loop body. Noun |
| infinite loop | Loop that does not reach a terminating condition or exit. Noun |
| sentinel | Value that marks the end of an input sequence. Noun |
| accumulator | Variable that retains a running calculation result. Noun |
| counter | Variable that records successive counts. Noun |
| augmented assignment | Assignment that combines an operation with storage of its result. Noun |
| iterable | Object from which an iterator can be obtained. Noun |
| iterator | Object that supplies successive items and retains consumption state. Noun |
| range | Immutable sequence of integers specified by start, stop, and step. Noun |
| progression | Sequence whose values follow a specified rule. Noun |
| parameter | Named input in a function definition. Noun |
| argument | Value supplied in a function call. Noun |
| positional argument | Argument assigned according to its position. Noun |
| keyword argument | Argument supplied with a parameter name. Noun |
| keyword-only parameter | Parameter that must receive its argument by keyword. Noun |
| default value | Value used when a caller omits an optional argument. Noun |
| type annotation | Metadata that expresses an intended type. Noun |
| argument unpacking | Expansion of an iterable or mapping into call arguments. Noun |
| docstring | Initial string statement that documents a Python object. Noun |
| lambda | Expression that creates a function with one expression body. Noun |
| scope | Region in which a name binding is accessible. Noun |
| LEGB | Local, enclosing function, global, and built-in name lookup order. Noun |
| local name | Name bound within a function. Noun |
| global name | Name bound at module level. Noun |
| nested function | Function defined inside another function. Noun |
| recursion | Function execution that calls the same function again. Noun |
| module | Python unit with its own global namespace. Noun |
| percentage point | Unit for the arithmetic difference between percentages. Noun |
| timing command | Interactive command that measures execution duration. Noun |
| VIP | Customer classification that selects an additional example discount. Noun |
