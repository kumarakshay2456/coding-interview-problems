# Week 2 - Day 7: Structural Design Patterns
# Adapter, Decorator, Facade

---

## What Are Structural Patterns?

Creational patterns (Day 6) answered: *"How do we CREATE objects?"*

Structural patterns answer: *"How do we COMPOSE objects and classes together
to form larger, more capable structures — while keeping them flexible and clean?"*

Think of structural patterns like **architecture** in the real world:
- How do you connect an old building to a new one? (Adapter)
- How do you add new features to a room without tearing it down? (Decorator)
- How do you give someone a simple reception desk instead of navigating a complex building? (Facade)

Today we cover 3 of the most commonly asked structural patterns in SDE-3 interviews.

---

## Pattern 1: Adapter

### The Problem It Solves

You have two things that need to work together, but their **interfaces are incompatible**.
You can't change either of them (one is a third-party library, the other is your existing code).
You need a **translator** in between.

### Real World Analogy

Think about a **power adapter** when you travel internationally.

- Your Indian laptop charger has a Type-D plug (round pins)
- The UK wall socket accepts Type-G plug (rectangular pins)
- You can't change your laptop charger. You can't change the UK wall socket.
- You use an **adapter** — it sits between them and makes them compatible

The adapter doesn't change what the charger does or what the socket provides.
It **translates** one interface to another.

### Another Example — USB to HDMI Adapter

Your laptop has only USB-C ports. The projector has only HDMI.
You don't buy a new laptop. You don't buy a new projector.
You use a USB-C to HDMI adapter.

### The Problem Without Adapter

```python
# Your existing code — works with this interface
class OldPaymentProcessor:
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing {currency} {amount} via old system")
        return True


class CheckoutService:
    def __init__(self, processor: OldPaymentProcessor):
        self.processor = processor

    def checkout(self, amount: float):
        success = self.processor.process_payment(amount, "INR")
        if success:
            print("Checkout complete!")


# All works fine with the old processor
checkout = CheckoutService(OldPaymentProcessor())
checkout.checkout(1500.0)

# ─── Problem: We want to use Stripe now ──────────────────────────
# But Stripe has a COMPLETELY DIFFERENT interface
class StripePaymentGateway:
    """Third-party library — we CANNOT change this code"""

    def charge_card(self, amount_in_paise: int, card_token: str,
                    metadata: dict) -> dict:
        # Stripe works in paise (smallest currency unit), not rupees
        # It requires a card_token and metadata dictionary
        # It returns a dict, not a bool
        print(f"Stripe: Charging {amount_in_paise} paise")
        return {"status": "succeeded", "charge_id": "ch_abc123"}


# CheckoutService calls processor.process_payment(amount, currency)
# StripeGateway exposes charge_card(amount_in_paise, card_token, metadata)
# These are INCOMPATIBLE — CheckoutService cannot use Stripe directly
```

`CheckoutService` expects `process_payment(amount, currency)`.
`StripePaymentGateway` offers `charge_card(amount_in_paise, card_token, metadata)`.

Different method names, different parameters, different return types.
We cannot change CheckoutService (it's used everywhere).
We cannot change Stripe (it's a third-party library).

### Adapter Solution

```python
from abc import ABC, abstractmethod


# Step 1: Define the TARGET interface (what CheckoutService expects)
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> bool:
        pass


# Step 2: Existing processor already matches — no change needed
class OldPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing {currency} {amount} via old system")
        return True


# Step 3: Third-party class — DO NOT TOUCH
class StripePaymentGateway:
    def charge_card(self, amount_in_paise: int, card_token: str,
                    metadata: dict) -> dict:
        print(f"Stripe: Charging {amount_in_paise} paise | Token: {card_token}")
        return {"status": "succeeded", "charge_id": "ch_abc123"}


# Step 4: THE ADAPTER — wraps Stripe, speaks the language CheckoutService understands
class StripeAdapter(PaymentProcessor):
    """
    Adapts StripePaymentGateway to the PaymentProcessor interface.

    Internally uses Stripe's API. Externally looks like PaymentProcessor.
    CheckoutService has NO IDEA it's talking to Stripe.
    """

    def __init__(self, stripe_gateway: StripePaymentGateway, card_token: str):
        self._stripe = stripe_gateway
        self._card_token = card_token

    def process_payment(self, amount: float, currency: str) -> bool:
        # TRANSLATE: rupees → paise (Stripe requires smallest unit)
        amount_in_paise = int(amount * 100)

        # TRANSLATE: flat params → Stripe's required format
        metadata = {"currency": currency, "source": "checkout"}

        # Call Stripe's actual method
        result = self._stripe.charge_card(
            amount_in_paise,
            self._card_token,
            metadata
        )

        # TRANSLATE: Stripe's dict response → bool that CheckoutService expects
        return result.get("status") == "succeeded"


# Step 5: CheckoutService unchanged — works with any PaymentProcessor
class CheckoutService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def checkout(self, amount: float):
        success = self.processor.process_payment(amount, "INR")
        if success:
            print("Checkout complete!")
        else:
            print("Payment failed!")


# Using old processor — no change
checkout_old = CheckoutService(OldPaymentProcessor())
checkout_old.checkout(1500.0)

# Using Stripe via adapter — CheckoutService doesn't know the difference!
stripe = StripePaymentGateway()
stripe_adapter = StripeAdapter(stripe, card_token="tok_visa_4242")
checkout_stripe = CheckoutService(stripe_adapter)
checkout_stripe.checkout(1500.0)

# Tomorrow if we add PayPal — just write PayPalAdapter
# CheckoutService never changes
```

### Another Real Backend Example — Database Adapter

```python
# Your code expects this interface
class DatabaseAdapter(ABC):
    @abstractmethod
    def find_by_id(self, table: str, id: int) -> dict:
        pass

    @abstractmethod
    def insert(self, table: str, data: dict) -> int:
        pass


# Third-party MongoDB client — different interface
class MongoDBClient:
    """Pymongo-style interface — we cannot change this"""
    def find_one(self, collection: str, filter_dict: dict) -> dict:
        print(f"MongoDB: find_one in {collection} with {filter_dict}")
        return {"_id": "abc123", "name": "Alice"}

    def insert_one(self, collection: str, document: dict) -> str:
        print(f"MongoDB: insert_one into {collection}")
        return "inserted_id_xyz"


# Adapter makes MongoDB look like our DatabaseAdapter
class MongoDBAdapter(DatabaseAdapter):
    def __init__(self, mongo_client: MongoDBClient):
        self._client = mongo_client

    def find_by_id(self, table: str, id: int) -> dict:
        # MongoDB uses {"_id": id} filter
        result = self._client.find_one(table, {"_id": id})
        # Normalize: rename _id → id for our standard format
        if result:
            result["id"] = result.pop("_id")
        return result

    def insert(self, table: str, data: dict) -> int:
        inserted_id = self._client.insert_one(table, data)
        return hash(inserted_id)   # Convert MongoDB string ID to int


# Usage — your service uses DatabaseAdapter, doesn't know it's MongoDB
mongo_adapter = MongoDBAdapter(MongoDBClient())
user = mongo_adapter.find_by_id("users", 42)
print(user)
```

### When to Use Adapter

- Integrating third-party libraries that have incompatible interfaces
- Using legacy code alongside new code
- Making a class work with an interface it wasn't designed for

---

## Pattern 2: Decorator

### The Problem It Solves

You want to **add new behavior to an object** dynamically — without modifying
the original class and without using inheritance.

### Real World Analogy

Think about a **cup of coffee**:
- Start with plain black coffee — base object
- Add milk → milky coffee
- Add sugar → sweet milky coffee
- Add vanilla syrup → vanilla sweet milky coffee
- Add whipped cream → full fancy coffee

Each addition **wraps** the previous coffee and adds something new.
You didn't modify the coffee machine. You didn't create a new subclass
for every possible combination. You **stacked layers**.

That's the Decorator pattern.

### Why Not Inheritance?

If we used inheritance, we'd need:
- `CoffeeWithMilk`
- `CoffeeWithSugar`
- `CoffeeWithMilkAndSugar`
- `CoffeeWithMilkAndSugarAndVanilla`
- ...

With just 4 toppings, that's 2⁴ = **16 subclasses**. Completely unmanageable.
Decorator solves this with **composable layers**.

### Python Example — Coffee Shop

```python
from abc import ABC, abstractmethod


# Component interface — what all coffees must implement
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# Concrete component — the base object
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 50.0   # ₹50 base price

    def description(self) -> str:
        return "Simple black coffee"


# Base decorator — also implements Coffee, wraps another Coffee
class CoffeeDecorator(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee   # The thing we're wrapping

    def cost(self) -> float:
        return self._coffee.cost()   # Pass through to wrapped coffee

    def description(self) -> str:
        return self._coffee.description()


# Concrete decorators — each adds ONE thing
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 20.0   # Milk costs ₹20 extra

    def description(self) -> str:
        return self._coffee.description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 10.0   # Sugar costs ₹10 extra

    def description(self) -> str:
        return self._coffee.description() + ", sugar"


class VanillaDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 35.0

    def description(self) -> str:
        return self._coffee.description() + ", vanilla syrup"


class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 45.0

    def description(self) -> str:
        return self._coffee.description() + ", whipped cream"


# ─── Build your coffee by stacking decorators ─────────────────────

# Plain coffee
coffee = SimpleCoffee()
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Simple black coffee → ₹50.0

# Add milk
coffee = MilkDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Simple black coffee, milk → ₹70.0

# Add sugar
coffee = SugarDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Simple black coffee, milk, sugar → ₹80.0

# Add vanilla on top of everything
coffee = VanillaDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Simple black coffee, milk, sugar, vanilla syrup → ₹115.0

# Build a completely different coffee — double sugar, no milk
coffee2 = SugarDecorator(SugarDecorator(SimpleCoffee()))
print(f"{coffee2.description()} → ₹{coffee2.cost()}")
# Simple black coffee, sugar, sugar → ₹70.0
```

### Real Backend Example — HTTP Middleware (Most Important for SDE-3)

In real backend systems, Decorator is how **middleware** works.
Each middleware wraps the request handler and adds a behavior:
logging, authentication, rate limiting, compression, caching.

```python
from abc import ABC, abstractmethod
from typing import Callable, Dict
import time


# Component — represents any request handler
class RequestHandler(ABC):
    @abstractmethod
    def handle(self, request: dict) -> dict:
        pass


# Concrete handler — the actual business logic
class APIHandler(RequestHandler):
    def handle(self, request: dict) -> dict:
        print(f"  [APIHandler] Processing: {request.get('path')}")
        return {
            "status": 200,
            "body": {"message": "Success", "data": {"user_id": 42}}
        }


# Base decorator
class HandlerDecorator(RequestHandler, ABC):
    def __init__(self, handler: RequestHandler):
        self._handler = handler


# Decorator 1: Logging
class LoggingDecorator(HandlerDecorator):
    def handle(self, request: dict) -> dict:
        print(f"[LOG] Request: {request.get('method')} {request.get('path')}")
        start = time.time()

        response = self._handler.handle(request)   # Call wrapped handler

        elapsed = (time.time() - start) * 1000
        print(f"[LOG] Response: {response['status']} in {elapsed:.2f}ms")
        return response


# Decorator 2: Authentication
class AuthDecorator(HandlerDecorator):
    VALID_TOKENS = {"secret_token_123", "admin_token_456"}

    def handle(self, request: dict) -> dict:
        token = request.get("headers", {}).get("Authorization", "")

        if token not in self.VALID_TOKENS:
            print(f"[AUTH] Unauthorized — invalid token")
            return {"status": 401, "body": {"error": "Unauthorized"}}

        print(f"[AUTH] Token valid — proceeding")
        return self._handler.handle(request)


# Decorator 3: Rate Limiting
class RateLimitDecorator(HandlerDecorator):
    def __init__(self, handler: RequestHandler, max_requests: int = 5):
        super().__init__(handler)
        self._max_requests = max_requests
        self._request_counts: Dict[str, int] = {}

    def handle(self, request: dict) -> dict:
        client_ip = request.get("ip", "unknown")
        count = self._request_counts.get(client_ip, 0)

        if count >= self._max_requests:
            print(f"[RATE LIMIT] IP {client_ip} has exceeded limit")
            return {"status": 429, "body": {"error": "Too Many Requests"}}

        self._request_counts[client_ip] = count + 1
        print(f"[RATE LIMIT] IP {client_ip}: request {count + 1}/{self._max_requests}")
        return self._handler.handle(request)


# Decorator 4: Caching
class CacheDecorator(HandlerDecorator):
    def __init__(self, handler: RequestHandler):
        super().__init__(handler)
        self._cache: dict = {}

    def handle(self, request: dict) -> dict:
        cache_key = f"{request.get('method')}:{request.get('path')}"

        if cache_key in self._cache:
            print(f"[CACHE] Cache HIT for {cache_key}")
            return self._cache[cache_key]

        print(f"[CACHE] Cache MISS for {cache_key} — calling handler")
        response = self._handler.handle(request)

        if response.get("status") == 200:   # Only cache successful responses
            self._cache[cache_key] = response

        return response


# ─── Stack the decorators — ORDER MATTERS ─────────────────────────
# Outermost layer runs first. Stack: Logger → RateLimit → Auth → Cache → Handler

handler = APIHandler()                          # Core handler
handler = CacheDecorator(handler)               # Layer 4 (closest to core)
handler = AuthDecorator(handler)                # Layer 3
handler = RateLimitDecorator(handler, max_requests=3)  # Layer 2
handler = LoggingDecorator(handler)             # Layer 1 (outermost)


request = {
    "method": "GET",
    "path": "/api/users/42",
    "ip": "192.168.1.1",
    "headers": {"Authorization": "secret_token_123"}
}

print("=== Request 1 ===")
resp = handler.handle(request)
print(f"Final Response: {resp['status']}\n")

print("=== Request 2 (same — should hit cache) ===")
resp = handler.handle(request)
print(f"Final Response: {resp['status']}\n")

print("=== Request 3 (bad auth) ===")
bad_request = {**request, "headers": {"Authorization": "wrong_token"}}
resp = handler.handle(bad_request)
print(f"Final Response: {resp['status']}")
```

### Python's Built-in `@decorator` Syntax

Python has first-class support for decorators with `@` syntax — you use it every day
with `@property`, `@staticmethod`, `@classmethod`. You can write your own:

```python
import functools
import time


def timing_decorator(func):
    """A simple function decorator that measures execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMING] {func.__name__} took {(end - start)*1000:.2f}ms")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """A parametrized decorator that retries a function on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


@timing_decorator
@retry(max_attempts=3, delay=0.1)
def fetch_user_from_api(user_id: int) -> dict:
    import random
    if random.random() < 0.6:   # 60% chance of failure (simulating flaky network)
        raise ConnectionError("Network timeout")
    return {"user_id": user_id, "name": "Alice"}


try:
    user = fetch_user_from_api(42)
    print(f"Got user: {user}")
except ConnectionError as e:
    print(f"All retries failed: {e}")
```

---

## Pattern 3: Facade

### The Problem It Solves

A complex system has many subsystems, each with its own interface.
To use the system, a caller has to understand and interact with ALL subsystems.
This creates high coupling and complexity for the caller.

**Facade** provides a **single, simple interface** to a complex subsystem.
It doesn't add new functionality — it simplifies access.

### Real World Analogy

When you call **customer support** for your internet connection:
- You call ONE number
- The support agent (facade) behind the scenes talks to: the billing system,
  the network operations center, the field engineer dispatch system,
  and the account management system
- You don't know any of these exist
- You just say "my internet is slow" and the agent handles everything

The support agent is the **facade** — one simple interface to a complex system.

### Another Analogy — Hotel Concierge

You're staying at a 5-star hotel. You tell the concierge:
*"I need airport pickup, a restaurant reservation, and a city tour tomorrow."*

The concierge calls the airport shuttle service, the restaurant booking system,
and the tour operator. You interact with ONE person. The concierge hides all
the complexity.

### Code Example — Home Theater System

```python
# ─── Complex subsystems — each has its own interface ─────────────

class Projector:
    def on(self): print("Projector: Turning ON")
    def off(self): print("Projector: Turning OFF")
    def set_input(self, source: str): print(f"Projector: Input set to {source}")
    def set_resolution(self, res: str): print(f"Projector: Resolution {res}")


class SoundSystem:
    def on(self): print("Sound System: Powering ON")
    def off(self): print("Sound System: Powering OFF")
    def set_volume(self, level: int): print(f"Sound System: Volume set to {level}")
    def set_mode(self, mode: str): print(f"Sound System: Mode set to {mode}")
    def connect_source(self, src: str): print(f"Sound System: Connected to {src}")


class StreamingDevice:
    def on(self): print("Streaming Device: Booting up")
    def off(self): print("Streaming Device: Shutting down")
    def connect_wifi(self): print("Streaming Device: Connected to WiFi")
    def open_app(self, app: str): print(f"Streaming Device: Opening {app}")
    def play(self, title: str): print(f"Streaming Device: Playing '{title}'")


class SmartLighting:
    def dim(self, level: int): print(f"Lighting: Dimmed to {level}%")
    def set_color(self, color: str): print(f"Lighting: Color set to {color}")
    def on(self): print("Lighting: ON")


class AirConditioner:
    def on(self): print("AC: ON")
    def set_temperature(self, temp: int): print(f"AC: Temperature set to {temp}°C")


# ─── THE FACADE ───────────────────────────────────────────────────

class HomeTheaterFacade:
    """
    Provides a simple interface to the complex home theater system.

    The user doesn't need to know about Projector, SoundSystem,
    StreamingDevice, Lighting, or AC individually.
    They just say "watch movie" or "end movie".
    """

    def __init__(self):
        self.projector = Projector()
        self.sound = SoundSystem()
        self.streaming = StreamingDevice()
        self.lighting = SmartLighting()
        self.ac = AirConditioner()

    def watch_movie(self, movie_title: str):
        """One call sets up the entire home theater experience"""
        print(f"\n🎬 Preparing to watch: '{movie_title}'")
        print("─" * 50)

        self.lighting.dim(10)
        self.lighting.set_color("warm white")

        self.ac.on()
        self.ac.set_temperature(22)

        self.projector.on()
        self.projector.set_input("HDMI-1")
        self.projector.set_resolution("4K")

        self.sound.on()
        self.sound.set_volume(40)
        self.sound.set_mode("Dolby Atmos")
        self.sound.connect_source("HDMI-1")

        self.streaming.on()
        self.streaming.connect_wifi()
        self.streaming.open_app("Netflix")
        self.streaming.play(movie_title)

        print("─" * 50)
        print("🍿 Enjoy your movie!\n")

    def end_movie(self):
        """One call shuts down everything properly"""
        print("\n⏹ Ending movie session...")
        print("─" * 50)

        self.streaming.off()
        self.projector.off()
        self.sound.off()
        self.lighting.on()
        print("─" * 50)
        print("Goodbye!\n")


# ─── Usage — single, clean interface ─────────────────────────────
theater = HomeTheaterFacade()
theater.watch_movie("Interstellar")
# ... watch the movie ...
theater.end_movie()
```

### Real Backend Example — Order Processing Facade

This is the most important example for an SDE-3 interview.
In a real e-commerce backend, placing an order involves many services:

```python
from dataclasses import dataclass
from typing import List


# ─── Complex subsystems ───────────────────────────────────────────

class InventoryService:
    def check_stock(self, product_id: str, quantity: int) -> bool:
        print(f"[Inventory] Checking stock for {product_id} x{quantity}")
        return True   # Simulate: in stock

    def reserve_items(self, product_id: str, quantity: int):
        print(f"[Inventory] Reserving {quantity} units of {product_id}")

    def release_reservation(self, product_id: str, quantity: int):
        print(f"[Inventory] Releasing reservation for {product_id} x{quantity}")


class PaymentService:
    def charge(self, user_id: str, amount: float, payment_method: str) -> str:
        print(f"[Payment] Charging ₹{amount} to {user_id} via {payment_method}")
        return "txn_abc123"   # Return transaction ID

    def refund(self, transaction_id: str):
        print(f"[Payment] Refunding transaction {transaction_id}")


class ShippingService:
    def create_shipment(self, order_id: str, address: dict) -> str:
        print(f"[Shipping] Creating shipment for order {order_id}")
        return "SHIP_XYZ789"   # Return tracking number

    def cancel_shipment(self, tracking_number: str):
        print(f"[Shipping] Cancelling shipment {tracking_number}")


class NotificationService:
    def send_order_confirmation(self, user_id: str, order_id: str):
        print(f"[Notification] Sending confirmation to user {user_id} for order {order_id}")

    def send_failure_notification(self, user_id: str, reason: str):
        print(f"[Notification] Sending failure notice to {user_id}: {reason}")


class AuditService:
    def log_order(self, order_id: str, status: str, details: dict):
        print(f"[Audit] Order {order_id}: {status} | {details}")


# ─── ORDER DATA ───────────────────────────────────────────────────

@dataclass
class OrderRequest:
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    amount: float
    payment_method: str
    shipping_address: dict


# ─── THE FACADE ───────────────────────────────────────────────────

class OrderFacade:
    """
    Coordinates the entire order placement across 5 services.
    The controller/API layer calls ONE method — place_order().
    All the orchestration is hidden inside.
    """

    def __init__(self):
        self._inventory = InventoryService()
        self._payment = PaymentService()
        self._shipping = ShippingService()
        self._notification = NotificationService()
        self._audit = AuditService()

    def place_order(self, order: OrderRequest) -> dict:
        print(f"\n{'='*50}")
        print(f"Processing Order: {order.order_id}")
        print(f"{'='*50}")

        transaction_id = None
        tracking_number = None

        try:
            # Step 1: Check inventory
            if not self._inventory.check_stock(order.product_id, order.quantity):
                raise ValueError("Item out of stock")

            # Step 2: Reserve inventory
            self._inventory.reserve_items(order.product_id, order.quantity)

            # Step 3: Charge payment
            transaction_id = self._payment.charge(
                order.user_id, order.amount, order.payment_method
            )

            # Step 4: Create shipment
            tracking_number = self._shipping.create_shipment(
                order.order_id, order.shipping_address
            )

            # Step 5: Notify user
            self._notification.send_order_confirmation(order.user_id, order.order_id)

            # Step 6: Audit log
            self._audit.log_order(order.order_id, "SUCCESS", {
                "transaction_id": transaction_id,
                "tracking_number": tracking_number
            })

            print(f"{'='*50}")
            print(f"Order {order.order_id} placed successfully!")
            return {
                "success": True,
                "order_id": order.order_id,
                "transaction_id": transaction_id,
                "tracking_number": tracking_number
            }

        except Exception as e:
            # Compensating actions — undo what we've done (saga pattern basics)
            print(f"\n[ERROR] Order failed: {e}. Rolling back...")

            if transaction_id:
                self._payment.refund(transaction_id)

            if tracking_number:
                self._shipping.cancel_shipment(tracking_number)

            self._inventory.release_reservation(order.product_id, order.quantity)
            self._notification.send_failure_notification(order.user_id, str(e))
            self._audit.log_order(order.order_id, "FAILED", {"reason": str(e)})

            return {"success": False, "error": str(e)}


# ─── Usage — The API controller only calls ONE method ─────────────
# (In real Flask/FastAPI, this would be in a route handler)

order_facade = OrderFacade()

order = OrderRequest(
    order_id="ORD_001",
    user_id="USR_42",
    product_id="PROD_LAPTOP",
    quantity=1,
    amount=65000.0,
    payment_method="credit_card",
    shipping_address={"city": "Mumbai", "pin": "400001"}
)

result = order_facade.place_order(order)
print(f"\nResult: {result}")
```

### Facade vs Adapter — The Difference

People often confuse these two. Here is the clear distinction:

| | Adapter | Facade |
|---|---|---|
| **Purpose** | Make INCOMPATIBLE interfaces work together | Make a COMPLEX system SIMPLE |
| **Interfaces** | Two existing incompatible interfaces | One new simplified interface over many |
| **Analogy** | Power plug adapter | Hotel concierge |
| **Changes interfaces?** | YES — translates one to another | NO — provides a NEW simplified one |
| **Use when** | You need two things to talk that can't | You want to hide complexity |

---

## All Three Patterns — Summary

| Pattern | Type | Problem Solved | Real Backend Use |
|---------|------|---------------|-----------------|
| **Adapter** | Structural | Incompatible interfaces | Third-party SDK integration |
| **Decorator** | Structural | Add behavior without modifying | Middleware (logging, auth, caching) |
| **Facade** | Structural | Complex subsystem access | Service orchestration, API layer |

---

## Interview Q&A

**Q: How does the Decorator pattern differ from Inheritance?**

> "Inheritance adds behavior at compile/define time — it's static. You decide
> upfront what a subclass does. Decorator adds behavior at runtime — it's dynamic.
> You wrap an object with as many decorators as needed, in any order, and can
> change the combination without writing new subclasses. For a coffee with 4 toppings,
> inheritance needs 16 subclasses. Decorator needs 4 decorator classes and
> composes them. Decorator also follows OCP — you add new behaviors by writing
> new decorators, not modifying existing ones."

**Q: Can you give a real example where you'd use Facade in a microservices system?**

> "In a microservices architecture, a 'checkout' operation might require calling
> inventory service, payment service, shipping service, notification service,
> and fraud detection. If the API gateway or BFF (Backend for Frontend) calls
> all five directly, it becomes tightly coupled to each service's interface.
> A Facade — often called an orchestrator service — abstracts this complexity.
> The client calls one endpoint, the orchestrator coordinates all five services,
> handles failures and rollbacks, and returns one unified response. The client
> never needs to know five services were involved."

**Q: When should you NOT use Facade?**

> "When the simplified interface hides too much — sometimes callers legitimately
> need fine-grained control over a subsystem. Also, Facade can become a 'God Object'
> if it grows to orchestrate too many things. Keep Facades focused on one workflow.
> If a Facade starts handling 20 different subsystems, it's a sign the system
> needs better decomposition, not a bigger Facade."

---

## Practice Exercise for Today

Build a **File Processing Facade** for a data pipeline:

Subsystems:
1. `FileReader` — reads CSV files, returns list of rows
2. `DataValidator` — validates each row (no empty fields, numbers are valid)
3. `DataTransformer` — transforms rows (trim strings, parse numbers, add timestamps)
4. `DatabaseWriter` — writes transformed rows to a database
5. `ReportGenerator` — generates a summary report (total rows, failed rows, success rate)

Facade:
- `DataPipelineFacade.process(file_path: str) -> dict`
- Should handle the entire pipeline: read → validate → transform → write → report
- On any failure, log the error and continue with remaining rows (don't crash)
- Return a summary: `{"processed": N, "failed": M, "success_rate": "%"}`

---

*Next: Day 8 — Behavioral Patterns (Strategy, Observer, Command)*
