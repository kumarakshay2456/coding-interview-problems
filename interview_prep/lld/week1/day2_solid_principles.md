# Week 1 - Day 2: SOLID Principles
# The 5 Rules Every Good OOP Developer Must Follow

---

## What is SOLID and Why Should You Care?

Imagine you join a new company and inherit a codebase written by someone who left.
You need to add one small feature — but every time you change one file, three other
things break. You fix those, two more break. It feels like pulling a thread from a
sweater and the whole thing unravels.

This happens because the code was written **without principles**. It grew organically,
without structure, and became what developers call **"spaghetti code"** — tangled,
fragile, and impossible to change safely.

**SOLID** is a set of **5 principles** introduced by Robert C. Martin (Uncle Bob)
that, when followed, produce code that is:
- Easy to understand
- Easy to change
- Easy to extend (add new features)
- Hard to accidentally break

SOLID is an acronym:
- **S** — Single Responsibility Principle
- **O** — Open/Closed Principle
- **L** — Liskov Substitution Principle
- **I** — Interface Segregation Principle
- **D** — Dependency Inversion Principle

Let's go through each one deeply.

---

## S — Single Responsibility Principle (SRP)

### The Rule
> **"A class should have only ONE reason to change."**

In plain English: *Each class should do ONE thing and do it well.*

### Real World Analogy

Think about a **restaurant**. The restaurant has:
- A **Chef** — cooks food
- A **Waiter** — takes orders and serves food
- A **Cashier** — handles billing and payments
- A **Manager** — manages the staff

Now imagine if the **Chef** also took orders, handled billing, managed staff,
AND cooked food. If the billing system changes, the Chef's job description changes.
If the menu changes, the billing system is affected. Everything is tangled.

That's bad design. In a well-run restaurant, **each person has one responsibility**.
If billing changes, only the Cashier is affected. If the menu changes, only the Chef
needs to update. Everything else stays the same.

### Code Example — Violation of SRP

```python
# BAD — This class is doing TOO MANY things
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_user_info(self):
        return f"Name: {self.name}, Email: {self.email}"

    # PROBLEM 1: Why is a User class saving to a database?
    def save_to_database(self):
        print(f"Saving {self.name} to database...")
        # database logic here

    # PROBLEM 2: Why is a User class sending emails?
    def send_welcome_email(self):
        print(f"Sending welcome email to {self.email}...")
        # email logic here

    # PROBLEM 3: Why is a User class generating reports?
    def generate_report(self):
        print(f"Generating report for {self.name}...")
        # report logic here
```

This `User` class has **4 reasons to change**:
1. If user info format changes
2. If the database changes (MySQL → PostgreSQL)
3. If the email provider changes (Gmail → SendGrid)
4. If the report format changes (PDF → Excel)

Every time ANY of these change, you touch the `User` class — and risk breaking the others.

### Code Example — Following SRP

```python
# GOOD — Each class has ONE responsibility

# Responsibility 1: Hold user data
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_user_info(self):
        return f"Name: {self.name}, Email: {self.email}"


# Responsibility 2: Handle database operations
class UserRepository:
    def save(self, user: User):
        print(f"Saving {user.name} to database...")

    def find_by_email(self, email: str):
        print(f"Finding user with email {email}...")


# Responsibility 3: Handle email sending
class EmailService:
    def send_welcome_email(self, user: User):
        print(f"Sending welcome email to {user.email}...")


# Responsibility 4: Handle report generation
class UserReportGenerator:
    def generate(self, user: User):
        print(f"Generating report for {user.name}...")


# Usage — everything is clean and separated
user = User("Alice", "alice@example.com")
repo = UserRepository()
email_service = EmailService()
report = UserReportGenerator()

repo.save(user)                    # Database concern
email_service.send_welcome_email(user)  # Email concern
report.generate(user)              # Report concern
```

Now each class has exactly **ONE reason to change**:
- Database changes? Only touch `UserRepository`
- Email provider changes? Only touch `EmailService`
- Report format changes? Only touch `UserReportGenerator`
- User data structure changes? Only touch `User`

Nothing else is affected.

### Why This Matters in an Interview

> "SRP keeps classes focused and small. In our payment service, we separated
> `PaymentProcessor` (business logic), `PaymentRepository` (database),
> and `PaymentNotifier` (email/SMS). When we switched from Stripe to Razorpay,
> we only changed `PaymentProcessor` — the database and notification code
> didn't need to be touched at all."

---

## O — Open/Closed Principle (OCP)

### The Rule
> **"A class should be OPEN for extension but CLOSED for modification."**

In plain English: *You should be able to ADD new behavior without CHANGING existing code.*

### Real World Analogy

Think about a **smartphone**. The phone comes with a basic camera app.
Now the manufacturer wants to add a night mode feature.

**Bad approach**: Open the camera app's core code, dig around, add night mode logic
in the middle of existing code, and risk breaking the existing day mode.

**Good approach**: The camera app was designed with a **plugin/extension system**.
Night mode is a new plugin that slots in — the original camera code is never touched.

This is the Open/Closed Principle.

### The Problem — Violating OCP

```python
# BAD — Every time we add a new shape, we modify existing code
class AreaCalculator:
    def calculate_area(self, shape):
        if shape["type"] == "circle":
            return 3.14 * shape["radius"] ** 2

        elif shape["type"] == "rectangle":
            return shape["width"] * shape["height"]

        # What if we need a Triangle? We ADD CODE HERE — modifying existing code
        elif shape["type"] == "triangle":
            return 0.5 * shape["base"] * shape["height"]

        # What if we need a Pentagon? We ADD MORE CODE HERE again...
        # This class keeps growing and is constantly being modified
        # Every change risks breaking existing shapes
```

This `AreaCalculator` must be **modified** every time a new shape is added.
This violates OCP. The class is NOT closed for modification.

### The Solution — Following OCP

```python
from abc import ABC, abstractmethod

# Abstract base — the CONTRACT that all shapes must follow
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


# Existing shapes — these are NEVER touched again
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


# Calculator — also NEVER touched again
class AreaCalculator:
    def calculate(self, shape: Shape) -> float:
        return shape.area()   # It doesn't care WHAT shape it is — just calls .area()


# EXTENDING — adding a new shape WITHOUT touching any existing code
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


class Pentagon(Shape):
    def __init__(self, side):
        self.side = side

    def area(self) -> float:
        return (5 * self.side ** 2) / (4 * (5 ** 0.5) / 5)  # pentagon formula


# Everything works — zero modification to existing classes
calculator = AreaCalculator()
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8), Pentagon(4)]

for shape in shapes:
    print(f"{shape.__class__.__name__} area: {calculator.calculate(shape)}")
```

We added `Triangle` and `Pentagon` WITHOUT touching `Circle`, `Rectangle`, or
`AreaCalculator`. The existing code is **closed** for modification.
New shapes are added by **extension** — creating new classes.

### Why This Matters in an Interview

> "OCP is critical in payment systems. We have a `PaymentProcessor` that works
> with an abstract `PaymentMethod`. When we added UPI payments, we just created
> a new `UPIPayment` class implementing the interface — zero changes to existing
> credit card or net banking code. The system extended naturally."

---

## L — Liskov Substitution Principle (LSP)

### The Rule
> **"Objects of a subclass should be replaceable with objects of the parent class
> without breaking the program."**

In plain English: *If Class B inherits from Class A, then wherever you use A,
you should be able to use B — and everything should still work correctly.*

### Real World Analogy

Imagine you have a **driver's license** — it says you can drive any car.

Now imagine you buy a "car" called XYZ — but it doesn't have a steering wheel,
uses a joystick instead, and the brakes are on the roof. You have a driver's license
(parent contract), but this "car" (child) behaves so differently that your license
is useless here.

That's an LSP violation. A subclass must **fully honor** the contract of its parent.
It should behave in a way that doesn't surprise the user.

### The Classic Example — Violation of LSP

```python
# The famous Square-Rectangle problem

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    # A square MUST have equal sides — so we override both setters
    def set_width(self, width):
        self.width = width
        self.height = width    # Force height = width

    def set_height(self, height):
        self.height = height
        self.width = height    # Force width = height


# This function works perfectly for Rectangle
def print_area(rectangle: Rectangle):
    rectangle.set_width(5)
    rectangle.set_height(10)
    # Expected area: 5 * 10 = 50
    print(f"Area: {rectangle.area()}")


r = Rectangle(2, 3)
print_area(r)     # Area: 50 — CORRECT

s = Square(2)
print_area(s)     # Area: 100 — WRONG! (10 * 10 because set_height also changed width)
```

`Square` is a subclass of `Rectangle`, but **substituting** a `Square` where a
`Rectangle` is expected **breaks the program**. This violates LSP.

The fix: don't force Square to inherit from Rectangle. Instead, both can inherit
from a common abstract `Shape`.

### A Backend Example — Violation of LSP

```python
# BAD — Child breaks the parent's contract
class Bird:
    def fly(self):
        print("Flying high!")


class Parrot(Bird):
    def fly(self):
        print("Parrot is flying!")   # Works fine


class Ostrich(Bird):
    def fly(self):
        raise Exception("Ostriches cannot fly!")  # BREAKS the contract!


# This code works for Bird and Parrot — but crashes for Ostrich
def make_bird_fly(bird: Bird):
    bird.fly()

make_bird_fly(Parrot())   # Works
make_bird_fly(Ostrich())  # CRASH — LSP violated
```

### The Fix — Restructure the Hierarchy

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def eat(self):
        pass


class FlyingBird(Bird):
    @abstractmethod
    def fly(self):
        pass


class WalkingBird(Bird):
    @abstractmethod
    def walk(self):
        pass


class Parrot(FlyingBird):
    def eat(self):
        print("Parrot is eating seeds.")

    def fly(self):
        print("Parrot is flying!")


class Ostrich(WalkingBird):
    def eat(self):
        print("Ostrich is eating grass.")

    def walk(self):
        print("Ostrich is running fast!")


# Now substitution is safe — no surprises
def make_flying_bird_fly(bird: FlyingBird):
    bird.fly()

make_flying_bird_fly(Parrot())   # Works perfectly
# make_flying_bird_fly(Ostrich()) # Type error at design time — caught early!
```

Now the hierarchy is honest. `Ostrich` never pretends it can fly.

### Why This Matters in an Interview

> "LSP prevents unexpected behavior in polymorphism. In our file storage service,
> we have a base `StorageBackend` with a `read()` method. S3, GCS, and local disk
> all extend it. LSP ensures that anywhere we use `StorageBackend`, any of the
> three implementations can be swapped in without breaking anything — no surprises."

---

## I — Interface Segregation Principle (ISP)

### The Rule
> **"A class should not be forced to implement methods it does not need."**

In plain English: *Don't create one giant interface. Create small, specific ones.
Classes should only implement what is relevant to them.*

### Real World Analogy

Imagine your job description says:
*"Software Engineer — must code, design UI, write marketing copy, do accounting,
cook team lunches, and fix office plumbing."*

That's absurd. You're a software engineer — why are you responsible for plumbing?

Now imagine there are separate job descriptions:
- Software Engineer: codes, reviews, documents
- UI Designer: designs, prototypes
- Accountant: manages books, taxes

Each role has only what's relevant. Nobody is forced to do irrelevant things.

That's ISP — **don't force classes to implement methods they don't use.**

### Code Example — Violation of ISP

```python
from abc import ABC, abstractmethod

# BAD — One fat interface that forces ALL machines to implement ALL methods
class Machine(ABC):

    @abstractmethod
    def print_document(self):
        pass

    @abstractmethod
    def scan_document(self):
        pass

    @abstractmethod
    def send_fax(self):
        pass

    @abstractmethod
    def staple_document(self):
        pass


# A modern all-in-one printer — fine, it can do everything
class AllInOnePrinter(Machine):
    def print_document(self):
        print("Printing...")

    def scan_document(self):
        print("Scanning...")

    def send_fax(self):
        print("Sending fax...")

    def staple_document(self):
        print("Stapling...")


# A simple, cheap printer — it can ONLY print!
# But it's FORCED to implement scan, fax, and staple anyway
class SimplePrinter(Machine):
    def print_document(self):
        print("Printing...")

    def scan_document(self):
        raise NotImplementedError("Simple printer cannot scan!")  # Forced, useless

    def send_fax(self):
        raise NotImplementedError("Simple printer cannot fax!")   # Forced, useless

    def staple_document(self):
        raise NotImplementedError("Simple printer cannot staple!")  # Forced, useless
```

`SimplePrinter` is polluted with methods it can never use.
This is an ISP violation.

### The Solution — Following ISP

```python
from abc import ABC, abstractmethod

# Small, focused interfaces — each doing ONE thing
class Printable(ABC):
    @abstractmethod
    def print_document(self):
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_document(self):
        pass


class Faxable(ABC):
    @abstractmethod
    def send_fax(self):
        pass


class Stapleable(ABC):
    @abstractmethod
    def staple_document(self):
        pass


# All-in-one printer implements ALL interfaces — it can do everything
class AllInOnePrinter(Printable, Scannable, Faxable, Stapleable):
    def print_document(self):
        print("Printing...")

    def scan_document(self):
        print("Scanning...")

    def send_fax(self):
        print("Sending fax...")

    def staple_document(self):
        print("Stapling...")


# Simple printer only implements what it CAN DO
class SimplePrinter(Printable):
    def print_document(self):
        print("Printing...")


# Scanner only implements what it CAN DO
class DocumentScanner(Scannable):
    def scan_document(self):
        print("Scanning...")


# No surprises, no useless NotImplementedError, no forced methods
simple = SimplePrinter()
simple.print_document()   # Works perfectly — clean and honest
```

Now each class only carries the weight of what it can actually do.

### Why This Matters in an Interview

> "ISP keeps interfaces lean. In our notification system, we have separate
> interfaces: `EmailSender`, `SMSSender`, and `PushSender`. An `EmailOnlyService`
> only implements `EmailSender` — it's not forced to have stub SMS or push methods
> that throw `NotImplementedError`. This makes the system clear about capabilities."

---

## D — Dependency Inversion Principle (DIP)

### The Rule
> **"High-level modules should not depend on low-level modules.
> Both should depend on abstractions (interfaces)."**

In plain English: *Your main business logic should not be tightly tied to
specific tools, databases, or services. It should talk to an abstract layer —
so you can swap out the actual tools without changing your business logic.*

### Real World Analogy

Think about a **power socket** in your wall.

The socket doesn't care if you plug in a phone charger, a laptop, a fan, or a lamp.
The socket exposes a **standard interface** (two/three holes, specific voltage).
Any device that matches that interface can use it.

Now imagine if the socket was hardwired directly to your phone's charging circuit.
When you upgrade your phone, you'd have to **rewire the entire wall**.

The socket (high-level infrastructure) depends on the **standard interface**,
not on the specific device (low-level implementation). This is DIP.

### Code Example — Violation of DIP

```python
# BAD — High-level class directly depends on low-level class

class MySQLDatabase:   # Low-level module — a specific tool
    def save(self, data):
        print(f"Saving '{data}' to MySQL database")

    def fetch(self, query):
        print(f"Fetching from MySQL: {query}")
        return "MySQL result"


class UserService:   # High-level module — business logic
    def __init__(self):
        # PROBLEM: UserService is HARDWIRED to MySQLDatabase
        # If we want to switch to MongoDB or PostgreSQL, we must CHANGE UserService
        self.database = MySQLDatabase()

    def create_user(self, name):
        self.database.save(name)

    def get_user(self, user_id):
        return self.database.fetch(user_id)
```

`UserService` (business logic) directly creates and uses `MySQLDatabase`.
If we want to switch to PostgreSQL, or use an in-memory DB for testing,
we have to **modify** `UserService` — violating both OCP and DIP.

### The Solution — Following DIP

```python
from abc import ABC, abstractmethod

# Step 1: Create an ABSTRACTION (the standard socket interface)
class DatabaseInterface(ABC):
    @abstractmethod
    def save(self, data: str):
        pass

    @abstractmethod
    def fetch(self, query: str) -> str:
        pass


# Step 2: Low-level modules implement the abstraction
class MySQLDatabase(DatabaseInterface):
    def save(self, data: str):
        print(f"Saving '{data}' to MySQL database")

    def fetch(self, query: str) -> str:
        print(f"Fetching from MySQL: {query}")
        return "MySQL result"


class MongoDatabase(DatabaseInterface):
    def save(self, data: str):
        print(f"Saving '{data}' to MongoDB")

    def fetch(self, query: str) -> str:
        print(f"Fetching from MongoDB: {query}")
        return "MongoDB result"


class InMemoryDatabase(DatabaseInterface):
    def __init__(self):
        self.storage = {}

    def save(self, data: str):
        self.storage[data] = data
        print(f"Saving '{data}' in memory")

    def fetch(self, query: str) -> str:
        return self.storage.get(query, "Not found")


# Step 3: High-level module depends on ABSTRACTION — not on a specific database
class UserService:
    def __init__(self, database: DatabaseInterface):  # Accepts any DB that follows the contract
        self.database = database

    def create_user(self, name: str):
        self.database.save(name)

    def get_user(self, user_id: str) -> str:
        return self.database.fetch(user_id)


# USAGE — inject whichever database you want, zero changes to UserService
mysql_service = UserService(MySQLDatabase())
mysql_service.create_user("Alice")     # Saving 'Alice' to MySQL database

mongo_service = UserService(MongoDatabase())
mongo_service.create_user("Bob")       # Saving 'Bob' to MongoDB

# For unit testing — use in-memory database, no real DB needed!
test_service = UserService(InMemoryDatabase())
test_service.create_user("TestUser")
print(test_service.get_user("TestUser"))  # TestUser
```

`UserService` doesn't know or care whether it's MySQL, MongoDB, or in-memory.
It just talks to the `DatabaseInterface` abstraction.
Swapping databases requires **zero changes** to `UserService`.

This technique is called **Dependency Injection** — the dependency (database) is
**injected from outside** rather than created inside. It is the key pattern for
writing testable, flexible backend code.

### Why This Matters in an Interview

> "DIP is fundamental in production systems. Our order service doesn't directly
> import a specific email library — it depends on a `NotificationInterface`.
> During testing, we inject a mock notifier so no real emails are sent.
> In production, we inject the real SendGrid implementation. The order service
> code never changes — only what we plug in changes."

---

## SOLID — Complete Summary

| Principle | Rule in One Line | Violation Sign | Fix |
|-----------|-----------------|----------------|-----|
| **S**ingle Responsibility | One class, one job | Class changes for multiple reasons | Split into smaller focused classes |
| **O**pen/Closed | Extend, don't modify | Adding features requires editing existing classes | Use abstract classes + polymorphism |
| **L**iskov Substitution | Child can replace parent safely | Subclass throws unexpected errors or ignores methods | Restructure inheritance hierarchy |
| **I**nterface Segregation | Don't force useless methods | Classes implement methods that throw `NotImplementedError` | Break into smaller interfaces |
| **D**ependency Inversion | Depend on abstractions, not concretes | High-level class directly imports low-level tools | Use interfaces + dependency injection |

---

## How SOLID Principles Work Together

These 5 principles are not independent — they reinforce each other:

- **SRP** makes your classes small and focused
- **OCP** makes your system easy to extend
- **LSP** makes inheritance safe and predictable
- **ISP** keeps interfaces clean and honest
- **DIP** makes your system testable and flexible

A real backend system that follows all 5 SOLID principles will be:
- Easy to test (you can mock dependencies — DIP)
- Easy to extend (add features without breaking things — OCP)
- Easy to understand (small, focused classes — SRP)
- Safe to use through inheritance (LSP)
- Not burdened with unnecessary contracts (ISP)

---

## Interview Q&A for This Topic

**Q: Which SOLID principle do you find most important?**

> "In backend development, I'd say Dependency Inversion — because it enables
> testability. If your business logic is tightly coupled to databases and external
> services, you cannot write unit tests without spinning up real infrastructure.
> DIP allows you to inject mocks, making the entire test suite fast and reliable.
> But in practice, all 5 work together — violating one often causes you to violate others."

**Q: How does SOLID relate to Design Patterns?**

> "Design Patterns are concrete solutions that implement SOLID principles.
> For example, the Strategy Pattern implements OCP — you can add new algorithms
> without changing existing code. The Factory Pattern supports DIP — high-level code
> asks a factory for an object without knowing the concrete type. Understanding SOLID
> helps you understand WHY design patterns exist, not just how to use them."

**Q: Can you over-apply SOLID?**

> "Yes — it's called over-engineering. If you have a simple script that reads a CSV
> and prints output, applying all 5 SOLID principles creates unnecessary complexity.
> SOLID shines in large, long-lived systems where requirements change frequently and
> multiple developers collaborate. The rule of thumb: apply SOLID when you can
> clearly see the need for flexibility or when the code will be maintained over time."

---

## Practice Exercise for Today

You are building a **notification system** for an e-commerce app. Users can receive
notifications via Email, SMS, or Push notification.

Apply ALL SOLID principles to design this system:

1. **SRP**: Separate `User`, `NotificationFormatter`, and `NotificationSender`
2. **OCP**: Adding a new channel (e.g., WhatsApp) should require NO changes to existing code
3. **LSP**: All notification types must fully honor the base contract
4. **ISP**: Don't force Email notifier to implement SMS methods
5. **DIP**: `OrderService` should not directly import `EmailSender`

Write the class structure (even just class names and method signatures) — you don't
need a full working implementation. The goal is to THINK in SOLID terms.

Solution and review will be at the start of Day 3.

---

*Next: Day 3 — UML Basics — How to draw and communicate system design visually*
