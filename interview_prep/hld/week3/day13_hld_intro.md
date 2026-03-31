# Week 3 - Day 13: Introduction to High-Level Design (HLD)
# Topic: What is HLD, Client-Server Architecture, How Systems Communicate

---

## What is High-Level Design — and Why Does It Exist?

Imagine you are hired to build a brand-new city.

Before laying a single brick, the city planners sit down and decide:
- Where will the roads go?
- Where will the hospitals, schools, and airports be located?
- How many lanes will the highway have?
- Which district handles residential, which handles commercial?
- Where does the water supply come from? How does sewage flow out?

This is **city planning** — the big picture. Nobody at this stage is deciding
what color tiles to use in the bathroom of house number 47. That comes later.

Now contrast this with an **interior designer** who works inside one specific building.
They decide: where the furniture goes, what the kitchen layout looks like, which
shade of white the walls should be. This is fine-grained, detailed, specific.

In software engineering:
- **HLD (High-Level Design)** = City planning. The big picture. How does the
  entire system fit together? What are the major components? How do they communicate?
- **LLD (Low-Level Design)** = Interior design. How is one specific component
  implemented internally? What classes, methods, and data structures does it use?

Both matter. A city with no plan becomes a chaotic mess of roads leading nowhere.
A building with no interior design is a concrete shell nobody can live in.

In interviews, **HLD questions** sound like:
- "Design YouTube"
- "Design a URL shortener like Bit.ly"
- "Design WhatsApp's messaging system"
- "Design an Uber-like ride-hailing service"

You are NOT expected to write code. You are expected to think at the
**system level** — components, data flow, trade-offs, scale.

---

## Section 1: HLD vs LLD — A Side-by-Side Comparison

| Aspect | HLD | LLD |
|---|---|---|
| **Focus** | System architecture | Component internals |
| **Question type** | "Design Twitter" | "Design the Tweet class" |
| **Output** | Block diagrams, component maps | Class diagrams, code |
| **Tools** | Boxes, arrows, services | Classes, methods, algorithms |
| **Analogy** | City map | Blueprint of one building |
| **Duration in interview** | 30-45 minutes | 30-45 minutes |
| **Key skill tested** | Breadth, trade-off thinking | Depth, OOP, patterns |

The most important thing to understand: **HLD is about trade-offs.**
There is rarely one "correct" answer. The interviewer wants to see you:
1. Ask smart clarifying questions
2. Reason about scale and bottlenecks
3. Make decisions and explain WHY
4. Know the trade-offs of every choice

---

## Section 2: The Client-Server Model — The Foundation of the Internet

Every web application you have ever used — Instagram, Google, Spotify, Gmail —
runs on a model called **Client-Server Architecture**.

### The Restaurant Analogy

Think of a restaurant.

- **You (the customer)** = the **Client**. You sit at the table with needs.
  You don't go into the kitchen yourself. You don't cook your own food.
  You make a **request**: "I would like pasta carbonara, please."

- **The Kitchen** = the **Server**. It receives orders, processes them
  (actually cooks the food), and prepares responses. The kitchen has the
  resources: ingredients, stoves, chefs.

- **The Waiter** = the **Network**. The waiter carries your order from your
  table (client) to the kitchen (server), and carries the food back to you.
  The waiter is the **messenger** — it doesn't cook, it just transports.

This is literally how the internet works:

```
[ Your Browser (Client) ]
         |
         |  HTTP Request: "GET /api/feed"
         v
[ Network (the Waiter) ]
         |
         v
[ Web Server (the Kitchen) ]
         |
         |  Fetches data, processes, builds response
         v
[ HTTP Response: JSON data with your feed ]
         |
         v
[ Your Browser renders the page ]
```

### What Exactly is a Client?

A **client** is anything that initiates a request and consumes a response.

- A web browser (Chrome, Safari) is a client
- A mobile app (Instagram on your phone) is a client
- A Python script making an API call is a client
- Even one server calling another server — the caller is the client

The client:
- Knows what it wants
- Sends a request
- Waits for a response
- Uses the response (renders UI, stores data, etc.)
- Has a limited view — it only knows what the server sends back

### What Exactly is a Server?

A **server** is a program that listens for requests, processes them, and sends back responses.

The server:
- Is always listening (like a restaurant kitchen open for orders)
- Has the actual data and business logic
- Can serve many clients simultaneously
- Returns structured responses (JSON, HTML, binary data)

The word "server" refers to the **role**, not the physical machine.
Your laptop can be a server if you run a web server on it.

### The Request-Response Cycle

Every interaction on the web follows this pattern:

```
1. Client initiates a connection
2. Client sends a REQUEST (method + URL + headers + optional body)
3. Server receives and parses the request
4. Server executes business logic (queries DB, calls other services, etc.)
5. Server builds a RESPONSE (status code + headers + body)
6. Server sends the response back
7. Client receives and processes the response
8. Connection is closed (or kept alive for reuse)
```

An HTTP request looks like this under the hood:
```
GET /api/users/42 HTTP/1.1
Host: api.myapp.com
Authorization: Bearer eyJhbGci...
Accept: application/json
```

And a response:
```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600

{
  "id": 42,
  "name": "Priya Sharma",
  "email": "priya@example.com"
}
```

---

## Section 3: How a Web Request Actually Travels

Let's trace exactly what happens when you type `www.amazon.com` and press Enter.
This is one of the most famous interview questions in the world.
Understanding each step deeply is essential.

```
[ Your Browser ]
      |
      | Step 1: DNS Lookup
      v
[ DNS Server ] -----> Returns IP address: 52.94.236.248
      |
      | Step 2: CDN Check
      v
[ CDN Edge Server ] -----> Returns cached static content (if available)
      |
      | Step 3: Load Balancer
      v
[ Load Balancer ] -----> Routes to one of many app servers
      |
      | Step 4: Application Server
      v
[ App Server ] -----> Runs business logic, queries DB
      |
      | Step 5: Database
      v
[ Database ] -----> Returns data
      |
      v
[ Response travels back through the same chain to your browser ]
```

### Step 1 — DNS: The Phone Book of the Internet

DNS stands for **Domain Name System**.

You type `www.amazon.com`. Your browser doesn't understand names.
It only understands IP addresses (like `52.94.236.248`).
DNS translates the human-readable name into a machine-readable IP address.

Think of DNS as a **phone book**: you look up "Amazon" and it gives you the phone number.
*(More detail in Day 14)*

### Step 2 — CDN: The Local Warehouse

CDN stands for **Content Delivery Network**.

Amazon has servers in Virginia, USA. You are in Mumbai, India.
If every request traveled from Mumbai to Virginia and back, it would be very slow.

A CDN is a **network of servers spread around the world**.
Static files (images, CSS, JavaScript, videos) are copied to CDN servers
close to users. When you request an image, the CDN server in Mumbai
responds — not the origin server in Virginia.

Think of it like this: instead of ordering from a central warehouse in
Delhi and waiting 7 days, you order from a local warehouse in your city
and receive it the same day.

### Step 3 — Load Balancer: The Traffic Police

Amazon gets millions of requests per second. No single server can handle all of them.
They run hundreds — sometimes thousands — of servers.

A **Load Balancer** sits in front of all those servers and decides:
"This request goes to Server 5. That request goes to Server 12."

Without a load balancer, all traffic would pile onto one server until it crashes —
like a city with only one road and no traffic management.

### Step 4 — Application Server: The Kitchen

The application server is where your actual code runs.
It receives the routed request, executes business logic:
- Validates the user's session
- Applies business rules
- Calls the database
- Formats and returns the response

In Amazon's case: it fetches your recommendations, checks your cart,
calculates prices, and assembles the page data.

### Step 5 — Database: The Filing Cabinet

The database is where all persistent data lives.
Products, users, orders, prices — all stored here.

The app server queries the database:
```sql
SELECT * FROM products WHERE category = 'electronics' LIMIT 20;
```

The database processes the query and returns rows, which the
app server packages into a JSON response and sends back.

---

## Section 4: Stateless vs Stateful Servers

This concept is **critical** in HLD. If you don't understand it, you cannot
design systems that scale.

### The Stateful Coffee Shop

Imagine a coffee shop where you have one specific barista, Ravi.
Every time you visit, Ravi remembers you:
- "Oh, you always get an oat milk cappuccino with no sugar, right?"
- He even remembers your loyalty points in his head
- He tracks your tab throughout the day

This is a **stateful** relationship. Ravi is storing **state** (memory of you)
between your visits.

**Problem**: What if Ravi is sick one day? Someone else serves you.
They have no memory of you. Your tab is lost. Your preferences are forgotten.

Now imagine there are 5 baristas and 500 customers. Each barista is trying to
remember 100 specific customers' preferences, tabs, and orders.
This becomes completely unmanageable.

**Stateful servers work the same way.** If a server remembers which user it is
serving (stores session data in its own memory), then:
- That user MUST always go back to the SAME server
- If that server crashes, the user's session is gone
- You cannot freely add or remove servers (scale) because customers are "stuck" to specific servers

### The Stateless Coffee Shop

Now imagine the coffee shop changes its model:
- Every order is written on a card by the customer
- The card contains: "Name: Priya. Order: Oat milk cappuccino, no sugar. Loyalty points: 47."
- The barista reads the card, makes the drink, stamps the card, hands it back
- The barista remembers NOTHING between visits — all the information is on the card

This is **stateless**. The barista (server) holds zero memory between requests.
Every request is **self-contained** — it carries everything the server needs to process it.

**Benefit**: Any barista can serve any customer. If one barista calls in sick,
the others pick up seamlessly. You can hire 10 more baristas and they
all work immediately — no "onboarding" needed.

**Stateless servers** work the same way:
- The client sends its identity (JWT token, session ID) with **every request**
- The server processes the request using that info — no local memory needed
- Any server in the cluster can handle any request
- Servers can be added or removed freely — this is horizontal scaling

```
STATEFUL (Bad for scale):
Client A --> Server 1 (remembers Client A's session)
Client A --> MUST go to Server 1 again
Client A --> Server 1 crashes --> Session lost!

STATELESS (Good for scale):
Client A sends token --> Server 1 handles it
Client A sends token --> Server 3 handles it (no problem!)
Client A sends token --> Server 7 handles it (no problem!)
```

### Where State Lives in Stateless Systems

But wait — you still need to store session data somewhere. The trick is:
**you store state outside the servers**, in a shared store:

- **Redis** (in-memory cache) for session data
- **Database** for persistent user data
- **JWT tokens** (state encoded in the token itself, no server memory needed)

This way every server can look up the shared store and get the state it needs,
without any one server "owning" a user.

---

## Section 5: Synchronous vs Asynchronous Communication

### The Phone Call vs The Text Message

Imagine you need information from your colleague.

**Synchronous (Phone call):**
- You call them
- They must answer RIGHT NOW
- You both stop everything else
- You wait until they answer and respond
- Only then can you continue with your work

**Asynchronous (Text message):**
- You send a text
- They read it when they are free
- They respond when they are ready
- YOU continue with other work while waiting
- When their reply arrives, you handle it

This is exactly how synchronous and asynchronous communication works in systems.

### Synchronous Communication

```
Client -----> Server A -----> Server B -----> Server C
                              WAIT...         WAIT...
              <----- response <----- response <-----
```

- Client blocks and waits for the response
- Easy to understand and debug
- Creates tight coupling — if Server C is slow, everything is slow
- If Server C is down, the whole chain fails

**Used when:** You need an immediate response to continue. E.g., checking
if a user's payment card is valid before confirming an order.

### Asynchronous Communication

```
Client -----> Server A -----> Message Queue -----> Server B (processes later)
               immediately gets "202 Accepted"        Server C (processes later)
               continues doing other things            Server D (processes later)
```

- Client sends a request and immediately gets back an acknowledgement
- Processing happens in the background
- The services are **decoupled** — Server B failing doesn't affect the client
- Much better for high-volume, non-urgent tasks

**Used when:** You don't need an immediate result. E.g., sending a welcome
email after registration. The user doesn't need to wait for the email to
be sent before seeing their dashboard.

### Real Example

**Ordering on Swiggy:**

Synchronous part:
- Check if restaurant is open: synchronous (you need to know NOW before showing the menu)
- Process payment: synchronous (you need to know if the payment succeeded)

Asynchronous part:
- Send order to restaurant: goes into a queue
- Notify the delivery partner: async
- Send you an order confirmation SMS: async
- Update analytics and revenue reports: async (nobody needs this in real time)

**Message Queues** (like Kafka, RabbitMQ, AWS SQS) are the infrastructure
that enable asynchronous communication. Think of them as a mailbox:
senders drop letters in, receivers pick them up when ready.

---

## Section 6: REST vs RPC — Two Ways to Design APIs

### REST — The Standard Menu

**REST (Representational State Transfer)** is a style for designing APIs.
Think of it like a restaurant with a standard, clearly organized menu:

- There are fixed categories: Starters, Mains, Desserts, Drinks
- Each item has a clear name
- You order by pointing to items on the menu

REST uses **URLs (resources)** and **HTTP methods (actions)**:

```
GET    /users/42          -> Get user with ID 42
POST   /users             -> Create a new user
PUT    /users/42          -> Update user 42 (full replacement)
PATCH  /users/42          -> Update part of user 42
DELETE /users/42          -> Delete user 42

GET    /users/42/orders   -> Get all orders for user 42
GET    /orders/99         -> Get order 99
POST   /orders            -> Create a new order
```

Key REST principles:
- **Stateless**: each request is self-contained
- **Resource-based**: URL represents a noun (thing), HTTP method represents the verb (action)
- **Uniform interface**: same patterns everywhere, easy to predict
- **Human readable**: a developer can read a REST URL and understand what it does

**Best used when:** Building public APIs, third-party integrations, browser-to-server communication.

### RPC — The "Just Tell Me What to Do" Style

**RPC (Remote Procedure Call)** is a style where you call a function on a remote server
as if it were a local function.

Think of it like calling a colleague on the phone and saying:
"Hey, can you run `calculateTax(order_id=99, region='UK')` for me and tell me the result?"
You're calling a procedure — a specific action — rather than working with a resource.

```
# REST style
GET /orders/99/tax

# RPC style (like gRPC)
POST /calculateTax
Body: { "order_id": 99, "region": "UK" }
```

RPC is action-oriented, not resource-oriented.

**gRPC** (Google's RPC framework) is the modern, high-performance version.
It uses Protocol Buffers (binary format) instead of JSON — much faster.

**Best used when:**
- Internal microservice-to-microservice communication (speed matters)
- When you need to call complex operations with many parameters
- Real-time streaming (gRPC supports bi-directional streaming)

### REST vs RPC Quick Comparison

| Aspect | REST | RPC / gRPC |
|---|---|---|
| **Style** | Resource-oriented | Action-oriented |
| **Format** | JSON (usually) | Binary (Protocol Buffers) |
| **Performance** | Good | Excellent |
| **Human readable** | Yes | No (binary) |
| **Best for** | Public APIs, browsers | Internal services, high speed |
| **Browser support** | Native | Needs extra setup |

---

## Section 7: Monolith vs Microservices — A Brief Introduction

*(This will be covered deeply in Week 4. Here is just enough to know the concept.)*

### The Monolith — One Big Restaurant

A **monolith** is a single application that contains all the code for every feature.

Think of it as a restaurant where one person does everything:
takes orders, cooks, serves, cleans, manages accounts, and handles complaints.

**Pros:** Simple to build, easy to test, no network communication overhead.
**Cons:** As it grows, it becomes a giant tangled mess. One bug can crash everything.
Scaling means scaling the ENTIRE application, even if only one part is under load.

### Microservices — Separate Kitchens

**Microservices** splits the application into small, independent services.
Each service owns one specific business domain.

Think of a large hotel with separate departments:
- Restaurant (food service)
- Room service
- Concierge
- Laundry
- Accounting

Each department operates independently. A problem in laundry does not shut down the restaurant.

In software:
- User Service: handles registration, login, profiles
- Order Service: handles order creation and tracking
- Payment Service: handles all payment logic
- Notification Service: sends emails and SMS
- Inventory Service: tracks product stock

**Pros:** Each service scales independently, teams work in isolation, one failure is contained.
**Cons:** Much more complex, network calls between services, need service discovery, monitoring, etc.

In a real interview, when asked to design a large system, you should naturally
lean toward microservices — but acknowledge the added operational complexity.

---

## Section 8: What Interviewers Look For in HLD

This is perhaps the most important section. Knowing the technology is not enough —
you need to know how to **present** your design.

### The Box Diagram

Draw a box diagram on the whiteboard (or shared screen). This is non-negotiable.
A design you cannot draw is a design you do not understand.

```
         +----------+          +-----------+
         |  Client  |          |  Mobile   |
         | (Browser)|          |   App     |
         +----+-----+          +-----+-----+
              |                      |
              +----------+-----------+
                         |
                    HTTPS Request
                         |
                         v
              +----------+----------+
              |      API Gateway     |
              | (Auth, Rate Limiting)|
              +----------+----------+
                         |
              +----------+-----------+
              |                      |
              v                      v
    +---------+------+    +----------+-----+
    |   User Service |    |  Order Service  |
    +-------+--------+    +--------+--------+
            |                      |
            v                      v
     +------+------+       +-------+------+
     |  Users DB   |       |  Orders DB   |
     | (PostgreSQL)|       |  (PostgreSQL)|
     +-------------+       +--------------+
```

### Explain Data Flow

Do not just draw boxes. Walk the interviewer through:

"When a user places an order, the request first hits the API Gateway,
which validates the JWT token and checks rate limits. Then it routes
to the Order Service. The Order Service calls the Inventory Service
to check stock, calls the Payment Service to charge the card,
and then writes the order to the Orders database. It then publishes
an OrderPlaced event to a Kafka queue. The Notification Service
consumes that event and sends a confirmation SMS asynchronously."

### Discuss Trade-offs

Every decision you make has a trade-off. The interviewer WANTS to hear you say:
- "I chose SQL here because we need strong consistency for financial transactions.
   The trade-off is that it scales less easily than NoSQL."
- "I'm using a message queue here which adds latency, but it decouples the
   services and prevents notification failures from affecting order processing."

Never present a design as "perfect." Always acknowledge what you are giving up.

---

## Section 9: How to Structure an HLD Answer — The Framework

Every HLD answer should follow this structure. Practice it until it is automatic.

### Step 1 — Clarify Requirements (3-5 minutes)

Never assume. Ask questions. This demonstrates senior-level thinking.

**Functional requirements** (what the system does):
- "What are the core features? Just the basics, or all features?"
- "Do users need to log in? Is it public or private?"
- "Is this read-heavy or write-heavy?"

**Non-functional requirements** (how the system performs):
- "What is the expected scale? How many users per day?"
- "What is the acceptable latency? Sub-100ms or is 500ms okay?"
- "Do we need 99.99% availability or is occasional downtime acceptable?"
- "Is consistency more important than availability? (e.g., banking vs social media)"
- "What are the data retention requirements?"

### Step 2 — Estimate Scale (2-3 minutes)

Back-of-envelope calculations show you can think in numbers.

Example for designing a URL shortener:
- "Let's say 100 million URLs are shortened per day"
- "That's 100M / 86,400 seconds = ~1,157 writes per second"
- "If read:write ratio is 100:1, that's ~115,700 reads per second"
- "Each URL record is about 500 bytes, so 100M * 500B = 50GB new data per day"
- "Over 5 years: 50GB * 365 * 5 = ~91 TB of storage needed"

This tells the interviewer you understand the actual demands of the system.

### Step 3 — Define APIs (3-5 minutes)

Sketch the key API endpoints. This anchors what the system actually does.

```
POST /shorten
Body: { "long_url": "https://very-long-url.com/..." }
Response: { "short_url": "https://bit.ly/abc123" }

GET /{short_code}
Response: 301 Redirect to original URL
```

### Step 4 — Design Components (10-15 minutes)

Draw the block diagram. For each component, explain:
- What it does
- What technology you'd use and why
- How it connects to other components

Cover these areas:
- Client layer (web, mobile)
- API layer (REST API, API Gateway)
- Service layer (which services? what does each own?)
- Data layer (which database for which data? why?)
- Caching layer (what is cached? what is the eviction policy?)
- Message queue layer (what events flow async?)
- CDN (what is served from CDN?)

### Step 5 — Deep Dive on Critical Components (5-10 minutes)

The interviewer will pick one or two components to go deeper on.
Common deep dives:
- "How would you design the database schema?"
- "How does the short URL generation algorithm work?"
- "How would you handle cache invalidation?"
- "How would you ensure the system doesn't go down if one service fails?"

### A Sample Opening Line

"Before I start designing, I want to clarify requirements and understand
the scale we are designing for. Is that okay?"

This one sentence tells the interviewer you are a thoughtful engineer.

---

## Interview Q&A

**Q1: What is the difference between HLD and LLD?**

> HLD (High-Level Design) focuses on the architecture of the overall system —
> which components exist, how they communicate, and what technologies are used.
> It answers the question: "What are the building blocks and how do they fit together?"
>
> LLD (Low-Level Design) focuses on the internal implementation of each component —
> class structures, method signatures, algorithms, and data structures.
> It answers: "How does one specific part actually work?"
>
> In an interview for a senior role, you are expected to do HLD first and
> then selectively deep dive into LLD for critical components.
> For example: HLD for "Design Twitter" means drawing the overall system.
> LLD would be designing the `Tweet` class or the `FeedGenerator` algorithm.

---

**Q2: What does it mean for a server to be stateless, and why is it important?**

> A stateless server holds no memory of previous requests.
> Each request from a client carries all the information the server needs to process it —
> typically via a JWT token or session ID in the header.
>
> Statelessness is important for two reasons:
>
> First, **horizontal scaling**: if the server holds no state, any request can go to
> any server in the cluster. You can add 50 new servers to handle traffic spikes
> and they are immediately useful — no synchronisation needed.
>
> Second, **resilience**: if one server crashes, no user data is lost, because
> no user data was stored on that server. The next request simply goes to another server.
>
> The state itself still exists — it lives in a shared external store like Redis
> or a database — but the servers themselves are interchangeable.

---

**Q3: When would you choose asynchronous communication over synchronous?**

> I choose asynchronous communication when three conditions are present:
>
> 1. The caller does NOT need an immediate result to continue its work
> 2. The operation is time-consuming and I don't want to block the caller
> 3. I want to decouple two services so that a failure in one doesn't cascade to the other
>
> For example, when a user registers on our platform, the core flow (create account,
> return success) is synchronous. But sending the welcome email is asynchronous —
> I publish an event to a message queue, and the Email Service processes it when ready.
>
> If sending the email were synchronous, a slow email provider would make the entire
> registration feel slow to the user. By making it async, the user gets their
> confirmation page instantly and the email arrives seconds later.
>
> On the other hand, I always keep payment processing synchronous. The user must
> know immediately whether their card was charged. Async would create terrible UX
> and potential double-charge bugs.

---

**Q4: What is the difference between REST and RPC? Which would you use internally between microservices?**

> REST is resource-oriented: URLs represent nouns (things like `/users`, `/orders`),
> and HTTP methods represent verbs (GET, POST, PUT, DELETE). It is human-readable,
> self-documenting, and works naturally with browsers.
>
> RPC (specifically gRPC) is action-oriented: you call a specific function on a
> remote server — like `calculateShippingCost(order_id, destination)`.
> gRPC uses Protocol Buffers (binary encoding) which is significantly faster than JSON.
>
> For internal microservice-to-microservice communication, I would choose gRPC because:
> - Performance is critical at this layer (many services calling each other per second)
> - I control both ends, so the binary format is fine
> - gRPC supports streaming, which is useful for real-time internal data pipelines
> - Strongly typed contracts (proto files) prevent mismatches between services
>
> For external-facing APIs (what browsers and mobile apps call), I'd use REST
> because it's universally supported, easy to integrate, and human-readable for
> third-party developers.

---

**Q5: Walk me through the components you would include when designing a large-scale system like Twitter.**

> I would structure the design in five layers:
>
> **Client Layer**: Web and mobile clients send requests over HTTPS.
>
> **API Gateway Layer**: All requests first hit the API Gateway, which handles
> authentication (JWT validation), rate limiting, SSL termination, and routing
> to the appropriate backend service.
>
> **Service Layer**: Separate microservices for each domain:
> - User Service (profiles, follows)
> - Tweet Service (create, delete tweets)
> - Timeline Service (generate and fetch feeds)
> - Search Service (full-text search using Elasticsearch)
> - Notification Service (push, email)
>
> **Data Layer**: Each service owns its own database.
> - Tweets stored in a distributed NoSQL store (Cassandra) for high write throughput
> - User relationships stored in a graph database
> - Media files stored in object storage (S3) and served via CDN
> - Hot timelines cached in Redis
>
> **Async Layer**: A Kafka message queue handles events like "user posted tweet",
> which triggers fan-out to followers' feeds, sends notifications, and updates analytics.
>
> The most interesting trade-off here is the timeline generation strategy:
> push model (pre-compute feeds on write) vs pull model (compute on read).
> For Twitter's scale, a hybrid approach is best: push for most users,
> pull for celebrities with 10M+ followers to avoid the fan-out explosion.

---

## Practice Exercise

Design a **URL Shortener** (like bit.ly) using the 5-step framework.

Work through the following:

1. **Clarify**: What features do you need? Analytics? Custom aliases? Expiry?
2. **Estimate**: Assume 100 million new URLs per day. Calculate reads/sec, storage needed.
3. **APIs**: Define the two core endpoints (shorten + redirect).
4. **Components**: Draw the block diagram. Which components do you need?
   Think about: where is the mapping stored? How do you generate a 6-character code?
   What gets cached and why?
5. **Deep dive**: How would you generate a unique short code for each URL?
   What happens when two users shorten the same long URL? How would you handle
   a URL that expires after 30 days?

Spend 30-40 minutes on this. Draw it out on paper. Then explain it out loud
as if you were in the interview. If you can explain it to someone with no
engineering background, you understand it.

---

*Next: Day 14 — Networking Basics: DNS, CDN, Load Balancer, Reverse Proxy, API Gateway*
