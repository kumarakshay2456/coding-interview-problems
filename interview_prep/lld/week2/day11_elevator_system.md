# Week 2 - Day 11: LLD Problem — Elevator System
# Full Design: Requirements → Entities → UML → Code

---

## Why Elevator System Is a Great Interview Problem

The Elevator System is a classic SDE-3 LLD problem because it naturally
combines multiple patterns:

- **State Pattern** — elevator has distinct states (Idle, Moving, Door Open)
- **Strategy Pattern** — scheduling algorithm decides which elevator to send
- **Observer Pattern** — floor displays update when elevator position changes
- **Command Pattern** — floor requests are queued commands

It also tests your ability to handle **real-time decision making** —
which elevator do you send when multiple are available?

---

## Step 1: Clarify Requirements

**Questions to ask:**
- How many floors does the building have?
- How many elevators are there?
- Can a request be made from inside the elevator (internal) AND outside on the floor (external)?
- What happens during an emergency? (Emergency stop, alarm)
- Should the elevator prioritize direction? (If moving up, pick up people going up first)
- Is there a weight limit per elevator?
- Are there any special floors? (Express to top floor, service elevator)
- What scheduling algorithm should be used?

**Assumed Requirements:**
1. Building has N floors, M elevators
2. External requests: floor button (UP or DOWN)
3. Internal requests: destination floor button inside the elevator
4. Elevator states: IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN, MAINTENANCE
5. Scheduling: SCAN algorithm (elevator continues in one direction, serves all requests, then reverses) — most efficient in real life
6. Doors open for 3 seconds then close automatically
7. Each elevator has a weight limit (capacity: 8 people)
8. Emergency stop supported
9. Display panel on each floor shows current elevator position

---

## Step 2: Identify Entities

| Noun Found | Class |
|-----------|-------|
| Building | `Building` (Facade) |
| Elevator | `Elevator` |
| Floor | `Floor` |
| Request | `ElevatorRequest` (Command) |
| Door | `Door` |
| Display Panel | `FloorDisplay` (Observer) |
| Scheduler | `ElevatorScheduler` (Strategy) |
| Button | `Button` (inside/outside) |

---

## Step 3: UML Diagram

```
┌──────────────────────────────────────────────────────────────────────┐

         ┌──────────────────────────┐
         │        Building           │  ← Facade
         │──────────────────────────│
         │ - floors: List[Floor]    │
         │ - elevators: List[Elev.] │
         │ - scheduler: Strategy    │
         │──────────────────────────│
         │ + request_elevator()     │
         │ + press_floor_button()   │
         └────────────┬─────────────┘
                      │ ◆
           ┌──────────┴───────────┐
           ▼                      ▼
  ┌────────────────┐   ┌──────────────────────┐
  │     Floor      │   │      Elevator         │
  │────────────────│   │──────────────────────│
  │ - floor_num    │   │ - elevator_id        │
  │ - display      │   │ - current_floor      │
  │────────────────│   │ - state: ElevState   │
  │ + press_up()   │   │ - direction: Dir     │
  │ + press_down() │   │ - capacity: int      │
  └────────────────┘   │ - request_queue      │
                        │──────────────────────│
  ┌──────────────────┐  │ + add_request()      │
  │ «interface»      │  │ + step()             │
  │ ElevatorScheduler│  │ + open_door()        │
  │──────────────────│  │ + close_door()       │
  │ + find_best()    │  │ + emergency_stop()   │
  └────────┬─────────┘  └──────────────────────┘
           │ IS-A
  ┌────────▼─────────┐
  │  SCANScheduler   │
  │──────────────────│
  │ + find_best()    │
  └──────────────────┘

  ┌──────────────────────────┐
  │     ElevatorRequest      │  ← Command
  │──────────────────────────│
  │ - source_floor: int      │
  │ - dest_floor: int        │
  │ - direction: Direction   │
  │ - request_type: enum     │
  │ - timestamp: datetime    │
  └──────────────────────────┘

  ┌──────────────────────────┐
  │      FloorDisplay         │  ← Observer
  │──────────────────────────│
  │ - floor_number: int      │
  │ - elevator_positions     │
  │──────────────────────────│
  │ + update()               │
  │ + show()                 │
  └──────────────────────────┘

Enums:
  ElevatorState → IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN, MAINTENANCE
  Direction     → UP, DOWN, IDLE
  RequestType   → INTERNAL (inside cabin), EXTERNAL (floor button)

└──────────────────────────────────────────────────────────────────────┘
```

---

## Step 4: The SCAN Scheduling Algorithm — Explained Simply

**Real World Analogy:** Think of a lift in a department store.

Imagine the elevator is on Floor 3, moving UP.
Waiting passengers:
- Floor 5 wants to go UP
- Floor 7 wants to go UP
- Floor 2 wants to go DOWN

SCAN algorithm:
1. Continue UP: pick up Floor 5 (going up), Floor 7 (going up)
2. Reached top — reverse direction
3. Now go DOWN: pick up Floor 2 (going down), Floor 1, etc.

It's like a lift scanning one direction fully, then reversing.
This is more efficient than FCFS (First Come First Served) which would
zigzag: Floor 3 → Floor 2 → Floor 3 → Floor 5 → Floor 3 → Floor 7.

**Choosing which elevator to send:**
When a new external request comes from floor F:
1. Prefer an IDLE elevator closest to floor F
2. If none idle, prefer an elevator already MOVING toward F in the right direction
3. Last resort: a moving elevator that will reverse and come to F

---

## Step 5: Full Code Implementation

```python
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Set
import time
import threading


# ─────────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────────

class ElevatorState(Enum):
    IDLE = "IDLE"
    MOVING_UP = "MOVING_UP"
    MOVING_DOWN = "MOVING_DOWN"
    DOOR_OPEN = "DOOR_OPEN"
    MAINTENANCE = "MAINTENANCE"
    EMERGENCY_STOP = "EMERGENCY_STOP"


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class RequestType(Enum):
    INTERNAL = "INTERNAL"   # Pressed inside the elevator cabin
    EXTERNAL = "EXTERNAL"   # Pressed on the floor panel


# ─────────────────────────────────────────────────────────────────
# ELEVATOR REQUEST — Command Pattern
# ─────────────────────────────────────────────────────────────────

@dataclass
class ElevatorRequest:
    """
    Encapsulates a single request for elevator service.
    Command Pattern: requests are objects that can be queued,
    prioritized, and processed independently.
    """
    destination_floor: int
    request_type: RequestType
    direction: Direction = Direction.IDLE     # For EXTERNAL requests — which way?
    source_floor: Optional[int] = None       # Which floor made the request (EXTERNAL)
    timestamp: datetime = field(default_factory=datetime.now)
    is_served: bool = False

    def __repr__(self) -> str:
        if self.request_type == RequestType.EXTERNAL:
            return (f"Request(Floor {self.source_floor} → {self.direction.value} "
                    f"| dest:{self.destination_floor})")
        return f"Request(Internal → Floor {self.destination_floor})"


# ─────────────────────────────────────────────────────────────────
# DOOR — Encapsulated door behavior
# ─────────────────────────────────────────────────────────────────

class Door:
    """
    Encapsulates door state and behavior.
    SRP: Door only manages open/close logic.
    """
    DOOR_OPEN_DURATION = 3   # seconds

    def __init__(self, elevator_id: str):
        self._elevator_id = elevator_id
        self._is_open = False

    def open(self):
        if not self._is_open:
            self._is_open = True
            print(f"  🚪 Elevator {self._elevator_id}: Door OPENING")

    def close(self):
        if self._is_open:
            self._is_open = False
            print(f"  🚪 Elevator {self._elevator_id}: Door CLOSING")

    def is_open(self) -> bool:
        return self._is_open


# ─────────────────────────────────────────────────────────────────
# FLOOR DISPLAY — Observer Pattern
# ─────────────────────────────────────────────────────────────────

class FloorDisplay:
    """
    Display panel on each floor showing elevator positions.
    Observer: updated whenever any elevator moves.
    """

    def __init__(self, floor_number: int, total_elevators: int):
        self.floor_number = floor_number
        # elevator_id → (current_floor, state)
        self._elevator_info: Dict[str, tuple] = {}

    def update(self, elevator_id: str, current_floor: int, state: ElevatorState):
        """Called by elevators when they move — Observer update"""
        self._elevator_info[elevator_id] = (current_floor, state)

    def show(self):
        print(f"\n  [Floor {self.floor_number:2d} Display]", end="")
        for elev_id, (floor, state) in self._elevator_info.items():
            direction = ""
            if state == ElevatorState.MOVING_UP:
                direction = "↑"
            elif state == ElevatorState.MOVING_DOWN:
                direction = "↓"
            elif state == ElevatorState.DOOR_OPEN:
                direction = "⎕"  # Door open symbol
            print(f"  {elev_id}:F{floor}{direction}", end="")
        print()


# ─────────────────────────────────────────────────────────────────
# ELEVATOR
# ─────────────────────────────────────────────────────────────────

class Elevator:
    """
    The core elevator class. Manages state, movement, and requests.

    Uses SCAN internally: serves all requests in current direction first,
    then reverses when no more requests in that direction.
    """

    def __init__(self, elevator_id: str, total_floors: int,
                 capacity: int = 8, starting_floor: int = 1):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.capacity = capacity

        self.current_floor: int = starting_floor
        self.state: ElevatorState = ElevatorState.IDLE
        self.direction: Direction = Direction.IDLE
        self.current_occupancy: int = 0

        self._door = Door(elevator_id)
        self._destination_floors: Set[int] = set()  # Floors to stop at
        self._observers: List[FloorDisplay] = []

        print(f"  Elevator {elevator_id} initialized at Floor {starting_floor}")

    # ─── Observer subscription ────────────────────────────────────
    def subscribe_display(self, display: FloorDisplay):
        self._observers.append(display)

    def _notify_observers(self):
        for display in self._observers:
            display.update(self.elevator_id, self.current_floor, self.state)

    # ─── Request handling ─────────────────────────────────────────
    def add_request(self, floor: int) -> bool:
        """
        Add a floor to the elevator's stop list.
        Returns False if the floor is invalid.
        """
        if floor < 1 or floor > self.total_floors:
            print(f"  ✗ Floor {floor} is out of range")
            return False
        if floor == self.current_floor and self._door.is_open():
            print(f"  Elevator {self.elevator_id} already at floor {floor} with door open")
            return False

        self._destination_floors.add(floor)
        print(f"  [Elevator {self.elevator_id}] Added stop: Floor {floor} "
              f"(queue: {sorted(self._destination_floors)})")
        return True

    def is_idle(self) -> bool:
        return self.state == ElevatorState.IDLE

    def has_requests(self) -> bool:
        return len(self._destination_floors) > 0

    def can_accept_passengers(self) -> bool:
        return (self.state != ElevatorState.MAINTENANCE and
                self.state != ElevatorState.EMERGENCY_STOP and
                self.current_occupancy < self.capacity)

    # ─── SCAN movement logic ──────────────────────────────────────
    def _get_next_floor(self) -> Optional[int]:
        """
        SCAN algorithm: determine the next floor to move to.

        If moving UP: find the nearest floor ABOVE current in destination list.
        If moving DOWN: find the nearest floor BELOW current in destination list.
        If IDLE: go to the nearest destination floor.
        """
        if not self._destination_floors:
            return None

        if self.direction == Direction.UP or self.direction == Direction.IDLE:
            # Floors above or at current (prefer going up)
            above = [f for f in self._destination_floors if f >= self.current_floor]
            if above:
                return min(above)    # Nearest above
            # No more above — scan downward
            below = [f for f in self._destination_floors if f < self.current_floor]
            if below:
                return max(below)    # Start going down

        elif self.direction == Direction.DOWN:
            # Floors below or at current (prefer going down)
            below = [f for f in self._destination_floors if f <= self.current_floor]
            if below:
                return max(below)    # Nearest below
            # No more below — scan upward
            above = [f for f in self._destination_floors if f > self.current_floor]
            if above:
                return min(above)    # Start going up

        return None

    def step(self) -> bool:
        """
        Simulates ONE step of elevator movement.
        Call this repeatedly (in a loop or thread) to simulate the elevator running.
        Returns True if the elevator did something, False if fully idle.
        """
        if self.state in (ElevatorState.MAINTENANCE, ElevatorState.EMERGENCY_STOP):
            return False

        # If door is open, close it before moving
        if self._door.is_open():
            self._door.close()
            self.state = ElevatorState.IDLE
            self._notify_observers()
            return True

        # If no requests, go idle
        if not self._destination_floors:
            if self.state != ElevatorState.IDLE:
                self.state = ElevatorState.IDLE
                self.direction = Direction.IDLE
                print(f"  Elevator {self.elevator_id}: IDLE at Floor {self.current_floor}")
                self._notify_observers()
            return False

        next_floor = self._get_next_floor()
        if next_floor is None:
            return False

        # Move one floor toward the next destination
        if next_floor > self.current_floor:
            self.current_floor += 1
            self.state = ElevatorState.MOVING_UP
            self.direction = Direction.UP
        elif next_floor < self.current_floor:
            self.current_floor -= 1
            self.state = ElevatorState.MOVING_DOWN
            self.direction = Direction.DOWN

        print(f"  🛗  Elevator {self.elevator_id}: Floor {self.current_floor} "
              f"[{self.state.value}]")
        self._notify_observers()

        # Check if we arrived at a destination floor
        if self.current_floor in self._destination_floors:
            self._destination_floors.discard(self.current_floor)
            self._arrive_at_floor()

        return True

    def _arrive_at_floor(self):
        """Handle arrival at a floor — open doors, let people in/out"""
        self.state = ElevatorState.DOOR_OPEN
        self._door.open()
        print(f"  ✅ Elevator {self.elevator_id}: Arrived at Floor {self.current_floor}")
        self._notify_observers()

    # ─── Manual operations ────────────────────────────────────────
    def open_door(self):
        if self.state in (ElevatorState.IDLE, ElevatorState.DOOR_OPEN):
            self._door.open()
            self.state = ElevatorState.DOOR_OPEN

    def close_door(self):
        self._door.close()
        self.state = ElevatorState.IDLE

    def emergency_stop(self):
        self.state = ElevatorState.EMERGENCY_STOP
        self._door.open()   # Open door for safety
        self._destination_floors.clear()
        print(f"  🚨 EMERGENCY STOP: Elevator {self.elevator_id} at Floor {self.current_floor}")

    def set_maintenance(self, active: bool):
        if active:
            self.state = ElevatorState.MAINTENANCE
            print(f"  🔧 Elevator {self.elevator_id}: Under MAINTENANCE")
        else:
            self.state = ElevatorState.IDLE
            print(f"  ✅ Elevator {self.elevator_id}: Back in SERVICE")

    def enter_passengers(self, count: int = 1) -> bool:
        if self.current_occupancy + count > self.capacity:
            print(f"  ⚠️  Elevator {self.elevator_id}: FULL! "
                  f"({self.current_occupancy}/{self.capacity})")
            return False
        self.current_occupancy += count
        return True

    def exit_passengers(self, count: int = 1):
        self.current_occupancy = max(0, self.current_occupancy - count)

    def __repr__(self) -> str:
        return (f"Elevator({self.elevator_id} | Floor:{self.current_floor} | "
                f"{self.state.value} | {self.current_occupancy}/{self.capacity})")


# ─────────────────────────────────────────────────────────────────
# SCHEDULING STRATEGY — Strategy Pattern
# ─────────────────────────────────────────────────────────────────

class ElevatorScheduler(ABC):
    """
    Strategy interface for deciding which elevator to assign
    to a given external request.
    """

    @abstractmethod
    def find_best_elevator(self, request: ElevatorRequest,
                            elevators: List[Elevator]) -> Optional[Elevator]:
        pass


class NearestIdleScheduler(ElevatorScheduler):
    """
    Simple strategy: pick the closest IDLE elevator.
    If none idle, pick the one closest overall.
    Good for low-traffic buildings.
    """

    def find_best_elevator(self, request: ElevatorRequest,
                            elevators: List[Elevator]) -> Optional[Elevator]:
        available = [e for e in elevators
                     if e.state != ElevatorState.MAINTENANCE
                     and e.state != ElevatorState.EMERGENCY_STOP
                     and e.can_accept_passengers()]

        if not available:
            return None

        target_floor = request.source_floor or request.destination_floor

        # Prefer idle elevators
        idle_elevators = [e for e in available if e.is_idle()]
        if idle_elevators:
            return min(idle_elevators,
                       key=lambda e: abs(e.current_floor - target_floor))

        # Fall back to closest overall
        return min(available,
                   key=lambda e: abs(e.current_floor - target_floor))


class SCANScheduler(ElevatorScheduler):
    """
    SCAN-based scheduler: considers elevator direction.

    Priority (highest to lowest):
    1. Idle elevator closest to the request
    2. Moving elevator that will PASS the source floor going in the RIGHT direction
    3. Any other elevator (will reverse eventually)

    This minimizes wait time and avoids unnecessary direction changes.
    """

    def find_best_elevator(self, request: ElevatorRequest,
                            elevators: List[Elevator]) -> Optional[Elevator]:
        target_floor = request.source_floor or request.destination_floor
        request_dir = request.direction

        available = [e for e in elevators
                     if e.state != ElevatorState.MAINTENANCE
                     and e.state != ElevatorState.EMERGENCY_STOP
                     and e.can_accept_passengers()]

        if not available:
            return None

        # Score each elevator — lower is better
        def score(elevator: Elevator) -> int:
            dist = abs(elevator.current_floor - target_floor)

            # Scenario 1: Elevator is idle → best choice
            if elevator.is_idle():
                return dist   # Just distance

            # Scenario 2: Moving in correct direction and will pass the floor
            moving_up = elevator.state == ElevatorState.MOVING_UP
            moving_down = elevator.state == ElevatorState.MOVING_DOWN

            if (moving_up and request_dir == Direction.UP
                    and elevator.current_floor <= target_floor):
                return dist   # Perfect match

            if (moving_down and request_dir == Direction.DOWN
                    and elevator.current_floor >= target_floor):
                return dist   # Perfect match

            # Scenario 3: Moving in wrong direction or wrong position
            # Add a large penalty — still possible but not preferred
            return dist + 1000

        return min(available, key=score)


# ─────────────────────────────────────────────────────────────────
# FLOOR
# ─────────────────────────────────────────────────────────────────

class Floor:
    """
    Represents a building floor.
    Has external buttons (UP / DOWN) and a display panel.
    """

    def __init__(self, floor_number: int, total_elevators: int,
                 is_ground: bool = False, is_top: bool = False):
        self.floor_number = floor_number
        self.display = FloorDisplay(floor_number, total_elevators)
        self._has_up_button = not is_top      # Top floor has no UP button
        self._has_down_button = not is_ground  # Ground floor has no DOWN button
        self._up_button_active = False
        self._down_button_active = False

    def press_up(self) -> Optional[ElevatorRequest]:
        if not self._has_up_button:
            print(f"  Floor {self.floor_number}: No UP button (top floor)")
            return None
        self._up_button_active = True
        print(f"  🔼 Floor {self.floor_number}: UP button pressed")
        return ElevatorRequest(
            destination_floor=self.floor_number,   # Placeholder — set by dispatcher
            request_type=RequestType.EXTERNAL,
            direction=Direction.UP,
            source_floor=self.floor_number
        )

    def press_down(self) -> Optional[ElevatorRequest]:
        if not self._has_down_button:
            print(f"  Floor {self.floor_number}: No DOWN button (ground floor)")
            return None
        self._down_button_active = True
        print(f"  🔽 Floor {self.floor_number}: DOWN button pressed")
        return ElevatorRequest(
            destination_floor=self.floor_number,   # Placeholder
            request_type=RequestType.EXTERNAL,
            direction=Direction.DOWN,
            source_floor=self.floor_number
        )

    def clear_button(self, direction: Direction):
        if direction == Direction.UP:
            self._up_button_active = False
        elif direction == Direction.DOWN:
            self._down_button_active = False


# ─────────────────────────────────────────────────────────────────
# BUILDING — The Facade
# ─────────────────────────────────────────────────────────────────

class Building:
    """
    The Facade. Provides a simple interface for the entire elevator system.
    Coordinates: floors, elevators, scheduler.
    """

    def __init__(self, name: str, total_floors: int, num_elevators: int,
                 scheduler: ElevatorScheduler = None):
        self.name = name
        self.total_floors = total_floors
        self._scheduler = scheduler or SCANScheduler()

        # Build floors
        self._floors: Dict[int, Floor] = {}
        for i in range(1, total_floors + 1):
            self._floors[i] = Floor(
                floor_number=i,
                total_elevators=num_elevators,
                is_ground=(i == 1),
                is_top=(i == total_floors)
            )

        # Build elevators and spread them across floors
        self._elevators: List[Elevator] = []
        for i in range(num_elevators):
            start_floor = max(1, (i * total_floors) // num_elevators)
            elev = Elevator(
                elevator_id=chr(65 + i),   # A, B, C, D...
                total_floors=total_floors,
                capacity=8,
                starting_floor=start_floor
            )
            self._elevators.append(elev)

            # Subscribe all floor displays to each elevator (Observer)
            for floor in self._floors.values():
                elev.subscribe_display(floor.display)

        print(f"\n🏢 {self.name} ({total_floors} floors, {num_elevators} elevators) — Ready\n")

    # ─── PUBLIC API ───────────────────────────────────────────────

    def call_elevator(self, floor_number: int, direction: Direction) -> bool:
        """
        External request: someone on a floor presses UP or DOWN.
        Scheduler picks the best elevator and assigns the request.
        """
        if floor_number not in self._floors:
            print(f"  ✗ Floor {floor_number} does not exist")
            return False

        floor = self._floors[floor_number]
        request = (floor.press_up() if direction == Direction.UP
                   else floor.press_down())

        if not request:
            return False

        best_elevator = self._scheduler.find_best_elevator(request, self._elevators)

        if not best_elevator:
            print(f"  ✗ No available elevator for Floor {floor_number} request")
            return False

        best_elevator.add_request(floor_number)
        print(f"  📋 Assigned: Elevator {best_elevator.elevator_id} "
              f"→ Floor {floor_number} ({direction.value})")
        return True

    def select_floor(self, elevator_id: str, destination_floor: int) -> bool:
        """
        Internal request: passenger inside elevator presses a floor button.
        """
        elevator = self._get_elevator(elevator_id)
        if not elevator:
            return False

        print(f"  🔢 Elevator {elevator_id}: Passenger selected Floor {destination_floor}")
        return elevator.add_request(destination_floor)

    def step_all(self, steps: int = 1):
        """
        Advance all elevators by N steps.
        In a real system, each elevator runs in its own thread.
        Here we simulate step-by-step for clarity.
        """
        for _ in range(steps):
            for elevator in self._elevators:
                elevator.step()

    def emergency_stop_all(self):
        """Emergency: stop ALL elevators immediately"""
        print("\n🚨 EMERGENCY: Stopping all elevators!")
        for elevator in self._elevators:
            elevator.emergency_stop()

    def emergency_stop_elevator(self, elevator_id: str):
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.emergency_stop()

    def set_maintenance(self, elevator_id: str, active: bool):
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.set_maintenance(active)

    # ─── DISPLAY ──────────────────────────────────────────────────

    def show_status(self):
        print(f"\n{'═'*55}")
        print(f"  {self.name} — Elevator Status")
        print(f"{'═'*55}")
        for elevator in self._elevators:
            queue = sorted(elevator._destination_floors)
            print(f"  Elevator {elevator.elevator_id}: "
                  f"Floor {elevator.current_floor:2d} | "
                  f"{elevator.state.value:<15} | "
                  f"Queue:{queue} | "
                  f"Occupancy:{elevator.current_occupancy}/{elevator.capacity}")
        print(f"{'═'*55}")

    def show_floor_displays(self, floors: List[int] = None):
        floors_to_show = floors or list(self._floors.keys())
        for f in floors_to_show:
            self._floors[f].display.show()

    # ─── PRIVATE ──────────────────────────────────────────────────

    def _get_elevator(self, elevator_id: str) -> Optional[Elevator]:
        for e in self._elevators:
            if e.elevator_id == elevator_id:
                return e
        print(f"  ✗ Elevator {elevator_id} not found")
        return None


# ─────────────────────────────────────────────────────────────────
# MAIN — Full Simulation
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Build a 10-floor building with 2 elevators
    building = Building(
        name="Tech Tower",
        total_floors=10,
        num_elevators=2,
        scheduler=SCANScheduler()
    )

    building.show_status()

    # ─── Scenario 1: Multiple external calls ──────────────────────
    print("\n── Scenario 1: Multiple people call elevators ──")
    building.call_elevator(5, Direction.UP)    # Person on floor 5 going up
    building.call_elevator(3, Direction.DOWN)  # Person on floor 3 going down
    building.call_elevator(8, Direction.DOWN)  # Person on floor 8 going down

    building.show_status()

    # Simulate elevator movement (5 steps)
    print("\n── Simulating elevator movement ──")
    building.step_all(steps=5)
    building.show_status()

    # ─── Scenario 2: Passenger inside selects floor ───────────────
    print("\n── Scenario 2: Passengers select destination floors ──")
    building.select_floor("A", 9)   # Passenger in elevator A wants Floor 9
    building.select_floor("B", 1)   # Passenger in elevator B wants Floor 1

    building.step_all(steps=8)
    building.show_status()

    # ─── Scenario 3: Elevator maintenance ─────────────────────────
    print("\n── Scenario 3: Elevator B goes for maintenance ──")
    building.set_maintenance("B", active=True)

    # New call — should only go to Elevator A
    building.call_elevator(7, Direction.UP)
    building.show_status()

    building.set_maintenance("B", active=False)

    # ─── Scenario 4: Emergency stop ───────────────────────────────
    print("\n── Scenario 4: Emergency in Elevator A ──")
    building.call_elevator(4, Direction.UP)
    building.call_elevator(6, Direction.DOWN)
    building.step_all(steps=2)
    building.emergency_stop_elevator("A")
    building.show_status()

    # ─── Scenario 5: Peak hour — many calls ───────────────────────
    print("\n── Scenario 5: Peak hour — all floors calling ──")
    # Reset
    building2 = Building("Peak Tower", total_floors=15, num_elevators=3,
                          scheduler=SCANScheduler())

    # Morning rush — everyone wants to go UP from ground floor
    for _ in range(5):
        building2.call_elevator(1, Direction.UP)

    # Evening rush — everyone wants to go DOWN
    for floor in [8, 10, 12, 14]:
        building2.call_elevator(floor, Direction.DOWN)

    building2.show_status()

    # Each elevator serves requests, some go to floor 1
    building2.select_floor("A", 5)
    building2.select_floor("A", 8)
    building2.select_floor("B", 12)
    building2.select_floor("C", 3)
    building2.select_floor("C", 7)

    building2.step_all(steps=10)
    building2.show_status()
    building2.show_floor_displays([1, 5, 8, 12])
```

---

## Step 6: Edge Cases to Discuss

### 1. Elevator Overloaded
**Problem:** Too many people try to enter.
**Solution:** `can_accept_passengers()` + `enter_passengers()` check capacity.
Remaining passengers wait for the next elevator.

### 2. Power Failure / Emergency
**Solution:** `emergency_stop()` opens doors at current floor, clears all requests.
`emergency_stop_all()` stops the entire building. Safety first.

### 3. Two Requests for Same Floor (Different Directions)
**Example:** Floor 5: one person wants UP, another wants DOWN.
**Solution:** These become TWO separate `ElevatorRequest` objects with different
`direction` fields. The scheduler can assign them to different elevators,
or the same elevator can handle both by opening doors at floor 5.

### 4. Elevator Stuck Between Floors
**Solution:** Maintenance mode. Trigger `emergency_stop()`.
Send all pending requests to remaining elevators via `call_elevator()`.

### 5. All Elevators Under Maintenance / Emergency
**Solution:** `call_elevator()` returns `False` and prints a message.
In a real system: trigger an alarm, notify building management.

---

## Design Patterns Used (Tell the Interviewer)

| Pattern | Where | Why |
|---------|-------|-----|
| **State** | `ElevatorState` enum + `step()` logic | Elevator behavior depends on its current state |
| **Strategy** | `ElevatorScheduler` | Swap SCAN vs NearestIdle without changing elevators |
| **Observer** | `FloorDisplay` + `subscribe_display()` | Floor displays update whenever elevator moves |
| **Command** | `ElevatorRequest` | Requests are objects that can be queued and prioritized |
| **Facade** | `Building` class | Simple `call_elevator()` hides all internal logic |
| **Singleton** | Could apply to `Building` | One building instance per process |

---

## Compare All Three LLD Problems

| Aspect | Parking Lot | Library | Elevator |
|--------|------------|---------|---------|
| **Core resource** | Spot | Book copy | Elevator cabin |
| **Assignment** | Find nearest spot | Find available copy | SCAN scheduler |
| **Queue/Reservation** | Not needed | Reservation queue | Request queue |
| **State machine** | Spot: Available/Occupied | Copy: Available/Borrowed | Elevator: Idle/Moving/Door |
| **Observer** | Display board | Reservation notification | Floor displays |
| **Strategy** | Fee calculation | Fine calculation | Scheduling algorithm |
| **Key challenge** | Multi-floor search | Reservation-return flow | Direction-aware scheduling |

---

*Next: Day 12 — LLD Mock Interview + Top 20 LLD Q&A*
