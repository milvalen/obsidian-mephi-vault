---
title: "Lesson 4: object-oriented programming"
type: lecture
program: applied-data-analysis
course: Python
status: draft
created: 2026-11-08
updated: 2026-11-08
---
# Lesson 4: object-oriented programming

[Python](python.md) · [Lesson 3](lesson-03-strings-and-collections.md)

## Context and evidence

The owner supplied the Lesson 4 notebook on 2026-11-08.
The author, lecture date, and original notebook URL are unknown.
Notebook metadata reports Python 3.13.12. Metadata does not verify the active runtime.
One stored output shows the date 2026-10-23. This date does not confirm the lecture date.
The notebook has no practice tasks or recall questions.
The agent checked the additions below with local Python 3.9.6 on 2026-11-08.
The vault does not retain the notebook, original text, or images.

Main reference: [classes, Python tutorial](https://docs.python.org/3/tutorial/classes.html).

## Basic concepts

Object-oriented programming (OOP) puts data and behavior together in objects.
The source gives these purposes: clear code, easier maintenance and extension, and code reuse.

| Term | Meaning | Example |
| --- | --- | --- |
| Class | Definition of the data and behavior of its instances | `User` |
| Instance | One object made from a class | `User("Vasya", 10)` |
| Attribute | Any name that an object has: data or a method | `user.name` |
| Instance variable | Data of one instance | `self.name = name` |
| Class variable | Data that all instances share | `prop = 333` in the class body |
| Method | Function in a class | `def info(self):` |
| `self` | Reference to the current instance | `self.name` |
| Constructor | `__init__`. Python calls it when it makes an instance | `def __init__(self, name):` |

A class is also an object. `type(MyTestCl)` and `type(list)` give `type`.
`dir(obj)` gives the attributes of an object. Built-in types such as `dict` are classes too.

```python
class User:
    def __init__(self, name, rating=0):
        self.name = name
        self.rating = rating

    def info_str(self):
        return f"User {self.name}, rating {self.rating}"
```

`obj.method()` passes `obj` to `self`.
A method without `return` gives `None`. Thus `print(somebody.info())` prints the text and then `None`.

Objects can refer to other objects. In the source, a `Message` keeps a reference to a `Contact` in `self.sender`.

## Class variables and instance variables

Agent check: an assignment through an instance makes an instance variable. It does not change the class variable.

```python
class D:
    n = 0

d1, d2 = D(), D()
d1.n = 5
assert (d1.n, d2.n, D.n) == (5, 0, 0)
```

Agent check: a list in a class variable is shared. `c1.items.append(1)` also changes `c2.items`.
Make such lists in `__init__`.

## Encapsulation

Encapsulation puts data and methods in one object and controls access to them.
The object then shows only the necessary interface and hides its implementation details.

| Form | Meaning | Limit |
| --- | --- | --- |
| `attr` | Public attribute | |
| `_attr` | Protected by convention | Python does not prevent access |
| `__attr` | Private through name mangling | Python changes the name to `_ClassName__attr` |
| `get_x`, `set_x` | Methods that control access | |
| `__slots__` | Fixed list of permitted attributes | See below |

Agent checks:

- Name mangling does not give full protection. `a._My__p` reads the private value.
- Outside the class, `a.__p = 99` makes a new attribute. The private value does not change.
- `__slots__` stops new attributes on instances of that class. A subclass without `__slots__` can add them again.

The source says that direct changes to fields are bad, and it uses `get_` and `set_` methods.
Agent addition: Python code often uses public attributes. Add a [`property`](https://docs.python.org/3/library/functions.html#property) when access needs a check.
The calling code does not change.

```python
class Player:
    def __init__(self, rating=0):
        self.rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value < 0:
            raise ValueError("rating must not be negative")
        self._rating = value
```

## Polymorphism

Polymorphism lets objects of different classes operate differently on the same method call.
A function that calls `animal.speak()` then operates on each class with that method.
New classes need no change to this function. The source connects this with the open/closed principle.

In the `Dog` and `Cat` example, the classes have no common parent.
This form is duck typing: the method is necessary, not the class.

## Exceptions

The source shows `try` and `except` in this part.
Without them, `1 / 0` stops the cell with `ZeroDivisionError`.

```python
try:
    print(1 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
```

## Inheritance

A subclass gets the attributes of its superclass. It can add attributes and override methods.
`super()` calls the superclass method. Python permits multiple inheritance.

```python
class Worker:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Junior(Worker):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.salary = 1000
```

`Shape.area` raises `NotImplementedError`, and each subclass overrides it.
A subclass without `area` causes the error only when you call `area`.
Agent addition: an [abstract base class](https://docs.python.org/3/library/abc.html) gives `TypeError` when you make the instance.

## Source corrections

| Source example | Correction or limit |
| --- | --- |
| `prop = 333` has the comment "property of the object" | It is a class variable, shared by all instances |
| `get_name` prints the name | A getter usually returns the value. `print` gives the caller `None` |
| The union annotation in `animal_sound` | It needs Python 3.10 or later. On 3.9.6 it causes `TypeError`. Annotations do not check types at execution |
| `except:` with no exception type | It also catches `KeyboardInterrupt`. Specify the exception type |
| `Contact` phone number as an integer | An integer loses leading zeros and `+`. Use a string |
| `3.14` in `Circle.area` | Use `math.pi` |
| `if type(worker) == Middle` in the salary total | This does not operate on a subclass of `Middle`. It also does not use polymorphism. Use a `total_pay()` method in each class |
| `Junior` and `Middle` both set `salary = 1000` | Move the shared value to `Worker` |

The source pattern `time or datetime.now()` gets the time at each call.
A default parameter `time=datetime.now()` gets the time once, when Python executes the definition.

## Recall questions

1. What is the difference between a class and an instance?
2. What does `self` refer to?
3. When does Python call `__init__`?
4. What is the difference between a class variable and an instance variable?
5. Why can a list in a class variable cause an error?
6. What does `__attr` do, and how can code outside the class still read it?
7. What does `__slots__` prevent?
8. What is duck typing?
9. What does `super()` do?
10. Why is `type(x) == Middle` worse than a method in each class?

Open questions: official course title, lecture date, and required runtime.
