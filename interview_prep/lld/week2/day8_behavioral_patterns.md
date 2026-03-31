# Week 2 - Day 8: Behavioral Design Patterns
# Strategy, Observer, Command

---

## What Are Behavioral Patterns?

Creational patterns → How objects are CREATED
Structural patterns → How objects are COMPOSED
Behavioral patterns → How objects COMMUNICATE and share responsibility

Behavioral patterns are about **defining the interaction between objects** —
who talks to whom, how decisions are made, and how events flow through the system.

These patterns appear most in real backend code — every time you think about
"how should these parts communicate?", a behavioral pattern is the answer.

---

## Pattern 1: Strategy

### The Problem It Solves

You have an algorithm or behavior that needs to change based on context —
but you don't want a massive `if-elif` chain that grows every time
a new variation is added.

**The core idea:** Extract the varying behavior into its own class (the "strategy"),
and let the context object use whichever strategy it needs at runtime.

### Real World Analogy

Think about **navigation apps** like Google Maps.

When you ask for directions from A to B, you can choose:
- Fastest route (by time)
- Shortest route (by distance)
- Avoid highways
- Walking route
- Cycling route

The destination is the same. The map is the same. But the **routing algorithm**
(the strategy) is different each time. You pick which one to apply at runtime.

The map app doesn't have one giant `if route_type == "fastest"` block.
Each routing algorithm is a separate, swappable strategy.

### The Problem Without Strategy

```python
class PaymentProcessor:
    def process(self, amount: float, method: str):
        if method == "credit_card":
            print(f"Processing ₹{amount} via Credit Card")
            print("  → Validating card number")
            print("  → Checking CVV")
            print("  → Charging via Visa/Mastercard network")

        elif method == "upi":
            print(f"Processing ₹{amount} via UPI")
            print("  → Verifying UPI ID")
            print("  → Sending payment request")
            print("  → Waiting for PIN confirmation")

        elif method == "net_banking":
            print(f"Processing ₹{amount} via Net Banking")
            print("  → Redirecting to bank portal")
            print("  → Session authentication")
            print("  → Transfer confirmation")

        # Adding crypto next month → modify this class again
        # Adding PayLater next month → modify this class again
        # This class becomes a 500-line monster
```

Every new payment method forces a modification of `PaymentProcessor`.
This violates OCP. The class grows indefinitely. Tests become complex.

### Strategy Solution

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ─── Step 1: Strategy Interface ────────────────────────────────────
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> dict:
        """Returns a result dict with success status and transaction details"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate that this payment method is properly configured"""
        pass


# ─── Step 2: Concrete Strategies ──────────────────────────────────
@dataclass
class CreditCardStrategy(PaymentStrategy):
    card_number: str
    card_holder: str
    cvv: str
    expiry: str

    def validate(self) -> bool:
        return (len(self.card_number) == 16 and
                len(self.cvv) == 3 and
                len(self.expiry) == 5)

    def pay(self, amount: float) -> dict:
        print(f"  [Credit Card] Validating card ending in {self.card_number[-4:]}")
        print(f"  [Credit Card] Charging ₹{amount} via card network")
        return {
            "success": True,
            "method": "credit_card",
            "transaction_id": f"CC_{hash(self.card_number) % 10000}",
            "amount": amount
        }


@dataclass
class UPIStrategy(PaymentStrategy):
    upi_id: str

    def validate(self) -> bool:
        return "@" in self.upi_id

    def pay(self, amount: float) -> dict:
        print(f"  [UPI] Sending payment request to {self.upi_id}")
        print(f"  [UPI] Waiting for PIN confirmation...")
        return {
            "success": True,
            "method": "upi",
            "transaction_id": f"UPI_{hash(self.upi_id) % 10000}",
            "amount": amount
        }


@dataclass
class WalletStrategy(PaymentStrategy):
    wallet_id: str
    balance: float

    def validate(self) -> bool:
        return self.balance > 0

    def pay(self, amount: float) -> dict:
        if amount > self.balance:
            print(f"  [Wallet] Insufficient balance: ₹{self.balance} < ₹{amount}")
            return {"success": False, "method": "wallet", "error": "Insufficient balance"}

        self.balance -= amount
        print(f"  [Wallet] Deducted ₹{amount}. Remaining balance: ₹{self.balance}")
        return {
            "success": True,
            "method": "wallet",
            "transaction_id": f"WLT_{hash(self.wallet_id) % 10000}",
            "amount": amount
        }


# Adding new method → NEW class only, zero changes to existing code (OCP)
@dataclass
class CryptoStrategy(PaymentStrategy):
    wallet_address: str
    crypto_type: str = "BTC"

    def validate(self) -> bool:
        return len(self.wallet_address) > 20

    def pay(self, amount: float) -> dict:
        print(f"  [Crypto] Broadcasting {amount} INR worth of {self.crypto_type}")
        print(f"  [Crypto] Transaction to {self.wallet_address[:10]}...")
        return {
            "success": True,
            "method": "crypto",
            "transaction_id": f"CRYPTO_{hash(self.wallet_address) % 10000}",
            "amount": amount
        }


# ─── Step 3: Context — uses the strategy ──────────────────────────
class Checkout:
    """
    Context class. Uses a PaymentStrategy but doesn't care which one.
    Strategy can be set or swapped at runtime.
    """

    def __init__(self):
        self._strategy: PaymentStrategy = None
        self._cart_total: float = 0.0

    def set_payment_method(self, strategy: PaymentStrategy):
        """Strategy can be changed at any time — even mid-session"""
        if not strategy.validate():
            raise ValueError("Payment method validation failed")
        self._strategy = strategy
        print(f"Payment method set: {strategy.__class__.__name__}")

    def add_to_cart(self, price: float):
        self._cart_total += price

    def complete_purchase(self) -> dict:
        if not self._strategy:
            raise RuntimeError("No payment method selected")
        if self._cart_total == 0:
            raise ValueError("Cart is empty")

        print(f"\nProcessing payment of ₹{self._cart_total}...")
        result = self._strategy.pay(self._cart_total)

        if result["success"]:
            print(f"Payment successful! TXN: {result['transaction_id']}")
            self._cart_total = 0.0   # Clear cart on success
        else:
            print(f"Payment failed: {result.get('error')}")

        return result


# ─── Usage ────────────────────────────────────────────────────────
checkout = Checkout()
checkout.add_to_cart(45000.0)
checkout.add_to_cart(1500.0)

# User chooses UPI
checkout.set_payment_method(UPIStrategy(upi_id="alice@okicici"))
result = checkout.complete_purchase()

# Another purchase — user switches to wallet
checkout.add_to_cart(800.0)
checkout.set_payment_method(WalletStrategy(wallet_id="WLT001", balance=500.0))
result = checkout.complete_purchase()   # Will fail — insufficient balance
```

### Strategy + Factory — The Common Combination

In real code, Strategy and Factory often work together — the Factory
decides WHICH strategy to use based on user input:

```python
class PaymentStrategyFactory:
    @staticmethod
    def create(method: str, **kwargs) -> PaymentStrategy:
        strategies = {
            "credit_card": lambda: CreditCardStrategy(
                kwargs["card_number"], kwargs["card_holder"],
                kwargs["cvv"], kwargs["expiry"]
            ),
            "upi": lambda: UPIStrategy(kwargs["upi_id"]),
            "wallet": lambda: WalletStrategy(kwargs["wallet_id"], kwargs["balance"]),
            "crypto": lambda: CryptoStrategy(kwargs["wallet_address"]),
        }
        if method not in strategies:
            raise ValueError(f"Unknown payment method: {method}")
        return strategies[method]()


# API handler receives user's choice — factory creates the right strategy
user_choice = "upi"
strategy = PaymentStrategyFactory.create(user_choice, upi_id="bob@paytm")
checkout.set_payment_method(strategy)
```

---

## Pattern 2: Observer

### The Problem It Solves

One object changes state, and **multiple other objects need to be notified
automatically** — without the first object knowing who they are.

**The core idea:** Define a one-to-many relationship. When the "subject" changes,
all registered "observers" are notified automatically.

### Real World Analogy

Think about **YouTube subscriptions**.

- A YouTube channel is the **subject** (publisher)
- Subscribers are the **observers** (listeners)
- When the channel uploads a video, YouTube notifies all subscribers
- The channel doesn't know WHO the subscribers are — it just says "new video"
- Each subscriber does their own thing with the notification
  (some watch immediately, some save for later, some ignore)
- New subscribers can join anytime. Old ones can unsubscribe anytime.
- The channel's upload logic doesn't change when subscribers join or leave.

### Another Analogy — Stock Market Ticker

A stock's price changes. Multiple systems react:
- Trading bots check buy/sell conditions
- Portfolio trackers update the user's holdings value
- Alert systems check if a price threshold was crossed
- News feed records the price change for history

The stock doesn't call each of these individually. They all **subscribe**
to price updates. The stock just broadcasts: "price changed."

### The Problem Without Observer

```python
class StockPrice:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

    def update_price(self, new_price: float):
        self.price = new_price

        # BAD — StockPrice is directly coupled to every system that cares about it
        # Adding a new consumer means MODIFYING this method
        trading_bot.on_price_change(self.symbol, new_price)     # Tight coupling!
        portfolio_tracker.update(self.symbol, new_price)         # Tight coupling!
        alert_system.check_threshold(self.symbol, new_price)     # Tight coupling!
        news_feed.record(self.symbol, new_price)                  # Tight coupling!
```

`StockPrice` knows about 4 specific systems. Adding a 5th means modifying
`StockPrice`. Removing one means modifying `StockPrice`. Testing is a nightmare.
This is the opposite of SRP and OCP.

### Observer Solution

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from datetime import datetime


# ─── Observer Interface ────────────────────────────────────────────
class StockObserver(ABC):
    @abstractmethod
    def on_price_update(self, symbol: str, old_price: float, new_price: float):
        pass


# ─── Subject ──────────────────────────────────────────────────────
class StockMarket:
    """
    The subject/publisher. Maintains a list of observers.
    Notifies all of them when price changes.
    Has NO knowledge of what the observers DO with the notification.
    """

    def __init__(self):
        self._stocks: dict = {}
        self._observers: List[StockObserver] = []

    def subscribe(self, observer: StockObserver):
        self._observers.append(observer)
        print(f"[Market] {observer.__class__.__name__} subscribed")

    def unsubscribe(self, observer: StockObserver):
        self._observers.remove(observer)
        print(f"[Market] {observer.__class__.__name__} unsubscribed")

    def update_price(self, symbol: str, new_price: float):
        old_price = self._stocks.get(symbol, new_price)
        self._stocks[symbol] = new_price

        change = ((new_price - old_price) / old_price * 100) if old_price else 0
        direction = "▲" if new_price > old_price else "▼"
        print(f"\n[Market] {symbol}: ₹{old_price} → ₹{new_price} {direction}{abs(change):.1f}%")

        # Notify ALL observers — market doesn't care WHO they are
        for observer in self._observers:
            observer.on_price_update(symbol, old_price, new_price)

    def get_price(self, symbol: str) -> float:
        return self._stocks.get(symbol, 0.0)


# ─── Concrete Observers ───────────────────────────────────────────
class TradingBot(StockObserver):
    def __init__(self, name: str, buy_below: float, sell_above: float):
        self.name = name
        self.buy_below = buy_below
        self.sell_above = sell_above

    def on_price_update(self, symbol: str, old_price: float, new_price: float):
        if new_price <= self.buy_below:
            print(f"  [TradingBot:{self.name}] BUY signal for {symbol} at ₹{new_price}")
        elif new_price >= self.sell_above:
            print(f"  [TradingBot:{self.name}] SELL signal for {symbol} at ₹{new_price}")


class PortfolioTracker(StockObserver):
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.holdings: dict = {}

    def add_holding(self, symbol: str, quantity: int):
        self.holdings[symbol] = quantity

    def on_price_update(self, symbol: str, old_price: float, new_price: float):
        if symbol in self.holdings:
            qty = self.holdings[symbol]
            old_val = qty * old_price
            new_val = qty * new_price
            gain = new_val - old_val
            print(f"  [Portfolio:{self.user_name}] {symbol} holdings value: "
                  f"₹{old_val:.0f} → ₹{new_val:.0f} ({'+' if gain >= 0 else ''}₹{gain:.0f})")


class PriceAlertSystem(StockObserver):
    def __init__(self):
        self.alerts: list = []   # (symbol, threshold, direction, callback_msg)

    def add_alert(self, symbol: str, threshold: float, direction: str, message: str):
        self.alerts.append((symbol, threshold, direction, message))

    def on_price_update(self, symbol: str, old_price: float, new_price: float):
        for alert_symbol, threshold, direction, message in self.alerts:
            if alert_symbol != symbol:
                continue
            if direction == "above" and new_price >= threshold:
                print(f"  [ALERT] 🔔 {message} (current: ₹{new_price})")
            elif direction == "below" and new_price <= threshold:
                print(f"  [ALERT] 🔔 {message} (current: ₹{new_price})")


class MarketLogger(StockObserver):
    def __init__(self):
        self.history: list = []

    def on_price_update(self, symbol: str, old_price: float, new_price: float):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "old_price": old_price,
            "new_price": new_price
        }
        self.history.append(entry)
        print(f"  [Logger] Recorded price change for {symbol}")


# ─── Usage ────────────────────────────────────────────────────────
market = StockMarket()

# Create observers
bot = TradingBot("AlphaBot", buy_below=2400, sell_above=2700)
tracker = PortfolioTracker("Alice")
tracker.add_holding("RELIANCE", 10)
alerts = PriceAlertSystem()
alerts.add_alert("RELIANCE", 2700, "above", "RELIANCE hit your target price!")
alerts.add_alert("RELIANCE", 2300, "below", "RELIANCE dropped below your stop-loss!")
logger = MarketLogger()

# Register observers
market.subscribe(bot)
market.subscribe(tracker)
market.subscribe(alerts)
market.subscribe(logger)

# Simulate price changes
market.update_price("RELIANCE", 2500)
market.update_price("RELIANCE", 2650)
market.update_price("RELIANCE", 2720)   # Should trigger sell + alert

# Unsubscribe bot — it no longer gets notifications
market.unsubscribe(bot)
market.update_price("RELIANCE", 2390)   # Bot won't react

print(f"\nLog has {len(logger.history)} entries")
```

### Event-Driven Backend — Observer in Microservices

In modern backend systems, Observer is implemented as an **event bus** or
**message queue** (Kafka, RabbitMQ). The pattern is identical — just distributed:

```
Order Service                  ← Subject (publishes events)
    │
    │ publishes: "OrderPlaced" event
    │
    ├──► Inventory Service     ← Observer (reduces stock)
    ├──► Notification Service  ← Observer (sends confirmation email)
    ├──► Analytics Service     ← Observer (records for reporting)
    └──► Fraud Detection       ← Observer (checks for suspicious patterns)
```

```python
# Simplified event bus — in-process version of Kafka/RabbitMQ
class EventBus:
    """Central event dispatcher — decouples publishers from subscribers"""

    def __init__(self):
        self._subscribers: dict = {}   # event_type → list of handlers

    def subscribe(self, event_type: str, handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: dict):
        print(f"\n[EventBus] Publishing: {event_type}")
        for handler in self._subscribers.get(event_type, []):
            handler(data)


# Create event bus (singleton in real apps)
event_bus = EventBus()

# Subscribers — each is a function (could also be a class method)
def handle_inventory(data):
    print(f"  [Inventory] Reducing stock for order {data['order_id']}")

def handle_notification(data):
    print(f"  [Notification] Sending confirmation to {data['user_email']}")

def handle_analytics(data):
    print(f"  [Analytics] Recording order of ₹{data['amount']}")

def handle_fraud_check(data):
    print(f"  [Fraud] Checking order {data['order_id']} for suspicious activity")

# Register handlers
event_bus.subscribe("OrderPlaced", handle_inventory)
event_bus.subscribe("OrderPlaced", handle_notification)
event_bus.subscribe("OrderPlaced", handle_analytics)
event_bus.subscribe("OrderPlaced", handle_fraud_check)

# Publisher — Order Service fires an event and forgets
# It doesn't know or care who handles it
event_bus.publish("OrderPlaced", {
    "order_id": "ORD_001",
    "user_email": "alice@example.com",
    "amount": 45000.0,
    "items": ["LAPTOP"]
})
```

---

## Pattern 3: Command

### The Problem It Solves

You want to **encapsulate a request as an object** — so that you can:
- Queue it for later execution
- Undo it (rollback)
- Log it (audit trail)
- Retry it on failure
- Store it (for replay)

**The core idea:** Instead of calling a method directly, wrap the call in a
Command object. The Command object knows HOW to execute the action — and HOW
to undo it.

### Real World Analogy

Think about a **restaurant order system**.

When a waiter takes your order:
1. They write it on an **order slip** (the command object)
2. They pass the slip to the kitchen queue (queueing)
3. The kitchen executes the order when ready (deferred execution)
4. If you change your mind, the order can be cancelled (undo)
5. The slip is kept for billing (logging/history)

The waiter doesn't cook the food. The chef doesn't talk to customers.
The **order slip (command)** decouples the requester from the executor.

### Another Analogy — Text Editor Undo/Redo

Every time you type, bold text, or insert an image in a Word document,
each action is a Command object stored in a history stack.
`Ctrl+Z` pops the last command and calls `undo()`.
`Ctrl+Y` re-executes it.

### Command Solution — Text Editor with Undo/Redo

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field


# ─── Command Interface ────────────────────────────────────────────
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ─── Receiver — the object that actually does the work ────────────
class TextDocument:
    def __init__(self):
        self.content: str = ""
        self.cursor_position: int = 0

    def get_content(self) -> str:
        return self.content

    def insert_text(self, position: int, text: str):
        self.content = self.content[:position] + text + self.content[position:]
        self.cursor_position = position + len(text)

    def delete_text(self, position: int, length: int):
        self.content = self.content[:position] + self.content[position + length:]
        self.cursor_position = position

    def replace_text(self, old: str, new: str):
        self.content = self.content.replace(old, new)

    def __repr__(self):
        return f'Document: "{self.content}"'


# ─── Concrete Commands ─────────────────────────────────────────────
class InsertTextCommand(Command):
    def __init__(self, document: TextDocument, position: int, text: str):
        self._doc = document
        self._position = position
        self._text = text

    def execute(self):
        self._doc.insert_text(self._position, self._text)
        print(f"  [InsertText] Added '{self._text}' at pos {self._position}")

    def undo(self):
        self._doc.delete_text(self._position, len(self._text))
        print(f"  [InsertText UNDO] Removed '{self._text}' from pos {self._position}")


class DeleteTextCommand(Command):
    def __init__(self, document: TextDocument, position: int, length: int):
        self._doc = document
        self._position = position
        self._length = length
        self._deleted_text: str = ""   # Store for undo

    def execute(self):
        # Save what we're about to delete (needed for undo)
        self._deleted_text = self._doc.content[self._position:self._position + self._length]
        self._doc.delete_text(self._position, self._length)
        print(f"  [DeleteText] Deleted '{self._deleted_text}' at pos {self._position}")

    def undo(self):
        # Re-insert the deleted text at original position
        self._doc.insert_text(self._position, self._deleted_text)
        print(f"  [DeleteText UNDO] Restored '{self._deleted_text}'")


class ReplaceTextCommand(Command):
    def __init__(self, document: TextDocument, old_text: str, new_text: str):
        self._doc = document
        self._old_text = old_text
        self._new_text = new_text
        self._original_content: str = ""

    def execute(self):
        self._original_content = self._doc.content  # Full snapshot for undo
        self._doc.replace_text(self._old_text, self._new_text)
        print(f"  [Replace] '{self._old_text}' → '{self._new_text}'")

    def undo(self):
        self._doc.content = self._original_content   # Restore full snapshot
        print(f"  [Replace UNDO] Restored original content")


# ─── Invoker — manages command history, executes, undo/redo ───────
class TextEditor:
    """
    The Invoker. Stores command history.
    Executes commands and supports undo/redo.
    Knows NOTHING about the actual text operations — only about commands.
    """

    def __init__(self, document: TextDocument):
        self._document = document
        self._history: List[Command] = []      # Executed commands (for undo)
        self._redo_stack: List[Command] = []   # Undone commands (for redo)

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()   # Any new action clears redo history

    def undo(self):
        if not self._history:
            print("  [Editor] Nothing to undo")
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        if not self._redo_stack:
            print("  [Editor] Nothing to redo")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)

    def show(self):
        print(f"\n  {self._document}")
        print(f"  History: {len(self._history)} commands | Redo stack: {len(self._redo_stack)}")


# ─── Usage ────────────────────────────────────────────────────────
doc = TextDocument()
editor = TextEditor(doc)

print("=== Building document ===")
editor.execute(InsertTextCommand(doc, 0, "Hello"))
editor.show()

editor.execute(InsertTextCommand(doc, 5, " World"))
editor.show()

editor.execute(InsertTextCommand(doc, 11, "!"))
editor.show()

print("\n=== Undo ===")
editor.undo()   # Removes "!"
editor.show()

editor.undo()   # Removes " World"
editor.show()

print("\n=== Redo ===")
editor.redo()   # Re-adds " World"
editor.show()

print("\n=== Replace ===")
editor.execute(ReplaceTextCommand(doc, "World", "Python"))
editor.show()

editor.undo()   # Undo the replace
editor.show()
```

### Real Backend Example — Transaction with Command + Audit Log

The Command pattern is perfect for **financial transactions** — you need
undo (refunds), audit trails, and retry logic:

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
import uuid


class BankCommand(ABC):
    def __init__(self):
        self.command_id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().isoformat()
        self.status = "pending"

    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def undo(self) -> bool:
        pass

    def to_audit_log(self) -> dict:
        return {
            "command_id": self.command_id,
            "type": self.__class__.__name__,
            "timestamp": self.timestamp,
            "status": self.status
        }


class BankAccount:
    def __init__(self, account_id: str, owner: str, balance: float = 0):
        self.account_id = account_id
        self.owner = owner
        self._balance = balance

    def credit(self, amount: float) -> bool:
        self._balance += amount
        return True

    def debit(self, amount: float) -> bool:
        if self._balance < amount:
            return False
        self._balance -= amount
        return True

    @property
    def balance(self):
        return self._balance

    def __repr__(self):
        return f"Account({self.owner}: ₹{self._balance:.2f})"


class TransferCommand(BankCommand):
    def __init__(self, from_account: BankAccount, to_account: BankAccount, amount: float):
        super().__init__()
        self._from = from_account
        self._to = to_account
        self._amount = amount

    def execute(self) -> bool:
        print(f"[Transfer:{self.command_id}] "
              f"₹{self._amount} from {self._from.owner} → {self._to.owner}")

        if not self._from.debit(self._amount):
            self.status = "failed"
            print(f"  ✗ Insufficient funds in {self._from.owner}'s account")
            return False

        self._to.credit(self._amount)
        self.status = "completed"
        print(f"  ✓ Transfer successful")
        return True

    def undo(self) -> bool:
        print(f"[Transfer UNDO:{self.command_id}] Reversing transfer")
        self._to.debit(self._amount)
        self._from.credit(self._amount)
        self.status = "reversed"
        print(f"  ✓ Transfer reversed")
        return True

    def to_audit_log(self) -> dict:
        log = super().to_audit_log()
        log.update({
            "from_account": self._from.account_id,
            "to_account": self._to.account_id,
            "amount": self._amount
        })
        return log


class TransactionManager:
    """Invoker — manages transactions with full audit trail"""

    def __init__(self):
        self._executed: List[BankCommand] = []
        self._audit_log: List[dict] = []

    def execute(self, command: BankCommand) -> bool:
        success = command.execute()
        self._executed.append(command)
        self._audit_log.append(command.to_audit_log())
        return success

    def undo_last(self):
        if not self._executed:
            return
        last = self._executed.pop()
        last.undo()
        self._audit_log.append(last.to_audit_log())

    def print_audit_log(self):
        print("\n=== AUDIT LOG ===")
        for entry in self._audit_log:
            print(f"  {entry['timestamp'][:19]} | {entry['type']} | "
                  f"ID:{entry['command_id']} | {entry['status']}")


# ─── Usage ────────────────────────────────────────────────────────
alice = BankAccount("ACC001", "Alice", balance=50000)
bob = BankAccount("ACC002", "Bob", balance=10000)
charlie = BankAccount("ACC003", "Charlie", balance=5000)

tm = TransactionManager()
print(f"Before: {alice}, {bob}, {charlie}")

tm.execute(TransferCommand(alice, bob, 15000))
tm.execute(TransferCommand(bob, charlie, 8000))
tm.execute(TransferCommand(charlie, alice, 20000))   # Will fail — insufficient funds

print(f"\nAfter: {alice}, {bob}, {charlie}")

print("\nUndo last successful transfer:")
tm.undo_last()
print(f"After undo: {alice}, {bob}, {charlie}")

tm.print_audit_log()
```

---

## All Three Patterns — Summary

| Pattern | Intent | Key Signal | Real Backend Use |
|---------|--------|-----------|-----------------|
| **Strategy** | Swap algorithms at runtime | `if method == "X"` chains | Payment methods, sorting, routing, compression |
| **Observer** | Notify many on state change | "When X happens, update Y, Z, W" | Event buses, webhooks, real-time feeds, pub/sub |
| **Command** | Encapsulate request as object | Need undo, queue, audit, retry | Transactions, task queues, CLI tools, undo/redo |

---

## How Strategy, Observer, and Command Work Together

These three often appear together in the same system:

```
User places an order (triggers event)
          │
          ▼
   [Observer/Event Bus]
   publishes "OrderPlaced"
          │
    ┌─────┴──────┐
    ▼            ▼
Payment       Inventory
Service       Service
    │
    ▼
[Strategy]
PaymentStrategyFactory
    → UPI / Card / Wallet
    │
    ▼
[Command]
TransferCommand
    → execute()
    → undo() if failure
    → logged in audit trail
```

---

## Interview Q&A

**Q: What is the difference between Strategy and State pattern?**

> "Both allow behavior to change, but for different reasons. Strategy changes
> behavior based on an EXTERNAL choice — the user picks a payment method.
> State changes behavior based on the object's INTERNAL state — a traffic light
> automatically changes from Red to Green to Yellow based on its own state machine.
> In Strategy, the context doesn't change the strategy automatically.
> In State, the state transitions happen inside the object."

**Q: How is Observer different from a simple callback function?**

> "A callback is a direct one-to-one coupling — the caller knows exactly which
> function to call. Observer is one-to-many and loosely coupled — the subject
> doesn't know who the observers are or what they do. You can add or remove
> observers at runtime without touching the subject. In a callback system, adding
> a 4th handler means modifying the publisher. In Observer, you just call
> `subscribe(new_handler)`. For event-driven microservices, Observer scales to
> message queues like Kafka where the publisher and consumer don't even run
> in the same process."

**Q: When would you use the Command pattern over direct method calls?**

> "Three situations: First, when you need UNDO — if an action must be reversible,
> wrap it in a Command with an `undo()` method. Second, when you need DEFERRED
> execution — task queues where commands are serialized and executed by workers
> later (Celery tasks are Command objects). Third, when you need an AUDIT TRAIL —
> financial systems where every action must be logged with who did what and when.
> Direct method calls give you none of these. Commands give you all three."

---

## Practice Exercise for Today

Build a **Smart Home Automation System** using all three patterns:

**Setup:**
- Devices: `Light`, `AirConditioner`, `SecurityCamera` (the Receivers)
- Commands: `TurnOnCommand`, `TurnOffCommand`, `SetTemperatureCommand`
- `SmartHomeController` as the Invoker (with undo support)

**Apply Observer:**
- When a `MotionSensor` detects motion, it notifies:
  - `Light` (turns on automatically)
  - `SecurityCamera` (starts recording)
  - `AlertSystem` (sends notification)

**Apply Strategy:**
- `AutomationMode` can be: "eco" (saves power), "comfort" (max comfort), "away" (security)
- Each mode defines different behavior for what devices do at night

---

*Next: Day 9 — LLD Problem: Parking Lot System (Full Design + Code)*
