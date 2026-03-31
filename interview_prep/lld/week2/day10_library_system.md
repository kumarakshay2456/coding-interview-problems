# Week 2 - Day 10: LLD Problem — Library Management System
# Full Design: Requirements → Entities → UML → Code

---

## Step 1: Clarify Requirements

When the interviewer says "Design a Library Management System", ask:

**Questions to ask:**
- What types of items does the library have? (Books only, or also DVDs, magazines?)
- Can a member borrow multiple items at once? What's the limit?
- How long is the borrowing period? Is it different per item type?
- What happens if a book is overdue? Is there a fine?
- Can members reserve/hold a book that is currently borrowed?
- Can a book have multiple copies?
- Do we need search functionality? (By title, author, ISBN?)
- Do we need member registration and management?
- Are there different types of members? (Student, Faculty with different privileges?)

**Assumed Requirements:**
1. Library has Books (multiple copies of each)
2. Two member types: `RegularMember` (can borrow 3 books, 14-day period) and
   `PremiumMember` (can borrow 5 books, 30-day period)
3. Members can search books by title, author, or ISBN
4. Members can borrow and return books
5. Members can reserve a book that is currently checked out
6. Overdue fine: ₹5 per day per book
7. A book can have multiple physical copies
8. System tracks complete borrow history
9. Librarian can add/remove books and manage members

---

## Step 2: Identify Entities

| Noun Found | Class |
|-----------|-------|
| Library | `Library` |
| Book | `Book` (catalog entry) |
| Book Copy | `BookCopy` (physical item) |
| Member | `Member` (abstract) |
| Regular Member | `RegularMember` |
| Premium Member | `PremiumMember` |
| Librarian | `Librarian` |
| Borrow Record | `BorrowRecord` |
| Reservation | `Reservation` |
| Fine | `Fine` |
| Search | `BookSearchService` |

---

## Step 3: UML Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐

          ┌─────────────────────────┐
          │        Library           │
          │─────────────────────────│
          │ - name: str             │
          │ - catalog: List[Book]   │
          │─────────────────────────│
          │ + add_book()            │
          │ + search_books()        │
          │ + checkout()            │
          │ + return_book()         │
          │ + reserve_book()        │
          └────────────┬────────────┘
                       │ ◆ (Composition)
              ┌────────┴────────┐
              ▼                 ▼
   ┌──────────────────┐  ┌──────────────────────┐
   │      Book        │  │  «abstract» Member   │
   │──────────────────│  │──────────────────────│
   │ - isbn: str      │  │ - member_id: str     │
   │ - title: str     │  │ - name: str          │
   │ - author: str    │  │ - email: str         │
   │ - copies: List   │  │ - active_borrows: [] │
   │──────────────────│  │──────────────────────│
   │ + get_available()│  │ + borrow_limit(): int│
   │ + add_copy()     │  │ + loan_period(): int │
   └───────┬──────────┘  │ + can_borrow(): bool │
           │ ◆           └─────────┬────────────┘
           │ 1..*                  │ IS-A
    ┌──────▼──────────┐    ┌───────┴──────────────┐
    │   BookCopy      │    ▼                      ▼
    │─────────────────│ ┌─────────────────┐ ┌────────────────┐
    │ - copy_id: str  │ │ RegularMember   │ │ PremiumMember  │
    │ - status: enum  │ │─────────────────│ │────────────────│
    │─────────────────│ │ limit = 3       │ │ limit = 5      │
    │ + checkout()    │ │ period = 14 days│ │ period = 30days│
    │ + return_copy() │ └─────────────────┘ └────────────────┘
    └──────┬──────────┘
           │ (creates on checkout)
    ┌──────▼──────────────┐
    │    BorrowRecord     │
    │─────────────────────│
    │ - record_id: str    │
    │ - member: Member    │
    │ - book_copy: BookCopy│
    │ - borrow_date: date │
    │ - due_date: date    │
    │ - return_date: date │
    │ - fine: float       │
    │─────────────────────│
    │ + is_overdue(): bool│
    │ + calculate_fine()  │
    │ + close()           │
    └─────────────────────┘

    ┌─────────────────────┐         ┌──────────────────────┐
    │    Reservation      │         │  BookSearchService   │
    │─────────────────────│         │──────────────────────│
    │ - member: Member    │         │ + by_title()         │
    │ - book: Book        │         │ + by_author()        │
    │ - reserved_at: date │         │ + by_isbn()          │
    │ - status: enum      │         │ + by_keyword()       │
    │─────────────────────│         └──────────────────────┘
    │ + cancel()          │
    │ + fulfill()         │
    └─────────────────────┘

└──────────────────────────────────────────────────────────────────────────┘

Key Relationships:
- Library ◆── Book: Composition (books are owned by the library)
- Book ◆── BookCopy: Composition (copies die if book is removed)
- Member ──► BorrowRecord: Association (member has borrow history)
- BookCopy ──► BorrowRecord: Association (copy tracks its borrow history)
- Member ──► Reservation: Association (member can have pending reservations)
```

---

## Step 5: Full Code Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from typing import Dict, List, Optional
import uuid


# ─────────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────────

class CopyStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    RESERVED = "RESERVED"
    LOST = "LOST"
    MAINTENANCE = "MAINTENANCE"


class ReservationStatus(Enum):
    PENDING = "PENDING"     # Waiting — book is currently borrowed
    READY = "READY"         # Book returned — member can now pick it up
    FULFILLED = "FULFILLED" # Member picked it up
    CANCELLED = "CANCELLED" # Member cancelled the reservation
    EXPIRED = "EXPIRED"     # Member didn't pick up in time


class MemberStatus(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"  # Has outstanding fines or violations
    EXPIRED = "EXPIRED"      # Membership expired


# ─────────────────────────────────────────────────────────────────
# FINE CALCULATOR — Strategy Pattern
# ─────────────────────────────────────────────────────────────────

class FineStrategy(ABC):
    @abstractmethod
    def calculate(self, days_overdue: int) -> float:
        pass


class StandardFineStrategy(FineStrategy):
    FINE_PER_DAY = 5.0   # ₹5 per day

    def calculate(self, days_overdue: int) -> float:
        return max(0.0, days_overdue * self.FINE_PER_DAY)


class ProgressiveFineStrategy(FineStrategy):
    """Fine doubles every 7 days overdue"""

    def calculate(self, days_overdue: int) -> float:
        if days_overdue <= 0:
            return 0.0
        weeks_overdue = days_overdue // 7
        remaining_days = days_overdue % 7
        fine = 0.0
        daily_rate = 5.0
        for week in range(weeks_overdue):
            fine += 7 * daily_rate
            daily_rate *= 2   # Double the rate each week
        fine += remaining_days * daily_rate
        return fine


# ─────────────────────────────────────────────────────────────────
# BORROW RECORD
# ─────────────────────────────────────────────────────────────────

class BorrowRecord:
    """
    Records a single borrowing transaction.
    Created when a book is checked out.
    Closed when the book is returned.
    Calculates overdue fines.
    """

    def __init__(self, member: "Member", book_copy: "BookCopy",
                 loan_days: int, fine_strategy: FineStrategy):
        self.record_id = f"BR-{str(uuid.uuid4())[:8].upper()}"
        self.member = member
        self.book_copy = book_copy
        self.borrow_date: date = date.today()
        self.due_date: date = date.today() + timedelta(days=loan_days)
        self.return_date: Optional[date] = None
        self.fine: float = 0.0
        self._fine_strategy = fine_strategy
        self.is_closed: bool = False

    def is_overdue(self) -> bool:
        check_date = self.return_date or date.today()
        return check_date > self.due_date

    def days_overdue(self) -> int:
        if not self.is_overdue():
            return 0
        check_date = self.return_date or date.today()
        return (check_date - self.due_date).days

    def calculate_fine(self) -> float:
        return self._fine_strategy.calculate(self.days_overdue())

    def close(self) -> float:
        """Mark the book as returned. Returns the fine amount."""
        if self.is_closed:
            raise RuntimeError(f"Record {self.record_id} is already closed")
        self.return_date = date.today()
        self.fine = self.calculate_fine()
        self.is_closed = True
        return self.fine

    def __repr__(self) -> str:
        status = "RETURNED" if self.is_closed else "ACTIVE"
        overdue = f" [OVERDUE {self.days_overdue()}d]" if self.is_overdue() else ""
        return (f"BorrowRecord({self.record_id} | "
                f"{self.book_copy.book.title[:20]} | "
                f"Due:{self.due_date} | {status}{overdue})")


# ─────────────────────────────────────────────────────────────────
# RESERVATION
# ─────────────────────────────────────────────────────────────────

class Reservation:
    """
    Holds a member's place in queue for a book that is currently borrowed.
    Observer pattern: when a book copy is returned, the reservation system
    is notified and moves the next reservation to READY.
    """

    EXPIRY_DAYS = 3   # Member has 3 days to pick up once book is ready

    def __init__(self, member: "Member", book: "Book"):
        self.reservation_id = f"RES-{str(uuid.uuid4())[:8].upper()}"
        self.member = member
        self.book = book
        self.reserved_at: datetime = datetime.now()
        self.ready_at: Optional[datetime] = None
        self.status = ReservationStatus.PENDING
        self.assigned_copy: Optional["BookCopy"] = None

    def mark_ready(self, copy: "BookCopy"):
        """Called when a copy becomes available for this reservation"""
        self.status = ReservationStatus.READY
        self.ready_at = datetime.now()
        self.assigned_copy = copy
        print(f"  [Reservation] {self.member.name}'s reservation for "
              f"'{self.book.title}' is READY for pickup! "
              f"(expires in {self.EXPIRY_DAYS} days)")

    def fulfill(self):
        """Called when member picks up the reserved book"""
        if self.status != ReservationStatus.READY:
            raise RuntimeError("Reservation is not in READY state")
        self.status = ReservationStatus.FULFILLED

    def cancel(self):
        self.status = ReservationStatus.CANCELLED

    def is_expired(self) -> bool:
        if self.status != ReservationStatus.READY or not self.ready_at:
            return False
        return (datetime.now() - self.ready_at).days > self.EXPIRY_DAYS

    def __repr__(self) -> str:
        return (f"Reservation({self.reservation_id} | "
                f"{self.member.name} | '{self.book.title}' | {self.status.value})")


# ─────────────────────────────────────────────────────────────────
# BOOK COPY — Physical item
# ─────────────────────────────────────────────────────────────────

class BookCopy:
    """
    Represents one PHYSICAL copy of a book.
    A book (catalog entry) can have many copies.
    Each copy has its own status and borrow history.
    """

    def __init__(self, book: "Book", copy_number: int):
        self.copy_id = f"{book.isbn}-C{copy_number:02d}"
        self.book = book
        self.copy_number = copy_number
        self.status = CopyStatus.AVAILABLE
        self.borrow_history: List[BorrowRecord] = []
        self._current_record: Optional[BorrowRecord] = None

    def is_available(self) -> bool:
        return self.status == CopyStatus.AVAILABLE

    def checkout(self, member: "Member", loan_days: int,
                 fine_strategy: FineStrategy) -> BorrowRecord:
        if not self.is_available():
            raise RuntimeError(
                f"Copy {self.copy_id} is not available (status: {self.status.value})"
            )
        record = BorrowRecord(member, self, loan_days, fine_strategy)
        self.borrow_history.append(record)
        self._current_record = record
        self.status = CopyStatus.BORROWED
        return record

    def return_copy(self) -> BorrowRecord:
        if self.status != CopyStatus.BORROWED:
            raise RuntimeError(
                f"Copy {self.copy_id} is not currently borrowed"
            )
        record = self._current_record
        fine = record.close()
        self._current_record = None
        self.status = CopyStatus.AVAILABLE
        return record

    def mark_lost(self):
        self.status = CopyStatus.LOST

    def __repr__(self) -> str:
        return f"BookCopy({self.copy_id} | {self.status.value})"


# ─────────────────────────────────────────────────────────────────
# BOOK — Catalog entry
# ─────────────────────────────────────────────────────────────────

class Book:
    """
    Represents a book in the catalog (not a physical copy).
    Think of this as the "master record" — title, author, ISBN.
    Manages multiple physical copies.
    Manages the reservation queue for this title.
    """

    def __init__(self, isbn: str, title: str, author: str,
                 genre: str = "", year: int = 0):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self._copies: List[BookCopy] = []
        self._reservation_queue: List[Reservation] = []
        self._copy_counter = 0

    def add_copy(self) -> BookCopy:
        self._copy_counter += 1
        copy = BookCopy(self, self._copy_counter)
        self._copies.append(copy)
        return copy

    def get_available_copy(self) -> Optional[BookCopy]:
        """Returns first available copy, or None if all are borrowed"""
        for copy in self._copies:
            if copy.is_available():
                return copy
        return None

    def get_available_count(self) -> int:
        return sum(1 for c in self._copies if c.is_available())

    def get_total_copies(self) -> int:
        return len(self._copies)

    def add_reservation(self, reservation: Reservation):
        self._reservation_queue.append(reservation)

    def notify_copy_returned(self, copy: BookCopy):
        """
        Observer pattern: called when a copy is returned.
        Notifies the next member in the reservation queue.
        """
        pending = [r for r in self._reservation_queue
                   if r.status == ReservationStatus.PENDING]
        if pending:
            next_reservation = pending[0]
            copy.status = CopyStatus.RESERVED   # Hold it for this reservation
            next_reservation.mark_ready(copy)

    def get_pending_reservations(self) -> List[Reservation]:
        return [r for r in self._reservation_queue
                if r.status == ReservationStatus.PENDING]

    def cancel_reservation(self, member: "Member") -> bool:
        for res in self._reservation_queue:
            if res.member == member and res.status in (
                ReservationStatus.PENDING, ReservationStatus.READY
            ):
                res.cancel()
                # If a copy was being held, release it
                if res.assigned_copy:
                    res.assigned_copy.status = CopyStatus.AVAILABLE
                return True
        return False

    def __repr__(self) -> str:
        avail = self.get_available_count()
        total = self.get_total_copies()
        return f"Book('{self.title}' by {self.author} | {avail}/{total} copies)"


# ─────────────────────────────────────────────────────────────────
# MEMBER HIERARCHY
# ─────────────────────────────────────────────────────────────────

class Member(ABC):
    """
    Abstract base for library members.
    Each member type defines its own borrowing rules.
    """

    def __init__(self, name: str, email: str, phone: str = ""):
        self.member_id = f"MEM-{str(uuid.uuid4())[:8].upper()}"
        self.name = name
        self.email = email
        self.phone = phone
        self.join_date: date = date.today()
        self.status = MemberStatus.ACTIVE
        self._active_borrows: List[BorrowRecord] = []
        self._active_reservations: List[Reservation] = []
        self._borrow_history: List[BorrowRecord] = []
        self.outstanding_fine: float = 0.0

    @property
    @abstractmethod
    def borrow_limit(self) -> int:
        """Maximum number of books this member can borrow at once"""
        pass

    @property
    @abstractmethod
    def loan_period_days(self) -> int:
        """How many days the member can keep a book"""
        pass

    @property
    @abstractmethod
    def member_type(self) -> str:
        pass

    def can_borrow(self) -> bool:
        """Returns True if this member is allowed to borrow more books"""
        if self.status != MemberStatus.ACTIVE:
            return False
        if self.outstanding_fine > 0:
            return False   # Must clear fines first
        return len(self._active_borrows) < self.borrow_limit

    def add_borrow_record(self, record: BorrowRecord):
        self._active_borrows.append(record)
        self._borrow_history.append(record)

    def close_borrow_record(self, record: BorrowRecord, fine: float):
        if record in self._active_borrows:
            self._active_borrows.remove(record)
        self.outstanding_fine += fine

    def add_reservation(self, reservation: Reservation):
        self._active_reservations.append(reservation)

    def pay_fine(self, amount: float) -> float:
        """Returns the remaining fine after payment"""
        self.outstanding_fine = max(0.0, self.outstanding_fine - amount)
        return self.outstanding_fine

    def get_active_borrows(self) -> List[BorrowRecord]:
        return self._active_borrows.copy()

    def get_borrow_history(self) -> List[BorrowRecord]:
        return self._borrow_history.copy()

    def __repr__(self) -> str:
        return (f"{self.member_type}({self.member_id} | {self.name} | "
                f"Borrowed:{len(self._active_borrows)}/{self.borrow_limit})")


class RegularMember(Member):
    """Standard library member — 3 books, 14-day loan period"""

    @property
    def borrow_limit(self) -> int:
        return 3

    @property
    def loan_period_days(self) -> int:
        return 14

    @property
    def member_type(self) -> str:
        return "RegularMember"


class PremiumMember(Member):
    """Premium member — 5 books, 30-day loan period, no fine on first offence"""

    @property
    def borrow_limit(self) -> int:
        return 5

    @property
    def loan_period_days(self) -> int:
        return 30

    @property
    def member_type(self) -> str:
        return "PremiumMember"

    def can_borrow(self) -> bool:
        # Premium members get one free pass — can still borrow with small fines
        if self.status != MemberStatus.ACTIVE:
            return False
        if self.outstanding_fine > 100:   # Block only if fine is significant
            return False
        return len(self._active_borrows) < self.borrow_limit


# ─────────────────────────────────────────────────────────────────
# BOOK SEARCH SERVICE — Single Responsibility
# ─────────────────────────────────────────────────────────────────

class BookSearchService:
    """
    SRP: Only responsible for searching books.
    Separated from Library so search logic can evolve independently.
    (Could be swapped for Elasticsearch in production)
    """

    def __init__(self, catalog: List[Book]):
        self._catalog = catalog

    def by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self._catalog:
            if book.isbn.lower() == isbn.lower():
                return book
        return None

    def by_title(self, title: str) -> List[Book]:
        title_lower = title.lower()
        return [b for b in self._catalog if title_lower in b.title.lower()]

    def by_author(self, author: str) -> List[Book]:
        author_lower = author.lower()
        return [b for b in self._catalog if author_lower in b.author.lower()]

    def by_genre(self, genre: str) -> List[Book]:
        genre_lower = genre.lower()
        return [b for b in self._catalog if genre_lower in b.genre.lower()]

    def by_keyword(self, keyword: str) -> List[Book]:
        """Searches across title, author, and genre"""
        kw = keyword.lower()
        return [
            b for b in self._catalog
            if kw in b.title.lower()
            or kw in b.author.lower()
            or kw in b.genre.lower()
        ]

    def available_only(self, books: List[Book]) -> List[Book]:
        """Filter a list to only include books with available copies"""
        return [b for b in books if b.get_available_count() > 0]


# ─────────────────────────────────────────────────────────────────
# LIBRARIAN — can manage the collection
# ─────────────────────────────────────────────────────────────────

class Librarian:
    """
    Has elevated privileges — can add/remove books and manage members.
    SRP: Separated from Library to keep the library focused on lending.
    """

    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id

    def add_book_to_library(self, library: "Library", book: Book,
                             num_copies: int = 1) -> Book:
        for _ in range(num_copies):
            book.add_copy()
        library._add_book(book)
        print(f"  [Librarian:{self.name}] Added '{book.title}' "
              f"with {num_copies} copy/copies")
        return book

    def add_copies(self, book: Book, num_copies: int):
        for _ in range(num_copies):
            book.add_copy()
        print(f"  [Librarian:{self.name}] Added {num_copies} more "
              f"copies of '{book.title}' (total: {book.get_total_copies()})")

    def suspend_member(self, member: Member, reason: str):
        member.status = MemberStatus.SUSPENDED
        print(f"  [Librarian:{self.name}] Suspended {member.name}: {reason}")

    def activate_member(self, member: Member):
        member.status = MemberStatus.ACTIVE
        print(f"  [Librarian:{self.name}] Activated {member.name}")

    def waive_fine(self, member: Member):
        waived = member.outstanding_fine
        member.outstanding_fine = 0.0
        print(f"  [Librarian:{self.name}] Waived ₹{waived:.2f} fine for {member.name}")


# ─────────────────────────────────────────────────────────────────
# LIBRARY — The Facade
# ─────────────────────────────────────────────────────────────────

class Library:
    """
    The main class. Facade over all library operations.
    Coordinates: Members, Books, BorrowRecords, Reservations.
    """

    def __init__(self, name: str, fine_strategy: FineStrategy = None):
        self.name = name
        self._catalog: List[Book] = []
        self._members: Dict[str, Member] = {}   # member_id → member
        self._fine_strategy = fine_strategy or StandardFineStrategy()
        self._search_service: BookSearchService = BookSearchService(self._catalog)

    # ─── INTERNAL (used by Librarian) ─────────────────────────────

    def _add_book(self, book: Book):
        """Called by Librarian only"""
        existing = self._search_service.by_isbn(book.isbn)
        if not existing:
            self._catalog.append(book)

    # ─── MEMBER MANAGEMENT ────────────────────────────────────────

    def register_member(self, member: Member) -> Member:
        self._members[member.member_id] = member
        print(f"✅ Registered: {member.name} as {member.member_type} "
              f"(ID: {member.member_id})")
        return member

    def get_member(self, member_id: str) -> Member:
        if member_id not in self._members:
            raise ValueError(f"Member {member_id} not found")
        return self._members[member_id]

    # ─── SEARCH ───────────────────────────────────────────────────

    def search(self, query: str, search_type: str = "keyword") -> List[Book]:
        """
        Unified search method — delegates to BookSearchService.
        search_type: "title", "author", "isbn", "genre", "keyword"
        """
        results = {
            "title":   self._search_service.by_title,
            "author":  self._search_service.by_author,
            "isbn":    lambda q: [self._search_service.by_isbn(q)] if self._search_service.by_isbn(q) else [],
            "genre":   self._search_service.by_genre,
            "keyword": self._search_service.by_keyword,
        }.get(search_type, self._search_service.by_keyword)(query)

        return results

    # ─── CORE LENDING OPERATIONS ──────────────────────────────────

    def checkout_book(self, member: Member, isbn: str) -> BorrowRecord:
        """
        Member borrows a book.
        Validates eligibility, finds a copy, creates borrow record.
        """
        # Validate member
        if member.status != MemberStatus.ACTIVE:
            raise PermissionError(
                f"Member {member.name} is {member.status.value}. Cannot borrow."
            )
        if not member.can_borrow():
            if member.outstanding_fine > 0:
                raise PermissionError(
                    f"{member.name} has outstanding fine of ₹{member.outstanding_fine:.2f}. "
                    f"Please clear it before borrowing."
                )
            raise PermissionError(
                f"{member.name} has reached borrow limit of {member.borrow_limit} books."
            )

        # Find the book
        book = self._search_service.by_isbn(isbn)
        if not book:
            raise ValueError(f"No book found with ISBN: {isbn}")

        # Check if member already has this book borrowed
        for record in member.get_active_borrows():
            if record.book_copy.book.isbn == isbn:
                raise RuntimeError(
                    f"{member.name} already has a copy of '{book.title}'"
                )

        # Check if member has a reservation for this book
        reservation = None
        for res in book.get_pending_reservations():
            if res.member == member:
                reservation = res
                break

        # Find an available copy
        # Priority: if member has a reservation with an assigned copy, use that
        available_copy = None
        if reservation and reservation.assigned_copy:
            available_copy = reservation.assigned_copy
            reservation.fulfill()
        else:
            available_copy = book.get_available_copy()

        if not available_copy:
            raise RuntimeError(
                f"No available copies of '{book.title}'. "
                f"You can reserve it (currently {len(book.get_pending_reservations())} "
                f"people waiting)."
            )

        # Create borrow record
        record = available_copy.checkout(
            member, member.loan_period_days, self._fine_strategy
        )
        member.add_borrow_record(record)

        print(f"\n📖 CHECKOUT:")
        print(f"   Member:  {member.name} ({member.member_type})")
        print(f"   Book:    '{book.title}' by {book.author}")
        print(f"   Copy:    {available_copy.copy_id}")
        print(f"   Due:     {record.due_date} ({member.loan_period_days} days)")
        print(f"   Record:  {record.record_id}")

        return record

    def return_book(self, member: Member, isbn: str) -> BorrowRecord:
        """
        Member returns a book.
        Calculates fine, updates records, notifies reservation queue.
        """
        # Find the active borrow record for this book
        active_record = None
        for record in member.get_active_borrows():
            if record.book_copy.book.isbn == isbn:
                active_record = record
                break

        if not active_record:
            raise ValueError(
                f"{member.name} does not have '{isbn}' borrowed"
            )

        book_copy = active_record.book_copy
        book = book_copy.book

        # Return the physical copy — calculates fine
        record = book_copy.return_copy()
        fine = record.fine
        member.close_borrow_record(record, fine)

        print(f"\n📚 RETURN:")
        print(f"   Member:  {member.name}")
        print(f"   Book:    '{book.title}'")
        print(f"   Copy:    {book_copy.copy_id}")
        print(f"   Duration: {(record.return_date - record.borrow_date).days} days")

        if record.is_overdue():
            print(f"   ⚠️  OVERDUE by {record.days_overdue()} days")
            print(f"   Fine:    ₹{fine:.2f}")
        else:
            print(f"   ✓ Returned on time. No fine.")

        if member.outstanding_fine > 0:
            print(f"   💰 Total outstanding fine: ₹{member.outstanding_fine:.2f}")

        # Observer: notify reservation queue that a copy is available
        book.notify_copy_returned(book_copy)

        return record

    def reserve_book(self, member: Member, isbn: str) -> Reservation:
        """
        Member reserves a book that is currently unavailable.
        Adds them to the reservation queue.
        """
        book = self._search_service.by_isbn(isbn)
        if not book:
            raise ValueError(f"No book found with ISBN: {isbn}")

        if book.get_available_copy():
            raise RuntimeError(
                f"'{book.title}' has available copies. "
                f"No need to reserve — just checkout directly."
            )

        # Check if member already reserved this book
        for res in book.get_pending_reservations():
            if res.member == member:
                raise RuntimeError(
                    f"{member.name} already has a pending reservation for '{book.title}'"
                )

        reservation = Reservation(member, book)
        book.add_reservation(reservation)
        member.add_reservation(reservation)

        queue_position = len(book.get_pending_reservations())
        print(f"\n🔖 RESERVATION:")
        print(f"   Member:   {member.name}")
        print(f"   Book:     '{book.title}'")
        print(f"   Position: #{queue_position} in queue")
        print(f"   ID:       {reservation.reservation_id}")

        return reservation

    def pay_fine(self, member: Member, amount: float):
        remaining = member.pay_fine(amount)
        print(f"\n💳 FINE PAYMENT:")
        print(f"   Member:    {member.name}")
        print(f"   Paid:      ₹{amount:.2f}")
        print(f"   Remaining: ₹{remaining:.2f}")
        if remaining == 0:
            print(f"   ✓ All fines cleared!")

    # ─── REPORTS ──────────────────────────────────────────────────

    def catalog_report(self):
        print(f"\n{'═'*55}")
        print(f"  {self.name} — Catalog Report")
        print(f"{'═'*55}")
        print(f"  {'Title':<30} {'Author':<20} {'Avail':<8} {'Total'}")
        print(f"  {'─'*30} {'─'*20} {'─'*8} {'─'*5}")
        for book in self._catalog:
            avail = book.get_available_count()
            total = book.get_total_copies()
            reservations = len(book.get_pending_reservations())
            res_note = f" ({reservations} waiting)" if reservations else ""
            print(f"  {book.title:<30} {book.author:<20} {avail:<8} {total}{res_note}")
        print(f"{'═'*55}")

    def member_report(self, member: Member):
        print(f"\n{'═'*50}")
        print(f"  Member Report: {member.name}")
        print(f"{'═'*50}")
        print(f"  ID:       {member.member_id}")
        print(f"  Type:     {member.member_type}")
        print(f"  Status:   {member.status.value}")
        print(f"  Fine:     ₹{member.outstanding_fine:.2f}")
        print(f"\n  Active Borrows ({len(member.get_active_borrows())}/{member.borrow_limit}):")
        for record in member.get_active_borrows():
            overdue = " ⚠️ OVERDUE" if record.is_overdue() else ""
            print(f"    • '{record.book_copy.book.title}' — Due: {record.due_date}{overdue}")
        print(f"\n  Borrow History ({len(member.get_borrow_history())} total):")
        for record in member.get_borrow_history():
            status = "Returned" if record.is_closed else "Active"
            fine_note = f" | Fine: ₹{record.fine:.2f}" if record.fine > 0 else ""
            print(f"    • [{status}] '{record.book_copy.book.title}'{fine_note}")
        print(f"{'═'*50}")


# ─────────────────────────────────────────────────────────────────
# MAIN — Full simulation
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Setup
    library = Library("City Public Library", fine_strategy=StandardFineStrategy())
    librarian = Librarian("Mrs. Sharma", "LIB-001")

    # Add books to catalog
    b1 = librarian.add_book_to_library(library,
         Book("978-0-13-110362-7", "The C Programming Language",
              "Kernighan & Ritchie", "Programming", 1978), num_copies=3)

    b2 = librarian.add_book_to_library(library,
         Book("978-0-20-163361-5", "The Pragmatic Programmer",
              "Hunt & Thomas", "Programming", 1999), num_copies=2)

    b3 = librarian.add_book_to_library(library,
         Book("978-0-06-112008-4", "To Kill a Mockingbird",
              "Harper Lee", "Fiction", 1960), num_copies=1)

    b4 = librarian.add_book_to_library(library,
         Book("978-0-74-327356-5", "Harry Potter and the Philosopher's Stone",
              "J.K. Rowling", "Fantasy", 1997), num_copies=2)

    # Register members
    alice = library.register_member(RegularMember("Alice", "alice@example.com"))
    bob = library.register_member(PremiumMember("Bob", "bob@example.com"))
    charlie = library.register_member(RegularMember("Charlie", "charlie@example.com"))

    library.catalog_report()

    # ─── Borrowing ────────────────────────────────────────────────
    r1 = library.checkout_book(alice, "978-0-13-110362-7")   # Alice borrows C book
    r2 = library.checkout_book(alice, "978-0-20-163361-5")   # Alice borrows Pragmatic
    r3 = library.checkout_book(bob, "978-0-13-110362-7")     # Bob borrows C book (copy 2)
    r4 = library.checkout_book(bob, "978-0-06-112008-4")     # Bob borrows Mockingbird

    # ─── Search ───────────────────────────────────────────────────
    print("\n🔍 Search by author 'Harper Lee':")
    results = library.search("Harper Lee", "author")
    for book in results:
        print(f"   {book}")

    print("\n🔍 Search by keyword 'programming':")
    results = library.search("programming", "keyword")
    for book in results:
        print(f"   {book}")

    # ─── Reservation ──────────────────────────────────────────────
    # Charlie wants Mockingbird — it's fully borrowed
    res1 = library.reserve_book(charlie, "978-0-06-112008-4")

    # Charlie tries to checkout — should fail (no available copy)
    try:
        library.checkout_book(charlie, "978-0-06-112008-4")
    except RuntimeError as e:
        print(f"\n✗ Expected error: {e}")

    # ─── Return ───────────────────────────────────────────────────
    # Bob returns Mockingbird — Charlie's reservation should activate
    print("\n" + "─"*50)
    library.return_book(bob, "978-0-06-112008-4")
    # Charlie should now be notified automatically (Observer)

    # Charlie picks up his reserved book
    library.checkout_book(charlie, "978-0-06-112008-4")

    # ─── Fine Simulation ──────────────────────────────────────────
    # Simulate an overdue return by manipulating the due date
    print("\n" + "─"*50)
    print("Simulating overdue return...")
    # Manually set the due date to 5 days ago (simulate late return)
    r1.due_date = date.today() - timedelta(days=5)

    library.return_book(alice, "978-0-13-110362-7")  # Alice returns C book (5 days late)

    # Alice tries to borrow again — blocked by fine
    try:
        library.checkout_book(alice, "978-0-06-112008-4")
    except PermissionError as e:
        print(f"\n✗ Expected: {e}")

    # Alice pays her fine
    library.pay_fine(alice, 25.0)  # ₹5/day × 5 days = ₹25

    # Now Alice can borrow again
    library.checkout_book(alice, "978-0-74-327356-5")  # Harry Potter

    # ─── Borrow limit test ────────────────────────────────────────
    print("\n" + "─"*50)
    print("Testing borrow limit for Regular Member (max 3):")
    library.checkout_book(alice, "978-0-06-112008-4")

    try:
        library.checkout_book(alice, "978-0-13-110362-7")  # 4th book — should fail
    except PermissionError as e:
        print(f"✗ Expected: {e}")

    # ─── Final reports ────────────────────────────────────────────
    library.catalog_report()
    library.member_report(alice)
    library.member_report(bob)
```

---

## Step 6: Edge Cases to Discuss

### 1. Concurrent Checkout of Last Copy
**Problem:** Two members checkout the last copy simultaneously.
**Solution:** Lock the copy's `checkout()` method with `threading.Lock()`.
Same pattern as Parking Lot.

### 2. Member Returns Wrong Book
**Solution:** `return_book()` verifies the member actually has that ISBN borrowed.
Already handled above.

### 3. Reservation Expiry
**Problem:** A reserved book is held for a member who never shows up.
**Solution:** A background job (cron) checks `reservation.is_expired()` daily.
Expired reservations release the copy and notify the next person in queue.

### 4. Book Removed From Catalog While Someone Has It
**Solution:** Soft-delete the book from the catalog. The borrow record still
holds a reference to the copy. Mark the book as "being removed" — new borrows
blocked, existing borrows allowed to complete normally.

### 5. Member Has Both Borrowed AND Reserved the Same Book
**Solution:** Already handled — `checkout_book()` checks active borrows before
allowing checkout. If they have one copy, they can't reserve more.

---

## Design Patterns Used (Tell the Interviewer)

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Strategy** | `FineStrategy` | Swap fine calculation without changing Library |
| **Observer** | `notify_copy_returned()` | Reservation queue auto-notified on return |
| **Facade** | `Library` class | Simple interface hiding borrow/return/reserve complexity |
| **Template Method** | `Member.can_borrow()` | Base logic + override for PremiumMember |
| **Composite** | `Book ◆── BookCopy` | Book manages its own copies |
| **Factory** | `Librarian.add_book_to_library()` | Librarian controls copy creation |

---

## Compare Parking Lot vs Library — Key Differences

| Aspect | Parking Lot | Library |
|--------|------------|---------|
| Resource | Spot (one vehicle fits) | Book copy (one member at a time) |
| "Catalog" | Floors → Spots | Books → Copies |
| Reservation | Not needed (many spots) | Needed (limited copies per title) |
| Fine | Time-based (per hour) | Overdue-based (per day late) |
| Roles | No librarian | Librarian manages catalog |
| Observer | Display board | Reservation queue notification |

---

*Next: Day 11 — LLD Problem: Elevator System*
