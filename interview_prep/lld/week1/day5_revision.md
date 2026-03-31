# Week 1 - Day 5: Revision + Exercise Solutions + Interview Simulation
# Consolidating OOP, SOLID, UML, and Python Deep Dive

---

## How to Use This Day

Day 5 is NOT about learning new things. It is about:
1. Reviewing what you learned in Days 1-4
2. Seeing the solutions to all practice exercises
3. Simulating a real interview — reading a question and answering it yourself
   BEFORE looking at the answer

**Golden Rule for Today:**
For every exercise solution below, try to write your version FIRST.
Cover the solution with your hand or close this section.
Write code. Then compare. Identify gaps.

This is how interviews work — you don't get to read the answer first.

---

## Week 1 Quick Revision Map

```
Day 1 — OOP Basics
├── Class = Blueprint, Object = Instance
├── Encapsulation = Hide data, expose safe methods (private __)
├── Inheritance = Child reuses parent (super(), IS-A)
├── Polymorphism = Same method, different behavior (override)
└── Abstraction = Hide HOW, show WHAT (ABC, @abstractmethod)

Day 2 — SOLID Principles
├── S = One class, one reason to change
├── O = Add features by extending, never editing existing code
├── L = Subclass must be safely substitutable for parent
├── I = Don't force useless method implementations
└── D = Depend on abstractions, inject concrete implementations

Day 3 — UML
├── Class box: Name | Attributes | Methods
├── Access: + public, - private, # protected
├── Association ──► (uses), Aggregation ◇── (has-a weak)
├── Composition ◆── (owns-strong), Inheritance ──▷ (is-a)
├── Realization - -▷ (implements), Dependency - -► (uses temp)
└── Multiplicity: 1, *, 1..*, 0..1

Day 4 — Python OOP Deep Dive
├── Dunder methods: __str__, __repr__, __eq__, __len__,
│   __iter__, __next__, __contains__, __enter__, __exit__
├── @property + @setter — controlled attribute access
├── @classmethod — alternative constructors (cls)
├── @staticmethod — utility functions (no self, no cls)
├── @dataclass — auto-generate boilerplate
└── __slots__ — memory optimization for many instances
```

---

## Exercise Solutions

### Day 1 Exercise Solution — E-Commerce OOP Model

**Problem:** Build `Product`, `DigitalProduct`, and `PhysicalProduct` classes.

```python
from abc import ABC, abstractmethod


class Product(ABC):
    """Base product class — cannot be instantiated directly"""

    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self._price = price    # Protected — use property for validation
        self.stock = stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def apply_discount(self, percent: float):
        """Reduces price by the given percentage"""
        if not 0 < percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        self._price = self._price * (1 - percent / 100)
        print(f"Discount applied! New price of '{self.name}': ₹{self._price:.2f}")

    @abstractmethod
    def is_available(self) -> bool:
        """Each product type decides its own availability logic"""
        pass

    def __str__(self) -> str:
        availability = "Available" if self.is_available() else "Out of Stock"
        return f"{self.name} | ₹{self._price:.2f} | {availability}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, price={self._price})"


class DigitalProduct(Product):
    """
    Digital products (e-books, software, music) are always available —
    there's no concept of physical stock running out.
    """

    def __init__(self, name: str, price: float, file_size_mb: float):
        super().__init__(name, price, stock=0)  # Stock concept doesn't apply
        self.file_size_mb = file_size_mb

    def is_available(self) -> bool:
        return True   # Digital products never "run out"

    def download(self):
        print(f"Downloading '{self.name}' ({self.file_size_mb} MB)...")


class PhysicalProduct(Product):
    """
    Physical products have real stock and shipping weight.
    """

    def __init__(self, name: str, price: float, stock: int, weight_kg: float):
        super().__init__(name, price, stock)
        self.weight_kg = weight_kg

    def is_available(self) -> bool:
        return self.stock > 0   # Available only if stock exists

    def calculate_shipping_cost(self) -> float:
        """Returns shipping cost: ₹50 per kg"""
        return self.weight_kg * 50

    def reduce_stock(self, quantity: int = 1):
        if quantity > self.stock:
            raise ValueError(f"Only {self.stock} units available")
        self.stock -= quantity
        print(f"Sold {quantity} unit(s) of '{self.name}'. Remaining: {self.stock}")


# --- Test It ---
ebook = DigitalProduct("Python Mastery Book", 499.0, file_size_mb=12.5)
laptop = PhysicalProduct("Dell Laptop", 65000.0, stock=5, weight_kg=2.1)
phone = PhysicalProduct("OnePlus 12", 45000.0, stock=0, weight_kg=0.2)

print(ebook)    # Python Mastery Book | ₹499.00 | Available
print(laptop)   # Dell Laptop | ₹65000.00 | Available
print(phone)    # OnePlus 12 | ₹45000.00 | Out of Stock

ebook.apply_discount(20)
print(f"Shipping cost for laptop: ₹{laptop.calculate_shipping_cost():.2f}")  # ₹105.00

laptop.reduce_stock(2)
print(laptop)   # Dell Laptop | ₹65000.00 | Available (3 remaining)
ebook.download()
```

**Key Decisions Made (Explain This in Interview):**
- `Product` is abstract because a bare "product" doesn't make sense — every product
  is either digital or physical
- `is_available()` is abstract because digital and physical have different rules
- `price` uses `@property` to prevent negative prices
- `DigitalProduct` sets `stock=0` because stock is irrelevant, not harmful
- Each class has one clear responsibility (SRP)

---

### Day 2 Exercise Solution — Notification System (SOLID)

**Problem:** Design a notification system applying all 5 SOLID principles.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class User:
    """SRP: User only holds user data"""
    user_id: str
    name: str
    email: str
    phone: str
    device_token: str = ""


@dataclass
class NotificationMessage:
    """SRP: Holds message content only"""
    subject: str
    body: str


# ─── ISP: Small, focused interfaces ──────────────────────────────────────────

class EmailSender(ABC):
    """ISP: Only email-capable services implement this"""
    @abstractmethod
    def send_email(self, user: User, message: NotificationMessage) -> bool:
        pass


class SMSSender(ABC):
    """ISP: Only SMS-capable services implement this"""
    @abstractmethod
    def send_sms(self, user: User, message: NotificationMessage) -> bool:
        pass


class PushSender(ABC):
    """ISP: Only push-notification-capable services implement this"""
    @abstractmethod
    def send_push(self, user: User, message: NotificationMessage) -> bool:
        pass


# ─── OCP + LSP: Concrete implementations ─────────────────────────────────────

class SendGridEmailSender(EmailSender):
    """LSP: Fully honors the EmailSender contract — no surprises"""
    def send_email(self, user: User, message: NotificationMessage) -> bool:
        print(f"[SendGrid] Sending email to {user.email}: {message.subject}")
        return True   # Simulate success


class TwilioSMSSender(SMSSender):
    """LSP: Fully honors the SMSSender contract"""
    def send_sms(self, user: User, message: NotificationMessage) -> bool:
        print(f"[Twilio] Sending SMS to {user.phone}: {message.body[:50]}")
        return True


class FirebasePushSender(PushSender):
    """LSP: Fully honors the PushSender contract"""
    def send_push(self, user: User, message: NotificationMessage) -> bool:
        if not user.device_token:
            print(f"[Firebase] No device token for {user.name} — skipping push")
            return False
        print(f"[Firebase] Sending push to {user.name}: {message.subject}")
        return True


# OCP: Adding WhatsApp requires ZERO changes to existing code
class WhatsAppSender(SMSSender):
    """New channel — extends, doesn't modify"""
    def send_sms(self, user: User, message: NotificationMessage) -> bool:
        print(f"[WhatsApp] Sending to {user.phone}: {message.body[:50]}")
        return True


# ─── DIP: High-level service depends on abstractions ─────────────────────────

class NotificationService:
    """
    DIP: This class depends on ABSTRACTIONS (EmailSender, SMSSender, PushSender)
    NOT on concrete classes (SendGrid, Twilio, Firebase).
    Inject the real implementation from outside.
    """

    def __init__(
        self,
        email_sender: EmailSender,
        sms_sender: SMSSender,
        push_sender: PushSender
    ):
        self._email_sender = email_sender
        self._sms_sender = sms_sender
        self._push_sender = push_sender

    def notify(self, user: User, message: NotificationMessage, channels: List[str]):
        results = {}
        if "email" in channels:
            results["email"] = self._email_sender.send_email(user, message)
        if "sms" in channels:
            results["sms"] = self._sms_sender.send_sms(user, message)
        if "push" in channels:
            results["push"] = self._push_sender.send_push(user, message)
        return results


# ─── Usage ────────────────────────────────────────────────────────────────────

# Production: inject real implementations
notification_service = NotificationService(
    email_sender=SendGridEmailSender(),
    sms_sender=TwilioSMSSender(),
    push_sender=FirebasePushSender()
)

user = User(
    user_id="U001",
    name="Alice",
    email="alice@example.com",
    phone="+919876543210",
    device_token="abc123"
)

message = NotificationMessage(
    subject="Your order has been shipped!",
    body="Your order #12345 is on its way. Expected delivery: 2 days."
)

notification_service.notify(user, message, channels=["email", "sms", "push"])

# For Testing: inject mock implementations — no real messages sent
class MockEmailSender(EmailSender):
    def send_email(self, user, message):
        print(f"[MOCK] Would send email to {user.email}")
        return True

test_service = NotificationService(
    email_sender=MockEmailSender(),
    sms_sender=TwilioSMSSender(),
    push_sender=FirebasePushSender()
)
```

---

### Day 3 Exercise Solution — Hospital Management UML

**Problem:** Draw UML for Hospital Management System.

```
Hospital Management System — UML Class Diagram
═══════════════════════════════════════════════

┌─────────────────────────┐
│        Hospital          │
│─────────────────────────│
│ - name: str             │
│ - address: str          │
│ - phone: str            │
│─────────────────────────│
│ + add_department(): void│
│ + find_doctor(): Doctor │
└────────────┬────────────┘
             │ ◆ (Composition — departments die with hospital)
             │ 1..*
┌────────────▼────────────┐
│       Department         │
│─────────────────────────│
│ - dept_id: str          │
│ - name: str             │
│ - floor: int            │
│─────────────────────────│
│ + add_doctor(): void    │
│ + get_doctors(): List   │
└────────────┬────────────┘
             │ ◇ (Aggregation — doctors exist independently)
             │ 1..*
┌────────────▼────────────┐         ┌─────────────────────────┐
│         Doctor           │         │         Patient          │
│─────────────────────────│         │─────────────────────────│
│ - doctor_id: str        │         │ - patient_id: str       │
│ + name: str             │         │ + name: str             │
│ - specialization: str   │         │ - date_of_birth: date   │
│ - license_number: str   │         │ - blood_group: str      │
│─────────────────────────│         │─────────────────────────│
│ + schedule(): List      │         │ + get_age(): int        │
│ + get_appointments(): List        │ + get_record(): MedRecord│
└────────────┬────────────┘         └──────────┬──────────────┘
             │                                  │
             │  (Association — treats)          │ ◆ 1 to 1
             └──────────────┬───────────────────┘ (Composition)
                            │                      ┌────────────────────────┐
              ┌─────────────▼──────────┐           │     MedicalRecord      │
              │       Appointment       │           │────────────────────────│
              │────────────────────────│           │ - record_id: str       │
              │ - appt_id: str         │           │ - diagnoses: List[str] │
              │ - date: datetime       │           │ - medications: List    │
              │ - status: str          │           │ - allergies: List[str] │
              │ - notes: str           │           │────────────────────────│
              │────────────────────────│           │ + add_diagnosis(): void│
              │ + confirm(): void      │           │ + get_history(): List  │
              │ + cancel(): void       │           └────────────────────────┘
              └────────────────────────┘

Multiplicities:
- Hospital ◆── Department: 1 to 1..*  (one hospital, one or more departments)
- Department ◇── Doctor: 1 to 1..*    (one dept, one or more doctors)
- Doctor ──► Appointment: 1 to *      (one doctor, many appointments)
- Patient ──► Appointment: 1 to *     (one patient, many appointments)
- Patient ◆── MedicalRecord: 1 to 1   (one patient, exactly one medical record)
```

---

### Day 4 Exercise Solution — PriorityQueue With Dunder Methods

```python
from dataclasses import dataclass, field
from typing import List, Iterator


@dataclass(order=True)  # order=True auto-generates __lt__, __le__, __gt__, __ge__
class Task:
    priority: int          # Lower number = higher priority (1 is most urgent)
    name: str = field(compare=False)   # Excluded from comparison — only priority matters
    description: str = field(compare=False, default="")

    def __str__(self) -> str:
        return f"Task[P{self.priority}]: {self.name}"

    def __repr__(self) -> str:
        return f"Task(priority={self.priority}, name={self.name!r})"


class PriorityQueue:
    """
    A priority queue where items are retrieved in priority order.
    Lower priority number = higher urgency (1 is most urgent, 10 is least).
    """

    def __init__(self):
        self._tasks: List[Task] = []

    def add(self, task: Task):
        """Add a task — maintains sorted order internally"""
        self._tasks.append(task)
        self._tasks.sort()   # Sort by priority (uses Task's __lt__)

    # Makes len(queue) work
    def __len__(self) -> int:
        return len(self._tasks)

    # Makes `for task in queue` work — iterates in priority order (already sorted)
    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    # Makes `task in queue` work
    def __contains__(self, task: Task) -> bool:
        return task in self._tasks

    # Context manager — setup
    def __enter__(self):
        print(f"PriorityQueue opened — ready to process tasks")
        return self

    # Context manager — cleanup, prints summary on exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\nPriorityQueue closed.")
        print(f"Summary: {len(self._tasks)} task(s) remaining unprocessed.")
        if self._tasks:
            print("Remaining tasks:")
            for task in self._tasks:
                print(f"  - {task}")
        return False   # Don't suppress exceptions

    def pop_highest_priority(self) -> Task:
        """Remove and return the highest priority task"""
        if not self._tasks:
            raise IndexError("Queue is empty")
        return self._tasks.pop(0)   # First item = highest priority (sorted)

    def __repr__(self) -> str:
        return f"PriorityQueue({len(self._tasks)} tasks)"


# --- Usage ---
with PriorityQueue() as queue:
    queue.add(Task(priority=3, name="Fix login bug", description="Users can't login"))
    queue.add(Task(priority=1, name="Server down!", description="Production outage"))
    queue.add(Task(priority=2, name="Deploy hotfix", description="Security patch"))
    queue.add(Task(priority=5, name="Update docs"))
    queue.add(Task(priority=1, name="Database backup", description="Critical backup"))

    print(f"Total tasks: {len(queue)}")  # 5

    # Check membership
    critical = Task(priority=1, name="Server down!")
    print(f"Is critical task in queue? {critical in queue}")   # True

    # Iterate in priority order
    print("\nAll tasks in priority order:")
    for task in queue:
        print(f"  {task}")

    # Process top 2 tasks
    print("\nProcessing top 2 tasks:")
    t1 = queue.pop_highest_priority()
    print(f"Processing: {t1}")
    t2 = queue.pop_highest_priority()
    print(f"Processing: {t2}")

# __exit__ prints summary automatically here
```

**Output:**
```
PriorityQueue opened — ready to process tasks
Total tasks: 5
Is critical task in queue? True

All tasks in priority order:
  Task[P1]: Server down!
  Task[P1]: Database backup
  Task[P2]: Deploy hotfix
  Task[P3]: Fix login bug
  Task[P5]: Update docs

Processing top 2 tasks:
Processing: Task[P1]: Server down!
Processing: Task[P1]: Database backup

PriorityQueue closed.
Summary: 3 task(s) remaining unprocessed.
Remaining tasks:
  - Task[P2]: Deploy hotfix
  - Task[P3]: Fix login bug
  - Task[P5]: Update docs
```

---

## Interview Simulation — Week 1

Below are 5 real SDE-3 LLD interview questions. For each one:
1. READ the question
2. CLOSE this section and think for 3-5 minutes
3. WRITE your answer (diagram + code structure)
4. COME BACK and compare

---

### Question 1 — Conceptual

**Q: "Explain polymorphism to me with a real-world backend example."**

**Model Answer:**
> "Polymorphism means the same method call behaves differently depending on the
> object. In a payment system, I'd define a `PaymentGateway` abstract class with
> a `process_payment(amount)` method. Then `StripeGateway`, `PayPalGateway`,
> and `RazorpayGateway` each implement it differently — Stripe hits their REST API,
> PayPal uses OAuth tokens, Razorpay uses HMAC signatures.
>
> The `CheckoutService` just calls `gateway.process_payment(amount)`. It has no
> idea which gateway it's talking to — and it doesn't need to. When we added
> Razorpay, we wrote one new class. Zero changes to `CheckoutService`. That's
> the power — extensibility without modification."

---

### Question 2 — SOLID

**Q: "I have a class that reads data from a CSV, validates it, transforms it,
and saves it to a database. What's wrong with this design?"**

**Model Answer:**
> "This violates SRP — the class has four separate reasons to change:
> 1. If the file format changes from CSV to JSON (reading)
> 2. If validation rules change (validating)
> 3. If the transformation logic changes (transforming)
> 4. If the database changes (saving)
>
> I would split it into: `CSVReader` (or an abstract `DataReader`),
> `DataValidator`, `DataTransformer`, and `DataRepository`.
> Each class has one responsibility, one reason to change.
> This also makes each piece independently testable — I can test validation
> with mock data without needing a real CSV file or database."

---

### Question 3 — Design

**Q: "Design a simple Logger class in Python that supports multiple log levels
(DEBUG, INFO, WARNING, ERROR) and multiple output destinations (console, file).
You should be able to add new destinations without changing the Logger."**

**Think first, then see below:**

```python
from abc import ABC, abstractmethod
from enum import Enum, auto
from datetime import datetime


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class LogHandler(ABC):
    """OCP + DIP: Abstract handler — add new destinations without changing Logger"""

    @abstractmethod
    def emit(self, level: LogLevel, message: str, timestamp: str):
        pass


class ConsoleHandler(LogHandler):
    COLORS = {
        LogLevel.DEBUG: "\033[36m",    # Cyan
        LogLevel.INFO: "\033[32m",     # Green
        LogLevel.WARNING: "\033[33m",  # Yellow
        LogLevel.ERROR: "\033[31m",    # Red
    }
    RESET = "\033[0m"

    def emit(self, level: LogLevel, message: str, timestamp: str):
        color = self.COLORS.get(level, "")
        print(f"{color}[{timestamp}] [{level.name}] {message}{self.RESET}")


class FileHandler(LogHandler):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def emit(self, level: LogLevel, message: str, timestamp: str):
        with open(self.file_path, "a") as f:
            f.write(f"[{timestamp}] [{level.name}] {message}\n")


# OCP: Add this without touching Logger
class JSONHandler(LogHandler):
    import json

    def emit(self, level: LogLevel, message: str, timestamp: str):
        entry = {"timestamp": timestamp, "level": level.name, "message": message}
        print(self.json.dumps(entry))


class Logger:
    """SRP: Only handles log routing. DIP: Depends on abstract handlers."""

    _instance = None   # Singleton — only one logger in the app

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = []
            cls._instance._min_level = LogLevel.DEBUG
        return cls._instance

    def add_handler(self, handler: LogHandler):
        self._handlers.append(handler)

    def set_level(self, level: LogLevel):
        self._min_level = level

    def _log(self, level: LogLevel, message: str):
        if level.value < self._min_level.value:
            return   # Skip messages below minimum level
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for handler in self._handlers:
            handler.emit(level, message, timestamp)

    def debug(self, message: str): self._log(LogLevel.DEBUG, message)
    def info(self, message: str):  self._log(LogLevel.INFO, message)
    def warning(self, message: str): self._log(LogLevel.WARNING, message)
    def error(self, message: str): self._log(LogLevel.ERROR, message)


# --- Usage ---
logger = Logger()
logger.add_handler(ConsoleHandler())
logger.add_handler(FileHandler("app.log"))
logger.set_level(LogLevel.INFO)   # Only INFO and above will be logged

logger.debug("This won't show — below minimum level")
logger.info("Application started")
logger.warning("Memory usage is high")
logger.error("Database connection failed!")

# Singleton test
logger2 = Logger()
print(logger is logger2)   # True — same instance
```

---

### Question 4 — UML Reading

**Q: "I describe a system: A `Library` has many `Books`. A `Book` can be borrowed
by at most one `Member` at a time. A `Member` can borrow multiple books.
When a book is borrowed, a `BorrowRecord` is created. Draw the UML."**

```
┌──────────┐   1      *   ┌──────────┐   0..1    *   ┌──────────┐
│ Library  │◆────────────│   Book   │──────────────►│  Member  │
│──────────│  owns        │──────────│  borrowed by  │──────────│
│- name    │              │- isbn    │               │- member_id│
│- address │              │- title   │               │- name    │
│──────────│              │- author  │               │- email   │
│+ add()   │              │- is_avail│               │──────────│
│+ search()│              │──────────│               │+ borrow()│
└──────────┘              │+ borrow()│               │+ return()│
                          │+ return()│               └──────────┘
                          └────┬─────┘
                               │ (creates)
                               │ 1      *
                          ┌────▼──────────┐
                          │ BorrowRecord  │
                          │───────────────│
                          │- record_id    │
                          │- borrow_date  │
                          │- due_date     │
                          │- return_date  │
                          │───────────────│
                          │+ is_overdue() │
                          └───────────────┘

Notes:
- Library ◆── Book: Composition (books are part of library)
- Book 0..1 ──► Member: Association (0..1 means a book may or may not be borrowed)
- Member * ──► BorrowRecord: Association (one member has many records)
- Book * ──► BorrowRecord: Association (one book has many records over time)
```

---

### Question 5 — Code Review

**Q: "What is wrong with this code? How would you fix it?"**

```python
class ReportGenerator:
    def generate(self, data, format_type):
        if format_type == "pdf":
            # 50 lines of PDF generation logic
            print("Generating PDF...")
        elif format_type == "excel":
            # 50 lines of Excel generation logic
            print("Generating Excel...")
        elif format_type == "csv":
            # 50 lines of CSV generation logic
            print("Generating CSV...")
```

**Model Answer:**
> "This violates both SRP and OCP. The class has three responsibilities
> (PDF, Excel, CSV generation) and must be modified every time a new format
> is needed — adding HTML or JSON means editing this class and risking
> breaking existing formats.
>
> Fix: Create an abstract `ReportFormatter` with a `format(data)` method.
> Then create `PDFFormatter`, `ExcelFormatter`, `CSVFormatter` as separate classes.
> `ReportGenerator` takes a `ReportFormatter` via dependency injection.
> Adding a new format is just adding a new class — zero changes to existing code."

---

## Week 1 Completion Checklist

Before moving to Week 2, make sure you can:

- [ ] Explain all 4 OOP pillars with real-world analogies (no code needed)
- [ ] Name all 5 SOLID principles and give one real example each
- [ ] Draw a UML class diagram for a simple system (3-5 classes, relationships, multiplicity)
- [ ] Write a Python class using `@property`, `@classmethod`, and at least 2 dunder methods
- [ ] Use `@dataclass` correctly with default values and `frozen=True`
- [ ] Identify SOLID violations in code you're shown
- [ ] Design a system by starting with the diagram, THEN writing code

If any box is unchecked — re-read that specific day before moving to Week 2.

---

*Next: Week 2, Day 6 — Creational Design Patterns (Singleton, Factory, Builder)*
*This is where patterns click — you'll see OOP and SOLID principles come alive in reusable, named solutions.*
