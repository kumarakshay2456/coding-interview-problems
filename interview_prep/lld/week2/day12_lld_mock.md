# Week 2 - Day 12: LLD Mock Interview
# Top 20 Questions, Model Answers, Red Flags, Green Flags, and Self-Assessment

---

## What This Day Covers

This is your mock interview day. You have spent 11 days learning requirements
gathering, entities, UML, patterns, and full code walkthroughs. Today you
practice **performing** that knowledge under pressure.

A mock interview is not just about knowing the answer. It is about communicating
like a senior engineer — structured, calm, collaborative, and pattern-aware.

---

## Part 1: How to Conduct Yourself in an LLD Interview

### The 5-Phase Interview Framework

Think of an LLD interview like building a house. You do not start hammering
nails before drawing blueprints. You do not argue over paint colors before
pouring the foundation.

---

### Phase 1: Clarify Requirements (3–5 minutes)

**What it is:** Ask targeted questions to shrink the problem space.

**Why it matters:** Every interviewer deliberately leaves requirements vague.
They want to see if you ask good questions or if you assume. Assuming is what
junior engineers do. Senior engineers ask.

**What to ask:**
- "Is this a single-tenant or multi-tenant system?"
- "What are the scale expectations — 100 users or 10 million?"
- "Should I design for extensibility or simplicity first?"
- "Are there any explicit non-functional requirements — latency, availability?"
- "Should I handle authentication/authorization, or is that out of scope?"

**Analogy:** A tailor does not start cutting fabric when you walk in. They ask
your size, the occasion, the fabric preference, and the deadline. Cutting first
means a wrong fit. Asking first means a perfect suit.

**Template to say out loud:**
> "Before I start designing, let me clarify a few things. I want to make sure
> I am solving the right problem, not just A problem."

---

### Phase 2: Identify Entities and Relationships (5 minutes)

**What it is:** Extract nouns from the requirements. Each noun is a potential class.
Each relationship between nouns is a potential association, aggregation, or
composition.

**Steps:**
1. Say the problem back in your own words.
2. Underline every noun — those are your classes.
3. Underline every verb — those are your methods.
4. Ask yourself: "Does this class OWN that class, or just USE it?"

**Ownership vs Usage:**
- A `Car` OWNS its `Engine` — if the car is destroyed, the engine is too.
  This is **Composition**.
- A `Driver` USES a `Car` — the driver can exist without a car.
  This is **Association**.
- A `Zoo` OWNS its `Animals` — but animals have their own lifecycle in some
  designs. This is **Aggregation**.

**Output at this phase:** A rough list like:

```
Classes: User, Booking, Seat, Movie, Theater, Payment
Relationships:
  - Theater has many Seats (Composition)
  - User makes many Bookings (Association)
  - Booking contains one Payment (Aggregation)
```

---

### Phase 3: Draw the UML / Whiteboard Diagram (5–7 minutes)

**What it is:** Sketch the class diagram on the whiteboard (or virtual
equivalent). You do not need to be an artist. You need to be clear.

**What to draw:**
- Boxes for each class with key attributes and methods
- Lines showing relationships: `---` for association, `◆---` for composition,
  `<|---` for inheritance, `<..` for dependency
- Multiplicity markers: `1`, `*`, `0..1`

**What to SAY while drawing:**
> "I am making Theater have a composition relationship with Seat, because
> if a Theater is removed from the system, its seats become meaningless.
> They do not exist independently."

Talking while drawing shows your thought process. Silence while drawing looks
like you are guessing.

**Tip:** Draw from top-level aggregates down. Start with the biggest box
(the facade / entry point), then expand inward.

---

### Phase 4: Discuss Design Patterns (3–5 minutes)

**What it is:** Name the patterns you are applying and WHY, not just HOW.

**Template:**
> "For the discount calculation, I will use the Strategy Pattern. This lets me
> swap between PercentageDiscount, FlatDiscount, and BuyOneGetOne at runtime
> without changing the order class. If we add a new promotion type next quarter,
> we add a new Strategy class — nothing existing breaks."

Naming patterns shows you have vocabulary. Explaining WHY shows you have wisdom.

**Common patterns and their one-line justification:**

| Pattern | When to use |
|---------|------------|
| Strategy | Multiple interchangeable algorithms |
| Observer | One event, many listeners |
| Factory | Object creation logic needs to be centralized |
| Singleton | Exactly one instance needed globally |
| Command | Encapsulate requests as objects (undo/redo) |
| State | Object behavior changes based on internal state |
| Decorator | Add features to objects without subclassing |
| Facade | Simplify a complex subsystem behind one interface |
| Builder | Step-by-step construction of complex objects |
| Template Method | Algorithm skeleton with customizable steps |

---

### Phase 5: Code the Core Classes (10–15 minutes)

**What it is:** Write Python (or whatever language you chose) for the 3–4 most
important classes. You do not need to code everything. Show the skeleton and
fill in the meaty methods.

**Priority order for what to code:**
1. The core domain model (the most important class — e.g., `Booking`, `Elevator`)
2. The pattern implementation (e.g., Strategy, Observer)
3. The entry point or facade
4. Edge cases in methods (e.g., what if seat is already booked?)

**What NOT to do:**
- Do not spend 10 minutes writing getters/setters. Say "I will add getters but
  skip them for brevity."
- Do not start with helper utilities. Start with business logic.
- Do not go silent. Narrate your decisions as you type.

---

### Talk Track Summary

```
"Let me start by clarifying requirements..."          (Phase 1)
"Now let me identify the key entities..."             (Phase 2)
"I'll sketch the class diagram here..."               (Phase 3)
"I see at least two patterns that apply here..."      (Phase 4)
"Let me code the core classes, starting with..."      (Phase 5)
"One tricky design decision here is..."               (throughout)
"A trade-off I am making is..."                       (throughout)
"In a real production system I would also..."         (at the end)
```

---

## Part 2: Top 20 LLD Interview Questions for SDE-3

---

### Question 1: Design a Vending Machine

**The Question:**
Design a vending machine that sells multiple products, accepts coins and
notes, returns change, and handles out-of-stock and insufficient-funds scenarios.

**Key Entities to Identify:**
- `VendingMachine` (Facade, Singleton)
- `Product` (what is being sold)
- `Slot` (physical location inside the machine, holds a product and quantity)
- `Coin` / `Note` (payment)
- `Payment` (aggregates coins/notes)
- `Inventory` (manages all slots)
- `VendingMachineState` (Idle, HasMoney, Dispensing, OutOfStock)
- `ChangeDispenser` (handles returning change)

**Key Patterns to Apply:**
- **State Pattern** — machine behavior changes based on state (Idle vs HasMoney
  vs Dispensing). You cannot select a product if no money is inserted.
- **Singleton** — one vending machine instance
- **Strategy** — change calculation (greedy coin selection)

**Model Answer Paragraph:**
> "The core challenge here is that the machine's behavior changes completely
> depending on what state it is in. If I try to handle all states with if-else
> inside one class, I get a god class immediately. Instead, I will use the
> State Pattern. Each state — Idle, HasMoney, Dispensing — is its own class
> with its own response to events like insertCoin() or selectProduct(). The
> machine delegates to its current state. This means adding a new state like
> Maintenance or CardPayment is just adding a new class. A tricky decision is
> how to handle partial payment — should money be returned instantly on
> insufficient funds, or held until the user asks for refund? I would hold it
> until explicitly refunded, which is what real machines do."

**Classes and Relationships:**

```
VendingMachine ◆── Inventory ◆── Slot ◆── Product
VendingMachine ◆── VendingMachineState (current state)
VendingMachine ◆── ChangeDispenser
VendingMachineState <|── IdleState
VendingMachineState <|── HasMoneyState
VendingMachineState <|── DispensingState
```

**One Tricky Design Decision:**
Should `Coin` be an enum or a class? Use an enum — coins have fixed
denominations (1, 2, 5, 10, 20, 50, 100 rupees). No need for a full class.

```python
from enum import Enum
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class Coin(Enum):
    ONE = 1
    TWO = 2
    FIVE = 5
    TEN = 10
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100


class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price


class Slot:
    def __init__(self, slot_id: str, product: Product, quantity: int):
        self.slot_id = slot_id
        self.product = product
        self.quantity = quantity

    def is_available(self) -> bool:
        return self.quantity > 0

    def dispense(self) -> Product:
        if not self.is_available():
            raise Exception(f"Slot {self.slot_id} is empty")
        self.quantity -= 1
        return self.product


class VendingMachineState(ABC):
    @abstractmethod
    def insert_coin(self, machine: "VendingMachine", coin: Coin): pass

    @abstractmethod
    def select_product(self, machine: "VendingMachine", slot_id: str): pass

    @abstractmethod
    def dispense(self, machine: "VendingMachine"): pass

    @abstractmethod
    def cancel(self, machine: "VendingMachine"): pass


class IdleState(VendingMachineState):
    def insert_coin(self, machine, coin):
        machine.add_coin(coin)
        print(f"Coin inserted: {coin.value}. Total: {machine.inserted_amount}")
        machine.set_state(machine.has_money_state)

    def select_product(self, machine, slot_id):
        print("Please insert money first.")

    def dispense(self, machine):
        print("No product selected.")

    def cancel(self, machine):
        print("Nothing to cancel.")


class HasMoneyState(VendingMachineState):
    def insert_coin(self, machine, coin):
        machine.add_coin(coin)
        print(f"Coin inserted: {coin.value}. Total: {machine.inserted_amount}")

    def select_product(self, machine, slot_id):
        slot = machine.inventory.get_slot(slot_id)
        if not slot:
            print("Invalid slot.")
            return
        if not slot.is_available():
            print("Product out of stock.")
            return
        if machine.inserted_amount < slot.product.price:
            print(f"Insufficient funds. Need {slot.product.price - machine.inserted_amount} more.")
            return
        machine.selected_slot = slot
        machine.set_state(machine.dispensing_state)
        machine.current_state.dispense(machine)

    def dispense(self, machine):
        print("Select a product first.")

    def cancel(self, machine):
        machine.return_change(machine.inserted_amount)
        machine.inserted_amount = 0
        machine.set_state(machine.idle_state)


class DispensingState(VendingMachineState):
    def insert_coin(self, machine, coin):
        print("Please wait, dispensing product.")

    def select_product(self, machine, slot_id):
        print("Please wait, dispensing product.")

    def dispense(self, machine):
        product = machine.selected_slot.dispense()
        change = machine.inserted_amount - product.price
        print(f"Dispensed: {product.name}")
        if change > 0:
            machine.return_change(change)
        machine.inserted_amount = 0
        machine.selected_slot = None
        machine.set_state(machine.idle_state)

    def cancel(self, machine):
        print("Cannot cancel while dispensing.")


class Inventory:
    def __init__(self):
        self._slots: Dict[str, Slot] = {}

    def add_slot(self, slot: Slot):
        self._slots[slot.slot_id] = slot

    def get_slot(self, slot_id: str) -> Optional[Slot]:
        return self._slots.get(slot_id)


class VendingMachine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.inventory = Inventory()
        self.inserted_amount: float = 0
        self.selected_slot: Optional[Slot] = None
        self._coins_inserted: List[Coin] = []

        # States
        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()
        self.current_state: VendingMachineState = self.idle_state
        self._initialized = True

    def set_state(self, state: VendingMachineState):
        self.current_state = state

    def add_coin(self, coin: Coin):
        self._coins_inserted.append(coin)
        self.inserted_amount += coin.value

    def return_change(self, amount: float):
        print(f"Returning change: {amount}")

    def insert_coin(self, coin: Coin):
        self.current_state.insert_coin(self, coin)

    def select_product(self, slot_id: str):
        self.current_state.select_product(self, slot_id)

    def cancel(self):
        self.current_state.cancel(self)
```

---

### Question 2: Design an ATM

**The Question:**
Design an ATM system that lets users authenticate with card and PIN, check
balance, withdraw cash, deposit, and transfer funds.

**Key Entities to Identify:**
- `ATM` (Facade)
- `Card` (holds card number, linked account)
- `Account` (Bank account — holds balance)
- `Transaction` (Withdrawal, Deposit, Transfer)
- `CashDispenser` (hardware — dispenses physical cash)
- `ATMState` (NoCard, HasCard, Authenticated, SelectingTransaction)
- `Bank` (validates PIN, holds accounts)
- `Receipt` (transaction record)

**Key Patterns to Apply:**
- **State Pattern** — ATM transitions through very clear states
- **Strategy Pattern** — different transaction types (withdraw, deposit, transfer)
  each implement a `Transaction` interface
- **Facade** — ATM class hides the complexity of PIN validation, bank API, cash
  dispenser hardware

**Model Answer Paragraph:**
> "An ATM is one of the cleanest State Pattern examples because the machine
> literally blocks you from doing things out of order. You cannot withdraw
> before authenticating. You cannot authenticate before inserting a card.
> Each state knows exactly what actions are legal. I will model states as
> classes: NoCardState, CardInsertedState, AuthenticatedState. The ATM delegates
> every action to its current state. When the state changes, the next action
> set changes automatically. The tricky part is the CashDispenser — it is
> hardware, so I will wrap it behind an interface. In tests I can mock it.
> In production it calls the real dispenser. This is the Facade + Dependency
> Inversion working together."

**Classes and Relationships:**

```
ATM ◆── CashDispenser
ATM ◆── CardReader
ATM ◆── ATMState
ATM --uses--> Bank (external service)
Account --has--> Transaction history
Transaction <|── Withdrawal
Transaction <|── Deposit
Transaction <|── Transfer
```

**One Tricky Design Decision:**
Where does PIN validation live? In `ATM`, `Bank`, or `Account`? It should live
in `Bank` — the ATM is just a terminal. The bank owns the authentication logic.
This means your ATM does not store PINs — it just forwards the card number and
entered PIN to the bank service and gets back a yes/no.

---

### Question 3: Design a Chess Game

**The Question:**
Design a two-player chess game. Handle piece movement, turn management,
check/checkmate detection, and game state.

**Key Entities to Identify:**
- `Game` (manages overall game flow)
- `Board` (8x8 grid)
- `Cell` (one square on the board)
- `Piece` (abstract — King, Queen, Rook, Bishop, Knight, Pawn)
- `Player` (White, Black — has a color and a set of pieces)
- `Move` (from cell, to cell, piece, captured piece)
- `GameStatus` (Active, Check, Checkmate, Stalemate, Draw)

**Key Patterns to Apply:**
- **Template Method** — `Piece.is_valid_move()` defines the skeleton, each
  subclass fills in the specific movement logic
- **Command Pattern** — `Move` is a command; support undo by reversing moves
- **Observer** — `GameStatusObserver` watches for check/checkmate conditions
  after each move

**Model Answer Paragraph:**
> "The core of chess is validating moves. Every piece moves differently, but
> the validation process has the same shape: check if the destination is on the
> board, check if the path is clear (for sliding pieces), check if the move
> leaves your own king in check. I will use Template Method — the base Piece
> class defines this skeleton and each subclass overrides the specific geometry.
> A tricky decision is check detection. After every move, I need to check if
> the opponent's king is in check. Rather than a brute-force scan, I check if
> any of the current player's pieces can attack the opponent's king position.
> Checkmate is check with no legal moves remaining — I verify this by trying
> every possible move and seeing if any resolves the check."

**Classes and Relationships:**

```
Game ◆── Board
Board ◆── Cell[8][8]
Cell ◆── Piece (0 or 1)
Piece <|── King, Queen, Rook, Bishop, Knight, Pawn
Game ◆── Player[2]
Player ◆── List[Piece]
Game ◆── List[Move] (move history)
```

**One Tricky Design Decision:**
Should `Board` know about chess rules, or just store cells? Keep `Board` dumb —
it just stores and retrieves cells. Put rule validation in a `MoveValidator`
class. This separates data from logic and makes rule changes easier.

---

### Question 4: Design a Hotel Booking System

**The Question:**
Design a hotel booking system where users can search rooms by date, type, and
availability; make bookings; and cancel with refund policies.

**Key Entities to Identify:**
- `Hotel` (has rooms, name, location)
- `Room` (number, type, price per night, status)
- `RoomType` (Standard, Deluxe, Suite — enum)
- `Booking` (guest, room, check-in, check-out, status)
- `Guest` (user details)
- `Payment` (booking payment)
- `CancellationPolicy` (strategy for refund calculation)
- `SearchService` (find available rooms)

**Key Patterns to Apply:**
- **Strategy Pattern** — cancellation policies (FreeCancellation,
  PartialRefund, NoRefund) are swappable
- **Builder Pattern** — building a `SearchQuery` with optional filters
  (dates, room type, amenities, price range)
- **Observer Pattern** — notify guest via email/SMS when booking status changes

**Model Answer Paragraph:**
> "Hotel booking has two very different workflows: searching and booking.
> For search, I will use a Builder to construct a flexible query object —
> the user may want to filter by date only, or by date plus room type, or
> by all criteria. A Builder lets me add filters incrementally without a
> constructor with 10 parameters. For cancellation, different hotels have
> different policies. A Strategy Pattern lets each booking carry its own
> CancellationPolicy. When the guest cancels, the policy calculates the
> refund. Swapping from FreeCancellation to PartialRefund for a specific
> booking requires zero changes to the Booking class itself."

**Classes and Relationships:**

```
Hotel ◆── List[Room]
Room --has--> RoomType (enum)
Booking --links--> Room, Guest, Payment
Booking ◆── CancellationPolicy (Strategy)
CancellationPolicy <|── FreeCancellation
CancellationPolicy <|── PartialRefund
CancellationPolicy <|── NonRefundable
SearchService --uses--> Hotel
Guest --has--> List[Booking]
```

**One Tricky Design Decision:**
How do you prevent double-booking? Use optimistic locking (check availability
and mark room as reserved in a transaction) or a `RoomLock` mechanism that
reserves the room for 15 minutes during checkout. Show you have thought about
race conditions.

---

### Question 5: Design a Food Delivery System (Swiggy / Zomato)

**The Question:**
Design a food delivery platform. Users browse restaurants, add items to a cart,
place orders, and track delivery in real time.

**Key Entities to Identify:**
- `User` (customer)
- `Restaurant` (menu, location, operating hours)
- `MenuItem` (name, price, category, availability)
- `Cart` (temporary order before checkout)
- `Order` (confirmed cart with status)
- `DeliveryAgent` (courier with location)
- `OrderStatus` (Placed, Accepted, Preparing, PickedUp, Delivered)
- `Notification` (SMS/email/push for status updates)
- `Payment` (UPI, card, COD)

**Key Patterns to Apply:**
- **Observer Pattern** — when `Order.status` changes, notify User, Restaurant,
  and DeliveryAgent
- **Strategy Pattern** — delivery fee calculation (distance-based,
  surge-based, flat-rate)
- **State Pattern** — `Order` transitions through states with enforced rules
  (cannot move from Delivered back to Preparing)
- **Factory Pattern** — `NotificationFactory` creates Email/SMS/Push notifications

**Model Answer Paragraph:**
> "The most interesting design challenge here is order status tracking. The
> order goes through clearly defined states and can only transition in one
> direction — you cannot undeliver an order. I will use the State Pattern so
> each status enforces its own transition rules. When state changes, multiple
> parties need to know: the user wants a push notification, the restaurant
> dashboard updates, the delivery agent app updates. I will use Observer for
> this — OrderStatusChanged event triggers all registered listeners. The
> delivery fee calculation varies by time of day and distance, so Strategy
> Pattern fits perfectly. I will mention that in a real system, delivery
> tracking would use a separate real-time service (like WebSockets or
> Server-Sent Events), not polling."

**Classes and Relationships:**

```
User --places--> Order
Restaurant ◆── List[MenuItem]
Order ◆── List[OrderItem]
OrderItem --references--> MenuItem
Order --assigned--> DeliveryAgent
Order ◆── OrderState (State Pattern)
Order --publishes--> OrderStatusChangedEvent (Observer)
OrderStatusChangedEvent --notifies--> User, Restaurant, DeliveryAgent
```

**One Tricky Design Decision:**
Should `Cart` and `Order` be the same class? No — keep them separate. `Cart`
is mutable, ephemeral, and user-facing. `Order` is immutable after placement,
has a payment, a delivery agent, and a full audit trail. Merging them creates
a god class that violates SRP.

---

### Question 6: Design a Movie Ticket Booking System (BookMyShow)

**The Question:**
Design a system where users can browse movies and shows, select seats, make
payment, and receive booking confirmation.

**Key Entities to Identify:**
- `Movie` (title, genre, duration, rating)
- `Theater` (name, location, list of screens)
- `Screen` (within a theater, has seats and shows)
- `Show` (specific screening — movie + screen + datetime)
- `Seat` (row, number, type — Regular/Premium/Recliner, status)
- `Booking` (user, show, seats, payment, confirmation code)
- `Payment` (amount, method, status)
- `User` (customer)

**Key Patterns to Apply:**
- **Singleton** — `BookingService` manages all bookings
- **Observer** — notify user on booking confirmation and cancellation
- **Factory** — create different seat types (Regular, Premium, Recliner)
  with different pricing

**Model Answer Paragraph:**
> "The hardest part of this system is the concurrent seat selection problem.
> Two users can see the same seat as available and both try to book it at the
> same time. In a real system I would use a distributed lock or a database
> transaction with row-level locking. In the LLD scope, I will model a
> SeatLock mechanism that temporarily reserves seats for 10 minutes when a user
> starts the booking flow. If they do not complete payment, the lock expires
> and the seat becomes available again. This is exactly how real-world ticket
> systems work — you have seen the countdown timer on BookMyShow. That timer
> is the lock expiry."

**Classes and Relationships:**

```
Theater ◆── List[Screen]
Screen ◆── List[Seat]
Screen --hosts--> List[Show]
Show --references--> Movie, Screen
Booking --references--> Show, User
Booking ◆── List[Seat] (booked)
Booking ◆── Payment
Seat --has--> SeatType (enum), SeatStatus (enum)
```

**One Tricky Design Decision:**
How do you model seat availability? Do not put a boolean `is_booked` on `Seat`
directly. Use a `SeatStatus` enum: Available, Locked, Booked. This supports
the lock-then-confirm flow cleanly. A seat can be Locked (someone is checking
out) without being permanently Booked.

---

### Question 7: Design a Ride Sharing System (Uber / Ola)

**The Question:**
Design a ride hailing app where riders request rides, nearby drivers are matched,
trips are tracked, and payment is processed on completion.

**Key Entities to Identify:**
- `Rider` (user requesting a ride)
- `Driver` (with vehicle, current location, availability status)
- `Vehicle` (make, model, license plate, type — Sedan/SUV/Auto)
- `Trip` (rider, driver, start/end location, fare, status)
- `Location` (latitude, longitude)
- `TripStatus` (Requested, DriverAssigned, InProgress, Completed, Cancelled)
- `FareCalculator` (Strategy for surge pricing, base fare)
- `MatchingService` (finds nearest available driver)

**Key Patterns to Apply:**
- **Strategy Pattern** — fare calculation (normal, surge, subscription)
- **Observer Pattern** — rider and driver both track trip status changes
- **State Pattern** — `Trip` transitions through states
- **Factory Pattern** — create different vehicle types with different
  base fares

**Model Answer Paragraph:**
> "The key algorithmic challenge is driver matching — finding the nearest
> available driver efficiently. In a real system this is a geospatial query
> (PostGIS, Elasticsearch with geo queries, or a specialized service). In
> the LLD design, I will model a MatchingService with a Strategy interface.
> Today it uses a simple nearest-driver algorithm. Tomorrow it can use
> a machine learning model that considers traffic, driver ratings, and
> estimated arrival time. The fare calculation is also a Strategy — during
> surge hours, the SurgePricingStrategy multiplies base fare by a dynamic
> multiplier. During normal hours, the BaseFareStrategy applies. The rider
> does not need to know which strategy is active."

**Classes and Relationships:**

```
Rider --requests--> Trip
Trip --assigns--> Driver
Driver ◆── Vehicle
Trip --uses--> FareCalculator (Strategy)
FareCalculator <|── BaseFareStrategy
FareCalculator <|── SurgePricingStrategy
MatchingService --queries--> List[Driver] (active drivers)
Trip ◆── TripState (State Pattern)
```

**One Tricky Design Decision:**
Should `Driver` store location or should there be a separate `DriverLocation`
service? Separate it — location updates happen every few seconds and should go
to a dedicated location tracking service, not the main `Driver` entity. This
is the Single Responsibility Principle at the service level.

---

### Question 8: Design Snake and Ladder Game

**The Question:**
Design a Snake and Ladder board game supporting multiple players, snakes,
ladders, dice rolling, and turn management.

**Key Entities to Identify:**
- `Game` (manages flow, win condition)
- `Board` (100 cells, snakes, ladders)
- `Cell` (position 1–100, optional snake or ladder)
- `Snake` (head position, tail position)
- `Ladder` (bottom position, top position)
- `Player` (name, current position)
- `Dice` (number of dice, roll logic)

**Key Patterns to Apply:**
- **Template Method** — `Game.play_turn()` defines the skeleton (roll, move,
  check snake/ladder, check win)
- **Strategy Pattern** — dice rolling strategy (normal, loaded/biased for
  testing)
- **Iterator** — cycling through players in order

**Model Answer Paragraph:**
> "This looks simple but has elegant design opportunities. The board setup is
> just data — snakes and ladders are a dictionary mapping head to tail or
> bottom to top. When a player lands on a cell, I check if there is a
> teleporter at that position. A snake teleports down; a ladder teleports up.
> The same lookup handles both if I use a unified SpecialCell map. The tricky
> part is making this testable — dice are random, which breaks unit tests.
> I will inject dice as a Strategy so in tests I inject a MockDice that always
> returns a specific value. This is Dependency Inversion in action."

**Classes and Relationships:**

```
Game ◆── Board
Board ◆── Dict[int, int] (teleporters: snakes + ladders)
Game ◆── List[Player]
Game ◆── Dice (Strategy)
Dice <|── RandomDice
Dice <|── MockDice (for testing)
```

**One Tricky Design Decision:**
Should snakes and ladders be separate classes or one unified `Teleporter`? Use
one `Teleporter` class with a direction indicator. Keeps the code DRY and
the board's lookup dictionary simple.

```python
from abc import ABC, abstractmethod
from typing import Dict, List
import random


class Dice(ABC):
    @abstractmethod
    def roll(self) -> int:
        pass


class RandomDice(Dice):
    def __init__(self, num_dice: int = 1):
        self.num_dice = num_dice

    def roll(self) -> int:
        return sum(random.randint(1, 6) for _ in range(self.num_dice))


class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0

    def move(self, steps: int, board_size: int):
        new_pos = self.position + steps
        if new_pos <= board_size:
            self.position = new_pos


class Board:
    def __init__(self, size: int = 100):
        self.size = size
        # key = landing position, value = teleport destination
        self._teleporters: Dict[int, int] = {}

    def add_snake(self, head: int, tail: int):
        assert head > tail, "Snake head must be above tail"
        self._teleporters[head] = tail

    def add_ladder(self, bottom: int, top: int):
        assert top > bottom, "Ladder top must be above bottom"
        self._teleporters[bottom] = top

    def get_final_position(self, position: int) -> int:
        return self._teleporters.get(position, position)


class Game:
    def __init__(self, players: List[Player], board: Board, dice: Dice):
        self.players = players
        self.board = board
        self.dice = dice
        self._current_index = 0
        self._winner = None

    def _current_player(self) -> Player:
        return self.players[self._current_index]

    def _next_player(self):
        self._current_index = (self._current_index + 1) % len(self.players)

    def play_turn(self) -> bool:
        """Returns True if the game is over."""
        player = self._current_player()
        roll = self.dice.roll()
        print(f"{player.name} rolls {roll}")
        player.move(roll, self.board.size)
        final = self.board.get_final_position(player.position)
        if final != player.position:
            action = "climbs ladder to" if final > player.position else "slides snake to"
            print(f"{player.name} {action} {final}")
            player.position = final
        print(f"{player.name} is now at position {player.position}")
        if player.position == self.board.size:
            self._winner = player
            print(f"{player.name} WINS!")
            return True
        self._next_player()
        return False

    def play(self):
        while not self.play_turn():
            pass
```

---

### Question 9: Design a Social Media Platform (Twitter / Instagram)

**The Question:**
Design a social media platform with user profiles, posts, followers, likes,
comments, feed generation, and notifications.

**Key Entities to Identify:**
- `User` (profile, followers, following)
- `Post` (text, media, timestamp, author)
- `Comment` (text, author, parent post)
- `Like` (user, target — post or comment)
- `Follow` (follower, followee)
- `Feed` (personalized list of posts)
- `Notification` (type: like, comment, follow, mention)
- `NotificationService` (dispatches notifications)

**Key Patterns to Apply:**
- **Observer Pattern** — when a user posts, all followers' feeds update;
  likes and comments trigger notifications
- **Decorator Pattern** — posts can have layers of content: text-only,
  text with image, text with video, text with poll
- **Factory Pattern** — `NotificationFactory` creates different notification
  types

**Model Answer Paragraph:**
> "Feed generation is the hardest problem here. For a small system, I can
> pull posts from all followed users ordered by time — this is a pull model.
> But at Twitter's scale, pre-computing feeds (push model) is necessary:
> when a user posts, the system pushes that post into every follower's
> feed cache. I will mention both approaches and say for this design I will
> implement the pull model for simplicity, noting the trade-off. For
> notifications, Observer is the right fit — the Post entity publishes events
> (liked, commented) and the NotificationService is a subscriber. New
> notification types just add new subscribers — open for extension, closed
> for modification."

**Classes and Relationships:**

```
User --has--> List[Post]
User --follows--> List[User]
Post --has--> List[Comment], List[Like]
Post --publishes--> PostEvent (Observer)
NotificationService --subscribes--> PostEvent
FeedService --reads--> User.following --aggregates--> Posts
```

**One Tricky Design Decision:**
Should `Like` apply to both posts and comments? Use a polymorphic `Likeable`
interface that both `Post` and `Comment` implement. This lets you add other
likeable entities in the future (Stories, Reels) without changing the `Like`
class.

---

### Question 10: Design a Shopping Cart

**The Question:**
Design an e-commerce shopping cart that holds items, applies coupons and
discounts, calculates totals, and checks out.

**Key Entities to Identify:**
- `Cart` (per-user, holds items)
- `CartItem` (product reference + quantity)
- `Product` (id, name, price, inventory)
- `Coupon` (code, discount type, validity)
- `Discount` (amount or percentage)
- `PriceCalculator` (total with discounts)
- `Checkout` (initiates payment flow)
- `Order` (result of completed checkout)

**Key Patterns to Apply:**
- **Strategy Pattern** — discount application: PercentageDiscount,
  FlatDiscount, BuyXGetY
- **Decorator Pattern** — layer discounts on top of each other:
  10% off + free shipping + coupon code
- **Builder Pattern** — `OrderBuilder` collects cart, address, payment
  method, and builds an Order

**Model Answer Paragraph:**
> "Discount calculation is the classic place to reach for Decorator. A cart
> starts with a base price. Then I apply a membership discount. On top of that,
> a seasonal coupon. On top of that, a minimum order discount. Each decorator
> wraps the previous one and adds its own reduction. This makes the combination
> of discounts composable — I can add new discount types without changing any
> existing code. The checkout flow itself uses a Builder — collecting all the
> pieces (cart contents, delivery address, payment method) before creating a
> single immutable Order. Once the Order is created, the cart is cleared."

**Classes and Relationships:**

```
Cart ◆── List[CartItem]
CartItem --references--> Product
Cart --uses--> PriceCalculator (Strategy / Decorator chain)
Checkout --reads--> Cart
Checkout --builds--> Order (Builder)
Order --references--> Payment, DeliveryAddress
```

**One Tricky Design Decision:**
Should the cart store `Product` or `CartItem`? Always `CartItem` — it holds
the quantity AND the price AT THE TIME of adding. If the product price changes
while the cart is open, the cart item price is locked. This prevents
a common UX bug.

---

### Question 11: Design a Chat System (WhatsApp / Slack)

**The Question:**
Design a real-time chat system supporting 1-to-1 and group messaging, message
delivery status (sent, delivered, read), and media sharing.

**Key Entities to Identify:**
- `User` (profile, online status, last seen)
- `Message` (sender, content, timestamp, type, status)
- `Chat` / `Conversation` (1-to-1 or group)
- `Group` (name, admin, members)
- `MessageStatus` (Sent, Delivered, Read)
- `Notification` (new message alert)
- `MediaMessage` (extends Message with file/image)

**Key Patterns to Apply:**
- **Observer Pattern** — when a message is received, all participants in the
  chat are notified
- **Decorator Pattern** — Message types: TextMessage is base; MediaMessage
  decorates with media URL; ForwardedMessage decorates with original sender
- **Command Pattern** — messages are commands that can be queued for offline
  delivery

**Model Answer Paragraph:**
> "The offline delivery problem is interesting. When a user is offline,
> messages should queue up and deliver when they reconnect. I will use the
> Command Pattern — each Message is a command. An offline user's message queue
> holds commands. When the user reconnects, the queue flushes. For group chats,
> a message is delivered when ALL members have received it (delivered status),
> and read-receipts are individual. I will track delivery separately per
> recipient rather than on the Message itself. A group of 500 users would
> need 500 delivery records per message — that is a trade-off worth mentioning."

**Classes and Relationships:**

```
User --participates-in--> List[Chat]
Chat <|── DirectChat
Chat <|── GroupChat
Chat ◆── List[Message]
Message <|── TextMessage
Message <|── MediaMessage
Message --has--> Dict[User, MessageStatus] (per-recipient delivery)
GroupChat ◆── List[User] (members)
```

**One Tricky Design Decision:**
Should `MessageStatus` live on `Message` or in a separate table? In a group
chat, status is per-recipient. So a `MessageDelivery` join entity is better:
`(message_id, user_id, status)`. Putting status on Message only works for
1-to-1 chats.

---

### Question 12: Design Splitwise / Bill Splitting App

**The Question:**
Design an app where groups of friends can log shared expenses, split bills
in various ways, and track who owes whom.

**Key Entities to Identify:**
- `User` (name, email, balance)
- `Group` (members, list of expenses)
- `Expense` (amount, paid by, split among, split type)
- `Split` (user, amount owed)
- `SplitType` (Equal, Exact, Percentage, Share-based)
- `Settlement` (user A pays user B — closes a debt)
- `BalanceSheet` (net amount owed between any two users)

**Key Patterns to Apply:**
- **Strategy Pattern** — split calculation: EqualSplit, ExactSplit,
  PercentageSplit, ShareBasedSplit each implement `SplitStrategy`
- **Command Pattern** — each expense or settlement is a command that modifies
  balances; supports undo

**Model Answer Paragraph:**
> "The split calculation is the heart of this system and a perfect Strategy
> Pattern application. When creating an expense, the user picks a split type.
> The expense delegates the split calculation to the chosen strategy. EqualSplit
> divides amount by number of users. PercentageSplit applies each user's
> percentage. ShareBasedSplit calculates proportional shares. Each is a separate
> class — adding a new split type like TipSplit requires zero changes to the
> Expense class. For settling debts, rather than tracking every pairwise debt
> (which grows as O(n²)), I track each user's net balance. Settlement
> minimization (finding the fewest transactions to settle all debts) is a
> classic greedy algorithm problem."

**Classes and Relationships:**

```
Group ◆── List[User], List[Expense]
Expense ◆── List[Split]
Expense --uses--> SplitStrategy (Strategy)
SplitStrategy <|── EqualSplit
SplitStrategy <|── ExactSplit
SplitStrategy <|── PercentageSplit
Settlement --records--> payer, payee, amount
User --has--> Dict[User, float] (balance with each other user)
```

**One Tricky Design Decision:**
Debt simplification — should the app minimize the number of transactions? Yes,
but flag this as optional and explain the algorithm: compute each user's net
balance, then greedily match the largest positive balance with the largest
negative balance. A user who owes $10 net can settle with one payment instead
of multiple smaller ones.

---

### Question 13: Design an Online Judge (LeetCode)

**The Question:**
Design an online code judge where users submit code solutions, which are
compiled and run against test cases, with results returned.

**Key Entities to Identify:**
- `Problem` (title, description, test cases, constraints)
- `TestCase` (input, expected output, time/memory limits)
- `Submission` (user, problem, code, language, status)
- `Judge` (executes code, compares output)
- `Verdict` (Accepted, Wrong Answer, TLE, MLE, Compile Error, Runtime Error)
- `Language` (Python, Java, C++ — each has a compiler/interpreter)
- `Sandbox` (isolated execution environment)
- `Leaderboard` (ranked by score and time)

**Key Patterns to Apply:**
- **Strategy Pattern** — each `Language` has a compile-and-run strategy
- **Command Pattern** — each `Submission` is a command queued for execution
- **Observer Pattern** — when a submission is judged, notify the user
- **Factory Pattern** — `JudgeFactory` creates the right judge based on language

**Model Answer Paragraph:**
> "The most critical design concern here is security and isolation. User code
> is untrusted — it can be malicious, infinite-looping, or memory-hogging.
> The Sandbox is the key abstraction. The Judge does not run code directly;
> it delegates to a Sandbox that enforces CPU and memory limits and kills
> processes that exceed them. The Sandbox is a hardware/OS concern — in the
> LLD, I model it as an interface. Different languages need different execution
> environments, so a LanguageStrategy encapsulates compile + run for each
> language. A StrategyFactory picks the right one based on the submission's
> language field."

**Classes and Relationships:**

```
Problem ◆── List[TestCase]
Submission --references--> Problem, User
Submission --has--> Verdict
Judge --uses--> LanguageStrategy (Strategy)
Judge --uses--> Sandbox
LanguageStrategy <|── PythonStrategy
LanguageStrategy <|── JavaStrategy
LanguageStrategy <|── CppStrategy
SubmissionQueue --delivers--> Judge (Command Pattern)
```

**One Tricky Design Decision:**
Should all test cases run even after the first failure? No — fail-fast for Wrong
Answer. But run all test cases for TLE detection (maybe only test case 50 out
of 100 causes TLE). Configuration determines behavior — make this configurable
per problem.

---

### Question 14: Design a Traffic Light System

**The Question:**
Design a traffic light system for an intersection that manages light state,
timing, and pedestrian signals. Support emergency vehicle override.

**Key Entities to Identify:**
- `TrafficLight` (one light unit — red, yellow, green)
- `Intersection` (manages a set of traffic lights)
- `TrafficLightState` (Red, Yellow, Green)
- `Timer` (controls duration of each state)
- `PedestrianSignal` (walk/don't walk)
- `EmergencyOverride` (switches all to red except emergency path)
- `TrafficController` (central controller managing multiple intersections)

**Key Patterns to Apply:**
- **State Pattern** — a traffic light IS a state machine: Red → Green →
  Yellow → Red
- **Observer Pattern** — when a light changes to Green, the pedestrian signal
  on that crossing changes to Don't Walk
- **Command Pattern** — emergency override is a command that can be
  issued and then reverted

**Model Answer Paragraph:**
> "A traffic light is perhaps the most textbook State Pattern example in
> existence. Each state has a fixed duration, transitions to exactly one next
> state, and has a defined behavior (what signals to show). I will model each
> state as a class with a handle() method that performs the transition after
> the timer fires. The emergency override is a Command — it saves the current
> state, applies the override (all red), and when cancelled, restores the
> saved state. This is the memento-like restoration combined with Command.
> I will also mention that in a real system, the controller receives real-time
> traffic density data from sensors and adapts timing dynamically — that would
> be a Strategy for timing calculation."

**Classes and Relationships:**

```
Intersection ◆── List[TrafficLight]
Intersection ◆── List[PedestrianSignal]
TrafficLight ◆── TrafficLightState (current)
TrafficLightState <|── RedState, GreenState, YellowState
TrafficController ◆── List[Intersection]
EmergencyOverride --commands--> TrafficController
```

**One Tricky Design Decision:**
How do you coordinate opposing traffic lights at the same intersection? When
North-South is green, East-West must be red. Model this as a phase in the
Intersection, not as independent lights. The Intersection class manages which
phase (set of light states) is active.

---

### Question 15: Design a Car Rental System

**The Question:**
Design a car rental system where users can search available cars by date,
type, and location; reserve them; and return them with damage assessment.

**Key Entities to Identify:**
- `Car` (make, model, license plate, type, status)
- `CarType` (Economy, Compact, SUV, Luxury — enum)
- `RentalLocation` (branch with available cars)
- `Reservation` (user, car, pickup/return date, location)
- `Rental` (active rental — links reservation to actual usage)
- `DamageReport` (photos, damage description, penalty)
- `RentalPriceCalculator` (Strategy for pricing)
- `User` (with driver's license, payment info)

**Key Patterns to Apply:**
- **Strategy Pattern** — pricing: daily rate, weekend rate, loyalty discount
- **Builder Pattern** — search query for cars
- **State Pattern** — car status: Available, Reserved, Rented, UnderMaintenance

**Model Answer Paragraph:**
> "A car has a lifecycle that maps perfectly to the State Pattern: Available
> means anyone can reserve it. Reserved means it is held for a specific user.
> Rented means it is currently out. UnderMaintenance means it cannot be rented.
> Transitions are enforced — you cannot go from Rented back to Available without
> going through an inspection that creates a DamageReport if needed. Pricing
> is a Strategy because different companies charge differently: some charge by
> mile, some by day, some by hour. Swapping the strategy changes the entire
> pricing model. I will also mention that allowing cross-location returns
> (pickup in Delhi, return in Mumbai) adds complexity — you need to track
> car location and potentially charge a one-way fee."

**Classes and Relationships:**

```
RentalLocation ◆── List[Car]
Car --has--> CarType (enum), CarStatus (State)
Reservation --references--> Car, User, RentalLocation
Rental --extends--> Reservation (or references it)
Rental ◆── DamageReport (0 or 1)
RentalPriceCalculator (Strategy) --used-by--> Reservation
```

**One Tricky Design Decision:**
Should a car belong to one location or float between locations? Model a car as
belonging to a home location but with a current location. Cross-location
rentals update current location without changing home location. This lets you
track fleet distribution.

---

### Question 16: Design an Airline Reservation System

**The Question:**
Design an airline reservation system for searching flights, booking seats,
selecting meals, managing cancellations, and generating boarding passes.

**Key Entities to Identify:**
- `Flight` (flight number, origin, destination, departure/arrival, aircraft)
- `Aircraft` (model, total seats)
- `Seat` (row, column, class — Economy/Business/First, status)
- `Booking` (passenger, flight, seat, status)
- `Passenger` (name, passport, frequent flyer)
- `Meal` (type — veg/non-veg/vegan, allocated to passenger)
- `BoardingPass` (generated at check-in)
- `FlightStatus` (Scheduled, Boarding, Departed, Landed, Cancelled)

**Key Patterns to Apply:**
- **Builder Pattern** — `BookingBuilder` collects passenger, flight, seat,
  meal preference before confirming
- **Observer Pattern** — when FlightStatus changes to Cancelled, notify all
  passengers
- **Factory Pattern** — create seat pricing based on class and booking time
  (early bird vs last minute)

**Model Answer Paragraph:**
> "Airline booking has a multi-step form that screams Builder Pattern —
> you collect passenger details, then pick a flight, then pick a seat, then
> add meals, then confirm payment. Each step is optional or sequential.
> Builder lets me validate at each step and only create the immutable Booking
> at the end. Flight status changes are the Observer moment — when a flight
> is cancelled, every affected Booking needs to be flagged and every passenger
> notified. Rather than iterating all bookings inside the Flight class (a law
> of Demeter violation), the Flight publishes a FlightCancelledEvent, and a
> BookingService listens and handles all affected bookings."

**Classes and Relationships:**

```
Flight --operates--> Aircraft
Aircraft ◆── List[Seat]
Booking --references--> Flight, Passenger
Booking ◆── List[Seat] (booked seats)
Booking ◆── Meal (optional)
Booking --generates--> BoardingPass (at check-in)
Flight --publishes--> FlightStatusChangedEvent
BookingService --subscribes--> FlightStatusChangedEvent
```

**One Tricky Design Decision:**
How do you handle overbooking? Airlines deliberately overbook. Model an
`OverbookingPolicy` on the Flight that allows booking N% more than capacity.
When too many passengers show up, a `BumpingService` handles volunteers and
compensation. This is a Strategy within a real-world constraint.

---

### Question 17: Design a Restaurant Management System

**The Question:**
Design a restaurant system that manages table reservations, order taking,
kitchen workflow, billing, and staff management.

**Key Entities to Identify:**
- `Table` (table number, capacity, status)
- `Reservation` (customer, table, date/time, party size)
- `Menu` (categories and menu items)
- `MenuItem` (name, price, prep time, availability)
- `Order` (table, items, status)
- `KitchenOrder` (sent to kitchen after table orders)
- `Bill` (order total, taxes, discounts)
- `Staff` (waiter, chef, cashier — roles)

**Key Patterns to Apply:**
- **Command Pattern** — each order modification is a command (add item,
  remove item, modify item); supports order correction
- **Observer Pattern** — when an order is placed, the kitchen display
  system updates in real time
- **State Pattern** — table status: Available, Reserved, Occupied, Billing
- **Strategy Pattern** — bill calculation (table tax, service charge,
  happy hour discounts)

**Model Answer Paragraph:**
> "The kitchen workflow is the interesting design challenge. When a waiter
> places an order, the kitchen needs to know immediately — this is an Observer
> event. The KitchenDisplay subscribes to OrderPlaced events and shows the
> chef what to prepare. Each order modification (customer changes their mind)
> is a Command, giving us an audit trail and the ability to void items. The
> bill generation uses Strategy because restaurants have different billing
> rules: some add 10% service charge, some have happy hour pricing, some have
> GST calculations that differ by item category. Plugging in the right strategy
> at bill time keeps the Bill class clean."

**Classes and Relationships:**

```
Table --has--> TableStatus (State)
Table --has--> Reservation (0 or 1)
Order --references--> Table
Order ◆── List[OrderItem]
KitchenOrder --mirrors--> Order (sent to kitchen)
KitchenDisplay --observes--> OrderPlacedEvent
Bill --generated-from--> Order
Bill --uses--> BillingStrategy (Strategy)
```

**One Tricky Design Decision:**
Should one Order span a whole evening (table of 4 orders appetizers, then
mains, then dessert all on one order) or should there be multiple orders?
Model it as one Order with multiple rounds of items — each round is an
`OrderBatch`. This keeps the bill unified while still tracking kitchen
batches separately.

---

### Question 18: Design a Hospital Appointment System

**The Question:**
Design a hospital appointment booking system where patients can book doctor
appointments, doctors can manage their schedules, and the hospital manages
multiple departments.

**Key Entities to Identify:**
- `Patient` (name, ID, medical record number)
- `Doctor` (name, specialization, department)
- `Department` (name, list of doctors)
- `TimeSlot` (start time, end time, status)
- `Appointment` (patient, doctor, time slot, status)
- `Schedule` (doctor's availability for a given week)
- `AppointmentStatus` (Scheduled, Confirmed, Cancelled, Completed, NoShow)
- `Notification` (appointment reminders)

**Key Patterns to Apply:**
- **Strategy Pattern** — appointment scheduling strategy (first available,
  preferred doctor, nearest clinic)
- **Observer Pattern** — appointment reminders sent 24 hours before via
  email/SMS
- **State Pattern** — appointment lifecycle: Scheduled → Confirmed →
  Completed or Cancelled

**Model Answer Paragraph:**
> "The scheduling problem has two sides: the patient's preference and the
> doctor's availability. I model a doctor's Schedule as a collection of
> TimeSlots for each day. Booking checks if a slot is Available, marks it
> as Reserved, and creates an Appointment. The appointment then follows its
> own state machine: Scheduled when created, Confirmed after payment or
> confirmation, Completed after the visit, Cancelled if the patient does not
> show or cancels. The reminder system is a scheduled Observer — a background
> job runs every hour, finds appointments happening in the next 24 hours,
> and fires notifications. The notification channel (email vs SMS vs app push)
> is a Strategy."

**Classes and Relationships:**

```
Hospital ◆── List[Department]
Department ◆── List[Doctor]
Doctor ◆── Schedule
Schedule ◆── Dict[date, List[TimeSlot]]
TimeSlot --has--> SlotStatus (Available, Reserved, Completed)
Appointment --references--> Patient, Doctor, TimeSlot
Appointment ◆── AppointmentState (State Pattern)
```

**One Tricky Design Decision:**
How do you handle recurring appointments? A patient with diabetes might need
monthly checkups. Model a `RecurringAppointmentRule` that generates individual
appointments at a given frequency. The rule is separate from any individual
appointment — cancelling one occurrence does not cancel the series.

---

### Question 19: Design an E-commerce Order System

**The Question:**
Design the order lifecycle in an e-commerce platform — from cart to payment,
fulfillment, shipping, and return management.

**Key Entities to Identify:**
- `Order` (items, totals, status)
- `OrderItem` (product, quantity, price at time of order)
- `Payment` (method, amount, status)
- `Shipment` (carrier, tracking number, estimated delivery)
- `Return` (reason, items, refund)
- `OrderStatus` (Created, PaymentPending, Confirmed, Packed, Shipped,
  Delivered, Returned, Refunded)
- `Warehouse` (inventory, fulfillment)
- `Carrier` (FedEx, UPS, Delhivery — external service)

**Key Patterns to Apply:**
- **State Pattern** — order lifecycle has strict state transitions; you
  cannot return an order that is not delivered
- **Observer Pattern** — each state change triggers customer notification,
  inventory update, and analytics event
- **Strategy Pattern** — shipping carrier selection (cheapest, fastest,
  most reliable)

**Model Answer Paragraph:**
> "The order state machine is the backbone of this design. I will explicitly
> model each state and its allowed transitions. The State Pattern enforces
> this — a Shipped order cannot go back to Packed. When state changes,
> multiple systems need to react: the customer gets a notification, the
> inventory system is updated, the analytics pipeline gets an event. I will
> use Observer for this — an OrderStateChangedEvent is published and different
> listeners handle their own concerns. The carrier selection is a Strategy —
> the CarrierSelectionStrategy can choose the cheapest carrier for standard
> orders and the fastest carrier for prime/express orders, and this can change
> without touching Order logic."

**Classes and Relationships:**

```
Order ◆── List[OrderItem]
Order ◆── Payment
Order ◆── Shipment (0 or 1)
Order ◆── Return (0 or 1)
Order ◆── OrderState (State Pattern)
Order --publishes--> OrderStateChangedEvent (Observer)
Shipment --references--> Carrier (Strategy)
CarrierStrategy <|── FastestCarrier
CarrierStrategy <|── CheapestCarrier
```

**One Tricky Design Decision:**
What happens to an order with 5 items when only 3 are in stock? Model
`partial fulfillment` — some items ship first, the rest are backordered.
An order can have multiple shipments. This means Order to Shipment is
one-to-many, not one-to-one.

---

### Question 20: Design a Notification System

**The Question:**
Design a multi-channel notification system that sends notifications via
email, SMS, push notifications, and in-app alerts, with retry logic,
templates, and user preferences.

**Key Entities to Identify:**
- `Notification` (content, type, recipient, priority, timestamp)
- `NotificationChannel` (Email, SMS, Push, InApp)
- `NotificationTemplate` (subject, body template with placeholders)
- `UserPreference` (which channels a user has enabled)
- `NotificationService` (entry point — dispatches to channels)
- `NotificationLog` (audit trail of all sent notifications)
- `RetryPolicy` (how many times to retry on failure)
- `NotificationStatus` (Pending, Sent, Delivered, Failed)

**Key Patterns to Apply:**
- **Strategy Pattern** — each channel (Email, SMS, Push) is a
  `NotificationStrategy`
- **Observer Pattern** — the notification system is itself the Observer
  of events from other systems (OrderShipped → triggers OrderShipmentNotification)
- **Chain of Responsibility** — notification pipeline: validate → enrich →
  check user preferences → send → log
- **Template Method** — `NotificationChannel.send()` defines the skeleton;
  each channel fills in the transport details
- **Decorator Pattern** — wrap notifications with retry logic, rate limiting,
  and logging without changing the core send logic

**Model Answer Paragraph:**
> "A notification system is a pipeline, not a single operation. The message
> goes through validation, template rendering, user preference filtering,
> sending, and logging. Chain of Responsibility models this naturally — each
> handler in the chain does its job and passes to the next. If a user has
> disabled SMS, the SMS preference handler short-circuits that branch. The
> actual sending is a Strategy — EmailSender, SMSSender, PushSender are
> all swappable. Retry logic wraps the Strategy with a Decorator, adding
> exponential backoff without touching the sender implementation. I will
> mention that in a production system, notifications are sent asynchronously
> via a message queue (Kafka, RabbitMQ) to avoid blocking the main request."

**Classes and Relationships:**

```
NotificationService --dispatches--> List[NotificationChannel]
NotificationChannel <|── EmailChannel
NotificationChannel <|── SMSChannel
NotificationChannel <|── PushChannel
NotificationChannel <|── InAppChannel
NotificationService --checks--> UserPreference
Notification --uses--> NotificationTemplate
NotificationPipeline (Chain of Responsibility):
  ValidationHandler → PreferenceHandler → TemplateHandler → SenderHandler → LogHandler
RetryDecorator --wraps--> NotificationChannel (Decorator)
```

**One Tricky Design Decision:**
Should you send through all enabled channels simultaneously or in a priority
order? For critical notifications (OTP, payment failure), send through all
channels simultaneously. For marketing, send via cheapest channel first, and
only escalate if the user does not engage. Model this as a `DispatchPolicy`
Strategy on the notification type.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import time


class ChannelType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class NotificationStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class Notification:
    recipient_id: str
    template_id: str
    data: Dict[str, str]  # template variables
    channels: List[ChannelType]
    priority: str = "normal"
    status: NotificationStatus = NotificationStatus.PENDING


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification, rendered_content: str) -> bool:
        """Returns True on success."""
        pass

    @property
    @abstractmethod
    def channel_type(self) -> ChannelType:
        pass


class EmailChannel(NotificationChannel):
    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.EMAIL

    def send(self, notification: Notification, rendered_content: str) -> bool:
        print(f"[EMAIL] Sending to user {notification.recipient_id}: {rendered_content[:50]}...")
        return True  # In real life: call email provider API


class SMSChannel(NotificationChannel):
    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.SMS

    def send(self, notification: Notification, rendered_content: str) -> bool:
        print(f"[SMS] Sending to user {notification.recipient_id}: {rendered_content[:50]}...")
        return True


class RetryDecorator(NotificationChannel):
    """Decorator that adds retry logic to any channel."""

    def __init__(self, channel: NotificationChannel, max_retries: int = 3, backoff: float = 1.0):
        self._channel = channel
        self._max_retries = max_retries
        self._backoff = backoff

    @property
    def channel_type(self) -> ChannelType:
        return self._channel.channel_type

    def send(self, notification: Notification, rendered_content: str) -> bool:
        for attempt in range(self._max_retries):
            if self._channel.send(notification, rendered_content):
                return True
            wait = self._backoff * (2 ** attempt)
            print(f"Retry {attempt + 1} for {self.channel_type} after {wait}s")
            time.sleep(wait)
        return False


class NotificationTemplate:
    def __init__(self, template_id: str, body: str):
        self.template_id = template_id
        self.body = body

    def render(self, data: Dict[str, str]) -> str:
        result = self.body
        for key, value in data.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result


class UserPreferenceService:
    def __init__(self):
        self._preferences: Dict[str, List[ChannelType]] = {}

    def set_preferences(self, user_id: str, channels: List[ChannelType]):
        self._preferences[user_id] = channels

    def get_allowed_channels(self, user_id: str) -> List[ChannelType]:
        return self._preferences.get(user_id, list(ChannelType))


class NotificationService:
    def __init__(self):
        self._channels: Dict[ChannelType, NotificationChannel] = {}
        self._templates: Dict[str, NotificationTemplate] = {}
        self._preference_service = UserPreferenceService()

    def register_channel(self, channel: NotificationChannel):
        self._channels[channel.channel_type] = channel

    def register_template(self, template: NotificationTemplate):
        self._templates[template.template_id] = template

    def send(self, notification: Notification):
        template = self._templates.get(notification.template_id)
        if not template:
            raise ValueError(f"Template {notification.template_id} not found")

        rendered = template.render(notification.data)
        allowed = self._preference_service.get_allowed_channels(notification.recipient_id)

        for channel_type in notification.channels:
            if channel_type not in allowed:
                print(f"User {notification.recipient_id} has disabled {channel_type}")
                continue
            channel = self._channels.get(channel_type)
            if channel:
                success = channel.send(notification, rendered)
                notification.status = (
                    NotificationStatus.SENT if success else NotificationStatus.FAILED
                )
```

---

## Part 3: Red Flags — What Makes Interviewers Nervous

These are the behaviors that signal a junior or sloppy engineer:

---

### Red Flag 1: Jumping Straight to Code

**What it looks like:**
The interviewer finishes the question and you immediately start writing classes.

**Why it is bad:**
You have not understood the problem. You are coding a solution to an imagined
problem, not the actual one.

**What to do instead:**
Say "Let me take a moment to clarify requirements and identify the key entities
before I start coding."

---

### Red Flag 2: Ignoring Edge Cases

**What it looks like:**
Your Booking class assumes payment always succeeds. Your Slot dispenser does
not check for empty inventory. Your State machine has no handling for
invalid transitions.

**Why it is bad:**
Production code fails at edges. Senior engineers think in edge cases first.

**Questions to ask yourself:**
- What if this fails?
- What if the input is null or empty?
- What if two users do this simultaneously?
- What if the external service is down?

---

### Red Flag 3: No Design Patterns Used

**What it looks like:**
Your design is a pile of if-else statements and switch cases inside one giant
class. Adding a new type requires modifying existing code.

**Why it is bad:**
It violates Open-Closed Principle and shows you do not have design vocabulary.

**Pattern to check:**
Ask yourself after every significant class: "Would this class need to change
if requirements change slightly?" If yes, extract a Strategy, State, or
Observer.

---

### Red Flag 4: God Classes

**What it looks like:**
One `OrderManager` class that handles creating orders, validating payments,
sending notifications, updating inventory, calculating tax, and logging.

**Why it is bad:**
It violates Single Responsibility Principle. Changes to tax logic can break
notification code. Testing is impossible without mocking everything.

**The rule of thumb:**
If you cannot describe what a class does in one sentence without using "and",
it is a god class. Split it.

---

### Red Flag 5: Ignoring Relationships

**What it looks like:**
All your classes are islands. No one has a reference to anyone else. Or
everything has a reference to everything (circular dependencies everywhere).

**Why it is bad:**
It shows you have not thought about the system as a whole. Real systems have
intentional relationships.

**The rule:**
Draw arrows on your UML. If you cannot explain why every arrow exists, you do
not understand your own design.

---

### Red Flag 6: Wrong Multiplicity

**What it looks like:**
Making a 1-to-many relationship 1-to-1. For example: modeling a user as having
exactly one booking, when in reality they can have many.

**Why it is bad:**
Your design breaks as soon as a second booking is made. Fundamental data model
is wrong.

---

### Red Flag 7: No Mention of Trade-offs

**What it looks like:**
Your design has one obvious approach and you present it as THE solution with
no alternatives considered.

**Why it is bad:**
Senior engineers know there is no perfect design — only designs with different
trade-offs. Showing you considered alternatives and made a deliberate choice
is what SDE-3 level looks like.

---

### Red Flag 8: Copying Without Understanding

**What it looks like:**
"I will use Singleton here" — then you implement a non-thread-safe Singleton
and cannot explain why Singleton is needed.

**Why it is bad:**
Interviewers test depth. They will ask "why Singleton and not a module-level
instance?" If you cannot answer, it shows you pattern-drop without judgment.

---

## Part 4: Green Flags — What Impresses Interviewers

These are the behaviors that separate SDE-3 candidates from SDE-2 candidates:

---

### Green Flag 1: Structured Requirements Clarification

**What it looks like:**
You ask 3–5 targeted questions, listen to the answers, and say "OK, so given
these constraints, here is what I will design."

**Why it impresses:**
It shows maturity. Junior engineers assume. Senior engineers clarify.

---

### Green Flag 2: Thinking Out Loud

**What it looks like:**
You narrate every decision. "I am making Cart and Order separate because Cart
is mutable and ephemeral, but Order is immutable and must be auditable."

**Why it impresses:**
Interviewers want to see your thought process, not just your output. A correct
design with no explanation is less impressive than an explained design with
minor flaws.

---

### Green Flag 3: Naming Patterns by Name

**What it looks like:**
"I am applying the Strategy Pattern here so the discount calculation can be
swapped without touching the Order class."

**Why it impresses:**
It shows vocabulary. Senior engineers communicate in patterns. It also signals
you will communicate clearly with other senior engineers on your team.

---

### Green Flag 4: Drawing UML Before Coding

**What it looks like:**
You spend 5 minutes with a diagram showing boxes, arrows, and multiplicity
before writing a single line of code.

**Why it impresses:**
It shows discipline. The best engineers design before they build. It also
gives you a map so you do not lose your place during coding.

---

### Green Flag 5: Discussing Trade-offs

**What it looks like:**
"I could model this with inheritance, but I am using composition because it is
more flexible. The trade-off is slightly more verbose code."

**Why it impresses:**
It shows you understand that every design decision has costs. "Composition over
inheritance" is a principle — knowing WHEN to apply it shows wisdom, not just
knowledge.

---

### Green Flag 6: Mentioning Production Concerns

**What it looks like:**
"In a real system I would use a message queue here for async processing. For
this design scope, I will use an in-memory queue."

**Why it impresses:**
It shows you have built real systems. You know what the design leaves out and
you are transparent about it.

---

### Green Flag 7: Edge Case Awareness Without Being Asked

**What it looks like:**
You proactively say "One edge case I want to handle: what if two users try to
book the same seat at the same time? I will use a SeatLock mechanism..."

**Why it impresses:**
It shows you think defensively. Defensive thinking is an SDE-3 hallmark.

---

### Green Flag 8: Clean Code Habits

**What it looks like:**
- Meaningful class and method names (not `obj`, `data`, `temp`)
- Short methods that do one thing
- No magic numbers (use constants or enums)
- Dependency injection instead of hardcoded instantiation

**Why it impresses:**
It shows you write code that other engineers can read and maintain.

---

### Green Flag 9: Asking About Extensibility

**What it looks like:**
"You mentioned this is a vending machine for snacks. Are there plans to
support hot beverages? Because that would change how I model the dispensing
mechanism."

**Why it impresses:**
It shows you think about future requirements. Senior engineers build systems
that can grow.

---

### Green Flag 10: Self-Correcting Gracefully

**What it looks like:**
"Actually, I realize I put too much logic in the Order class. Let me pull the
discount calculation into a separate PriceCalculator so Order stays focused
on its lifecycle."

**Why it impresses:**
It shows self-awareness and iterative thinking. No design is perfect on the
first pass. The ability to identify and fix your own mistakes is more valuable
than getting it right the first time.

---

## Part 5: Week 2 Self-Assessment Checklist

Use this checklist to evaluate your readiness before real interviews.
Rate yourself 1–5 for each item. Anything below 3 needs another day of review.

---

### Section A: Requirements and Entity Modeling

```
[ ] I ask clarifying questions before designing (not after)
[ ] I can extract entities from a problem description in under 3 minutes
[ ] I can identify relationships (composition vs aggregation vs association)
[ ] I correctly apply multiplicity (1, *, 0..1) to relationships
[ ] I distinguish between what a class OWNS vs what it USES
[ ] I think about edge cases before being prompted
```

---

### Section B: UML and Diagrams

```
[ ] I can draw a class diagram with correct notation in under 5 minutes
[ ] My diagrams include: class name, key attributes, key methods
[ ] My diagrams show relationships with correct arrow types
[ ] I draw diagrams BEFORE writing code, not after
[ ] I can narrate my diagram while drawing it
```

---

### Section C: Design Patterns

```
[ ] I can explain what problem each of the 10 core patterns solves
[ ] I apply Strategy when behavior needs to be swappable
[ ] I apply Observer when multiple parties need to react to an event
[ ] I apply State when an object's behavior changes with internal state
[ ] I apply Factory when object creation is complex or conditional
[ ] I apply Builder when constructing objects with many optional parts
[ ] I apply Decorator when adding behavior without changing the original class
[ ] I apply Singleton only when truly needed (and can defend it)
[ ] I apply Command when requests need to be queued or undone
[ ] I apply Facade when simplifying a complex subsystem
[ ] I can name the pattern I am using AND explain why
```

---

### Section D: Code Quality

```
[ ] My classes have a single, clear responsibility
[ ] My methods are short (under 20 lines each)
[ ] I use meaningful names for classes, methods, and variables
[ ] I use enums for fixed sets (status, type, category)
[ ] I use abstract base classes or interfaces to define contracts
[ ] I inject dependencies instead of hardcoding them
[ ] I can write working Python for any of the 20 problems above
[ ] My code compiles / runs without syntax errors
```

---

### Section E: Specific Problem Readiness

Rate yourself on each problem (1 = cannot start, 5 = could explain and code in 20 min):

```
[ ] Vending Machine          ___/5
[ ] ATM                      ___/5
[ ] Chess Game               ___/5
[ ] Hotel Booking            ___/5
[ ] Food Delivery            ___/5
[ ] Movie Ticket Booking     ___/5
[ ] Ride Sharing             ___/5
[ ] Snake and Ladder         ___/5
[ ] Social Media Platform    ___/5
[ ] Shopping Cart            ___/5
[ ] Chat System              ___/5
[ ] Splitwise                ___/5
[ ] Online Judge             ___/5
[ ] Traffic Light            ___/5
[ ] Car Rental               ___/5
[ ] Airline Reservation      ___/5
[ ] Restaurant Management    ___/5
[ ] Hospital Appointment     ___/5
[ ] E-commerce Order         ___/5
[ ] Notification System      ___/5
```

---

### Section F: Interview Performance

```
[ ] I can stay calm and talk through a new problem I have not seen before
[ ] I can recover gracefully when the interviewer redirects me
[ ] I can explain a design decision in plain English, not just code
[ ] I finish within the time limit (20-25 minutes total)
[ ] I proactively mention trade-offs without being asked
[ ] I self-correct my design when I spot a flaw
[ ] I can discuss production concerns (scalability, async, locking)
```

---

### Section G: Week 2 Topic Coverage

```
[ ] Day 6  — Creational Patterns (Factory, Builder, Singleton, Prototype, Object Pool)
[ ] Day 7  — Structural Patterns (Adapter, Decorator, Facade, Composite, Proxy, Bridge)
[ ] Day 8  — Behavioral Patterns (Strategy, Observer, Command, State, Template Method, Iterator)
[ ] Day 9  — Parking Lot (full design + code)
[ ] Day 10 — Library System (full design + code)
[ ] Day 11 — Elevator System (full design + code)
[ ] Day 12 — LLD Mock (top 20 Q&A, red flags, green flags)
```

---

### Scoring Guide

Count your checkmarks in each section:

| Score | Meaning |
|-------|---------|
| 90%+ checked | You are ready for SDE-3 LLD interviews |
| 75–90% checked | One more week of problem practice recommended |
| 50–75% checked | Review weak pattern areas and do 5 more timed practices |
| Below 50% | Go back to Week 1 and Week 2 foundations |

---

### Recommended Next Steps After Day 12

1. **Pick 3 problems from the Top 20 that you rated 3 or below.**
   Design them fully — requirements, UML, code — without looking at notes.

2. **Do one timed mock.** Set a 25-minute timer. Pick a random problem.
   Talk out loud as if the interviewer is in the room.

3. **Record yourself.** Watch the replay. Notice where you go silent,
   where you jump to code too early, where you forget to name a pattern.

4. **Review the Red Flags list before every practice session.**
   Turn each red flag into a habit-breaker.

5. **Start Week 3 (HLD) only after you can comfortably score 4/5 on
   at least 15 of the 20 problems.**

---

## Summary: The LLD Interview in One Page

```
BEFORE THE INTERVIEW
  - Know 10 patterns by name, problem, and example
  - Know 20 classic problems cold
  - Practice talking while designing

DURING PHASE 1 (Clarify)
  - Ask 3-5 questions
  - Confirm scope (auth? payments? scale?)
  - Say requirements back in your own words

DURING PHASE 2 (Entities)
  - List classes from nouns
  - List methods from verbs
  - Map relationships (own vs use)

DURING PHASE 3 (UML)
  - Draw top-down
  - Label arrows and multiplicity
  - Talk while drawing

DURING PHASE 4 (Patterns)
  - Name the pattern
  - Explain the problem it solves
  - Explain the benefit (extensibility, testability)

DURING PHASE 5 (Code)
  - Start with the most important class
  - Show pattern implementation
  - Handle at least one edge case in code

THROUGHOUT
  - Mention trade-offs
  - Mention edge cases
  - Mention production concerns
  - Self-correct without being asked
```

---

*Day 12 of 14 — Week 2 Complete. You have covered all 10 core patterns,
3 full LLD problems, and 20 mock interview questions. You have the vocabulary,
the frameworks, and the patterns. Now practice until they are automatic.*
