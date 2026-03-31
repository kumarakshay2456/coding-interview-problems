# Week 2 - Day 6: Creational Design Patterns
# Singleton, Factory Method, Abstract Factory, Builder

---

## What Are Design Patterns?

Imagine you are a new chef in a professional kitchen. You are asked to make
"Hollandaise sauce." Instead of figuring it out from scratch, you open a
**recipe book** — a known, tested, named solution that experienced chefs have
already proven works.

Design Patterns are the **recipe book of software engineering**.

They are named, reusable solutions to problems that come up again and again
in software design. They were formalized in 1994 by four authors (the "Gang of Four")
in a book called *"Design Patterns: Elements of Reusable Object-Oriented Software"*.

You don't invent these. You recognize the pattern in a problem and apply it.

### Three Categories of Patterns

| Category | Concern | Examples |
|----------|---------|---------|
| **Creational** | How objects are CREATED | Singleton, Factory, Builder |
| **Structural** | How objects are COMPOSED | Adapter, Decorator, Facade |
| **Behavioral** | How objects COMMUNICATE | Strategy, Observer, Command |

Today we cover **Creational Patterns** — controlling how and when objects are created.

---

## Pattern 1: Singleton

### The Problem It Solves

Some things in a system should exist **exactly once**. Having multiple instances
would cause bugs, inconsistency, or waste.

**Real World Analogy:**
A country has exactly **one government**. You don't create a second government
when the first one is busy. There is one, shared instance — and everyone
interacts with the same one.

Other real examples:
- A database connection pool — one pool, shared by all requests
- A logger — one logger for the whole app
- A configuration manager — one place that holds all settings
- A thread pool — one pool managing all worker threads

### The Problem Without Singleton

```python
class DatabasePool:
    def __init__(self):
        self.connections = []
        print("Creating new connection pool...")   # Expensive operation!
        # Imagine: creating 10 connections to the database
        for i in range(10):
            self.connections.append(f"connection_{i}")

# BAD — Every time someone needs the pool, a new one is created
# Each creation opens 10 new connections — expensive and wasteful

pool1 = DatabasePool()   # Creates 10 connections
pool2 = DatabasePool()   # Creates 10 MORE connections — wasteful!
pool3 = DatabasePool()   # Creates 10 MORE connections — broken design!

print(pool1 is pool2)    # False — these are different objects!
```

Three different parts of the code created three separate pools.
You now have 30 open connections. The app thinks it has 10 but actually has 30.
This causes connection leaks, performance issues, and inconsistency.

### The Singleton Solution

```python
class DatabasePool:
    _instance = None   # Class-level variable — shared by ALL instances

    def __new__(cls):
        """
        __new__ is called BEFORE __init__.
        It controls object CREATION (not initialization).

        If no instance exists yet — create one and store it.
        If an instance already exists — return the existing one.
        """
        if cls._instance is None:
            print("Creating database pool for the first time...")
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False   # Flag to prevent re-initialization
        return cls._instance

    def __init__(self):
        if self._initialized:
            return   # Don't reinitialize if already set up
        print("Initializing connection pool with 10 connections...")
        self.connections = [f"connection_{i}" for i in range(10)]
        self._initialized = True

    def get_connection(self):
        if self.connections:
            return self.connections.pop()
        raise Exception("No available connections!")

    def return_connection(self, conn):
        self.connections.append(conn)


# All three variables point to the SAME object
pool1 = DatabasePool()   # "Creating database pool for the first time..."
pool2 = DatabasePool()   # No output — returns existing instance
pool3 = DatabasePool()   # No output — returns existing instance

print(pool1 is pool2)    # True — same object!
print(pool2 is pool3)    # True — same object!

# All three operate on the same pool
conn = pool1.get_connection()
print(f"Got: {conn}")
print(f"Remaining connections in pool: {len(pool2.connections)}")  # 9 — same pool!
pool3.return_connection(conn)
print(f"After return: {len(pool1.connections)}")   # 10 again — all three see the same state
```

### Thread-Safe Singleton (For Production Code)

In a real multi-threaded backend, two threads might simultaneously find
`_instance is None` and BOTH create a new instance. We prevent this with a lock:

```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()   # Class-level lock

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:             # Only one thread enters this block at a time
                if cls._instance is None:    # Double-check after acquiring lock
                    cls._instance = super().__new__(cls)
        return cls._instance
```

The "double-check" is important: after a thread acquires the lock,
it checks again because another thread might have created the instance
between the first check and acquiring the lock.

### Singleton Using a Decorator (Pythonic Way)

```python
def singleton(cls):
    """A decorator that turns any class into a Singleton"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ConfigManager:
    def __init__(self):
        self.settings = {
            "debug": False,
            "db_url": "postgresql://localhost/myapp",
            "redis_url": "redis://localhost:6379"
        }

    def get(self, key: str):
        return self.settings.get(key)

    def set(self, key: str, value):
        self.settings[key] = value


config1 = ConfigManager()
config2 = ConfigManager()
print(config1 is config2)   # True

config1.set("debug", True)
print(config2.get("debug"))  # True — same instance!
```

### When to Use Singleton

Use it when:
- Exactly one shared resource should exist (DB pool, config, logger, cache)
- Creating multiple instances would break the system (inconsistent state)
- The resource is expensive to create (network connections, file handles)

**Warning:** Singleton is often overused. Don't use it just because something
"seems like it should be one." Use it only when having multiple truly breaks things.

---

## Pattern 2: Factory Method

### The Problem It Solves

Sometimes you need to create objects, but you don't know ahead of time
**which specific type** you'll need. The decision happens at runtime.

**Real World Analogy:**
A **vehicle rental company** has a booking system. When a customer books,
they specify what they want: car, motorcycle, or truck. The booking system
doesn't manually build each vehicle — it calls the **factory**:
*"Give me a vehicle of this type"* and the factory figures out the specifics.

The booking system doesn't need to know HOW a car or truck is assembled.
It just asks the factory.

### The Problem Without Factory

```python
class Notification:
    pass

class EmailNotification(Notification):
    def __init__(self, to_email: str, subject: str):
        self.to_email = to_email
        self.subject = subject
        print(f"Email ready: {subject} → {to_email}")

class SMSNotification(Notification):
    def __init__(self, to_phone: str, message: str):
        self.to_phone = to_phone
        self.message = message
        print(f"SMS ready: {message[:30]} → {to_phone}")

class PushNotification(Notification):
    def __init__(self, device_token: str, title: str):
        self.device_token = device_token
        self.title = title
        print(f"Push ready: {title} → {device_token}")


# BAD — The caller must know how to construct every type
# This code is repeated everywhere in the codebase
def send_notification(channel: str, user_data: dict):
    if channel == "email":
        notif = EmailNotification(user_data["email"], user_data["subject"])
    elif channel == "sms":
        notif = SMSNotification(user_data["phone"], user_data["message"])
    elif channel == "push":
        notif = PushNotification(user_data["token"], user_data["title"])
    else:
        raise ValueError(f"Unknown channel: {channel}")
    # ... send notif
```

This `if-elif` block will be copied everywhere. Adding a new channel (WhatsApp)
means finding EVERY copy and updating it. Violates OCP.

### Factory Method Solution

```python
from abc import ABC, abstractmethod


# ─── Product hierarchy ─────────────────────────────────────────────
class Notification(ABC):
    @abstractmethod
    def send(self) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class EmailNotification(Notification):
    def __init__(self, to_email: str, subject: str, body: str):
        self.to_email = to_email
        self.subject = subject
        self.body = body

    def send(self) -> bool:
        print(f"[EMAIL] To: {self.to_email} | Subject: {self.subject}")
        return True

    def __str__(self):
        return f"EmailNotification({self.to_email})"


class SMSNotification(Notification):
    def __init__(self, to_phone: str, message: str):
        self.to_phone = to_phone
        self.message = message

    def send(self) -> bool:
        print(f"[SMS] To: {self.to_phone} | Message: {self.message[:40]}")
        return True

    def __str__(self):
        return f"SMSNotification({self.to_phone})"


class PushNotification(Notification):
    def __init__(self, device_token: str, title: str, body: str):
        self.device_token = device_token
        self.title = title
        self.body = body

    def send(self) -> bool:
        print(f"[PUSH] Token: {self.device_token[:10]}... | Title: {self.title}")
        return True

    def __str__(self):
        return f"PushNotification({self.device_token[:8]}...)"


# ─── Factory ──────────────────────────────────────────────────────
class NotificationFactory:
    """
    The factory — centralizes all object creation logic.
    The rest of the code just calls create() and gets the right object back.
    """

    @staticmethod
    def create(channel: str, **kwargs) -> Notification:
        creators = {
            "email": lambda: EmailNotification(
                kwargs["email"], kwargs["subject"], kwargs.get("body", "")
            ),
            "sms": lambda: SMSNotification(
                kwargs["phone"], kwargs["message"]
            ),
            "push": lambda: PushNotification(
                kwargs["token"], kwargs["title"], kwargs.get("body", "")
            ),
        }

        if channel not in creators:
            raise ValueError(f"Unknown channel: '{channel}'. Valid: {list(creators.keys())}")

        return creators[channel]()


# ─── Usage ────────────────────────────────────────────────────────
# The caller just asks the factory — no if-elif chains anywhere
def send_notification(channel: str, **kwargs):
    notification = NotificationFactory.create(channel, **kwargs)
    return notification.send()


send_notification("email", email="alice@example.com", subject="Welcome!", body="Hello Alice")
send_notification("sms", phone="+919876543210", message="Your OTP is 123456")
send_notification("push", token="device_abc_123", title="New message", body="You have a message")

# Adding WhatsApp: just add it to the `creators` dict — ZERO changes to send_notification
```

---

## Pattern 3: Abstract Factory

### The Problem It Solves

Factory Method creates one type of object. **Abstract Factory** creates
**families of related objects** — where the objects must be compatible with each other.

**Real World Analogy:**
Think about furniture styles: **Modern** and **Victorian**.

- Modern furniture family: Modern Chair + Modern Table + Modern Sofa
- Victorian furniture family: Victorian Chair + Victorian Table + Victorian Sofa

You never want a Victorian Chair with a Modern Table — they clash.
An abstract factory ensures you get a **consistent family**.

### Python Example — UI Theme System

```python
from abc import ABC, abstractmethod


# ─── Abstract Products ────────────────────────────────────────────
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> str:
        pass


class TextInput(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def validate(self, text: str) -> bool:
        pass


# ─── Light Theme Family ───────────────────────────────────────────
class LightButton(Button):
    def render(self) -> str:
        return "[  Light Button  ]"    # White background, dark text

    def on_click(self) -> str:
        return "Light button clicked — subtle animation"


class LightTextInput(TextInput):
    def render(self) -> str:
        return "[ Light Input Field: white bg, gray border ]"

    def validate(self, text: str) -> bool:
        return len(text) > 0


# ─── Dark Theme Family ────────────────────────────────────────────
class DarkButton(Button):
    def render(self) -> str:
        return "[ Dark Button ]"       # Dark background, white text

    def on_click(self) -> str:
        return "Dark button clicked — glow animation"


class DarkTextInput(TextInput):
    def render(self) -> str:
        return "[ Dark Input Field: dark bg, white border ]"

    def validate(self, text: str) -> bool:
        return len(text.strip()) > 0   # Also strips whitespace


# ─── Abstract Factory ─────────────────────────────────────────────
class UIFactory(ABC):
    """Creates a family of compatible UI components"""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_text_input(self) -> TextInput:
        pass


class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_text_input(self) -> TextInput:
        return LightTextInput()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_text_input(self) -> TextInput:
        return DarkTextInput()


# ─── Application — uses the factory ──────────────────────────────
class LoginForm:
    """
    This class has NO IDEA whether it's using Light or Dark theme.
    It just uses the factory to create components — guaranteed compatible.
    """

    def __init__(self, factory: UIFactory):
        self.submit_button = factory.create_button()
        self.username_input = factory.create_text_input()
        self.password_input = factory.create_text_input()

    def render(self):
        print("=== Login Form ===")
        print(self.username_input.render())
        print(self.password_input.render())
        print(self.submit_button.render())

    def submit(self, username: str, password: str):
        if self.username_input.validate(username) and self.password_input.validate(password):
            print(self.submit_button.on_click())
            print(f"Logging in as: {username}")
        else:
            print("Validation failed!")


# Light theme — all components are Light family
user_preference = "dark"   # Could come from DB, cookie, or config

factory = DarkThemeFactory() if user_preference == "dark" else LightThemeFactory()
form = LoginForm(factory)
form.render()
form.submit("alice", "password123")
```

### Factory Method vs Abstract Factory

| | Factory Method | Abstract Factory |
|---|---|---|
| **Creates** | ONE type of object | A FAMILY of related objects |
| **Focus** | One product | Multiple related products |
| **Example** | `NotificationFactory.create("email")` | `UIFactory.create_button() + create_input()` |
| **Use when** | You need one kind of object, type decided at runtime | You need multiple objects that must work together |

---

## Pattern 4: Builder

### The Problem It Solves

Some objects are **complex to construct** — they have many optional parts,
required parts, and the order of assembly matters.

**Real World Analogy:**
Think about ordering a **custom burger at McDonald's**:
- Bun type (sesame / plain)
- Patty (beef / chicken / veggie)
- Cheese? (yes / no / double)
- Sauce? (ketchup / mayo / bbq / none)
- Extras? (lettuce, tomato, onion)

The cashier doesn't ask you to build the burger yourself — you specify
**what you want step by step**, and the kitchen builds it for you.

The Builder Pattern separates the **specification** (what you want) from
the **construction** (how it's assembled).

### The Problem Without Builder

```python
# BAD — Constructor with too many optional parameters
class QueryBuilder:
    def __init__(self, table, select=None, where=None, order_by=None,
                 limit=None, offset=None, join=None, group_by=None,
                 having=None, distinct=False):
        # 9 parameters — confusing, error-prone
        pass

# Which argument is which? Easy to mix up
query = QueryBuilder("users", ["id", "name"], "age > 18", "name ASC",
                     100, 0, None, None, None, True)
```

This is called **"telescoping constructor"** — it gets longer as features are added.

### Builder Solution

```python
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Query:
    """The final product — a built SQL query"""
    table: str
    select_columns: List[str]
    conditions: List[str]
    order_by: Optional[str]
    limit: Optional[int]
    offset: int
    joins: List[str]
    is_distinct: bool

    def to_sql(self) -> str:
        """Convert the query object to a SQL string"""
        distinct = "DISTINCT " if self.is_distinct else ""
        columns = ", ".join(self.select_columns) if self.select_columns else "*"
        sql = f"SELECT {distinct}{columns} FROM {self.table}"

        for join in self.joins:
            sql += f" {join}"

        if self.conditions:
            sql += f" WHERE {' AND '.join(self.conditions)}"

        if self.order_by:
            sql += f" ORDER BY {self.order_by}"

        if self.limit:
            sql += f" LIMIT {self.limit}"

        if self.offset:
            sql += f" OFFSET {self.offset}"

        return sql


class QueryBuilder:
    """
    The Builder — accumulates configuration step by step.
    Each method returns `self` so calls can be chained.
    """

    def __init__(self, table: str):
        self._table = table
        self._select = []
        self._conditions = []
        self._order_by = None
        self._limit = None
        self._offset = 0
        self._joins = []
        self._distinct = False

    def select(self, *columns: str) -> "QueryBuilder":
        self._select.extend(columns)
        return self   # Return self for method chaining

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        self._order_by = f"{column} {direction}"
        return self

    def limit(self, count: int) -> "QueryBuilder":
        self._limit = count
        return self

    def offset(self, count: int) -> "QueryBuilder":
        self._offset = count
        return self

    def join(self, table: str, on: str, join_type: str = "INNER") -> "QueryBuilder":
        self._joins.append(f"{join_type} JOIN {table} ON {on}")
        return self

    def distinct(self) -> "QueryBuilder":
        self._distinct = True
        return self

    def build(self) -> Query:
        """Final step — construct and return the Query object"""
        if not self._table:
            raise ValueError("Table name is required")
        return Query(
            table=self._table,
            select_columns=self._select,
            conditions=self._conditions,
            order_by=self._order_by,
            limit=self._limit,
            offset=self._offset,
            joins=self._joins,
            is_distinct=self._distinct
        )


# ─── Usage — clean, readable, self-documenting ────────────────────

# Simple query
q1 = (QueryBuilder("users")
      .select("id", "name", "email")
      .where("age > 18")
      .order_by("name")
      .limit(10)
      .build())

print(q1.to_sql())
# SELECT id, name, email FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10


# Complex query with join
q2 = (QueryBuilder("orders")
      .select("orders.id", "users.name", "orders.total")
      .join("users", "orders.user_id = users.id")
      .where("orders.total > 1000")
      .where("orders.status = 'completed'")
      .order_by("orders.total", "DESC")
      .limit(50)
      .offset(100)
      .build())

print(q2.to_sql())
# SELECT orders.id, users.name, orders.total FROM orders
# INNER JOIN users ON orders.user_id = users.id
# WHERE orders.total > 1000 AND orders.status = 'completed'
# ORDER BY orders.total DESC LIMIT 50 OFFSET 100


# Distinct query
q3 = (QueryBuilder("products")
      .select("category")
      .distinct()
      .order_by("category")
      .build())

print(q3.to_sql())
# SELECT DISTINCT category FROM products ORDER BY category ASC
```

### Real-World Builder Example — HTTP Request Builder

```python
class HTTPRequest:
    def __init__(self, method, url, headers, body, timeout, retries):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.retries = retries

    def __repr__(self):
        return f"{self.method} {self.url} (timeout={self.timeout}s, retries={self.retries})"


class HTTPRequestBuilder:
    def __init__(self):
        self._method = "GET"
        self._url = ""
        self._headers = {}
        self._body = None
        self._timeout = 30
        self._retries = 3

    def method(self, method: str) -> "HTTPRequestBuilder":
        self._method = method.upper()
        return self

    def url(self, url: str) -> "HTTPRequestBuilder":
        self._url = url
        return self

    def header(self, key: str, value: str) -> "HTTPRequestBuilder":
        self._headers[key] = value
        return self

    def bearer_token(self, token: str) -> "HTTPRequestBuilder":
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def json_body(self, data: dict) -> "HTTPRequestBuilder":
        import json
        self._body = json.dumps(data)
        self._headers["Content-Type"] = "application/json"
        return self

    def timeout(self, seconds: int) -> "HTTPRequestBuilder":
        self._timeout = seconds
        return self

    def retries(self, count: int) -> "HTTPRequestBuilder":
        self._retries = count
        return self

    def build(self) -> HTTPRequest:
        if not self._url:
            raise ValueError("URL is required")
        return HTTPRequest(
            self._method, self._url, self._headers,
            self._body, self._timeout, self._retries
        )


request = (HTTPRequestBuilder()
           .method("POST")
           .url("https://api.example.com/orders")
           .bearer_token("eyJhbGciOiJIUzI1NiJ9...")
           .header("X-Request-ID", "abc123")
           .json_body({"product_id": "P001", "quantity": 2})
           .timeout(10)
           .retries(2)
           .build())

print(request)
```

---

## Creational Patterns — Summary

| Pattern | Problem Solved | Key Signal to Use It |
|---------|---------------|---------------------|
| **Singleton** | Exactly one instance needed globally | Config, Logger, DB Pool, Cache |
| **Factory Method** | Object type decided at runtime | `if type == "X": create X` chains |
| **Abstract Factory** | Families of related objects must be compatible | Themes, cross-platform UI, test vs prod environments |
| **Builder** | Complex construction with many optional steps | > 4 constructor parameters, esp. optional ones |

---

## Interview Q&A

**Q: When would you choose Factory over Abstract Factory?**

> "Factory Method when I need to create one type of object dynamically —
> like creating the right notification type at runtime. Abstract Factory when
> I need to create a family of related objects that must work together —
> like creating a complete database environment (real connection, real transaction,
> real repository) vs a test environment (in-memory connection, mock transaction,
> fake repository). The key question is: do you need ONE product or a FAMILY of products?"

**Q: Isn't Singleton just a global variable? Why use it?**

> "Singleton is more than a global variable. A global variable is just data accessible
> everywhere — it has no lifecycle control, no lazy initialization, and no thread safety.
> Singleton controls WHEN the instance is created (lazy — only when first needed),
> GUARANTEES exactly one exists, and can be made thread-safe with locking.
> That said, Singleton has a downside: it makes code harder to test because
> you can't easily swap it out. That's why modern Python code often combines
> Singleton with Dependency Injection — the Singleton creates one instance,
> but it's injected rather than accessed globally."

**Q: What is method chaining in Builder and why is it useful?**

> "Method chaining (also called a Fluent Interface) returns `self` from each builder
> method, allowing calls to be chained like `builder.select().where().limit().build()`.
> It reads almost like English — you can see at a glance what the query does.
> Without chaining, you'd write each method on a separate line with the variable
> repeated: `b.select(); b.where(); b.limit(); query = b.build()` — less readable.
> Python's `QueryBuilder`, SQLAlchemy's query API, and Django's ORM all use this pattern."

---

## Practice Exercise for Today

Build an **HTTP Response Builder** for a REST API framework.

Requirements:
1. `HTTPResponse` should have: `status_code`, `body`, `headers`, `content_type`
2. `HTTPResponseBuilder` must support chaining:
   - `.status(200)` — set status code
   - `.json(data: dict)` — set JSON body + content-type header
   - `.html(content: str)` — set HTML body + content-type header
   - `.header(key, value)` — add any header
   - `.cookie(name, value, expires=None)` — add a Set-Cookie header
   - `.build()` — return the final `HTTPResponse`
3. Common factory methods:
   - `HTTPResponse.ok(data)` — 200 with JSON
   - `HTTPResponse.created(data)` — 201 with JSON
   - `HTTPResponse.not_found(message)` — 404 with error JSON
   - `HTTPResponse.server_error()` — 500 with error JSON

---

*Next: Day 7 — Structural Patterns (Adapter, Decorator, Facade)*
