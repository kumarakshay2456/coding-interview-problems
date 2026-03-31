# Week 4 - Day 25: Final Revision + SDE-3 Top Interview Questions + Complete Cheat Sheet
# The Last Day — Everything You Need, Nothing You Don't

---

## How to Use This Day

Day 25 is the culmination of 25 days of deliberate practice.
This document is designed to be read the morning of your interview — or the night before.

It does NOT introduce new concepts.
It crystallizes everything you already know into fast-access reference format.

**How to read this document:**
1. Read each section once, slowly, nodding as you recognize concepts
2. For every cheat sheet row, mentally reconstruct the reasoning — WHY is that pattern used?
3. For the top interview questions, close the answers and say your version out loud
4. Run through the interview framework mentally before bed

**The goal of today:** Walk into your interview feeling like you have seen everything before.
Because you have.

---

## The 25-Day Journey — What You Built

```
WEEK 1 — Foundations
├── Day 1:  OOP Basics — Encapsulation, Inheritance, Polymorphism, Abstraction
├── Day 2:  SOLID Principles — 5 rules that keep code maintainable
├── Day 3:  UML Diagrams — The visual language of design
├── Day 4:  Python OOP Deep Dive — Dunders, properties, decorators
└── Day 5:  Week 1 Revision — Integrated understanding

WEEK 2 — LLD Design Patterns + Real Problems
├── Day 6:  Creational Patterns — Singleton, Factory, Abstract Factory, Builder, Prototype
├── Day 7:  Structural Patterns — Adapter, Decorator, Facade, Proxy, Composite, Bridge
├── Day 8:  Behavioral Patterns — Strategy, Observer, Command, State, Template, Chain, Iterator
├── Day 9:  LLD Problem — Parking Lot (complete design)
├── Day 10: LLD Problem — Library Management System
└── Day 11: LLD Problem — Elevator System

WEEK 3 — HLD Foundations
├── Day 12: HLD Introduction — Scale, reliability, availability
├── Day 13: DNS, CDN, Load Balancers — The internet's infrastructure
├── Day 14: Caching — Strategies, eviction, distributed caches
├── Day 15: Databases Deep Dive — SQL vs NoSQL, sharding, replication
├── Day 16: Message Queues + Async Design
├── Day 17: API Design — REST, gRPC, rate limiting
└── Day 18: Week 3 Revision — HLD component mastery

WEEK 4 — HLD System Design Problems
├── Day 19: Design URL Shortener (TinyURL)
├── Day 20: Design News Feed (Twitter/Facebook)
├── Day 21: Design Chat System (WhatsApp)
├── Day 22: Design Video Platform (YouTube)
├── Day 23: Design Ride-Sharing (Uber/Lyft)
├── Day 24: Design E-Commerce (Amazon)
└── Day 25: Final Revision — This document
```

---

## Section 1: Complete LLD Cheat Sheet — All Design Patterns

One row per pattern. Internalize the signal column — that is what tells you which pattern to use in an interview.

### Creational Patterns — HOW objects are created

| Pattern | Problem It Solves | Key Signal to Use It | Real Example |
|---------|-------------------|----------------------|--------------|
| **Singleton** | Only one instance should ever exist | "Only one X in the system", global config/logging | Database connection pool, Logger, AppConfig |
| **Factory Method** | Subclasses decide which class to instantiate | "Create objects without specifying the exact class", plugin systems | Payment gateway (CreditCard/PayPal/UPI), Notification (SMS/Email/Push) |
| **Abstract Factory** | Create families of related objects without specifying concrete classes | "Multiple product families that must work together" | UI themes (DarkTheme: DarkButton + DarkCheckbox), Cloud providers (AWS: EC2 + S3) |
| **Builder** | Construct complex objects step-by-step with many optional parts | "Object has too many constructor parameters", telescoping constructor problem | HTTP Request builder, SQL Query builder, Pizza/Burger order |
| **Prototype** | Create new objects by cloning an existing object | "Creating objects is expensive, but cloning is cheap" | Copying a pre-filled form, duplicating a complex game map, resuming a session |

### Structural Patterns — HOW objects are assembled

| Pattern | Problem It Solves | Key Signal to Use It | Real Example |
|---------|-------------------|----------------------|--------------|
| **Adapter** | Make two incompatible interfaces work together | "We have existing code that cannot be changed, but we need it to fit a new interface" | Plug adapter (UK to US), legacy API wrapper, third-party payment SDK |
| **Decorator** | Add responsibilities to objects dynamically without subclassing | "We need combinations of features at runtime" | Coffee with milk/sugar/whip, Java I/O streams, middleware in web frameworks |
| **Facade** | Provide a simple interface to a complex subsystem | "The client shouldn't need to know how the subsystem works" | Travel booking API (one call books hotel + flight + car), compiler (one compile() call) |
| **Proxy** | Control access to another object | "We need lazy loading, caching, access control, or logging before/after the real object" | Virtual proxy (lazy image loading), protection proxy (auth checks), caching proxy |
| **Composite** | Treat individual objects and compositions uniformly | "Tree structure where leaves and branches behave the same way" | File system (File and Folder both have size()), UI components, org chart |
| **Bridge** | Decouple abstraction from implementation so both can vary independently | "Avoid cartesian explosion of subclasses when two dimensions vary" | Remote control (abstraction) + TV/Radio (implementation), drawing shapes on multiple renderers |

### Behavioral Patterns — HOW objects communicate

| Pattern | Problem It Solves | Key Signal to Use It | Real Example |
|---------|-------------------|----------------------|--------------|
| **Strategy** | Define a family of algorithms and make them interchangeable | "Multiple ways to do the same thing, chosen at runtime" | Sorting algorithms, payment methods, route planning (fastest/shortest/scenic) |
| **Observer** | One-to-many dependency — when one object changes, all dependents are notified | "Many things need to react when something changes" | Event listeners, stock price alerts, YouTube subscriptions, Kafka consumers |
| **Command** | Encapsulate a request as an object (supports undo/redo/queuing) | "We need undo, queuing, logging of operations, or macro commands" | Text editor undo/redo, task scheduler, restaurant order queue, remote control buttons |
| **State** | Object behavior changes based on its internal state | "Object has distinct phases/modes with different behavior in each" | Elevator (Idle/Moving/DoorOpen), Traffic light, Vending machine, ATM (Idle/CardInserted/PinVerified) |
| **Template Method** | Define the skeleton of an algorithm, let subclasses fill in specific steps | "Same high-level algorithm, different implementation of some steps" | Data mining (open file → parse → analyze → report), game turn (setup → play → end) |
| **Chain of Responsibility** | Pass a request along a chain of handlers, each deciding to handle or pass | "Multiple handlers, not sure which one will handle the request" | HTTP middleware pipeline, support ticket escalation, ATM cash dispensing |
| **Iterator** | Provide a way to access elements of a collection without exposing its internals | "We need to traverse a custom data structure uniformly" | Python's `__iter__`/`__next__`, database cursor, playlist traversal |

---

## Section 2: Complete HLD Cheat Sheet — Infrastructure Components

### The Core Infrastructure Components

| Component | What It Does | When to Use It | Key Decisions to Mention |
|-----------|-------------|----------------|--------------------------|
| **DNS** | Translates human-readable domain names (google.com) into IP addresses. Acts as the internet's phone book. | Always present in HLD. Mention it when discussing how a user reaches your system. | DNS-based load balancing, TTL values, GeoDNS for routing users to the nearest data center |
| **CDN** | Geographically distributed servers that cache static assets (images, JS, CSS, videos) close to users. | Any system serving static content, media-heavy platforms, global user base | Push CDN (you upload content) vs Pull CDN (CDN fetches on first request), cache invalidation |
| **Load Balancer** | Distributes incoming traffic across multiple servers to prevent any single server from being overwhelmed. | Any horizontally scaled service with multiple instances | Layer 4 (TCP/IP) vs Layer 7 (HTTP, content-aware), Round-robin vs Least-connections vs IP-hash, sticky sessions |
| **Cache** | Stores frequently accessed data in fast memory (RAM) to reduce database load and improve latency. | Read-heavy systems, expensive computations, session data | Cache-aside vs Write-through vs Write-back, eviction policies (LRU, LFU, TTL), Redis vs Memcached |
| **SQL Database** | Relational database with ACID transactions, joins, and structured schemas. Enforces data integrity. | Financial transactions, user accounts, anything requiring strong consistency and complex queries | Vertical vs horizontal scaling, read replicas, connection pooling, when NOT to use SQL (unstructured data at scale) |
| **NoSQL Database** | Non-relational store optimized for specific access patterns. Trades some consistency for scale and flexibility. | High-scale writes, flexible schemas, key-value lookups, wide-column, documents, graphs | Choose the right type: Key-Value (Redis), Document (MongoDB), Wide-Column (Cassandra), Graph (Neo4j) |
| **Message Queue** | Decouples producers from consumers. Producer writes a message, consumer processes it asynchronously. | Async processing, spike absorption, reliable delivery between services | Kafka (high throughput, replay) vs RabbitMQ (complex routing), at-least-once vs exactly-once delivery, DLQ |
| **API Gateway** | Single entry point for all client requests. Handles auth, rate limiting, routing, SSL termination, and monitoring. | Microservices architecture, public APIs, mobile backends | Rate limiting per user/IP, JWT validation, request/response transformation, versioning |

### Database Selection Quick Reference

| Database Type | Best For | Examples | Avoid When |
|--------------|----------|----------|------------|
| **SQL (RDBMS)** | Financial records, user auth, inventory, anything with complex relationships | PostgreSQL, MySQL | Need horizontal write scaling, schema is constantly changing |
| **Key-Value** | Sessions, caching, user preferences, shopping carts | Redis, DynamoDB | Need complex queries or relationships |
| **Document** | Product catalogs, user profiles, content management | MongoDB, CouchDB | Need strict schema enforcement or multi-document ACID |
| **Wide-Column** | Time series, activity feeds, write-heavy at scale | Cassandra, HBase | Need strong consistency or complex queries |
| **Graph** | Social networks, recommendation engines, fraud detection | Neo4j, Amazon Neptune | Data is not inherently connected (most data isn't) |
| **Search Engine** | Full-text search, relevance ranking, autocomplete | Elasticsearch, Solr | You need a primary database (use as secondary index only) |

---

## Section 3: Top 10 LLD Questions for SDE-3

For each question: the 2-line strategy is what you say in the first 60 seconds of your answer.
It signals to the interviewer that you have seen this before and know where to go.

### 1. Design a Parking Lot

**2-line strategy:**
Model it around `ParkingLot` (Facade), `ParkingFloor`, `ParkingSpot` (Leaf in Composite), and `Ticket`.
Use **Strategy** for pricing (hourly/flat/VIP), **Factory** to create spot types (Compact/Large/EV), and **State** for spot status (Available/Occupied/Reserved).

**Key entities:** `ParkingLot`, `ParkingFloor`, `ParkingSpot`, `Vehicle`, `Ticket`, `PricingStrategy`
**Key patterns:** Facade, Composite, Strategy, Factory, State
**SDE-3 depth signal:** Mention multi-floor, multi-entrance/exit, concurrent ticket assignment, real-time spot availability via Observer.

---

### 2. Design a Library Management System

**2-line strategy:**
Model around `Library` (Facade), `Book` (item), `BookCopy` (physical instance), `Member`, and `Loan`.
Use **Observer** for overdue notifications, **Strategy** for search (by title/author/ISBN), and **Singleton** for the catalog.

**Key entities:** `Library`, `Book`, `BookCopy`, `Member`, `Loan`, `Catalog`, `Reservation`
**Key patterns:** Facade, Observer, Strategy, Singleton, Iterator
**SDE-3 depth signal:** Distinguish Book (the concept) from BookCopy (the physical item). Multiple copies of the same book.

---

### 3. Design an Elevator System

**2-line strategy:**
Model around `Building` (Facade), `Elevator` (State machine), `ElevatorRequest` (Command), and `ElevatorScheduler` (Strategy).
The scheduler picks the best elevator using SCAN algorithm; the elevator's State determines what actions are valid.

**Key entities:** `Building`, `Elevator`, `ElevatorRequest`, `Door`, `FloorDisplay`, `ElevatorScheduler`
**Key patterns:** State, Command, Strategy, Observer, Facade
**SDE-3 depth signal:** SCAN scheduling algorithm, distinguishing internal vs external requests, weight capacity, emergency handling.

---

### 4. Design a Vending Machine

**2-line strategy:**
The entire vending machine is a **State machine** — Idle → HasMoney → ProductSelected → Dispensing → Change.
Use **Command** for button presses, **Strategy** for pricing, and **Observer** to notify when inventory is low.

**Key entities:** `VendingMachine`, `Product`, `Slot`, `Payment`, `Change`, `Display`
**Key patterns:** State (primary), Command, Strategy, Observer
**SDE-3 depth signal:** Handle partial payments (multiple coins before total reached), handle exact change not available scenario, admin mode for restocking.

---

### 5. Design an ATM

**2-line strategy:**
ATM is a **State machine** — Idle → CardInserted → PinVerified → TransactionSelected → Processing → Complete.
Use **Chain of Responsibility** to dispense cash (try 500s, then 100s, then 50s), **Command** for transactions, and **Proxy** for bank communication.

**Key entities:** `ATM`, `Card`, `Account`, `Transaction`, `CashDispenser`, `BankProxy`
**Key patterns:** State, Chain of Responsibility, Command, Proxy, Template Method
**SDE-3 depth signal:** Cash dispensing algorithm (greedy), network failure handling, card skimming prevention (card ejected before cash dispensed).

---

### 6. Design Chess

**2-line strategy:**
Model `Board` (8×8 grid of `Cell`s), each `Cell` optionally containing a `Piece`.
Use **Strategy** for each piece's move validation (RookStrategy, BishopStrategy), and **Command** for moves (supports undo).

**Key entities:** `Game`, `Board`, `Cell`, `Piece`, `Player`, `Move`
**Key patterns:** Strategy (move validation), Command (undo moves), Composite (board), Observer (check detection)
**SDE-3 depth signal:** Check and checkmate detection, en passant + castling edge cases, game state serialization (save/resume).

---

### 7. Design BookMyShow (Movie Ticket Booking)

**2-line strategy:**
Core entities are `Movie`, `Show`, `Screen`, `Seat`, and `Booking`.
Use **Facade** for the booking flow, **Strategy** for seat pricing (regular/premium/recliner), and **State** for seat status (Available/Locked/Booked).

**Key entities:** `Movie`, `Theatre`, `Screen`, `Show`, `Seat`, `Booking`, `Payment`, `User`
**Key patterns:** Facade, Strategy, State, Observer (confirmation notifications), Factory (payment)
**SDE-3 depth signal:** Seat locking during payment (optimistic vs pessimistic locking), concurrent booking of same seat, cancellation and refund flow.

---

### 8. Design Uber (Driver-Rider Matching — LLD focus)

**2-line strategy:**
Core entities are `Rider`, `Driver`, `Trip`, and `Location`.
Use **Strategy** for matching algorithm (nearest driver, surge pricing), **Observer** for location updates, and **State** for driver status (Available/On-Trip/Offline).

**Key entities:** `Rider`, `Driver`, `Trip`, `Location`, `MatchingStrategy`, `PricingStrategy`
**Key patterns:** Strategy (matching, pricing), Observer (location tracking), State (driver availability), Command (trip requests)
**SDE-3 depth signal:** Driver notification (push to nearest N drivers, first accept wins), trip cancellation handling, rating system post-trip.

---

### 9. Design Splitwise

**2-line strategy:**
Core entities are `Group`, `User`, `Expense`, and `Balance`.
Use **Strategy** for split types (equal/percentage/exact/share), and **Observer** for notifications when an expense is added.

**Key entities:** `User`, `Group`, `Expense`, `Balance`, `SplitStrategy`, `Settlement`
**Key patterns:** Strategy (split calculation), Observer (notifications), Facade (simplify settlement)
**SDE-3 depth signal:** Debt simplification algorithm (minimize the number of transactions to settle all debts), handling multi-currency, group vs direct expenses.

---

### 10. Design a Notification System

**2-line strategy:**
The notification system is a **Chain of Responsibility** — try push → fallback to SMS → fallback to email.
Use **Observer** for event subscriptions, **Factory** for creating the right notification type, and **Strategy** for priority/retry logic.

**Key entities:** `NotificationService`, `Notification`, `Channel`, `Template`, `User`, `Preference`
**Key patterns:** Chain of Responsibility (fallback), Observer (subscriptions), Factory (channel creation), Strategy (retry), Template Method (notification format)
**SDE-3 depth signal:** User preferences (user has opted out of SMS), rate limiting per channel, batching vs real-time, delivery receipts and retry with exponential backoff.

---

## Section 4: Top 10 HLD Questions for SDE-3

For each system, the key components listed are what you MUST mention to be taken seriously at SDE-3 level.

### 1. Design URL Shortener (TinyURL)

**Core requirements:** Long URL → short URL, redirect, analytics

**Key components to mention:**
- **API Layer:** `POST /shorten` (returns short URL), `GET /:shortCode` (302 redirect)
- **Hash generation:** Base62 encoding of auto-increment ID (or MD5 first 6 chars with collision handling)
- **Database:** SQL for URL mappings (simple key-value, easy joins for analytics)
- **Cache:** Redis cache for hot short codes (80/20 rule — cache the top 20% that gets 80% of traffic)
- **Scalability:** Read-heavy (read >> write), horizontal scaling of redirect service, CDN for static redirects

**SDE-3 depth:** Custom aliases, expiry dates, rate limiting per user, click analytics (separate analytics DB), collision resolution.

---

### 2. Design a Rate Limiter

**Core requirements:** Limit requests per user/IP, distributed, low latency

**Key components to mention:**
- **Algorithms:** Token Bucket (allows bursts), Fixed Window (simple, boundary problem), Sliding Window Log (accurate, memory-heavy), Sliding Window Counter (good balance)
- **Storage:** Redis with atomic operations (INCR, TTL) for distributed rate limiting
- **Placement:** API Gateway (before hitting services), or as a middleware library
- **Response:** Return `HTTP 429 Too Many Requests` with `Retry-After` header

**SDE-3 depth:** Different limits for different tiers (free vs paid), soft vs hard limits, rate limiting by endpoint (not just global), handling Redis failure gracefully.

---

### 3. Design a News Feed (Twitter/Facebook)

**Core requirements:** User posts content, followers see posts in chronological/ranked order

**Key components to mention:**
- **Fan-out strategies:** Fan-out on write (push to all follower timelines at write time, fast read) vs Fan-out on read (pull at read time, slower read but simple writes)
- **Hybrid approach:** Fan-out on write for regular users, fan-out on read for celebrities (millions of followers)
- **Feed storage:** Redis sorted set per user (score = timestamp), pre-computed timeline
- **Ranking service:** Separate ML service scores posts; feed retrieval merges pre-computed + ranking
- **Media:** CDN for images/videos, S3 for storage

**SDE-3 depth:** Celebrity problem (fan-out on read), timeline pagination, feed freshness vs consistency trade-off, A/B testing different ranking algorithms.

---

### 4. Design WhatsApp / Chat System

**Core requirements:** 1:1 messages, group chat, online status, delivery receipts

**Key components to mention:**
- **WebSocket:** Persistent TCP connection between client and chat server for real-time delivery
- **Message routing:** When user A sends to user B, chat server checks which server B is connected to via a service registry (Zookeeper)
- **Message storage:** NoSQL (Cassandra) — write-heavy, append-only, key by (chat_id, timestamp)
- **Delivery receipts:** Sent (server received) → Delivered (recipient device received) → Read (recipient opened)
- **Offline messages:** Store in queue/DB, push when user comes online

**SDE-3 depth:** End-to-end encryption (Signal Protocol), group chat fan-out, media via S3 + CDN with thumbnail previews, message deletion (soft delete), last seen / online status propagation.

---

### 5. Design YouTube / Video Platform

**Core requirements:** Upload video, transcode, stream, comment, search

**Key components to mention:**
- **Upload flow:** Client uploads raw video → Object storage (S3) → triggers transcoding pipeline (async, worker queues) → multiple resolutions stored in S3 → CDN serves video chunks
- **Streaming:** Adaptive Bitrate Streaming (ABR) — client requests chunks, switches quality based on bandwidth
- **Metadata DB:** SQL for videos, users, channels; Elasticsearch for search
- **CDN:** Absolutely essential — video bytes are served from edge nodes near the user
- **Recommendation:** Separate ML service, user activity events to Kafka → stream processing → update recommendation model

**SDE-3 depth:** Transcoding pipeline (FFmpeg workers), video chunking, resume playback (store watch progress), copyright detection (fingerprinting), LIVE streaming architecture differences.

---

### 6. Design Uber / Lyft (Ride-Sharing)

**Core requirements:** Match riders to drivers, real-time location, trip tracking, pricing

**Key components to mention:**
- **Location service:** Drivers send GPS updates every 4 seconds → stored in Redis geospatial index (`GEOADD`, `GEORADIUS`)
- **Matching:** Rider requests → find drivers within radius → send offer to nearest N → first accept wins
- **Trip service:** SQL for trips (need ACID for billing), state machine (Requested → Accepted → In-Progress → Completed)
- **Surge pricing:** Demand/supply ratio computed in real-time per geographic cell (H3/Geohash)
- **Maps:** Use Google Maps or HERE Maps API for routing, ETA calculation

**SDE-3 depth:** Driver location write volume (1M drivers × 1 update/4s = 250K writes/sec → Redis, not SQL), WebSocket for real-time driver position on rider's map, dispatch optimization as a matching problem.

---

### 7. Design Amazon / E-Commerce

**Core requirements:** Product catalog, search, cart, checkout, orders, inventory

**Key components to mention:**
- **Product catalog:** NoSQL (document DB) — flexible schema per product type
- **Search:** Elasticsearch with inverted index; faceted search (filter by price, brand, rating)
- **Inventory:** SQL with strong consistency — must not oversell (pessimistic locking or atomic decrement)
- **Cart:** Redis (session-based, fast, ephemeral until checkout)
- **Order service:** SQL for orders + ACID transactions; event-driven updates to downstream services
- **Checkout:** Saga pattern — book inventory → process payment → confirm order → send notifications (each step compensatable on failure)

**SDE-3 depth:** Flash sale inventory handling (Redis atomic DECR, then async sync to DB), personalization, recommendation engine, A/B testing infrastructure, seller onboarding.

---

### 8. Design Google Search

**Core requirements:** Crawl the web, index, rank, return results in < 100ms

**Key components to mention:**
- **Crawler:** Distributed web crawlers respect robots.txt, politeness delay, detect duplicate content (SimHash)
- **Index:** Inverted index — maps word → list of (document_id, position, frequency). Stored in distributed fashion across thousands of machines
- **Ranking:** PageRank (link authority) + 200+ signals (freshness, query match, user location, CTR)
- **Query processing:** Query expansion → index lookup → candidate ranking → result serving
- **Caching:** Popular query results cached in Redis; most queries have been asked before

**SDE-3 depth:** This is the most complex system. Focus on the inverted index structure, MapReduce for batch index building, and the serving stack for query-time latency. Personalization layer.

---

### 9. Design Instagram

**Core requirements:** Post photos/videos, follow users, see feed, stories, explore

**Key components to mention:**
- **Media storage:** S3 + CDN (photos/videos never go into a database)
- **Post metadata:** SQL (PostgreSQL) for posts, users, follows, likes
- **Feed:** Same news feed fan-out architecture — push to follower timelines in Redis sorted sets
- **Stories:** TTL-based (expire after 24h), stored in separate table with expiry timestamp
- **Explore / Discovery:** ML-based recommendation, separate pipeline consuming engagement events
- **Notifications:** Kafka events → notification workers → push/email/SMS

**SDE-3 depth:** Photo deduplication (perceptual hash), content moderation pipeline, NSFW detection, follower graph stored in a graph DB or denormalized in Cassandra for fast follow lookups.

---

### 10. Design Pastebin

**Core requirements:** User pastes text, gets a short URL, anyone with URL can view, optional expiry

**Key components to mention:**
- **Write path:** Client posts text → API server → generate unique key (Base58, 8 chars) → store text in object storage (S3), store metadata (key, owner, expiry, visibility) in SQL
- **Read path:** Client hits short URL → load balancer → cache check (Redis) → S3 if miss → return text
- **Expiry:** Background job scans DB for expired pastes and deletes from S3 + DB; TTL in Redis handles cache expiry automatically
- **Analytics:** View count in Redis (INCR) — async sync to DB, no need to hit DB on every view

**SDE-3 depth:** Syntax highlighting (client-side, not server concern), visibility settings (public/private/unlisted), large paste support (up to 10MB → directly to S3, metadata only in DB), rate limiting per IP.

---

## Section 5: The SDE-3 Interview Framework

This is the sequence of steps you follow in every interview.
Internalize this framework — it turns a chaotic design question into a structured conversation.

### LLD Framework — 6 Steps

```
Step 1: CLARIFY (2-3 minutes)
├── "Can I ask a few clarifying questions before I start?"
├── What are the core use cases? (top 3)
├── What scale do we need? (1 user? 1M users?)
├── Are there specific constraints? (mobile clients? real-time?)
└── Output: a bullet-point list of requirements on the whiteboard

Step 2: IDENTIFY ENTITIES (3-4 minutes)
├── "Let me identify the core entities first."
├── Go through the requirements and underline every NOUN
├── Each noun is a candidate class
├── Eliminate duplicates and helpers, keep the core domain objects
└── Output: a list of 5-10 entity names

Step 3: UML / CLASS DIAGRAM (5-7 minutes)
├── Draw boxes for each entity
├── Add key attributes (not all — just important ones)
├── Add key methods
├── Draw relationships: association, composition, inheritance, implements
├── Show multiplicities (1..*, 0..1)
└── Output: a class diagram on whiteboard (rough is fine)

Step 4: CODE THE CORE (10-15 minutes)
├── "Let me code the core entities first, then the key logic."
├── Start with base classes / interfaces
├── Code the most important entity in full
├── Code the most interesting method (the one the interviewer is watching for)
├── Leave stubs for secondary methods with a comment
└── Output: working Python/Java code for core flow

Step 5: APPLY PATTERNS (3-5 minutes)
├── "I can see a few design patterns that fit here."
├── Name the pattern, why you chose it, where it applies
├── Refactor code to use the pattern if not already
├── This shows SDE-3 maturity — juniors code, seniors pattern
└── Output: code using at least 1-2 appropriate patterns

Step 6: EDGE CASES + EXTENSIBILITY (3-5 minutes)
├── "Let me think about edge cases."
├── What happens with null inputs?
├── What happens with concurrent access?
├── How would you extend this in 6 months? (open for extension, closed for modification = OCP)
└── Output: edge case list + 1-2 extensibility improvements
```

### HLD Framework — 6 Steps

```
Step 1: CLARIFY REQUIREMENTS (3-5 minutes)
├── Functional: What are the top 3 features?
│   "Users can post tweets. Users can follow. Users see a feed."
├── Non-functional: Scale, latency, consistency, availability
│   "100M daily active users. Feed load < 200ms. High availability."
├── Out of scope: "We won't cover billing/analytics today unless you'd like."
└── Output: Functional + non-functional requirements written down

Step 2: ESTIMATE CAPACITY (3-5 minutes)
├── Users: DAU, MAU, concurrent users
├── Traffic: Reads per second, writes per second
│   Example: 100M DAU, each reads 20 posts/day = 2B reads/day = ~23K RPS
├── Storage: Data per record × records per day × retention period
│   Example: 100 bytes/post × 1M posts/day × 365 days × 5 years = ~180GB
├── Bandwidth: Peak throughput for video/media
└── Output: A table of estimates (round numbers are fine, reasoning matters more)

Step 3: API DESIGN (3-5 minutes)
├── Define 3-5 core endpoints
│   POST /tweets         { content, media_ids[] }
│   GET  /feed           { user_id, cursor, limit }
│   POST /follow         { target_user_id }
├── Include: auth (who calls this?), key params, response structure
├── Mention pagination strategy (cursor-based for infinite scroll)
└── Output: API contract for core use cases

Step 4: HIGH-LEVEL DESIGN (8-10 minutes)
├── Draw the core components:
│   Client → DNS → CDN → Load Balancer → API Servers → [Services] → [Databases]
├── Show data flow for the most important use case
│   "When user posts a tweet: API server → write to SQL → publish event to Kafka
│    → fan-out worker reads Kafka → pushes to follower timelines in Redis"
├── Use boxes and arrows, label every arrow with the protocol (HTTP, gRPC, Kafka)
└── Output: An architecture diagram covering all major components

Step 5: DEEP DIVE — Pick 2 Hard Problems (10-15 minutes)
├── The interviewer will often guide: "How does the feed actually work?"
├── If not, YOU pick the two hardest/most interesting subproblems
├── Go deep: data model, algorithms, concrete numbers, trade-offs
│   "We use a Redis Sorted Set per user. Score = Unix timestamp.
│    Fan-out worker writes to 1000 followers synchronously — not for celebrities.
│    For users with > 1M followers, we switch to pull-on-read."
└── Output: Detailed design for 2 major components

Step 6: SCALABILITY + FAILURE HANDLING (5-7 minutes)
├── Bottlenecks: "The first bottleneck is the fan-out service for popular accounts."
├── Single points of failure: "The DB is a SPOF — we add read replicas + auto-failover."
├── Horizontal scaling: "API servers are stateless — add more behind LB."
├── Caching strategy: What to cache, TTL, invalidation
└── Output: A list of known bottlenecks + solutions
```

---

## Section 6: Common Mistakes SDE-3 Candidates Make

These are not beginner mistakes. These are the mistakes that cost candidates senior roles.

### Mistake 1: Starting to Code Before Designing

**What it looks like:**
Interviewer: "Design a parking lot."
Candidate: "Sure, let me write a class..."

**Why it fails:**
The interviewer is watching how you THINK, not just whether you can type.
Jumping to code without design shows you cannot lead a team through ambiguity.

**Fix:**
Spend the first 10 minutes purely on requirements and design.
Say: "Before I write any code, let me make sure I understand the problem and draw out the structure."

---

### Mistake 2: Not Asking Clarifying Questions

**What it looks like:**
"Design a chat system — okay, I'll design WhatsApp."

**Why it fails:**
The problem is intentionally ambiguous. The interviewer wants to see if you ask the RIGHT questions.
Different clarifications lead to very different systems.
(1:1 vs group? Messages only vs calls? Real-time vs store-and-forward?)

**Fix:**
Always ask:
- Scale: "How many users are we designing for?"
- Features: "Which 3 features are most important to nail today?"
- Constraints: "Any specific technology constraints or preferences?"
- Non-functional: "What is the latency requirement for the critical path?"

---

### Mistake 3: Building a Perfect System Instead of a Practical One

**What it looks like:**
Spending 15 minutes designing a 5-database, 12-microservice architecture for a URL shortener.

**Why it fails:**
Over-engineering is a red flag. SDE-3s know when to keep it simple.
A URL shortener needs exactly: one API, one SQL table, one Redis cache.
Starting with 12 services before you have users is a failure mode.

**Fix:**
Start simple. Design the MVP architecture. Then say:
"This works for 10K users. Here is what I would change to handle 10M users."
Show you can evolve the design, not that you start with maximum complexity.

---

### Mistake 4: Ignoring Non-Functional Requirements

**What it looks like:**
Designing the entire system without mentioning availability, latency, consistency, or scalability.

**Why it fails:**
The functional design is the easy part — any engineer can draw boxes.
What separates SDE-3s is understanding WHAT HAPPENS WHEN THINGS GO WRONG:
- What happens when the DB is down?
- What happens at 10× normal traffic?
- What happens when a network partition occurs?

**Fix:**
Explicitly mention non-functional requirements at the start.
Come back to them at the end: "Given that we need 99.99% availability,
the DB must be replicated across 3 AZs with automatic failover."

---

### Mistake 5: Not Discussing Trade-offs

**What it looks like:**
"We'll use Cassandra for the database."

**Why it fails:**
Making a technology choice without explaining WHY is a missed opportunity.
It signals that you either memorized "Cassandra = good" or you don't understand the trade-off.

**Fix:**
ALWAYS say the trade-off alongside the decision:
"We'll use Cassandra because our write rate is 100K/sec and our queries are
always by partition key. The trade-off is eventual consistency — we accept
that a user might see a slightly stale timeline for a few seconds."

---

## Section 7: The Trade-off Matrix

Memorize these. Every HLD interview will involve at least 2 of these decisions.

| Decision | Option A | Option B | Choose A When | Choose B When |
|----------|----------|----------|---------------|---------------|
| **SQL vs NoSQL** | SQL (PostgreSQL, MySQL) | NoSQL (Cassandra, MongoDB, DynamoDB) | ACID transactions required, complex joins, strong consistency needed (payments, orders, auth) | Massive write throughput, flexible/evolving schema, horizontal scaling from day 1, simple access patterns by key |
| **Cache-aside vs Write-through** | Cache-aside (lazy loading): app checks cache first, on miss loads from DB and populates cache | Write-through: every DB write also writes to cache, cache always warm | Read-heavy workloads, can tolerate brief staleness after restart (cache starts cold) | Cache freshness is critical, write patterns are predictable, read-after-write consistency needed |
| **Push vs Pull feed** | Fan-out on write (Push): when user posts, immediately push to all follower timelines | Fan-out on read (Pull): when user opens app, pull latest posts from followed accounts | Users have few followers (< 10K), reads are much more frequent than writes, low-latency feed essential | Users have millions of followers (celebrities), write amplification unacceptable, follower count is highly variable |
| **Sync vs Async processing** | Synchronous: request waits for the operation to complete, returns result | Asynchronous: request is accepted, processing happens later via queue, client polls or gets notified | User needs the result immediately, failure must be reported back inline, simple workflows | Long-running operations (video encoding, report generation), decoupling services needed, spike absorption, retry semantics needed |
| **Monolith vs Microservices** | Monolith: all features in one deployable unit, shared memory, one DB | Microservices: independent services, each with own DB, communicate via HTTP/gRPC/events | Early-stage product, small team (< 10 engineers), domain boundaries not yet clear, simplicity matters most | Product is mature, large team needing independent deployments, clear domain boundaries, different scaling requirements per service |
| **Strong vs Eventual Consistency** | Strong consistency: all nodes see the same data at the same time | Eventual consistency: nodes converge to the same state, may briefly diverge | Banking, inventory (cannot oversell), reservations, any system where stale reads cause real harm | Social feeds, view counts, likes, activity data, recommendation signals — where slight staleness is invisible to users |
| **Read replica vs Write sharding** | Read replicas: one primary for writes, N replicas for reads | Write sharding (horizontal partitioning): data split across shards, each shard handles a subset of writes | Read-heavy workload (> 90% reads), data fits on one machine, simplicity preferred | Write throughput exceeds single machine capacity, data too large for one node, need geographic distribution |

---

## Section 8: Numbers Every SDE-3 Should Know

Knowing these numbers is what lets you do back-of-envelope calculations in real-time during an interview.
You don't need precision — you need order-of-magnitude intuition.

### Latency Numbers (Approximate, 2024)

| Operation | Latency | Human Intuition |
|-----------|---------|-----------------|
| L1 cache reference | 1 ns | Lightning — nothing faster |
| L2 cache reference | 4 ns | Still in CPU land |
| L3 cache reference | 10 ns | Still CPU, slightly farther |
| RAM access (main memory) | 100 ns | 100× slower than L1 cache |
| SSD random read | 100 μs (100,000 ns) | 1,000× slower than RAM |
| HDD random read | 10 ms (10,000,000 ns) | 100,000× slower than RAM |
| Read 1 MB from RAM | 250 μs | Fast in-process data transfer |
| Read 1 MB from SSD | 1 ms | Still fast for sequential reads |
| Round-trip within same data center | 500 μs | Fast local network |
| Round-trip cross-region (US East to West) | 40 ms | Noticeable for users |
| Round-trip cross-continent (US to Europe) | 150 ms | Clearly noticeable |
| DNS lookup | 1-100 ms | Cached = 1ms, cold = 100ms |

**Key insight:** RAM is fast. SSD is 1000× slower. Network is 10,000× slower than RAM.
This is WHY we cache. This is WHY we co-locate services.

---

### Storage Units — Never Confuse These in an Interview

| Unit | Bytes | Real-world size |
|------|-------|-----------------|
| 1 KB (Kilobyte) | 1,000 bytes | A short text message |
| 1 MB (Megabyte) | 1,000,000 bytes | A high-quality photo (JPEG) |
| 1 GB (Gigabyte) | 1,000,000,000 bytes | A movie (compressed) |
| 1 TB (Terabyte) | 1,000,000,000,000 bytes | 1,000 movies |
| 1 PB (Petabyte) | 1,000,000,000,000,000 bytes | The entirety of Netflix's library |

---

### Traffic Estimates — The QPS Calculator

| Scenario | Calculation | Result |
|----------|-------------|--------|
| 1 million requests per day | 1,000,000 / 86,400 seconds | ~12 QPS |
| 10 million requests per day | 10,000,000 / 86,400 | ~115 QPS |
| 100 million requests per day | 100,000,000 / 86,400 | ~1,150 QPS |
| 1 billion requests per day | 1,000,000,000 / 86,400 | ~11,500 QPS |
| Peak traffic (assume 3× average) | Multiply QPS × 3 | Peak QPS |

**Shortcut:** 1 million requests/day ≈ 12 QPS. So 100M DAU each making 10 requests = 1B/day ≈ 12,000 QPS average, ~36,000 QPS peak.

---

### Common Capacity Reference Points

| Reference | Value | Use This For |
|-----------|-------|--------------|
| Tweet / short text post | 140-280 bytes | Social media text |
| User profile row | ~1 KB | User metadata |
| High-quality photo (JPEG) | 1-3 MB | Image platforms |
| 1 minute of compressed video (720p) | ~10 MB | Video platforms |
| 1 minute of HD video (1080p) | ~50 MB | Video platforms |
| MySQL row | ~100 bytes average | DB storage calculations |
| Redis value limit (practical) | 10 MB (hard limit 512 MB) | Cache design |
| Single server throughput (HTTP) | ~10,000 QPS (general rule) | When to scale out |
| Kafka topic throughput | Millions of messages/second | Message queue sizing |
| PostgreSQL read (with index) | ~10,000 QPS per replica | DB throughput |
| Cassandra write throughput | ~100,000 writes/sec per node | NoSQL write sizing |

---

### The "Powers of Two" Reference

```
2^10  = 1,024        ≈ 1 thousand     (1 KB)
2^20  = 1,048,576    ≈ 1 million      (1 MB)
2^30  = ~1 billion               (1 GB)
2^40  = ~1 trillion              (1 TB)

Characters in a short text:  100
Bytes in a typical DB row:   1,000 (1 KB)
Users of a mid-size startup: 1,000,000 (1M)
DAU of a large tech company: 100,000,000 (100M)
```

---

## Section 9: Day-of-Interview Checklist

These are the 10 minutes before the interview begins.
The technical prep is done. Now you set yourself up to perform.

### 60 Minutes Before

- [ ] Review this document one final time (Section 3 and 4 especially)
- [ ] Do one mock "say your name and background" out loud — your voice should be warm, not rusty
- [ ] Prepare your workspace: paper, pen, water, headset tested if remote
- [ ] Close all tabs except what you need. No distractions visible.

### 30 Minutes Before

- [ ] Eat something light. Your brain needs glucose.
- [ ] Brief walk or stretch — reduces cortisol, improves blood flow to prefrontal cortex
- [ ] Reread the interview framework steps (Section 5) — these should feel automatic

### 10 Minutes Before

- [ ] Log into the platform early. Test audio, video, shared screen (for remote).
- [ ] Have paper and pen ready for back-of-envelope calculations
- [ ] Mentally say: "I am going to have a technical conversation with a peer. I know this material."
- [ ] Write at the top of your paper: **Clarify → Estimate → API → Design → Deep Dive → Scale**

### During the Interview — The Opening

When the question is posed, say:
> "That's a great problem. Before I jump in, can I ask a few clarifying questions to make sure I'm solving the right problem?"

This one sentence:
1. Buys you 2-3 minutes to think
2. Demonstrates senior-level instinct
3. Sets the interviewer's expectation that you are structured

### When You Get Stuck

Do not go silent. Say one of these:
- "Let me think through this out loud for a moment..."
- "I can see two approaches here. Let me compare them..."
- "I'm not 100% sure on this — my instinct is X, but the trade-off would be Y. What do you think?"

Interviewers actively help candidates who communicate. They cannot help candidates who go silent.

### The Last 5 Minutes

If time is running out:
- Stop coding. Say: "I want to make sure I cover the key points even if the code isn't complete."
- Summarize your design in 3 sentences.
- Mention the 1-2 things you would improve given more time.

---

## Section 10: 25-Day Completion Checklist

Use this as a self-assessment. For each item, mark: Strong / Needs Review / Not Covered

### OOP + Language Fundamentals

- [ ] I can explain the 4 pillars of OOP with examples
- [ ] I can apply each of the 5 SOLID principles and explain why each matters
- [ ] I can draw a UML class diagram from a verbal problem statement
- [ ] I understand Python dunder methods and when to use them
- [ ] I can write `@property`, `@classmethod`, `@staticmethod` correctly from memory

### LLD Design Patterns

- [ ] **Singleton** — I can implement it thread-safely and know when NOT to use it
- [ ] **Factory + Abstract Factory** — I can distinguish them and use them appropriately
- [ ] **Builder** — I can explain why it's better than telescoping constructors
- [ ] **Prototype** — I know when cloning is better than creating
- [ ] **Adapter** — I can explain the "plug adapter" analogy and implement it
- [ ] **Decorator** — I can explain how it avoids subclass explosion
- [ ] **Facade** — I can design a Facade over a complex subsystem
- [ ] **Proxy** — I can implement a caching proxy and an access-control proxy
- [ ] **Composite** — I can explain the tree structure and uniform treatment principle
- [ ] **Strategy** — I can refactor if/else chains into Strategy pattern
- [ ] **Observer** — I can implement pub/sub with loose coupling
- [ ] **Command** — I can implement undo/redo with Command pattern
- [ ] **State** — I can convert a state machine to the State pattern
- [ ] **Template Method** — I can design a reusable algorithm skeleton

### LLD Design Problems

- [ ] **Parking Lot** — I can design this end-to-end in 30 minutes
- [ ] **Library System** — I can design this and explain Book vs BookCopy distinction
- [ ] **Elevator System** — I can explain SCAN algorithm and the State machine
- [ ] **Vending Machine** — I can diagram all the states and transitions
- [ ] **ATM** — I can explain the cash dispensing algorithm and State machine
- [ ] **BookMyShow** — I can explain concurrent seat booking and locking
- [ ] **Splitwise** — I can explain the debt simplification algorithm
- [ ] **Notification System** — I can design the fallback chain and retry logic

### HLD Components

- [ ] **DNS** — I can explain DNS resolution and GeoDNS
- [ ] **CDN** — I can explain Push vs Pull and when to use a CDN
- [ ] **Load Balancer** — I can explain L4 vs L7 and routing algorithms
- [ ] **Cache** — I can explain Cache-aside, Write-through, Write-back, and eviction policies
- [ ] **SQL** — I can explain ACID, indexing, read replicas, and when SQL breaks down
- [ ] **NoSQL** — I can choose the right NoSQL type for a given problem
- [ ] **Message Queue** — I can explain Kafka vs RabbitMQ, at-least-once, and DLQ
- [ ] **API Gateway** — I can explain rate limiting, auth, and routing at the gateway level

### HLD Design Problems

- [ ] **URL Shortener** — I can design this in 30 minutes including hash collision handling
- [ ] **Rate Limiter** — I can explain Token Bucket and implement it with Redis
- [ ] **News Feed** — I can explain fan-out on write vs read and the celebrity problem
- [ ] **Chat System (WhatsApp)** — I can explain WebSocket, message routing, and delivery receipts
- [ ] **YouTube** — I can explain the video upload, transcoding, and CDN streaming pipeline
- [ ] **Uber** — I can explain geospatial indexing, driver matching, and surge pricing
- [ ] **Amazon** — I can explain the checkout Saga pattern and inventory locking
- [ ] **Google Search** — I can explain the inverted index at a conceptual level
- [ ] **Instagram** — I can explain media storage and the feed architecture
- [ ] **Pastebin** — I can design this as an S3 + SQL + Redis system

### Interview Skills

- [ ] I always clarify before designing
- [ ] I can do back-of-envelope estimates confidently
- [ ] I state trade-offs alongside every major decision
- [ ] I know the LLD 6-step framework by heart
- [ ] I know the HLD 6-step framework by heart
- [ ] I know the latency numbers (RAM vs SSD vs Network)
- [ ] I know how to calculate QPS from DAU

---

## Section 11: What's Next — Continued Learning

You have completed a structured 25-day foundation.
This is not the end — it is the foundation on which you build continued expertise.

### Books (Ranked by SDE-3 Relevance)

| Book | Why Read It | When to Read |
|------|-------------|--------------|
| **Designing Data-Intensive Applications** — Martin Kleppmann | The single best book on distributed systems. Covers databases, replication, consistency, stream processing with depth and clarity. | After this course. Read one chapter per week. |
| **System Design Interview Vol 1 & 2** — Alex Xu | Excellent structured walkthroughs of 30+ system design problems. Matches interview format closely. | Read alongside your interview prep. Good for examples. |
| **Clean Code** — Robert C. Martin | The original guide to writing maintainable code. Chapter 3 (Functions) and Chapter 10 (Classes) are directly applicable to LLD interviews. | Great for keeping code quality sharp. |
| **Design Patterns: Elements of Reusable Object-Oriented Software** — Gang of Four | The canonical source for the 23 classic patterns. Dense but authoritative. | Reference book — look up patterns you want to deepen. |
| **Clean Architecture** — Robert C. Martin | Explains how to structure entire systems, not just individual classes. Bridges LLD and HLD thinking. | After you're comfortable with design patterns. |
| **Database Internals** — Alex Petrov | Deep dive into how databases work: B-trees, LSM trees, consensus protocols. | When you want to go from "I know Cassandra" to "I understand WHY Cassandra works this way." |

---

### Engineering Blogs — Read Weekly

| Blog | What You Learn | Link |
|------|----------------|------|
| **High Scalability** | Real-world architecture write-ups from major companies. Case studies at scale. | highscalability.com |
| **AWS Architecture Blog** | How AWS themselves solve distributed systems problems. Auth patterns, data pipelines. | aws.amazon.com/blogs/architecture |
| **Netflix Tech Blog** | Chaos engineering, microservices patterns, streaming infrastructure at insane scale. | netflixtechblog.com |
| **Uber Engineering Blog** | Geospatial systems, real-time data, dispatch algorithms, ML infrastructure. | eng.uber.com |
| **Cloudflare Blog** | Networking, CDN, DDoS mitigation, edge computing — deeply technical. | blog.cloudflare.com |
| **Martin Fowler's Blog** | Patterns of enterprise architecture, microservices, refactoring, event sourcing. | martinfowler.com |
| **The Morning Paper** (archived) | Summaries of influential CS papers. Great for breadth of distributed systems knowledge. | blog.acolyer.org |

---

### Distributed Systems Papers — For the Curious

Reading original papers separates candidates who have heard terms from those who understand them.

| Paper | Why It Matters |
|-------|----------------|
| **Google MapReduce (2004)** | The foundational paper on batch distributed processing. Still referenced everywhere. |
| **Google Bigtable (2006)** | The original wide-column store paper. Directly influenced Cassandra and HBase. |
| **Amazon Dynamo (2007)** | The paper that invented consistent hashing and the CAP trade-off in practice. Every NoSQL system cites this. |
| **Google Spanner (2012)** | True globally distributed SQL with external consistency. TrueTime concept is mind-expanding. |
| **Kafka: A Distributed Messaging System (2011)** | How LinkedIn built Kafka. Explains the log-based design from first principles. |
| **Raft Consensus Algorithm (2014)** | Easier to understand than Paxos. Underpins etcd, Consul, and most modern coordination systems. |

---

### Practice Platforms

| Platform | What to Use It For |
|----------|-------------------|
| **LeetCode** | Algorithms and data structures — continue with medium/hard problems |
| **Grokking System Design** (Educative.io) | Structured HLD problem walkthroughs |
| **Excalidraw** | Free whiteboard for practicing drawing architecture diagrams |
| **GitHub: donnemartin/system-design-primer** | Excellent open-source resource with HLD fundamentals and example problems |
| **Pramp** | Free peer-to-peer mock interviews — do at least 2 per week before your interview |
| **interviewing.io** | Anonymous technical interviews with engineers from FAANG companies |

---

## Final Words

You have spent 25 days building a systematic understanding of software design — from the fundamentals of object-oriented thinking, through 14 classic design patterns, through the entire infrastructure of modern distributed systems, and through 20+ complete design problems.

The engineer you are today is meaningfully different from the engineer you were on Day 1.

In the interview, remember three things:

**1. Think out loud.**
The interviewer cannot assess reasoning they cannot hear.
Your thought process is the interview — not just the final answer.

**2. Trade-offs over perfection.**
Every decision has a trade-off. The interviewer wants to know you understand yours.
"I chose X because of Y, and the trade-off I'm accepting is Z" is the language of a senior engineer.

**3. You have seen this before.**
Every question will feel familiar, because you have prepared for this.
Steady breath. Start with clarifying questions. Follow the framework.
The answer will come.

Good luck. You are ready.

---

*End of Day 25 — Week 4 — 25-Day Interview Preparation Program*
*LLD + HLD Complete*
