# Week 1 - Day 1: Object Oriented Programming (OOP) Basics
# Topic: Classes, Objects, Inheritance, Polymorphism, Encapsulation, Abstraction

---

## What is OOP and Why Does It Exist?

Before OOP, programmers wrote code in a style called **procedural programming** — which
means you write a list of instructions, one after another, like a recipe.

Imagine you are cooking and your recipe says:
1. Boil water
2. Add pasta
3. Drain water
4. Add sauce

This works for small things. But what if you are running a **restaurant** with 50 dishes,
100 employees, and 500 customers? Writing one giant recipe-style list becomes a nightmare.
You lose track of what does what. Bugs hide everywhere. Changing one line breaks something else.

**OOP solves this** by saying: *"Let's model the real world. The world has things (objects),
and things have properties and behaviors."*

---

## 1. CLASS — The Blueprint

### Real World Analogy

Think of a **class** as an **architectural blueprint** of a house.

The blueprint is NOT a house. You cannot live in a blueprint. But it describes:
- How many rooms the house will have
- Where the windows are
- What color the walls will be

Once you have the blueprint, you can **build multiple houses** from it — each house is
a real, physical thing based on that one blueprint.

In programming:
- **Class** = Blueprint
- **Object** = The actual house built from that blueprint

### Python Example

```python
# This is the BLUEPRINT (Class)
class Car:
    # Properties every car will have
    def __init__(self, brand, color, speed):
        self.brand = brand      # What brand is this car?
        self.color = color      # What color is this car?
        self.speed = speed      # How fast can this car go?

    # Behavior every car can do
    def drive(self):
        print(f"The {self.color} {self.brand} is driving at {self.speed} km/h")

    def honk(self):
        print(f"{self.brand} goes BEEP BEEP!")
```

Here, `Car` is just a blueprint. It does not exist in memory as a real car yet.
`__init__` is a **special method** (called a constructor) that runs automatically
when you create a new car. Think of it as the factory machine that assembles
the car when you order one.

---

## 2. OBJECT — The Real Instance

### Real World Analogy

Now that we have the blueprint, let's **build actual cars**:

```python
# Building actual cars from the blueprint (Creating Objects)
car1 = Car(brand="Toyota", color="Red", speed=120)
car2 = Car(brand="BMW", color="Black", speed=200)
car3 = Car(brand="Tesla", color="White", speed=250)

# Each car behaves independently
car1.drive()   # The Red Toyota is driving at 120 km/h
car2.drive()   # The Black BMW is driving at 200 km/h
car3.honk()    # Tesla goes BEEP BEEP!
```

`car1`, `car2`, `car3` are three **objects** — three separate real cars,
all built from the same `Car` blueprint.

Changing `car1`'s color does NOT affect `car2`. They are independent.

```python
car1.color = "Blue"   # Only car1 becomes Blue
print(car2.color)     # Still "Black" — unaffected
```

### Why This Matters in an Interview

> "We use classes to define the structure and behavior of entities in our system.
> For example, in an e-commerce app, we'd have a `User` class, an `Order` class,
> and a `Product` class — each with their own properties and behaviors,
> keeping the code organized and reusable."

---

## 3. ENCAPSULATION — Hiding the Messy Details

### Real World Analogy

Think about your **TV remote control**.

You press the volume button and the TV gets louder. But you have NO idea what happens
inside — the signal sent, the frequency used, the circuit activated. You don't need to know.
The remote **hides** the complexity and gives you only the buttons you need.

This is **Encapsulation**: *wrapping data (properties) and the methods (behaviors)
that operate on that data into one unit, and hiding the internal details from the outside.*

### The Problem Without Encapsulation

```python
# BAD - No encapsulation
class BankAccount:
    def __init__(self):
        self.balance = 0  # Anyone can directly change this!

account = BankAccount()
account.balance = -999999  # Uh oh! Anyone can set it to anything
```

This is dangerous. A bank account balance should never be set directly from outside.

### The Solution — Encapsulation

```python
# GOOD - With encapsulation
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.__balance = 0  # __ makes it PRIVATE — outsiders cannot touch it directly

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive!")
            return
        self.__balance += amount
        print(f"Deposited {amount}. New balance: {self.__balance}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds!")
            return
        self.__balance -= amount
        print(f"Withdrew {amount}. Remaining balance: {self.__balance}")

    def get_balance(self):
        return self.__balance  # Controlled way to READ the balance


account = BankAccount("Alice")
account.deposit(1000)     # Works fine
account.withdraw(500)     # Works fine
account.withdraw(9999)    # "Insufficient funds!" — protected!

# account.__balance = 999999  # This will FAIL — it's private!
print(account.get_balance())  # Read-only access through a method
```

### Key Points
- `__balance` (double underscore) = private variable — cannot be accessed outside the class
- We provide **controlled access** through methods like `deposit`, `withdraw`, `get_balance`
- This is called **data hiding** — the internal state is protected from misuse

### Why This Matters in an Interview

> "Encapsulation protects the internal state of an object. For example, in a payment system,
> the account balance should never be modified directly. We expose only safe, validated methods
> like `deposit()` and `withdraw()` that ensure the balance is always in a valid state."

---

## 4. INHERITANCE — Reusing and Extending Existing Code

### Real World Analogy

Imagine you have a general blueprint for a **Vehicle** — it has wheels, an engine,
and can move. Now you want to create a **Car**, a **Truck**, and a **Motorcycle**.

Instead of building each from scratch, you say:
*"All three ARE vehicles. Let them INHERIT everything from Vehicle,
and I'll only add what makes each one special."*

```
Vehicle (Parent)
├── has: wheels, engine, can_move()
│
├── Car (Child) — inherits Vehicle + adds: music_system, air_conditioning
├── Truck (Child) — inherits Vehicle + adds: cargo_capacity, towing_power
└── Motorcycle (Child) — inherits Vehicle + adds: helmet_storage
```

### Python Example

```python
# PARENT class (also called Base class or Super class)
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def move(self):
        print(f"{self.brand} is moving at {self.speed} km/h")

    def stop(self):
        print(f"{self.brand} has stopped.")


# CHILD class — inherits everything from Vehicle
class Car(Vehicle):
    def __init__(self, brand, speed, num_doors):
        super().__init__(brand, speed)   # Call parent's __init__ to set brand & speed
        self.num_doors = num_doors       # Car-specific property

    def play_music(self):
        print(f"{self.brand}'s music system is ON!")


# CHILD class — inherits everything from Vehicle
class Truck(Vehicle):
    def __init__(self, brand, speed, cargo_tons):
        super().__init__(brand, speed)
        self.cargo_tons = cargo_tons

    def load_cargo(self):
        print(f"{self.brand} is loading {self.cargo_tons} tons of cargo.")


# Using them
my_car = Car("Honda", 150, 4)
my_car.move()         # Inherited from Vehicle — "Honda is moving at 150 km/h"
my_car.play_music()   # Car-specific — "Honda's music system is ON!"

my_truck = Truck("Volvo", 100, 20)
my_truck.move()        # Inherited from Vehicle — "Volvo is moving at 100 km/h"
my_truck.load_cargo()  # Truck-specific — "Volvo is loading 20 tons of cargo."
```

### `super()` — Calling the Parent

`super().__init__(brand, speed)` means:
*"Hey parent class, please run YOUR __init__ to set up the basic stuff.
I'll handle only the extra things that are specific to me."*

Think of it like: when a new employee joins a company, HR handles the standard
onboarding (ID card, email, payroll). The team manager only handles the role-specific
training. `super()` calls HR (the parent).

### Why This Matters in an Interview

> "Inheritance helps us avoid repeating code. In a notification system, we'd have
> a base `Notification` class with common logic like `send()` and `log()`.
> Then `EmailNotification`, `SMSNotification`, and `PushNotification` would
> inherit from it and only override what's different."

---

## 5. POLYMORPHISM — One Interface, Many Behaviors

### Real World Analogy

The word "Polymorphism" comes from Greek: *poly* = many, *morph* = forms.

Think about the word **"open"**:
- Open a **door** — you turn a handle
- Open a **bottle** — you twist a cap
- Open a **file on computer** — you double-click
- Open a **bank account** — you fill forms

Same word, same action concept — but **completely different behavior** depending on context.

In programming: *the same method name can behave differently depending on which
object calls it.*

### Python Example

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        # Generic — to be overridden by children
        print("Some generic animal sound")


class Dog(Animal):
    def speak(self):            # OVERRIDES parent's speak
        print(f"{self.name} says: Woof Woof!")


class Cat(Animal):
    def speak(self):            # OVERRIDES parent's speak
        print(f"{self.name} says: Meow!")


class Duck(Animal):
    def speak(self):            # OVERRIDES parent's speak
        print(f"{self.name} says: Quack!")


# POLYMORPHISM in action
animals = [Dog("Rex"), Cat("Whiskers"), Duck("Donald")]

for animal in animals:
    animal.speak()   # Same method call — different behavior each time!

# Output:
# Rex says: Woof Woof!
# Whiskers says: Meow!
# Donald says: Quack!
```

Notice: we call `animal.speak()` on every animal in the loop.
We don't care WHICH specific animal it is — Python figures it out automatically.
This is the power of polymorphism.

### Real Backend Example

```python
class PaymentProcessor:
    def process(self, amount):
        raise NotImplementedError


class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        print(f"Processing {amount} via Credit Card — charging card ending in 4242")


class PayPalProcessor(PaymentProcessor):
    def process(self, amount):
        print(f"Processing {amount} via PayPal — sending to paypal@user.com")


class CryptoProcessor(PaymentProcessor):
    def process(self, amount):
        print(f"Processing {amount} via Crypto — broadcasting to blockchain")


# The ORDER system does NOT care which payment method is used
# It just calls .process() and polymorphism handles the rest
def checkout(processor: PaymentProcessor, amount: float):
    processor.process(amount)

checkout(CreditCardProcessor(), 500)   # Credit Card flow
checkout(PayPalProcessor(), 500)       # PayPal flow
checkout(CryptoProcessor(), 500)       # Crypto flow
```

The `checkout` function is **unaware** of the specific payment type.
You can add a new payment method tomorrow (e.g., `ApplePayProcessor`)
without touching `checkout` at all. This is maintainable, scalable code.

### Why This Matters in an Interview

> "Polymorphism allows us to write flexible, extensible code. For example, in a
> notification service, a single `send()` call works across Email, SMS, and Push —
> without the caller needing to know the implementation details. Adding a new
> channel doesn't require changing any existing code."

---

## 6. ABSTRACTION — Show Only What's Necessary

### Real World Analogy

When you drive a car, you interact with:
- Steering wheel
- Accelerator
- Brake
- Gear shift

You do NOT see or interact with:
- Fuel injection system
- Engine pistons
- Transmission gears turning

The car **abstracts away** the complex machinery and gives you a **simple interface**.

**Abstraction** = *Hiding the complex implementation details and showing only
the essential features to the user.*

### Abstraction vs Encapsulation — The Difference

People often confuse these two. Here's the clear difference:

| | Encapsulation | Abstraction |
|---|---|---|
| **What it does** | Hides DATA (properties) | Hides IMPLEMENTATION (how it works) |
| **Focus** | Protecting internal state | Simplifying the interface |
| **Analogy** | Bank vault hides cash | Car hides engine complexity |

### Python Example — Abstract Class

```python
from abc import ABC, abstractmethod

# Abstract class — like a CONTRACT
# It says: "Anyone who inherits me MUST implement these methods"
class Shape(ABC):

    @abstractmethod
    def area(self):
        pass   # No implementation here — just the contract

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):  # This is NOT abstract — it has a real implementation
        print(f"I am a shape with area {self.area()} and perimeter {self.perimeter()}")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):                           # MUST implement — it's in the contract
        return 3.14 * self.radius * self.radius

    def perimeter(self):                      # MUST implement — it's in the contract
        return 2 * 3.14 * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# Usage
c = Circle(5)
c.describe()    # "I am a shape with area 78.5 and perimeter 31.4"

r = Rectangle(4, 6)
r.describe()    # "I am a shape with area 24 and perimeter 20"

# shape = Shape()  # ERROR! Cannot create an object of abstract class directly
```

`Shape` is the **abstract class** — it defines WHAT must exist but not HOW.
`Circle` and `Rectangle` define the HOW.

The user of these classes just calls `.area()` — they don't care how it's calculated.
That's abstraction.

### Why This Matters in an Interview

> "Abstraction lets us define contracts without revealing implementation.
> For example, a `DatabaseConnector` abstract class might define `connect()`,
> `query()`, and `disconnect()`. PostgreSQL, MySQL, and MongoDB implementations
> each fulfill this contract differently — but the rest of the application
> just uses the abstract interface and works with any database seamlessly."

---

## Quick Revision Summary

| Concept | One-line Definition | Real World |
|---|---|---|
| **Class** | Blueprint / Template | Architectural drawing of a house |
| **Object** | Instance built from blueprint | The actual house you live in |
| **Encapsulation** | Hide data, expose safe methods | TV remote hides circuit complexity |
| **Inheritance** | Child reuses parent's code | Kids inherit traits from parents |
| **Polymorphism** | Same method, different behavior | "Open" means different things in different contexts |
| **Abstraction** | Hide implementation, show interface | Car hides engine, shows steering wheel |

---

## Interview Q&A for This Topic

**Q: What is the difference between Abstraction and Encapsulation?**

> Encapsulation is about **data protection** — hiding the internal state using
> private variables and exposing it only through controlled methods.
> Abstraction is about **complexity hiding** — hiding the implementation details
> and showing only the necessary interface to the outside world.
> Encapsulation is achieved using access modifiers (private/public).
> Abstraction is achieved using abstract classes and interfaces.

**Q: What is the difference between Inheritance and Composition?**

> Inheritance follows "IS-A" relationship — a Dog IS-A Animal.
> Composition follows "HAS-A" relationship — a Car HAS-A Engine.
> Composition is generally preferred over inheritance in modern design
> because it's more flexible and avoids tight coupling between classes.
> (We will cover Composition in depth in Design Patterns week)

**Q: Can Python support multiple inheritance?**

> Yes, Python supports multiple inheritance — a class can inherit from more
> than one parent. But it should be used carefully because it can lead to
> the "Diamond Problem" (ambiguity when two parents have the same method).
> Python resolves this using MRO — Method Resolution Order — which follows
> the C3 linearization algorithm to determine which parent's method to call.

```python
class A:
    def hello(self):
        print("Hello from A")

class B(A):
    def hello(self):
        print("Hello from B")

class C(A):
    def hello(self):
        print("Hello from C")

class D(B, C):   # Multiple inheritance
    pass

d = D()
d.hello()   # Prints "Hello from B" — Python checks B before C (left to right)
print(D.__mro__)  # Shows the resolution order
```

---

## Practice Exercise for Today

Build a small OOP model for an **E-commerce system** with the following:

1. Create a `Product` class with: `name`, `price`, `stock`
   - Method: `apply_discount(percent)` — reduces price
   - Method: `is_available()` — returns True if stock > 0

2. Create a `DigitalProduct(Product)` child class
   - Add: `file_size_mb` property
   - Override: `is_available()` — digital products are always available (no stock limit)

3. Create a `PhysicalProduct(Product)` child class
   - Add: `weight_kg` property
   - Add: `calculate_shipping_cost()` — returns weight_kg * 50 (rupees per kg)

Try writing this yourself first — solution will be in Day 2 review.

---

*Next: Day 2 — SOLID Principles (The 5 rules every good OOP developer must follow)*
