# Week 2 - Day 9: LLD Problem — Parking Lot System
# Full Design: Requirements → Entities → UML → Code

---

## How to Approach ANY LLD Problem in an Interview

Before writing a single line of code, follow this process every time.
Interviewers watch HOW you think, not just what you code.

```
Step 1: Clarify Requirements      (2-3 minutes)
Step 2: Identify Entities         (2 minutes)
Step 3: Define Relationships      (2 minutes)
Step 4: Draw UML Diagram          (3-4 minutes)
Step 5: Write Code                (15-20 minutes)
Step 6: Handle Edge Cases         (5 minutes)
```

Never skip Steps 1-4. An interviewer who sees you jump straight to code
will assume you don't know how to design systems.

---

## Step 1: Clarify Requirements

When the interviewer says "Design a Parking Lot", ask these questions:

**You:** "Before I start, can I clarify a few things?"
- What types of vehicles do we need to support? (Cars, motorcycles, trucks?)
- Is the parking lot multi-floor or single level?
- What are the different spot sizes? (Compact, regular, large?)
- How is pricing calculated? (Per hour? Flat rate?)
- Do we need to track entry/exit time?
- Do we need to handle reserved spots or VIP spots?
- Should the system find the nearest available spot?

**Assumed Requirements (for this problem):**
1. The parking lot has multiple floors
2. Each floor has multiple parking spots
3. Three spot types: SMALL (for motorcycles), MEDIUM (for cars), LARGE (for trucks/buses)
4. Three vehicle types: MOTORCYCLE, CAR, TRUCK
5. A vehicle can only park in a spot that fits it (motorcycle in any, car in medium+, truck in large only)
6. System issues a ticket on entry and calculates fee on exit
7. Pricing: SMALL = ₹10/hr, MEDIUM = ₹20/hr, LARGE = ₹40/hr
8. System can find nearest available spot for a given vehicle
9. Show real-time capacity: total spots, occupied, available

---

## Step 2: Identify Entities (Nouns → Classes)

Read the requirements and extract all nouns:

| Noun Found | Becomes Class |
|-----------|--------------|
| Parking Lot | `ParkingLot` |
| Floor | `ParkingFloor` |
| Spot | `ParkingSpot` |
| Vehicle | `Vehicle` (abstract) |
| Motorcycle | `Motorcycle` |
| Car | `Car` |
| Truck | `Truck` |
| Ticket | `ParkingTicket` |
| Fee | `FeeCalculator` |
| Entry/Exit | `EntranceGate`, `ExitGate` |

---

## Step 3: Define Attributes and Methods

### ParkingLot
- Attributes: `name`, `address`, `floors`
- Methods: `find_available_spot(vehicle)`, `issue_ticket(vehicle)`, `process_exit(ticket)`, `get_capacity()`

### ParkingFloor
- Attributes: `floor_number`, `spots`
- Methods: `get_available_spots(spot_type)`, `get_spot(spot_id)`

### ParkingSpot
- Attributes: `spot_id`, `spot_type`, `is_occupied`, `current_vehicle`
- Methods: `occupy(vehicle)`, `vacate()`, `is_available()`

### Vehicle (abstract)
- Attributes: `license_plate`, `vehicle_type`
- Methods: `get_spot_type_needed()` — returns what spot size this vehicle needs

### ParkingTicket
- Attributes: `ticket_id`, `vehicle`, `spot`, `entry_time`, `exit_time`, `fee`
- Methods: `calculate_fee()`, `close()`

### FeeCalculator
- Methods: `calculate(spot_type, duration_hours)` — Strategy pattern!

---

## Step 4: UML Diagram

```
┌──────────────────────────────────────────────────────────────────────┐

                    ┌───────────────────────┐
                    │      ParkingLot       │
                    │───────────────────────│
                    │ - name: str           │
                    │ - address: str        │
                    │───────────────────────│
                    │ + find_spot(vehicle)  │
                    │ + issue_ticket()      │
                    │ + process_exit()      │
                    │ + get_capacity()      │
                    └───────────┬───────────┘
                                │ ◆ 1..*  (Composition)
                    ┌───────────▼───────────┐
                    │     ParkingFloor      │
                    │───────────────────────│
                    │ - floor_number: int   │
                    │ - display_board       │
                    │───────────────────────│
                    │ + get_available()     │
                    │ + get_spot()          │
                    └───────────┬───────────┘
                                │ ◆ 1..*  (Composition)
                    ┌───────────▼───────────┐
                    │      ParkingSpot      │
                    │───────────────────────│
                    │ - spot_id: str        │
                    │ - spot_type: SpotType │
                    │ - is_occupied: bool   │
                    │───────────────────────│
                    │ + occupy(vehicle)     │
                    │ + vacate()            │
                    │ + is_available()      │
                    └───────────┬───────────┘
                                │ 0..1 (Association)
              ┌─────────────────┴──────────────────┐
              ▼                                     ▼
  ┌───────────────────────┐         ┌───────────────────────┐
  │  «abstract» Vehicle   │         │    ParkingTicket      │
  │───────────────────────│         │───────────────────────│
  │ - license_plate: str  │         │ - ticket_id: str      │
  │ - vehicle_type: enum  │         │ - entry_time: datetime│
  │───────────────────────│         │ - exit_time: datetime │
  │ + get_spot_type(): enum│        │ - fee: float          │
  └───────────┬───────────┘         │───────────────────────│
              │ IS-A                │ + calculate_fee()     │
    ┌─────────┼──────────┐          │ + close()             │
    ▼         ▼          ▼          └───────────────────────┘
┌────────┐ ┌──────┐ ┌─────────┐
│Motorcycle│ │ Car │ │  Truck  │
└────────┘ └──────┘ └─────────┘

  ┌───────────────────────┐
  │   «interface»         │
  │   FeeStrategy         │
  │───────────────────────│
  │ + calculate(type,hrs) │
  └───────────┬───────────┘
              │ (realization)
  ┌───────────▼───────────┐
  │  HourlyFeeStrategy    │
  │───────────────────────│
  │ RATES: dict           │
  │───────────────────────│
  │ + calculate()         │
  └───────────────────────┘

└──────────────────────────────────────────────────────────────────────┘

Enums:
  SpotType  → SMALL, MEDIUM, LARGE
  VehicleType → MOTORCYCLE, CAR, TRUCK
```

---

## Step 5: Full Code Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional
import uuid


# ─────────────────────────────────────────────────────────────────
# ENUMS — define all constant types cleanly
# ─────────────────────────────────────────────────────────────────

class SpotType(Enum):
    SMALL = "SMALL"      # For motorcycles
    MEDIUM = "MEDIUM"    # For cars
    LARGE = "LARGE"      # For trucks/buses


class VehicleType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    TRUCK = "TRUCK"


class TicketStatus(Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


# ─────────────────────────────────────────────────────────────────
# VEHICLE HIERARCHY
# ─────────────────────────────────────────────────────────────────

class Vehicle(ABC):
    """
    Abstract base for all vehicles.
    Each vehicle type knows what spot size it needs.
    """

    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate.upper()
        self.vehicle_type = vehicle_type

    @abstractmethod
    def get_spot_type_needed(self) -> SpotType:
        """
        Returns the MINIMUM spot type this vehicle can park in.
        Motorcycle → SMALL (can use any spot)
        Car → MEDIUM (needs at least medium)
        Truck → LARGE (needs large only)
        """
        pass

    def __repr__(self) -> str:
        return f"{self.vehicle_type.value}({self.license_plate})"


class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

    def get_spot_type_needed(self) -> SpotType:
        return SpotType.SMALL   # Motorcycles prefer small spots


class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

    def get_spot_type_needed(self) -> SpotType:
        return SpotType.MEDIUM


class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)

    def get_spot_type_needed(self) -> SpotType:
        return SpotType.LARGE


# ─────────────────────────────────────────────────────────────────
# FEE STRATEGY — Strategy Pattern for pricing
# ─────────────────────────────────────────────────────────────────

class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, spot_type: SpotType, duration_hours: float) -> float:
        pass


class HourlyFeeStrategy(FeeStrategy):
    """
    Charges per hour based on spot type.
    Partial hours are rounded up (30 min = 1 hour charge).
    """
    RATES = {
        SpotType.SMALL:  10.0,   # ₹10 per hour for small spots
        SpotType.MEDIUM: 20.0,   # ₹20 per hour for medium spots
        SpotType.LARGE:  40.0,   # ₹40 per hour for large spots
    }

    def calculate(self, spot_type: SpotType, duration_hours: float) -> float:
        import math
        rate = self.RATES[spot_type]
        # Round up to nearest hour — 1.5 hrs = 2 hrs charge
        billable_hours = math.ceil(duration_hours)
        return rate * billable_hours


class FlatRateFeeStrategy(FeeStrategy):
    """Flat rate — same price regardless of how long you stay"""
    FLAT_RATES = {
        SpotType.SMALL:  50.0,
        SpotType.MEDIUM: 100.0,
        SpotType.LARGE:  200.0,
    }

    def calculate(self, spot_type: SpotType, duration_hours: float) -> float:
        return self.FLAT_RATES[spot_type]


# ─────────────────────────────────────────────────────────────────
# PARKING TICKET
# ─────────────────────────────────────────────────────────────────

class ParkingTicket:
    """
    Issued when a vehicle enters. Holds all info about a parking session.
    Calculates fee when the vehicle exits.
    """

    def __init__(self, vehicle: Vehicle, spot: "ParkingSpot", fee_strategy: FeeStrategy):
        self.ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.fee: float = 0.0
        self.status = TicketStatus.ACTIVE
        self._fee_strategy = fee_strategy

    def close(self) -> float:
        """Call this when vehicle exits. Returns the fee to be paid."""
        if self.status == TicketStatus.CLOSED:
            raise RuntimeError(f"Ticket {self.ticket_id} is already closed")

        self.exit_time = datetime.now()
        duration = (self.exit_time - self.entry_time).total_seconds() / 3600
        # Minimum charge of 1 hour
        duration = max(duration, 1.0)
        self.fee = self._fee_strategy.calculate(self.spot.spot_type, duration)
        self.status = TicketStatus.CLOSED
        return self.fee

    def get_duration_str(self) -> str:
        end = self.exit_time or datetime.now()
        duration_sec = (end - self.entry_time).total_seconds()
        hours = int(duration_sec // 3600)
        minutes = int((duration_sec % 3600) // 60)
        return f"{hours}h {minutes}m"

    def __repr__(self) -> str:
        return (f"Ticket({self.ticket_id} | {self.vehicle} | "
                f"Spot:{self.spot.spot_id} | {self.status.value})")


# ─────────────────────────────────────────────────────────────────
# PARKING SPOT
# ─────────────────────────────────────────────────────────────────

class ParkingSpot:
    """
    A single parking spot. Knows its type and whether it's occupied.
    Enforces that only appropriate vehicles can park here.
    """

    # Defines which vehicle types are ALLOWED in each spot type
    ALLOWED_VEHICLES: Dict[SpotType, List[VehicleType]] = {
        SpotType.SMALL:  [VehicleType.MOTORCYCLE],
        SpotType.MEDIUM: [VehicleType.MOTORCYCLE, VehicleType.CAR],
        SpotType.LARGE:  [VehicleType.MOTORCYCLE, VehicleType.CAR, VehicleType.TRUCK],
    }

    def __init__(self, spot_id: str, spot_type: SpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self._is_occupied = False
        self._current_vehicle: Optional[Vehicle] = None

    def is_available(self) -> bool:
        return not self._is_occupied

    def can_fit(self, vehicle: Vehicle) -> bool:
        """Returns True if this vehicle type is allowed in this spot"""
        return vehicle.vehicle_type in self.ALLOWED_VEHICLES[self.spot_type]

    def occupy(self, vehicle: Vehicle) -> None:
        if self._is_occupied:
            raise RuntimeError(f"Spot {self.spot_id} is already occupied")
        if not self.can_fit(vehicle):
            raise ValueError(
                f"{vehicle.vehicle_type.value} cannot park in {self.spot_type.value} spot"
            )
        self._is_occupied = True
        self._current_vehicle = vehicle

    def vacate(self) -> None:
        if not self._is_occupied:
            raise RuntimeError(f"Spot {self.spot_id} is already empty")
        self._is_occupied = False
        self._current_vehicle = None

    @property
    def current_vehicle(self) -> Optional[Vehicle]:
        return self._current_vehicle

    def __repr__(self) -> str:
        status = f"[{self._current_vehicle.license_plate}]" if self._is_occupied else "[FREE]"
        return f"Spot({self.spot_id} | {self.spot_type.value} | {status})"


# ─────────────────────────────────────────────────────────────────
# DISPLAY BOARD — Observer Pattern
# ─────────────────────────────────────────────────────────────────

class DisplayBoard:
    """
    Shows real-time availability on each floor.
    Updated whenever a spot is occupied or vacated — Observer pattern.
    """

    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self._counts: Dict[SpotType, int] = {
            SpotType.SMALL: 0,
            SpotType.MEDIUM: 0,
            SpotType.LARGE: 0,
        }

    def update(self, spot_type: SpotType, delta: int):
        """delta = +1 (spot freed) or -1 (spot taken)"""
        self._counts[spot_type] += delta

    def show(self):
        print(f"  Floor {self.floor_number} Available: "
              f"Small={self._counts[SpotType.SMALL]} | "
              f"Medium={self._counts[SpotType.MEDIUM]} | "
              f"Large={self._counts[SpotType.LARGE]}")


# ─────────────────────────────────────────────────────────────────
# PARKING FLOOR
# ─────────────────────────────────────────────────────────────────

class ParkingFloor:
    """
    One floor of the parking lot.
    Manages a collection of spots and a display board.
    """

    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self._spots: Dict[str, ParkingSpot] = {}
        self.display_board = DisplayBoard(floor_number)

    def add_spot(self, spot: ParkingSpot) -> None:
        self._spots[spot.spot_id] = spot
        if spot.is_available():
            self.display_board.update(spot.spot_type, +1)

    def get_available_spots(self, vehicle: Vehicle) -> List[ParkingSpot]:
        """Returns all spots on this floor that can fit the given vehicle"""
        return [
            spot for spot in self._spots.values()
            if spot.is_available() and spot.can_fit(vehicle)
        ]

    def occupy_spot(self, spot_id: str, vehicle: Vehicle) -> None:
        spot = self._spots[spot_id]
        spot.occupy(vehicle)
        self.display_board.update(spot.spot_type, -1)   # Update display

    def vacate_spot(self, spot_id: str) -> None:
        spot = self._spots[spot_id]
        spot.vacate()
        self.display_board.update(spot.spot_type, +1)   # Update display

    def get_spot(self, spot_id: str) -> ParkingSpot:
        if spot_id not in self._spots:
            raise ValueError(f"Spot {spot_id} not found on floor {self.floor_number}")
        return self._spots[spot_id]

    def get_total_count(self) -> Dict[SpotType, int]:
        counts = {t: 0 for t in SpotType}
        for spot in self._spots.values():
            counts[spot.spot_type] += 1
        return counts

    def get_available_count(self) -> Dict[SpotType, int]:
        counts = {t: 0 for t in SpotType}
        for spot in self._spots.values():
            if spot.is_available():
                counts[spot.spot_type] += 1
        return counts

    def __repr__(self) -> str:
        return f"Floor({self.floor_number}, {len(self._spots)} spots)"


# ─────────────────────────────────────────────────────────────────
# PARKING LOT — The Facade
# ─────────────────────────────────────────────────────────────────

class ParkingLot:
    """
    The main class. Acts as a Facade over floors and spots.
    Uses Singleton pattern — only one parking lot instance.
    Orchestrates: finding spots, issuing tickets, processing exits.
    """

    _instance = None

    @classmethod
    def get_instance(cls, name: str = "", address: str = "") -> "ParkingLot":
        if cls._instance is None:
            cls._instance = cls(name, address)
        return cls._instance

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self._floors: List[ParkingFloor] = []
        self._active_tickets: Dict[str, ParkingTicket] = {}   # ticket_id → ticket
        self._vehicle_ticket_map: Dict[str, str] = {}         # license_plate → ticket_id
        self._fee_strategy: FeeStrategy = HourlyFeeStrategy() # Default strategy

    def set_fee_strategy(self, strategy: FeeStrategy) -> None:
        """Strategy pattern — swap pricing at runtime"""
        self._fee_strategy = strategy

    def add_floor(self, floor: ParkingFloor) -> None:
        self._floors.append(floor)

    # ─── CORE OPERATIONS ──────────────────────────────────────────

    def find_nearest_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Finds the nearest available spot for a vehicle.
        "Nearest" = lowest floor number, then preferred spot type first.

        Strategy: prefer exact-fit spots first to avoid wasting large spots
        on small vehicles.
        """
        preferred_type = vehicle.get_spot_type_needed()

        # First pass: find spots of the EXACT preferred type
        for floor in self._floors:
            for spot in floor.get_available_spots(vehicle):
                if spot.spot_type == preferred_type:
                    return spot

        # Second pass: find any fitting spot (larger than needed)
        for floor in self._floors:
            available = floor.get_available_spots(vehicle)
            if available:
                return available[0]

        return None   # No spot available

    def issue_ticket(self, vehicle: Vehicle) -> ParkingTicket:
        """
        Called when a vehicle enters.
        Finds a spot, assigns it, creates and returns a ticket.
        """
        # Check if vehicle is already parked
        if vehicle.license_plate in self._vehicle_ticket_map:
            raise RuntimeError(
                f"Vehicle {vehicle.license_plate} is already parked. "
                f"Ticket: {self._vehicle_ticket_map[vehicle.license_plate]}"
            )

        spot = self.find_nearest_available_spot(vehicle)
        if not spot:
            raise RuntimeError(
                f"No available spot for {vehicle.vehicle_type.value}. Parking lot is full!"
            )

        # Find which floor this spot is on and occupy it
        floor = self._get_floor_for_spot(spot.spot_id)
        floor.occupy_spot(spot.spot_id, vehicle)

        # Create ticket
        ticket = ParkingTicket(vehicle, spot, self._fee_strategy)
        self._active_tickets[ticket.ticket_id] = ticket
        self._vehicle_ticket_map[vehicle.license_plate] = ticket.ticket_id

        print(f"\n✅ ENTRY: {vehicle}")
        print(f"   Ticket: {ticket.ticket_id}")
        print(f"   Spot:   {spot.spot_id} ({spot.spot_type.value}) on Floor {floor.floor_number}")
        print(f"   Time:   {ticket.entry_time.strftime('%H:%M:%S')}")

        return ticket

    def process_exit(self, ticket_id: str) -> float:
        """
        Called when a vehicle exits.
        Closes the ticket, frees the spot, calculates and returns the fee.
        """
        if ticket_id not in self._active_tickets:
            raise ValueError(f"Ticket {ticket_id} not found or already closed")

        ticket = self._active_tickets[ticket_id]
        fee = ticket.close()

        # Free the spot
        floor = self._get_floor_for_spot(ticket.spot.spot_id)
        floor.vacate_spot(ticket.spot.spot_id)

        # Clean up tracking maps
        del self._active_tickets[ticket_id]
        del self._vehicle_ticket_map[ticket.vehicle.license_plate]

        print(f"\n✅ EXIT: {ticket.vehicle}")
        print(f"   Ticket:   {ticket.ticket_id}")
        print(f"   Duration: {ticket.get_duration_str()}")
        print(f"   Spot:     {ticket.spot.spot_id} ({ticket.spot.spot_type.value})")
        print(f"   Fee:      ₹{fee:.2f}")

        return fee

    def process_exit_by_plate(self, license_plate: str) -> float:
        """Convenience method — exit by license plate instead of ticket ID"""
        plate = license_plate.upper()
        if plate not in self._vehicle_ticket_map:
            raise ValueError(f"No active ticket found for vehicle {plate}")
        ticket_id = self._vehicle_ticket_map[plate]
        return self.process_exit(ticket_id)

    # ─── REPORTING ────────────────────────────────────────────────

    def get_capacity_report(self):
        """Prints a full capacity report for the parking lot"""
        print(f"\n{'═'*50}")
        print(f"  {self.name} — Capacity Report")
        print(f"{'═'*50}")

        total_all = {t: 0 for t in SpotType}
        avail_all = {t: 0 for t in SpotType}

        for floor in self._floors:
            total = floor.get_total_count()
            avail = floor.get_available_count()
            print(f"\n  Floor {floor.floor_number}:")
            for spot_type in SpotType:
                t = total[spot_type]
                a = avail[spot_type]
                bar = "█" * (t - a) + "░" * a
                print(f"    {spot_type.value:8s}: [{bar}] {a}/{t} available")
            total_all = {t: total_all[t] + total[t] for t in SpotType}
            avail_all = {t: avail_all[t] + avail[t] for t in SpotType}

        total_spots = sum(total_all.values())
        avail_spots = sum(avail_all.values())
        print(f"\n  TOTAL: {avail_spots}/{total_spots} spots available")
        print(f"  Active tickets: {len(self._active_tickets)}")
        print(f"{'═'*50}")

    def show_display_boards(self):
        """Shows the live display board for each floor"""
        print(f"\n[Live Display — {self.name}]")
        for floor in self._floors:
            floor.display_board.show()

    # ─── PRIVATE HELPERS ──────────────────────────────────────────

    def _get_floor_for_spot(self, spot_id: str) -> ParkingFloor:
        """Find which floor a spot belongs to"""
        for floor in self._floors:
            try:
                floor.get_spot(spot_id)
                return floor
            except ValueError:
                continue
        raise ValueError(f"Spot {spot_id} not found in any floor")


# ─────────────────────────────────────────────────────────────────
# HELPER — Build a parking lot easily
# ─────────────────────────────────────────────────────────────────

def build_parking_lot(name: str, address: str,
                      floors: int, spots_per_floor: dict) -> ParkingLot:
    """
    Factory function to build a parking lot.
    spots_per_floor = {SpotType.SMALL: 10, SpotType.MEDIUM: 20, SpotType.LARGE: 5}
    """
    lot = ParkingLot(name, address)

    for floor_num in range(1, floors + 1):
        floor = ParkingFloor(floor_num)
        spot_counter = 1

        for spot_type, count in spots_per_floor.items():
            for _ in range(count):
                prefix = spot_type.value[0]   # S, M, or L
                spot_id = f"F{floor_num}-{prefix}{spot_counter:03d}"
                floor.add_spot(ParkingSpot(spot_id, spot_type))
                spot_counter += 1

        lot.add_floor(floor)

    return lot


# ─────────────────────────────────────────────────────────────────
# MAIN — Full simulation
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Build the lot
    lot = build_parking_lot(
        name="City Center Parking",
        address="MG Road, Bangalore",
        floors=3,
        spots_per_floor={
            SpotType.SMALL: 5,
            SpotType.MEDIUM: 10,
            SpotType.LARGE: 3,
        }
    )

    print(f"{'='*50}")
    print(f"  {lot.name} — Open for Business!")
    print(f"{'='*50}")

    lot.get_capacity_report()

    # Vehicles arrive
    bike1 = Motorcycle("KA01-MH-1234")
    bike2 = Motorcycle("MH02-AB-5678")
    car1 = Car("KA03-CD-9999")
    car2 = Car("DL04-EF-1111")
    car3 = Car("TN05-GH-2222")
    truck1 = Truck("KA06-IJ-3333")

    # Issue tickets
    t1 = lot.issue_ticket(bike1)
    t2 = lot.issue_ticket(car1)
    t3 = lot.issue_ticket(truck1)
    t4 = lot.issue_ticket(car2)
    t5 = lot.issue_ticket(bike2)

    lot.show_display_boards()
    lot.get_capacity_report()

    # Simulate exits
    print("\n" + "─"*50)
    print("Vehicles start leaving...")

    lot.process_exit(t1.ticket_id)          # Bike exits by ticket ID
    lot.process_exit_by_plate("DL04-EF-1111")  # Car exits by license plate

    lot.get_capacity_report()

    # Try to park same vehicle twice
    print("\nTrying to park the same car twice...")
    try:
        lot.issue_ticket(car1)   # car1 is still parked!
    except RuntimeError as e:
        print(f"  ✗ Error: {e}")

    # Fill up large spots and try to park another truck
    t6 = lot.issue_ticket(Car("KA09-AA-0001"))
    t7 = lot.issue_ticket(Car("KA09-BB-0002"))

    # Switch to flat rate pricing
    print("\nSwitching to flat rate pricing...")
    lot.set_fee_strategy(FlatRateFeeStrategy())

    t8 = lot.issue_ticket(Car("KA10-CC-9999"))
    lot.process_exit(t8.ticket_id)   # Immediately exit — flat rate charges same

    # Final state
    lot.get_capacity_report()
```

---

## Step 6: Edge Cases to Discuss

Always mention these in the interview — it shows senior-level thinking:

### 1. Concurrent Entry (Race Condition)
**Problem:** Two vehicles arrive simultaneously, both see the same spot as available,
both try to park in it.

**Solution:**
```python
import threading

class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        # ... existing code ...
        self._lock = threading.Lock()

    def occupy(self, vehicle):
        with self._lock:   # Only one thread can check-and-occupy at a time
            if self._is_occupied:
                raise RuntimeError(f"Spot {self.spot_id} just got taken")
            # ... rest of occupy logic
```

### 2. Vehicle Stays After Closing Time
**Solution:** Add a `max_hours` limit. If exceeded, charge an overstay penalty.

### 3. Lost Ticket
**Solution:** `process_exit_by_plate()` method — already implemented above.
Charge a "lost ticket fee" as a minimum.

### 4. Multiple Vehicles With Same License Plate
**Solution:** Before issuing a ticket, check if that plate already has an
active ticket. Already handled in `issue_ticket()` above.

### 5. Parking Lot Full
**Solution:** Already handled — `find_nearest_available_spot()` returns `None`,
and `issue_ticket()` raises an exception with a clear message.

---

## Design Patterns Used (Tell the Interviewer)

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Singleton** | `ParkingLot.get_instance()` | Only one parking lot per process |
| **Strategy** | `FeeStrategy` | Swap pricing without changing the lot |
| **Factory** | `build_parking_lot()` | Builds lot without exposing construction |
| **Facade** | `ParkingLot` class | Simple interface over floors + spots |
| **Observer** | `DisplayBoard` updates | Live availability updates |
| **Template: Composition** | `ParkingLot ◆ Floor ◆ Spot` | Strong ownership lifecycle |

---

## Interview Answer Template

When asked "Design a Parking Lot", structure your answer like this:

> "I'll start by clarifying requirements... [ask questions]
>
> The key entities are: ParkingLot, ParkingFloor, ParkingSpot, Vehicle hierarchy,
> and ParkingTicket. I'll use Composition for the lot→floor→spot relationship
> since their lifecycles are tied together.
>
> For pricing flexibility, I'll apply the Strategy pattern — different pricing
> models can be swapped without changing the core logic.
>
> For vehicle-spot compatibility, each vehicle knows what spot size it needs,
> and each spot knows what vehicles it can accept.
>
> Let me draw the class diagram first... [draw UML]
>
> Now let me write the code, starting with the enums, then Vehicle hierarchy,
> then ParkingSpot, ParkingFloor, and finally ParkingLot as the Facade..."

---

*Next: Day 10 — LLD Problem: Library Management System*
