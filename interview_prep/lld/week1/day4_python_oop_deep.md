# Week 1 - Day 4: Python OOP Deep Dive
# Dunder Methods, Properties, Class/Static Methods, ABC, and Pythonic Patterns

---

## Why Python-Specific OOP Matters in Interviews

Most OOP concepts are language-agnostic — classes, inheritance, polymorphism work
the same in Java, C++, and Python. But Python has its own special features that
make it uniquely powerful and expressive.

In an SDE-3 interview with Python, the interviewer expects you to write
**Pythonic code** — code that doesn't just work, but uses Python's strengths
the way an experienced Python developer would.

If you write Python like you're writing Java, that's a red flag.

Today we cover the Python-specific features that separate a good Python developer
from a great one.

---

## Part 1: Dunder Methods (Magic Methods)

### What Are Dunder Methods?

"Dunder" stands for **Double UNDERscore** — methods that start and end with `__`.

You've already seen one: `__init__`. But Python has dozens of these, and they are
the secret behind how Python's built-in operations actually work.

**The Key Insight:**
When you write `a + b` in Python, Python internally calls `a.__add__(b)`.
When you write `len(my_list)`, Python calls `my_list.__len__()`.
When you write `print(my_object)`, Python calls `my_object.__str__()`.

These dunder methods let you **hook into Python's built-in behavior** and make
your custom classes behave like native Python types.

Think of it like this: Python gives you a set of **hooks** — predefined slots
you can fill in. If you fill them in, your object behaves naturally with
Python's built-in operators and functions.

---

### `__str__` and `__repr__` — String Representation

**`__str__`**: What humans see when they print the object (user-friendly)
**`__repr__`**: What developers see for debugging (precise, technical)

**Real World Analogy:**
- `__str__` is like your **name on a business card**: "Alice Johnson, Software Engineer"
- `__repr__` is like your **passport number**: precise, unique, meant for identification

```python
class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    # For humans — what print() shows
    def __str__(self) -> str:
        return f"{self.name} — ₹{self.price:.2f}"

    # For developers — what the debugger/REPL shows
    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.price}, stock={self.stock})"


p = Product("Laptop", 75000.00, 10)

print(p)         # Laptop — ₹75000.00          (calls __str__)
print(repr(p))   # Product(name='Laptop', price=75000.0, stock=10)  (calls __repr__)

# In a list, Python uses __repr__
products = [Product("Phone", 20000, 5), Product("Tablet", 35000, 3)]
print(products)  # Uses __repr__ for each item
```

**Rule of thumb:** Always define `__repr__`. Define `__str__` when you want a
different human-friendly format. If only `__repr__` is defined, Python uses it
for both `str()` and `repr()`.

---

### `__len__` — Making Your Object Work With `len()`

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item: str):
        self.items.append(item)

    # Now len(cart) works naturally
    def __len__(self) -> int:
        return len(self.items)


cart = ShoppingCart()
cart.add_item("Laptop")
cart.add_item("Mouse")
cart.add_item("Keyboard")

print(len(cart))    # 3  — works just like len(list)!
if cart:            # Python calls __len__ for truthiness check too
    print("Cart is not empty")
```

Without `__len__`, calling `len(cart)` would throw a `TypeError`.
With it, your custom class behaves exactly like a built-in Python container.

---

### `__eq__`, `__lt__`, `__le__` — Comparison Operators

These dunder methods let your objects be compared using `==`, `<`, `<=`, `>`, `>=`.

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    # Makes == work
    def __eq__(self, other) -> bool:
        if not isinstance(other, Employee):
            return False
        return self.salary == other.salary

    # Makes < work
    def __lt__(self, other) -> bool:
        return self.salary < other.salary

    # Makes <= work
    def __le__(self, other) -> bool:
        return self.salary <= other.salary

    def __repr__(self):
        return f"Employee({self.name}, {self.salary})"


emp1 = Employee("Alice", 80000)
emp2 = Employee("Bob", 60000)
emp3 = Employee("Charlie", 80000)

print(emp1 == emp3)   # True  — same salary
print(emp1 == emp2)   # False — different salary
print(emp2 < emp1)    # True  — Bob earns less

# Now you can sort a list of employees naturally!
employees = [emp1, emp2, emp3]
employees.sort()   # Works because __lt__ is defined
print(employees)   # Sorted by salary ascending
```

---

### `__add__`, `__sub__`, `__mul__` — Arithmetic Operators

```python
class Vector:
    """Represents a mathematical vector (used in physics, ML, game dev)"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Makes v1 + v2 work
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    # Makes v1 - v2 work
    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    # Makes v1 * 3 work (scalar multiplication)
    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


v1 = Vector(2, 3)
v2 = Vector(1, 4)

print(v1 + v2)    # Vector(3, 7)
print(v1 - v2)    # Vector(1, -1)
print(v1 * 3)     # Vector(6, 9)
```

---

### `__contains__` — Makes `in` Operator Work

```python
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, name: str, quantity: int):
        self.products[name] = quantity

    # Makes "Laptop" in inventory work
    def __contains__(self, product_name: str) -> bool:
        return product_name in self.products


inventory = Inventory()
inventory.add_product("Laptop", 10)
inventory.add_product("Mouse", 50)

print("Laptop" in inventory)    # True   — calls __contains__
print("Keyboard" in inventory)  # False
```

---

### `__iter__` and `__next__` — Making Objects Iterable

This lets your custom object work in a `for` loop — just like a list or dictionary.

**Real World Analogy:**
A **book** is a collection of pages. You can iterate through a book page by page.
`__iter__` is opening the book. `__next__` is turning to the next page.

```python
class NumberRange:
    """A custom range that generates only EVEN numbers"""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start

    # Called when iteration begins — returns the iterator object (self here)
    def __iter__(self):
        self.current = self.start   # Reset to beginning
        return self

    # Called each time the for loop needs the next value
    def __next__(self) -> int:
        while self.current <= self.end:
            value = self.current
            self.current += 1
            if value % 2 == 0:    # Only yield even numbers
                return value
        raise StopIteration       # Tells Python: "we're done iterating"


# Now works in a for loop naturally!
even_range = NumberRange(1, 10)
for num in even_range:
    print(num)    # 2, 4, 6, 8, 10

# Also works with list comprehension, sum, max, etc.
print(list(even_range))   # [2, 4, 6, 8, 10]
print(sum(even_range))    # 30
```

---

### `__getitem__` and `__setitem__` — Makes Indexing Work

```python
class Matrix:
    """A 2D matrix that supports matrix[row][col] syntax"""

    def __init__(self, rows: int, cols: int):
        self.data = [[0] * cols for _ in range(rows)]

    # Makes matrix[0] work (returns a row)
    def __getitem__(self, index: int):
        return self.data[index]

    # Makes matrix[0] = [1, 2, 3] work
    def __setitem__(self, index: int, value):
        self.data[index] = value

    def __repr__(self):
        return "\n".join(str(row) for row in self.data)


m = Matrix(3, 3)
m[0] = [1, 2, 3]
m[1] = [4, 5, 6]
m[2] = [7, 8, 9]

print(m[1][2])   # 6  — natural indexing!
print(m)
# [1, 2, 3]
# [4, 5, 6]
# [7, 8, 9]
```

---

### `__enter__` and `__exit__` — Context Managers (`with` statement)

This is one of the most important patterns in Python backend development.

**Real World Analogy:**
Think of borrowing a book from a library. When you borrow it:
1. You check it out (setup — `__enter__`)
2. You read it (do your work)
3. You return it (cleanup — `__exit__`)

The library ensures the book is ALWAYS returned — even if you get sick in the middle.

In code, this means: **resources are always cleaned up**, even if an error occurs.

```python
class DatabaseConnection:
    def __init__(self, host: str):
        self.host = host
        self.connection = None

    # Called when entering the `with` block
    def __enter__(self):
        print(f"Connecting to database at {self.host}...")
        self.connection = f"connection_to_{self.host}"   # Simulated connection
        return self   # The `as` variable in `with ... as db` gets this value

    # Called when EXITING the `with` block — whether normally or due to an error
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing database connection to {self.host}...")
        self.connection = None
        # If exc_type is not None, an exception occurred
        if exc_type:
            print(f"An error occurred: {exc_val}")
        return False  # False = don't suppress exceptions


# Usage — connection is ALWAYS closed, even if query fails
with DatabaseConnection("localhost:5432") as db:
    print(f"Running query on {db.connection}")
    # Even if an error happens here, __exit__ will be called

# Output:
# Connecting to database at localhost:5432...
# Running query on connection_to_localhost:5432
# Closing database connection to localhost:5432...
```

This is how Python's `open()` for files works internally. The `with` statement
guarantees cleanup — no more forgetting to close files or database connections.

---

## Part 2: Properties — Controlled Attribute Access

### The Problem

In Day 1, we used `__balance` (private) with a `get_balance()` method.
This is fine, but Python has a more elegant, Pythonic way — **Properties**.

Properties let you access an attribute like a normal variable (`obj.balance`)
while secretly running a method behind the scenes to validate or compute it.

**Real World Analogy:**
A **thermostat display** shows you a simple temperature number.
But behind the display, it converts Fahrenheit to Celsius, checks sensor health,
and applies calibration. You see a simple number — the complexity is hidden.

### `@property` — The Getter

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius   # Single underscore = convention for "internal use"

    # @property makes this method behave like an attribute (no parentheses needed)
    @property
    def celsius(self) -> float:
        return self._celsius

    # Computed property — no stored value, calculated on the fly
    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9/5) + 32


temp = Temperature(100)
print(temp.celsius)      # 100    — looks like attribute access, but runs a method!
print(temp.fahrenheit)   # 212.0  — computed dynamically, not stored

# temp.celsius = 50    # ERROR — no setter defined yet, this is read-only
```

### `@property.setter` — The Setter With Validation

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        # Validation — runs automatically when you do temp.celsius = X
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        # When user sets fahrenheit, internally store as celsius
        self.celsius = (value - 32) * 5/9   # Uses celsius setter (with validation)


temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0

temp.celsius = 100       # Works — calls the setter
print(temp.fahrenheit)   # 212.0

temp.fahrenheit = 32     # Works — sets via fahrenheit setter, converts internally
print(temp.celsius)      # 0.0

temp.celsius = -300      # ValueError: Temperature -300°C is below absolute zero!
```

### Properties in a Real Backend Class

```python
class User:
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self._email = email
        self._age = age

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError(f"Invalid email: {value}")
        self._email = value.lower().strip()   # Normalize automatically

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not 0 < value < 150:
            raise ValueError(f"Age {value} is not realistic")
        self._age = value

    @property
    def is_adult(self) -> bool:
        return self._age >= 18   # Computed property — always fresh


user = User("Alice", "alice@example.com", 25)
print(user.email)      # alice@example.com
print(user.is_adult)   # True

user.email = "  ALICE@GMAIL.COM  "  # Normalized to "alice@gmail.com"
print(user.email)      # alice@gmail.com

user.age = 200         # ValueError: Age 200 is not realistic
```

---

## Part 3: Class Methods and Static Methods

Python has three types of methods. Understanding the difference is a common
interview question.

### Instance Methods — The Default

Normal methods. They receive `self` — the specific object instance.
They can access and modify the object's own data.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):         # Instance method — operates on THIS object
        self.count += 1
        return self.count
```

### Class Methods (`@classmethod`) — Operate on the Class Itself

Receive `cls` (the class) instead of `self` (the instance).
They can access and modify **class-level** data — data shared by ALL instances.

Most commonly used as **alternative constructors** — multiple ways to create objects.

**Real World Analogy:**
A factory has a standard way to build cars. But it also has special assembly lines —
"build from parts list", "build from order number", "build from specification file".
These are alternative ways to build the same product. `@classmethod` creates these
alternative constructors.

```python
class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    # Alternative constructor — create from string "2024-03-15"
    @classmethod
    def from_string(cls, date_string: str) -> "Date":
        year, month, day = map(int, date_string.split("-"))
        return cls(year, month, day)   # cls(...) is same as Date(...)

    # Alternative constructor — create today's date
    @classmethod
    def today(cls) -> "Date":
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

    def __repr__(self):
        return f"Date({self.year}-{self.month:02d}-{self.day:02d})"


# Standard way
d1 = Date(2024, 3, 15)

# Alternative constructors
d2 = Date.from_string("2024-03-15")
d3 = Date.today()

print(d1)   # Date(2024-03-15)
print(d2)   # Date(2024-03-15)
print(d3)   # Today's date
```

### Static Methods (`@staticmethod`) — Utility Functions

They receive neither `self` nor `cls`. They don't operate on the instance OR the class.
They are just **regular utility functions** that logically belong to the class
but don't need access to its data.

**Real World Analogy:**
A `MathUtils` class might have a static `is_prime(n)` method.
It doesn't need any object data — it's just a utility that belongs in that namespace.

```python
class PasswordValidator:
    MIN_LENGTH = 8

    def __init__(self, password: str):
        self.password = password

    # Instance method — uses self.password
    def is_valid(self) -> bool:
        return (
            self.has_min_length() and
            PasswordValidator.has_uppercase(self.password) and
            PasswordValidator.has_digit(self.password)
        )

    def has_min_length(self) -> bool:
        return len(self.password) >= self.MIN_LENGTH

    # Static method — pure utility, doesn't need self or cls
    @staticmethod
    def has_uppercase(password: str) -> bool:
        return any(c.isupper() for c in password)

    @staticmethod
    def has_digit(password: str) -> bool:
        return any(c.isdigit() for c in password)

    # Class method — uses cls to access class-level config
    @classmethod
    def set_min_length(cls, length: int):
        cls.MIN_LENGTH = length


validator = PasswordValidator("MyPass123")
print(validator.is_valid())   # True

# Static methods can also be called on the class directly
print(PasswordValidator.has_uppercase("Hello"))   # True
print(PasswordValidator.has_digit("Hello"))       # False
```

### When to Use Which

| Method Type | Use When... | Receives |
|-------------|-------------|---------|
| Instance method | You need object's data (`self.x`) | `self` |
| Class method | Alternative constructors or class-level data | `cls` |
| Static method | Pure utility with no object/class data needed | Nothing |

---

## Part 4: Abstract Base Classes (ABC) — Deep Dive

We touched on ABC in Day 1. Let's go deeper with practical patterns.

### Why ABC Over Regular Classes?

When you define an abstract class, Python **enforces the contract**.
You cannot accidentally create an instance of the abstract class,
and you cannot forget to implement a required method.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def speak(self) -> str:
        """Every animal MUST implement this"""
        pass

    @abstractmethod
    def move(self) -> str:
        """Every animal MUST implement this"""
        pass

    # Non-abstract — concrete method, shared by all animals
    def describe(self):
        print(f"I am {self.name}. I say '{self.speak()}' and I {self.move()}")


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

    def move(self) -> str:
        return "run on four legs"


class Snake(Animal):
    def speak(self) -> str:
        return "Hiss!"

    def move(self) -> str:
        return "slither"


# Animal()  — TypeError! Cannot instantiate abstract class
# If you forget to implement speak() or move() in a subclass — TypeError at instantiation

dog = Dog("Rex")
dog.describe()    # I am Rex. I say 'Woof!' and I run on four legs

snake = Snake("Sly")
snake.describe()  # I am Sly. I say 'Hiss!' and I slither
```

### ABC with Properties

Abstract properties force subclasses to provide computed attributes:

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self):
        print(f"{self.__class__.__name__}: area={self.area:.2f}, perimeter={self.perimeter:.2f}")


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    @property
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    shape.describe()

# Circle: area=78.54, perimeter=31.42
# Rectangle: area=24.00, perimeter=20.00
```

---

## Part 5: Dataclasses — Modern Python OOP

Python 3.7+ introduced `@dataclass` — a decorator that automatically generates
`__init__`, `__repr__`, `__eq__`, and more based on your field declarations.

**Real World Analogy:**
Imagine writing a standard form for every new employee — name, age, department.
Instead of writing the same paperwork structure every time, HR has a **template form**.
You just fill in the fields. `@dataclass` is that template.

```python
from dataclasses import dataclass, field
from typing import List

# WITHOUT dataclass — lots of boilerplate
class ProductOld:
    def __init__(self, name: str, price: float, tags: list):
        self.name = name
        self.price = price
        self.tags = tags

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, tags={self.tags})"

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


# WITH dataclass — clean and automatic
@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)  # Mutable default — use field()
    in_stock: bool = True                           # Default value

    # You can still add your own methods
    def apply_discount(self, percent: float):
        self.price = self.price * (1 - percent / 100)


p1 = Product("Laptop", 75000.0, ["electronics", "computers"])
p2 = Product("Laptop", 75000.0, ["electronics", "computers"])
p3 = Product("Mouse", 1500.0)

print(p1)          # Product(name='Laptop', price=75000.0, tags=['electronics', 'computers'], in_stock=True)
print(p1 == p2)    # True  — __eq__ auto-generated
print(p1 == p3)    # False

p1.apply_discount(10)
print(p1.price)    # 67500.0
```

### Frozen Dataclass — Immutable Objects

```python
@dataclass(frozen=True)   # Makes object immutable — like a tuple
class Coordinate:
    latitude: float
    longitude: float


loc = Coordinate(28.6139, 77.2090)   # New Delhi
print(loc)   # Coordinate(latitude=28.6139, longitude=77.209)

# loc.latitude = 0.0   # FrozenInstanceError — cannot modify!

# Since frozen=True, it's hashable — can be used as dict key or in sets!
location_cache = {loc: "New Delhi"}
print(location_cache[Coordinate(28.6139, 77.2090)])   # New Delhi
```

---

## Part 6: `__slots__` — Memory Optimization

By default, every Python object stores its attributes in a dictionary (`__dict__`).
This is flexible but uses more memory. For classes with many instances,
`__slots__` saves significant memory by pre-declaring attributes.

```python
# Normal class — uses __dict__ internally (flexible but heavier)
class PointNormal:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# With __slots__ — no __dict__, lower memory footprint
class PointSlotted:
    __slots__ = ['x', 'y']   # Declare all allowed attributes upfront

    def __init__(self, x, y):
        self.x = x
        self.y = y


import sys
p1 = PointNormal(1, 2)
p2 = PointSlotted(1, 2)

print(sys.getsizeof(p1))   # ~48 bytes + dict overhead (~232 bytes for __dict__)
print(sys.getsizeof(p2))   # ~56 bytes — no __dict__

# p2.z = 10   # AttributeError — only x and y are allowed (slots are strict)
```

Use `__slots__` when you will create **millions of instances** of a class
(e.g., processing large datasets, game objects, ML feature vectors).

---

## Complete Dunder Methods Reference

| Dunder Method | Triggered By | Use Case |
|---------------|-------------|---------|
| `__init__` | `MyClass()` | Object initialization |
| `__str__` | `print(obj)`, `str(obj)` | Human-readable string |
| `__repr__` | `repr(obj)`, REPL display | Developer debugging string |
| `__len__` | `len(obj)` | Container size |
| `__eq__` | `obj1 == obj2` | Equality comparison |
| `__lt__` | `obj1 < obj2` | Less-than comparison |
| `__add__` | `obj1 + obj2` | Addition operator |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj` | Start iteration |
| `__next__` | Next iteration step | Iteration value |
| `__getitem__` | `obj[key]` | Index/key access |
| `__setitem__` | `obj[key] = val` | Index/key assignment |
| `__enter__` | `with obj as x:` | Context manager setup |
| `__exit__` | End of `with` block | Context manager cleanup |
| `__call__` | `obj()` | Make object callable like a function |

---

## Interview Q&A for This Topic

**Q: What is the difference between `__str__` and `__repr__`?**

> "`__str__` is for end users — it returns a readable, friendly string suitable
> for display. `__repr__` is for developers — it returns an unambiguous string
> that ideally allows recreating the object. The convention for `__repr__` is
> `ClassName(field1=value1, field2=value2)`. If only one is defined, Python
> falls back to `__repr__` for both. Always define `__repr__` at minimum."

**Q: When would you use `@classmethod` vs `@staticmethod`?**

> "`@classmethod` is used when the method needs access to the class itself —
> most commonly to create alternative constructors like `Date.from_string()` or
> `User.from_json()`. `@staticmethod` is used for pure utility functions that
> logically belong to the class but don't need any class or instance data —
> like a `validate_email()` helper on a `User` class. If neither `cls` nor `self`
> is needed, use `@staticmethod`."

**Q: What are context managers and why are they important in backend code?**

> "Context managers (the `with` statement) guarantee that setup and cleanup code
> runs — even if an exception occurs. In backend code, this is critical for:
> database connections (always close after query), file handles (always close after read),
> locks and mutexes (always release after critical section), and transactions (always
> commit or rollback). Without context managers, a crashed request could leave
> database connections open, eventually exhausting the connection pool."

**Q: What is the benefit of `@dataclass`?**

> "Dataclasses eliminate boilerplate. For a class with 5 fields, writing `__init__`,
> `__repr__`, and `__eq__` by hand is 20+ lines of repetitive code. `@dataclass`
> generates all of this automatically from the type annotations. It's not just
> about saving keystrokes — it reduces human error in repetitive code. For immutable
> value objects like `Coordinate` or `Money`, `@dataclass(frozen=True)` also makes
> them hashable, which is necessary for using them as dictionary keys."

---

## Practice Exercise for Today

Build a **`PriorityQueue`** class using dunder methods:

Requirements:
1. Items are `Task` objects with `name: str` and `priority: int` (1=high, 10=low)
2. `Task` must support comparison (`<`, `==`) based on priority
3. `Task` must have proper `__str__` and `__repr__`
4. `PriorityQueue` must support:
   - `queue.add(task)` — add a task
   - `len(queue)` — number of tasks
   - `for task in queue:` — iterate in priority order (highest first)
   - `task in queue` — check if a task is in the queue
   - Use as a context manager with `with PriorityQueue() as q:` that prints a summary on exit

Bonus: Use `@dataclass` for the `Task` class.

---

*Next: Day 5 — Week 1 Revision + Practice Exercise Solutions + Interview Simulation*
