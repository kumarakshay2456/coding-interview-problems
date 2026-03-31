# Week 1 - Day 3: UML Basics
# Class Diagrams, Relationships, and How to Communicate Design Visually

---

## What is UML and Why Does It Exist?

Imagine you are a new architect hired to build a large office building.
Before a single brick is laid, you sit down with the client, the engineers,
the electricians, and the interior designers — and you show them **blueprints**.

Everyone in that room speaks different technical languages:
- The client understands rooms and layouts
- The electrician understands wiring diagrams
- The structural engineer understands load-bearing walls

But everyone understands **the blueprint** — because it is a universal visual language.

**UML (Unified Modeling Language)** is the blueprint language of software.

It is a standard, visual way to describe how a software system is structured —
what classes exist, what properties and methods they have, and how they relate
to each other — WITHOUT writing a single line of code.

### Why UML Matters in Interviews

In an LLD interview, the interviewer will say:
> *"Design a Parking Lot system"* or *"Design an Elevator system"*

You are expected to:
1. Think out loud about the entities involved
2. Draw a class diagram (on paper or whiteboard)
3. Explain the relationships between classes
4. THEN write the code

If you skip the diagram and jump straight to code, you look like someone who
codes without thinking. The diagram shows that you **think before you build**.

---

## Part 1: The Class Box — How to Represent a Single Class

A class in UML is drawn as a rectangle divided into **3 sections**:

```
┌─────────────────────────┐
│       ClassName          │   ← Section 1: Class Name (bold, centered)
├─────────────────────────┤
│  - attribute1: type      │   ← Section 2: Attributes (properties/variables)
│  - attribute2: type      │
│  + attribute3: type      │
├─────────────────────────┤
│  + method1(): return     │   ← Section 3: Methods (behaviors/functions)
│  - method2(param): type  │
│  # method3(): void       │
└─────────────────────────┘
```

### Access Modifiers (The Symbols)

The symbols before each attribute and method tell us who can access them:

| Symbol | Meaning | Python Equivalent |
|--------|---------|-------------------|
| `+` | Public — anyone can access | `self.name` (no underscore) |
| `-` | Private — only this class can access | `self.__name` (double underscore) |
| `#` | Protected — this class and subclasses | `self._name` (single underscore) |
| `~` | Package — accessible within the same package | (less common in Python) |

### Real Example — A BankAccount Class

```
┌───────────────────────────────┐
│          BankAccount           │
├───────────────────────────────┤
│  - account_number: str        │
│  - __balance: float           │
│  + owner: str                 │
├───────────────────────────────┤
│  + deposit(amount: float): void│
│  + withdraw(amount: float): bool│
│  + get_balance(): float       │
│  - validate_amount(amount): bool│
└───────────────────────────────┘
```

This diagram tells us:
- `account_number` and `__balance` are **private** — only BankAccount can touch them
- `owner` is **public** — anyone can read it
- `deposit` and `withdraw` are **public** — external code can call them
- `validate_amount` is **private** — it's an internal helper, not for outside use

### Python Code That Matches This Diagram

```python
class BankAccount:
    def __init__(self, account_number: str, owner: str):
        self.__account_number = account_number   # private
        self.__balance: float = 0.0              # private
        self.owner: str = owner                  # public

    def deposit(self, amount: float) -> None:    # public
        if self.__validate_amount(amount):
            self.__balance += amount

    def withdraw(self, amount: float) -> bool:   # public
        if self.__validate_amount(amount) and self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def get_balance(self) -> float:              # public
        return self.__balance

    def __validate_amount(self, amount) -> bool: # private
        return amount > 0
```

The UML diagram and the code tell the exact same story — just in different formats.
In an interview, you draw the diagram first, then write the code. The interviewer
can follow along because the diagram already gave them the full picture.

---

## Part 2: Relationships Between Classes

This is the most important part of UML for interviews. The relationships show
**how classes interact and depend on each other**.

There are 6 main relationships. We'll go through each one with a real-world analogy.

---

### Relationship 1: ASSOCIATION — "Uses" or "Knows About"

**Symbol in UML:** A plain arrow `──────►`

**Definition:** Class A uses Class B, but they are independent.
Neither owns the other. They can exist without each other.

**Real World Analogy:**
A **Doctor** treats a **Patient**. The doctor knows about the patient,
but if the doctor leaves the hospital, the patient still exists.
If the patient leaves, the doctor still exists. They are independent.

```
┌─────────┐           ┌─────────┐
│ Doctor  │──────────►│ Patient │
└─────────┘  treats   └─────────┘
```

**Python Code:**

```python
class Patient:
    def __init__(self, name: str):
        self.name = name


class Doctor:
    def __init__(self, name: str):
        self.name = name

    # Doctor uses Patient — but doesn't own or contain it
    def treat(self, patient: Patient):
        print(f"Dr. {self.name} is treating {patient.name}")


# Both exist independently
patient = Patient("Alice")
doctor = Doctor("Dr. Smith")
doctor.treat(patient)   # Association — Doctor "uses" Patient
```

---

### Relationship 2: AGGREGATION — "Has-A" (Weak Ownership)

**Symbol in UML:** A line with an **empty diamond** at the owning end `◇──────`

**Definition:** Class A contains Class B, but Class B can exist independently
of Class A. The relationship is "has-a" but not "owns-exclusively".

**Real World Analogy:**
A **Department** has **Employees**. If the department is shut down,
the employees still exist — they just move to other departments.
The department doesn't exclusively own the employees.

```
┌────────────┐          ┌──────────┐
│ Department │◇────────│ Employee │
└────────────┘  has-a  └──────────┘
```

**Python Code:**

```python
class Employee:
    def __init__(self, name: str):
        self.name = name


class Department:
    def __init__(self, dept_name: str):
        self.dept_name = dept_name
        self.employees: list[Employee] = []   # Has-a — but doesn't own exclusively

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def remove_employee(self, employee: Employee):
        self.employees.remove(employee)


# Employee exists independently — can be created without a Department
emp1 = Employee("Alice")
emp2 = Employee("Bob")

dept = Department("Engineering")
dept.add_employee(emp1)
dept.add_employee(emp2)

# Department is deleted — but emp1 and emp2 still exist in memory
del dept
print(emp1.name)   # Alice — still alive!
```

---

### Relationship 3: COMPOSITION — "Owns" (Strong Ownership)

**Symbol in UML:** A line with a **filled diamond** at the owning end `◆──────`

**Definition:** Class A contains Class B, and Class B CANNOT exist without Class A.
If A is destroyed, B is destroyed too. This is the strongest "has-a" relationship.

**Real World Analogy:**
A **House** has **Rooms**. If the house is demolished, the rooms cease to exist.
A room cannot float around in isolation without belonging to a house.

```
┌───────┐          ┌──────┐
│ House │◆────────│ Room │
└───────┘  owns   └──────┘
```

**Another Example:**
A **Human** has a **Heart**. If the human ceases to exist, the heart ceases to exist
as a functioning part. A heart doesn't independently exist outside a body.

```python
class Room:
    def __init__(self, room_type: str):
        self.room_type = room_type


class House:
    def __init__(self, address: str):
        self.address = address
        # Rooms are CREATED inside House — they don't exist independently
        self.rooms = [
            Room("bedroom"),
            Room("kitchen"),
            Room("bathroom")
        ]
        # When House is deleted, these Room objects are deleted too
        # No external reference holds them

    def show_rooms(self):
        for room in self.rooms:
            print(f"{self.address} has a {room.room_type}")


house = House("123 Main St")
house.show_rooms()
# If we delete house, all rooms are gone — they were composed inside it
```

### Aggregation vs Composition — The Key Difference

| | Aggregation | Composition |
|---|---|---|
| **Diamond** | Empty ◇ | Filled ◆ |
| **Ownership** | Weak — child can exist alone | Strong — child dies with parent |
| **Example** | Department ◇── Employee | House ◆── Room |
| **Lifecycle** | Independent | Dependent |

A simple question to decide which one: *"Can the child exist without the parent?"*
- YES → Aggregation
- NO → Composition

---

### Relationship 4: INHERITANCE / GENERALIZATION — "IS-A"

**Symbol in UML:** A line with a **hollow arrowhead** pointing to the parent `──────▷`

**Definition:** Class B IS-A type of Class A. B inherits all properties and
behaviors from A. This is the classic parent-child (superclass-subclass) relationship.
We covered this in detail in Day 1 — here we just learn the UML symbol.

```
          ┌─────────┐
          │ Vehicle │
          └────┬────┘
               │  IS-A
       ┌───────┴──────┐
       ▽              ▽
  ┌─────────┐    ┌─────────┐
  │   Car   │    │  Truck  │
  └─────────┘    └─────────┘
```

The hollow arrowhead always points **toward the parent (superclass)**.

---

### Relationship 5: REALIZATION — "Implements an Interface"

**Symbol in UML:** A **dashed line** with a hollow arrowhead `- - - - ▷`

**Definition:** Class A implements the contract defined by Interface B.
This is how we show that a class fulfills an abstract contract.

```
┌──────────────────┐          ┌──────────────────┐
│  «interface»     │          │  «interface»     │
│  Flyable         │          │  Swimmable       │
└──────────────────┘          └──────────────────┘
         ▲                             ▲
         ¦ (implements)                ¦ (implements)
         ¦                             ¦
    ┌────┴─────────────────────────────┘
    │          Duck                    │
    └──────────────────────────────────┘
```

Duck implements BOTH `Flyable` and `Swimmable` interfaces.

```python
from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self): pass

class Swimmable(ABC):
    @abstractmethod
    def swim(self): pass

class Duck(Flyable, Swimmable):   # Realization — implements both interfaces
    def fly(self):
        print("Duck is flying!")

    def swim(self):
        print("Duck is swimming!")
```

---

### Relationship 6: DEPENDENCY — "Uses Temporarily"

**Symbol in UML:** A **dashed arrow** `- - - - ►`

**Definition:** Class A temporarily uses Class B (e.g., as a method parameter
or local variable). It's the weakest relationship — A doesn't store B permanently.

**Real World Analogy:**
A **Chef** uses a **Knife** to cook. The knife is a temporary tool —
the chef uses it during the task and puts it down. The chef doesn't "have" a knife
as a permanent attribute the way a house "has" rooms.

```
┌───────┐  uses  ┌───────┐
│ Chef  │- - - ►│ Knife │
└───────┘        └───────┘
```

```python
class Knife:
    def cut(self, ingredient: str):
        print(f"Cutting {ingredient} with the knife")


class Chef:
    def __init__(self, name: str):
        self.name = name

    # Knife is a PARAMETER — temporary use, not stored in the class
    def prepare_food(self, knife: Knife, ingredient: str):
        print(f"Chef {self.name} is preparing {ingredient}")
        knife.cut(ingredient)   # Uses knife temporarily


knife = Knife()
chef = Chef("Gordon")
chef.prepare_food(knife, "carrot")   # Dependency — temporary use
```

---

## Part 3: Reading a Full UML Diagram

Let's put it all together with a real example — an **Online Order System**.

```
┌──────────────────────────────────────────────────────────────────┐

          ┌─────────────┐
          │   «interface»│
          │  Payable     │
          │─────────────│
          │+ pay(): bool │
          └──────┬───────┘
                 ¦ (realization)
                 ¦
          ┌──────┴───────┐
          │    Order      │
          │───────────────│
          │- order_id: str│
          │- total: float │
          │+ place(): void│
          │+ cancel(): bool│
          │+ pay(): bool  │
          └──────┬────────┘
                 │ (composition — order owns items)
                 │
          ┌──────▼────────┐
          │   OrderItem   │
          │───────────────│
          │- product: str │
          │- quantity: int│
          │- price: float │
          │+ subtotal(): float│
          └───────────────┘


  ┌─────────┐                   ┌─────────────┐
  │  User   │ ────────────────► │    Order    │
  │─────────│  places (assoc.)  │─────────────│
  │- user_id│                   │             │
  │+ name   │                   │             │
  └─────────┘                   └─────────────┘


  ┌───────────────┐              ┌─────────────┐
  │ ShoppingCart  │◇────────────│    Order    │
  │───────────────│  has (agg.) │─────────────│
  │- cart_id: str │              │             │
  │+ add_item()   │              │             │
  │+ checkout()   │              │             │
  └───────────────┘              └─────────────┘

└──────────────────────────────────────────────────────────────────┘
```

**Reading this diagram:**
- `Order` **realizes** the `Payable` interface — it must implement `pay()`
- `Order` **composes** `OrderItem` — items cannot exist without an order
- `User` **associates** with `Order` — user places an order (uses it, doesn't own it)
- `ShoppingCart` **aggregates** `Order` — a cart has orders, but orders can exist independently

---

## Part 4: Multiplicity — How Many?

UML also lets you express how many objects are involved in a relationship.

```
┌──────────┐  1        *  ┌──────────┐
│   User   │──────────────│  Order   │
└──────────┘              └──────────┘
```

| Notation | Meaning |
|----------|---------|
| `1` | Exactly one |
| `*` or `0..*` | Zero or more |
| `1..*` | One or more |
| `0..1` | Zero or one (optional) |
| `2..5` | Between 2 and 5 |

**Reading the example:** One User can have many (`*`) Orders.
One Order belongs to exactly one (`1`) User.

```
┌──────────┐  1      1..*  ┌────────────┐
│   Order  │───────────────│ OrderItem  │
└──────────┘               └────────────┘
```
One Order must have at least one (`1..*`) OrderItem.

---

## Part 5: How to Draw UML in an Interview (Step by Step)

When the interviewer says *"Design a Parking Lot"*, follow this process:

### Step 1 — Identify the Nouns (Entities)
Read the requirements. Every noun is a potential class:
> "A parking lot has multiple floors. Each floor has parking spots.
> A vehicle parks in a spot. A ticket is issued when a vehicle enters."

Nouns → Classes: `ParkingLot`, `Floor`, `ParkingSpot`, `Vehicle`, `Ticket`

### Step 2 — Identify the Attributes
For each class, ask: *"What does this thing know about itself?"*
- `ParkingSpot` knows: its number, its type (compact/large), whether it's occupied
- `Vehicle` knows: its license plate, its type (car/truck/motorcycle)
- `Ticket` knows: entry time, spot assigned, vehicle

### Step 3 — Identify the Methods
For each class, ask: *"What can this thing do?"*
- `ParkingLot` can: `find_available_spot()`, `issue_ticket()`, `process_exit()`
- `ParkingSpot` can: `occupy()`, `free()`, `is_available()`

### Step 4 — Identify the Relationships
- `ParkingLot` **composes** `Floor` (floor dies with lot)
- `Floor` **composes** `ParkingSpot` (spot dies with floor)
- `Ticket` **associates** with `Vehicle` (ticket references vehicle)
- `ParkingSpot` **associates** with `Vehicle` (spot temporarily holds vehicle)

### Step 5 — Draw the Diagram
Draw boxes, add attributes and methods, draw relationship lines with correct symbols.

---

## UML Relationships — Complete Cheat Sheet

```
Relationship      Symbol              Meaning                Example
─────────────────────────────────────────────────────────────────────
Association       ──────►             A uses B               Doctor uses Patient
Aggregation       ◇──────             A has B (weak)         Dept has Employee
Composition       ◆──────             A owns B (strong)      House owns Room
Inheritance       ──────▷             B is-a A               Car is-a Vehicle
Realization       - - - ▷             A implements interface  Duck implements Flyable
Dependency        - - - ►             A uses B temporarily    Chef uses Knife
```

---

## Interview Q&A for This Topic

**Q: What is the difference between Aggregation and Composition?**

> "Both are 'has-a' relationships, but they differ in lifecycle.
> In aggregation, the child object can exist independently of the parent —
> like an Employee that can exist even if their Department is deleted.
> In composition, the child cannot exist without the parent —
> like a Room that has no meaning if the House it belongs to is demolished.
> Composition implies full ownership and shared lifecycle."

**Q: When would you use Association vs Composition in code?**

> "I use Association when a class needs to use another class temporarily or
> reference it — like a Doctor treating a Patient, where neither owns the other.
> I use Composition when one class is fundamentally made up of another —
> like an Order that is composed of OrderItems. If the Order is deleted,
> there's no reason for those OrderItems to exist independently."

**Q: Do you need to draw UML perfectly in an interview?**

> "No — precision matters less than clarity. The goal is to communicate your
> thinking to the interviewer. Use boxes for classes, arrows for relationships,
> and verbally explain the diagram as you draw. Interviewers care more about
> whether you identified the right entities and relationships than whether
> your arrow style is textbook-perfect."

---

## Practice Exercise for Today

Draw a UML class diagram (in text or on paper) for a **Hospital Management System**:

**Requirements:**
- A hospital has multiple departments
- Each department has multiple doctors
- A doctor can treat multiple patients
- Each appointment is between one doctor and one patient, on a specific date
- A patient has a medical record that belongs exclusively to them

**Your task:**
1. Identify all classes
2. Identify attributes for each class (at least 2-3 per class)
3. Identify 1-2 methods per class
4. Draw relationships with correct symbols (association/aggregation/composition)
5. Add multiplicity (1, *, 1..*)

Solution and review at the start of Day 4.

---

*Next: Day 4 — Python OOP Deep Dive — Dunder methods, Properties, ABC, and Pythonic patterns*
