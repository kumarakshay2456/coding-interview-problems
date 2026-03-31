# Day 19 — Microservices vs Monolith, API Gateway, Service Communication

---

## 1. Monolith — The Giant Swiss Army Knife

### What Is a Monolith?

A **monolith** is a software application where all the components — the user interface, business logic, and data access — are packaged and deployed as a **single unit**. One codebase, one deployable artifact, one running process.

Think of it as a **Swiss Army Knife**. Everything you need is folded into one tool — a blade, a screwdriver, a bottle opener, scissors. It's convenient because it's self-contained. You pick it up and everything is right there.

That's a monolith. Your e-commerce app has the product catalog code, the cart logic, the payment logic, the user profile system, and the notification system all bundled into one giant application.

### How It Looks in Practice

```
[ Single Deployable Unit ]
  ├── User Module
  ├── Product Module
  ├── Cart Module
  ├── Payment Module
  ├── Notification Module
  └── Shared Database
```

One deployment command pushes everything. One database holds everything. One server runs everything.

### Pros of Monolith

| Advantage | Why It Matters |
|---|---|
| Simple to develop initially | Developers work in one codebase, one language, one IDE. No network calls between components. |
| Easy to test | You can test the entire system end-to-end in one place. |
| Simple deployment | One thing to build, one thing to deploy, one thing to monitor. |
| Low operational overhead | No need for service registries, API gateways, distributed tracing early on. |
| Easy debugging | Stack traces are local. You don't have to hop between 12 services to find a bug. |
| Fast initial velocity | A 3-person team can ship features fast without coordination overhead. |

### Cons of Monolith

Here is where the Swiss Army Knife analogy breaks down. Imagine your Swiss Army Knife blade gets dull. To sharpen it, you have to disassemble the **entire knife** and reassemble it — you can't just swap out the blade independently.

| Disadvantage | Real-World Impact |
|---|---|
| Hard to scale selectively | If your payment module is under load but your catalog is fine, you still have to scale the whole app. You're buying 10 Swiss Army Knives just because one blade is dull. |
| Long deployment cycles | A bug fix in the notification code requires redeploying the entire application. Risk is high. |
| Technology lock-in | The whole app uses one language and framework. You can't use Python's ML libraries for the recommendation engine and Java for payments — it's all one thing. |
| Codebase becomes unmaintainable | As the app grows, the codebase gets massive. A change in the payment module can accidentally break the cart. Tight coupling is the enemy. |
| Team scaling is hard | 50 engineers all working in the same codebase creates merge conflicts, coordination overhead, and dependency hell. |
| Single point of failure | A memory leak in the notification module can crash the entire app — taking payments down with it. |

---

## 2. Microservices — The Team of Specialists

### What Is a Microservice?

**Microservices** is an architectural approach where an application is built as a **collection of small, independent services**, each responsible for a specific business capability, each running in its own process, and each communicating over a network (usually HTTP or messaging).

The analogy: think of a **hospital**. Instead of one doctor who does everything — surgery, radiology, pediatrics, cardiology — you have **specialists**. The cardiologist handles hearts. The radiologist handles imaging. The pediatrician handles children. Each is an expert in their domain. They collaborate by passing information (test results, referrals) between departments.

If the radiology department is overwhelmed, you hire more radiologists. You don't need to hire more cardiologists at the same time. You scale independently.

### How It Looks in Practice

```
[ Client ]
    |
[ API Gateway ]
    |
    ├──→ [ User Service ]           → [ User DB ]
    ├──→ [ Product Service ]        → [ Product DB ]
    ├──→ [ Cart Service ]           → [ Cart DB ]
    ├──→ [ Payment Service ]        → [ Payment DB ]
    └──→ [ Notification Service ]   → [ Notification DB ]
```

Each service is a separate deployable. Each has its own database. They talk to each other over the network.

### Pros of Microservices

| Advantage | Why It Matters |
|---|---|
| Scale independently | Payment service getting hammered during a sale? Scale just that service. Cart service is idle? Keep it at 2 instances. Save money, use resources efficiently. |
| Deploy independently | Bug fix in notifications? Deploy just that service. Zero risk to the payment or product services. |
| Tech diversity | Use Go for the high-performance feed service. Use Python for the ML recommendation service. Use Node.js for the real-time chat. Best tool for each job. |
| Fault isolation | If the recommendation service crashes, users just don't get recommendations. They can still browse, add to cart, and checkout. The blast radius is contained. |
| Team autonomy | The "Order Team" owns the Order Service end-to-end. They deploy on their own schedule. No merge conflicts with the "User Team." |
| Easier to understand | Each service is small. A new developer can understand the Payment Service in a day instead of trying to understand 300,000 lines of monolith code. |

### Cons of Microservices

The hospital analogy also reveals the downsides. Think about the coordination required. A patient needs four specialists. Each writes their notes in different formats. The specialists have to schedule consultations. If one department's system goes down, it can block the whole workflow.

| Disadvantage | Real-World Impact |
|---|---|
| Operational complexity | You now have 20 services to deploy, monitor, log, and debug. You need Kubernetes, service meshes, distributed tracing, centralized logging. This is a serious infrastructure investment. |
| Network latency | What used to be a local function call is now an HTTP request over the network. One user request might fan out to 8 service calls. Latency adds up. |
| Distributed transactions | Updating a user's order requires changes in Order Service, Inventory Service, and Payment Service atomically. There is no single database transaction to wrap around them. Extremely hard to get right. |
| Data consistency challenges | Each service has its own DB. Getting a consistent view across services is hard. Data can be temporarily inconsistent (eventual consistency). |
| Service coordination overhead | Services need to find each other (service discovery). They need to handle each other failing (circuit breakers). This is boilerplate infrastructure code you have to write and maintain. |
| Testing is harder | Integration testing requires spinning up multiple services. Local development is more complex. |

---

## 3. When to Use Monolith vs Microservices

This is one of the most important judgment calls in system design. The wrong choice can doom a project.

### The Decision Framework

**Use a Monolith when:**

- You are **starting a new product** and don't know the domain well yet. Boundaries between services are not clear. Getting them wrong is costly — splitting a monolith incorrectly is painful. Martin Fowler calls this the "Monolith First" pattern.
- Your **team is small** (under 5-10 engineers). Microservices add overhead that kills small team velocity.
- Your **scale requirements are modest**. If you have 10,000 users and no hypergrowth on the horizon, the complexity of microservices is unjustified.
- You need to **ship fast** to validate a business idea. Correctness and speed of iteration matter more than operational elegance.
- Your **domain is well-understood and stable**. Low change frequency means the benefits of independent deployability are limited.

**Use Microservices when:**

- Your **team has grown** (20+ engineers) and multiple teams are stepping on each other in the monolith.
- **Different parts of the system have wildly different scaling needs**. The video transcoding service needs 100x more CPU than the user profile service.
- You need **high availability** for specific components. Deploying frequently requires independent deployability.
- You have **domain complexity** that maps cleanly to distinct bounded contexts (see DDD below).
- **Technology diversity is genuinely needed** — like needing ML (Python), real-time (Go), and transactional (Java) in the same product.

**The Honest Truth:** Most companies that are using microservices successfully started as monoliths and evolved. Amazon, Netflix, Uber — all started as monoliths. They migrated to microservices as the organization and scale demanded it.

---

## 4. Service Decomposition — How to Split a Monolith

### Domain-Driven Design (DDD) — The Blueprint for Splitting

**Domain-Driven Design (DDD)** is a software design approach that says: your code structure should mirror your business structure. The business has natural boundaries — your code should too.

The key concept in DDD for microservices is the **Bounded Context**.

**Bounded Context analogy:** Think of a hospital again. The word "patient" means something specific in the radiology department (a person getting an X-ray, with an imaging order). The same word "patient" in billing means something completely different (an account with insurance, a billing address, outstanding charges). The same entity, different models, different databases, different rules. Each department is a **bounded context** — a boundary within which a specific domain model applies.

### How to Decompose a Monolith

**Step 1: Identify business domains.** List the major business capabilities. For an e-commerce app:
- User management (registration, profiles, authentication)
- Product catalog (items, categories, search)
- Shopping cart (add/remove items, pricing)
- Order management (place order, order history)
- Payment processing (charge, refund)
- Inventory management (stock levels, reservations)
- Notification (email, SMS, push)
- Shipping/fulfillment (dispatch, tracking)

**Step 2: Define bounded contexts.** Each business domain above is a candidate for a bounded context — and therefore a candidate for a service.

**Step 3: Identify seams.** Look for parts of the monolith with minimal coupling to the rest. These are the easiest to extract first. Usually, something like a notification service or reporting service can be peeled off with relatively low risk.

**Step 4: Strangle the monolith gradually.** Don't try to rewrite everything at once. Use the **Strangler Fig Pattern** — add new functionality as new services, and gradually move old functionality out of the monolith. Over time, the monolith shrinks and the service ecosystem grows, until the monolith is gone.

**Golden Rule of Service Decomposition:**
- Services should be **loosely coupled** (minimal dependencies on each other) and **highly cohesive** (everything inside the service is related to one business capability).

---

## 5. Service Communication

Once you have multiple services, they need to talk to each other. There are two fundamental models: **synchronous** and **asynchronous**.

### Synchronous Communication

The caller sends a request and **waits for a response** before proceeding. Like a phone call — you ask a question and wait on the line for the answer.

#### REST (Representational State Transfer)

The most common approach. Services communicate over HTTP using standard methods (GET, POST, PUT, DELETE) and return JSON or XML.

**When to use REST:**
- When you need a **simple request-response** and the response is needed immediately to continue processing.
- When services are called by **external clients** (browsers, mobile apps).
- When you want **human-readable, easy-to-debug** communication.
- When the operation is a **query** (read) or a simple **command** (create/update).
- When **broad compatibility** matters — REST over HTTP is supported everywhere.

**Downside:** Text-based (JSON), verbose, slower serialization/deserialization than binary protocols.

#### gRPC (Google Remote Procedure Call)

gRPC is a high-performance RPC framework developed by Google. It uses **Protocol Buffers (protobuf)** — a binary serialization format — and runs over HTTP/2.

Think of the difference: REST is like sending letters (text, readable, any format). gRPC is like a direct phone line with a standardized conversation protocol — faster, more structured, but requires both sides to agree on the protocol up front.

**When to use gRPC:**
- **Internal service-to-service communication** where performance matters.
- When you are moving **large volumes of data** between services — binary is significantly smaller and faster than JSON.
- When you need **streaming** — gRPC supports bidirectional streaming natively (REST does not).
- When you want **strongly-typed contracts** — the protobuf definition IS the contract, and both client and server code can be generated automatically, reducing errors.
- When services are **polyglot** (different languages) — gRPC has official support for ~10 languages.

**Downside:** Not human-readable, harder to debug with plain tools, requires protobuf schema management.

**REST vs gRPC Summary:**

| Factor | REST | gRPC |
|---|---|---|
| Protocol | HTTP/1.1 | HTTP/2 |
| Format | JSON (text) | Protobuf (binary) |
| Performance | Good | Excellent |
| Streaming | Limited | Full bidirectional |
| Browser support | Excellent | Limited (needs proxy) |
| Debugging ease | Easy (Postman, curl) | Harder |
| Best for | External APIs, simple services | Internal high-performance communication |

### Asynchronous Communication — Message Queues

The caller sends a message and **does not wait** for a response. It fires the message into a queue and moves on. The receiver picks up the message when it's ready and processes it independently.

Like dropping a letter in a mailbox. You don't stand by the mailbox waiting for a reply. You go about your day. The post office handles delivery. The recipient reads and responds at their convenience.

**When to use asynchronous messaging:**
- When the action **does not need an immediate response**. After a user places an order, you need to send a confirmation email — but you don't need to wait for the email to be sent before telling the user "your order is placed."
- When you need to **decouple** the sender from the receiver. The Order Service doesn't need to know that a Notification Service exists. It just fires an "OrderPlaced" event.
- When you need to handle **spikes in load**. If 10,000 orders come in at once, the queue absorbs the spike. The downstream services process at their own pace.
- When operations are **long-running**. Video encoding, report generation — put it in a queue, process it in the background.

We'll cover Kafka and RabbitMQ in depth in Day 20.

---

## 6. API Gateway — The Front Door

### What Is an API Gateway?

An **API Gateway** is a server that acts as the **single entry point** for all client requests into your microservices architecture. Instead of clients knowing about all 20 services and calling them directly, every request goes through the gateway, which routes it to the right service.

The analogy: the **hotel concierge**. When you arrive at a large hotel, you don't wander around trying to figure out which staff member handles what. You go to the concierge. They direct you to the right person or handle the request themselves. They know the hotel's internal structure so you don't have to.

The client (browser, mobile app) talks to one endpoint: the API Gateway. The gateway handles everything else internally.

### What the API Gateway Handles

**1. Routing**
The gateway examines each incoming request and routes it to the appropriate service.
- `GET /products/123` → routes to Product Service
- `POST /orders` → routes to Order Service
- `GET /users/profile` → routes to User Service

**2. Authentication and Authorization**
Every request needs to be authenticated. Without a gateway, each microservice would have to independently verify JWTs, validate sessions, or call an auth service. That's massive duplication.

With the gateway: the gateway validates the JWT token on every request. It passes the verified user identity downstream. Services trust that if a request reached them through the gateway, it's already authenticated.

**3. Rate Limiting**
Protects your services from being overwhelmed by too many requests — whether from a misbehaving client, a scraper, or a DDoS attack. The gateway enforces "100 requests per minute per user" centrally, without each service implementing this logic.

**4. SSL Termination**
Clients communicate with the gateway over HTTPS (encrypted). The gateway decrypts the traffic and forwards requests to internal services over HTTP (within the secure internal network). This means only the gateway needs SSL certificates — internal services don't.

**5. Logging and Monitoring**
Every single request passes through the gateway. This is the perfect place to log every request, measure latency, track error rates, and emit metrics — without any individual service having to do it.

**6. Request/Response Transformation**
The gateway can reshape requests before forwarding them (add headers, transform formats) and reshape responses before returning them (aggregate data from multiple services, strip internal fields the client shouldn't see).

**7. Load Balancing**
The gateway can distribute requests across multiple instances of a service. If Payment Service has 5 instances, the gateway round-robins or load-balances requests across all 5.

**8. API Composition (Aggregation)**
Sometimes one client request requires data from multiple services. The gateway can fan out to User Service and Order Service and Product Service, aggregate the results, and return a single response to the client. This reduces the number of round trips the client has to make.

### Popular API Gateways
- **AWS API Gateway** — managed, scales automatically, integrates with Lambda and other AWS services
- **Kong** — open-source, plugin-based, extremely flexible
- **NGINX** — can be configured as a gateway/reverse proxy
- **Traefik** — popular in Kubernetes environments, auto-discovers services
- **Envoy** — high-performance proxy, used as the data plane in service meshes like Istio

### API Gateway vs Load Balancer

| Feature | Load Balancer | API Gateway |
|---|---|---|
| Primary job | Distribute traffic across instances | Route requests to different services + cross-cutting concerns |
| Awareness | Routes to same service, multiple instances | Routes to different services |
| Auth/Rate limiting | No | Yes |
| Protocol handling | TCP/HTTP | HTTP, WebSocket, gRPC |

---

## 7. Service Discovery — How Services Find Each Other

### The Problem

In a monolith, one module calls another by a local function call. No network involved.

In microservices, Service A needs to call Service B over the network. But Service B might have 10 instances running across 20 servers, and those servers come and go dynamically (auto-scaling, crashes, deployments). Service A can't have a hardcoded IP address for Service B — that IP changes constantly.

How does Service A find where Service B is right now?

### The Phone Directory Analogy

Think of service discovery as a **phone directory** (or a more modern DNS). Services register themselves ("I'm the Payment Service, I'm at 10.0.1.25:8080") in a **service registry** — the phone directory. When Service A wants to call Service B, it looks up Service B in the registry to get its current address.

### Client-Side Discovery

The **client (calling service) is responsible** for querying the service registry and then making the request directly to the discovered instance.

**Flow:**
1. Payment Service starts up and registers itself with the registry: "I'm at 10.0.1.25:8080."
2. Order Service wants to call Payment Service.
3. Order Service queries the registry: "Where is Payment Service?"
4. Registry returns: "It's at 10.0.1.25:8080."
5. Order Service calls Payment Service directly.

**Example tools:** Netflix Eureka, Consul (with client-side libraries like Ribbon)

**Pros:** Simple, client controls load balancing strategy.
**Cons:** Every service client needs to implement discovery logic. Language-specific libraries needed for each language.

### Server-Side Discovery

The **client sends the request to a router/load balancer**, which is responsible for querying the registry and forwarding to the right instance. The client knows nothing about discovery.

**Flow:**
1. Payment Service registers with the registry.
2. Order Service sends a request to a fixed address (e.g., the API gateway or a load balancer).
3. The load balancer queries the registry and forwards to the right Payment Service instance.

**Example tools:** AWS ALB + ECS, Kubernetes (built-in), Consul + Fabio

**Pros:** Client code is simple — no discovery logic needed.
**Cons:** The load balancer/router is now a critical component.

**In Kubernetes:** Service Discovery is built in. Every service gets a DNS name (`payment-service.default.svc.cluster.local`). Kubernetes routes to healthy instances automatically.

---

## 8. Circuit Breaker Pattern

### The Problem — Cascading Failures

In a distributed system, services call other services. If Service B is slow or failing, every call from Service A to Service B will hang, consuming threads, connections, and resources. These blocked threads in Service A start accumulating. Service A slows down. Service C calls Service A. Service C starts hanging. The entire chain fails like dominoes.

This is a **cascading failure** — one failing service brings down the whole system.

### The Electrical Circuit Analogy

This pattern is named after the electrical circuit breaker in your home's electrical panel. When there's an electrical overload or short circuit, the breaker **trips** — it breaks the circuit to prevent the wiring from melting. You can reset it once the problem is fixed.

The Circuit Breaker pattern does the same thing in software. When calls to a downstream service start failing too much, the circuit breaker **trips** — it stops making real calls and immediately returns an error or fallback response. This protects the upstream service from hanging and prevents the failure from spreading.

### The Three States

**Closed (Normal operation):**
- Requests flow through normally.
- The circuit breaker counts failures in a rolling window.
- If the failure rate drops below a threshold (say, less than 50% failures in 60 seconds), everything is fine — stay Closed.

**Open (Failure detected):**
- The failure rate exceeded the threshold.
- The circuit breaker **trips open**. For a configured timeout period (say, 30 seconds), ALL requests are immediately rejected without even attempting to call the service.
- The caller gets an immediate error or fallback response (like a cached result or a "service unavailable" message).
- This gives the failing service time to recover without being bombarded by calls.

**Half-Open (Testing recovery):**
- After the timeout period, the circuit breaker allows a **small number of test requests** through.
- If they succeed → the service has recovered → circuit closes back to normal.
- If they fail → the service is still down → circuit opens again for another timeout period.

```
[CLOSED] ──── too many failures ───→ [OPEN]
    ↑                                    |
    |                            timeout expires
    |                                    |
    └──── test requests succeed ── [HALF-OPEN]
          test requests fail ──────────→ [OPEN]
```

### Why It Matters

Without a circuit breaker: 1,000 requests/second pile up trying to call a failing service. Each request waits 30 seconds before timing out. 30,000 threads hanging. Server out of memory. Entire system crashes.

With a circuit breaker: First 5 seconds of failures → circuit opens. Next 29,995 requests → immediately rejected with an error. Caller can use a fallback. Failing service has breathing room to restart. Damage is contained.

**Popular implementations:** Netflix Hystrix (now in maintenance), Resilience4j (Java), Polly (.NET), Hystrix (Golang)

---

## 9. Saga Pattern — Distributed Transactions

### The Problem

In a monolith with a single database, you wrap multiple operations in a database transaction: either all succeed, or all are rolled back. Atomic, consistent.

In microservices, a single business operation might span multiple services:

**"User places an order" involves:**
1. Order Service: Create the order record
2. Inventory Service: Reserve the item stock
3. Payment Service: Charge the user's card
4. Notification Service: Send confirmation email

Each service has its own database. You cannot wrap all four steps in one database transaction — they are in different databases, possibly different database engines.

What happens if payment fails after inventory was already reserved? You have inconsistent state — stock is reserved but no order exists.

### The Traditional (Bad) Solution: 2PC

**Two-Phase Commit (2PC)** is a distributed protocol that tries to achieve atomicity across multiple databases. It requires a coordinator to ask all participants "are you ready to commit?" and then issue a "commit" or "rollback" command.

Problems: It's blocking (participants hold locks while waiting), it's slow (multiple network round trips), and it's fragile (coordinator failure leaves participants stuck). Microservices architectures generally avoid 2PC.

### The Saga Pattern

A **Saga** is a sequence of local transactions. Each step completes its local transaction and publishes an event (or sends a message) to trigger the next step. If any step fails, compensating transactions are executed to undo the previous steps.

Think of a **package shipment relay race**. Runner 1 runs their leg and hands the baton to Runner 2. Runner 2 runs their leg and passes to Runner 3. If Runner 3 drops the baton (fails), the judges run the race in reverse — they take the baton from Runner 2, then Runner 1, undoing the legs. That's a compensating transaction.

### Choreography Saga

In the **choreography** approach, there is **no central coordinator**. Each service listens for events, does its work, and publishes new events. Services react to each other's events.

**Example — Order Placement:**
1. Order Service creates an order. Publishes `OrderCreated` event.
2. Inventory Service listens for `OrderCreated`. Reserves stock. Publishes `StockReserved` event.
3. Payment Service listens for `StockReserved`. Charges card. Publishes `PaymentSucceeded` event.
4. Notification Service listens for `PaymentSucceeded`. Sends confirmation email.

**If Payment fails:**
1. Payment Service publishes `PaymentFailed` event.
2. Inventory Service listens for `PaymentFailed`. Releases the stock reservation (compensating transaction).
3. Order Service listens for `PaymentFailed`. Marks the order as cancelled.

**Pros of Choreography:**
- Loose coupling — services only know about events, not each other.
- No single point of failure.
- Easy to add new services that react to existing events.

**Cons of Choreography:**
- Hard to track the overall state of a saga. "Where is this order in the process?" is difficult to answer.
- Harder to understand the overall flow — it's distributed across many services.
- Risk of cyclic dependencies between event listeners.

### Orchestration Saga

In the **orchestration** approach, a central **orchestrator service** (often called a Saga Orchestrator) knows the entire flow and tells each service what to do.

**Example — Order Placement:**
1. Client calls Order Orchestrator: "Place this order."
2. Orchestrator calls Inventory Service: "Reserve stock for Order #123." Inventory confirms.
3. Orchestrator calls Payment Service: "Charge $49.99 for Order #123." Payment confirms.
4. Orchestrator calls Notification Service: "Send confirmation for Order #123."
5. Orchestrator updates Order status: "Completed."

**If Payment fails:**
1. Orchestrator receives failure from Payment Service.
2. Orchestrator calls Inventory Service: "Release the stock reservation for Order #123." (compensating transaction)
3. Orchestrator marks the order as "Failed."

**Pros of Orchestration:**
- The overall flow is visible in one place — easy to understand and debug.
- Easier to handle complex failure scenarios and compensations.
- The orchestrator is the single source of truth for the saga's state.

**Cons of Orchestration:**
- The orchestrator can become a bottleneck or single point of failure.
- Tighter coupling between the orchestrator and the services it calls.
- Risk of the orchestrator becoming a "God object" that knows too much.

### Choreography vs Orchestration

| Factor | Choreography | Orchestration |
|---|---|---|
| Coordination | Decentralized (events) | Centralized (orchestrator) |
| Coupling | Lower | Higher |
| Visibility | Hard to track flow | Easy to track flow |
| Complexity | High (distributed logic) | Moderate (central logic) |
| Single point of failure | No | Yes (orchestrator) |
| Best for | Simple, linear flows | Complex flows with many compensations |

---

## 10. Real Example: Swiggy/Zomato Microservices

Let's look at how a food delivery platform like Swiggy or Zomato might decompose their system.

### Core Services

```
[ Mobile App / Web Client ]
         |
[ API Gateway ] ← Auth, Rate Limiting, Routing, SSL
         |
    ┌────┴────────────────────────────────┐
    |         |           |              |
[ User     [ Restaurant [ Order       [ Search
 Service ]   Service ]    Service ]     Service ]
    |              |          |              |
[ User DB ] [Menu DB ] [Order DB ]  [Search Index
                                      (Elasticsearch)]
    |
[ Notification Service ] ← Email / SMS / Push
    |
[ Delivery Service ]  ← Tracks delivery agents
    |
[ Payment Service ] ← Integrates with payment gateways
    |
[ Review & Rating Service ]
    |
[ Analytics Service ] ← Uses Kafka for event streaming
```

### How a Food Order Flows

1. User opens the app → request hits API Gateway → Gateway routes to Restaurant Service for menu.
2. User places an order → API Gateway → Order Service.
3. Order Service publishes `OrderPlaced` event to Kafka.
4. **Payment Service** consumes `OrderPlaced` → charges the user → publishes `PaymentSucceeded`.
5. **Restaurant Service** consumes `OrderPlaced` → notifies the restaurant (new order alert).
6. **Delivery Service** consumes `PaymentSucceeded` → assigns a nearby delivery agent.
7. **Notification Service** consumes `PaymentSucceeded` → sends "Order confirmed" SMS/push notification.
8. Delivery agent picks up food → Delivery Service updates status → Notification Service sends "Out for delivery" push.
9. Delivery completed → Delivery Service publishes `OrderDelivered` → Review Service triggers a "Rate your experience" notification.

### Why This Works

- **Independent scaling:** Restaurant Service is read-heavy during browsing. Payment Service is write-heavy and needs high reliability. They scale independently.
- **Fault isolation:** If the Review & Rating Service goes down, orders still work. Core user experience is unaffected.
- **Tech diversity:** Search Service uses Elasticsearch. Analytics Service uses Kafka Streams. Payment Service uses Java for reliability. Delivery tracking might use Go for real-time performance.
- **Team ownership:** A "Delivery Team" owns the Delivery Service end-to-end. They deploy independently 10 times a day without coordinating with the Payment Team.

---

## 11. Interview Q&A

### Q1: "What is the main difference between a monolith and microservices? When would you use each?"

**Model Answer:**

"A monolith is a single deployable unit where all components are tightly coupled and share a codebase and database. Microservices is an architecture where the system is decomposed into small, independently deployable services, each owning its own data and communicating over the network.

I'd use a monolith when starting a new product with a small team — it's faster to build, easier to test, and has lower operational overhead. The domain boundaries often aren't clear early on, and getting microservice boundaries wrong is very expensive to fix.

I'd migrate to microservices when the team is large enough that coordination on a single codebase hurts velocity, when different components have drastically different scaling needs, or when independent deployability and fault isolation become critical business needs.

The most important anti-pattern is jumping to microservices prematurely because it sounds modern. The 'Monolith First' approach — starting with a well-structured monolith and extracting services when there's a clear need — is often the right strategy."

---

### Q2: "What is an API Gateway and why is it important in a microservices architecture?"

**Model Answer:**

"An API Gateway is the single entry point for all client requests into a microservices system. Without it, clients would need to know the address of every individual service, handle authentication for each service call, and manage rate limiting themselves — that's messy and insecure.

The gateway centralizes cross-cutting concerns: authentication (verify the JWT once, not in every service), rate limiting (enforce usage limits at the edge), SSL termination (handle HTTPS at the boundary, use HTTP internally), routing (map URL paths to the right service), logging (log every request in one place), and load balancing.

It also enables API composition — the gateway can call multiple services and aggregate responses into one, reducing round trips for the client.

The tradeoff is that the API Gateway is a critical piece of infrastructure — if it goes down, everything goes down. It needs to be highly available, horizontally scalable, and carefully monitored. You'd typically run multiple instances behind a load balancer."

---

### Q3: "Explain the Circuit Breaker pattern. What problem does it solve?"

**Model Answer:**

"The Circuit Breaker pattern prevents cascading failures in a distributed system. Without it, if Service B starts failing, every call from Service A to B will hang waiting for a timeout. If thousands of requests are in flight, thousands of threads hang in Service A. Service A becomes unresponsive. Services calling Service A also start failing. One failing service takes down the whole system.

The Circuit Breaker wraps calls to Service B. In the Closed state, requests flow normally and failures are counted. When the failure rate exceeds a threshold, the circuit Opens — for a timeout period, all calls to Service B are immediately rejected without actually making the call. This gives Service B time to recover and prevents Service A from accumulating hung threads.

After the timeout, the circuit moves to Half-Open and allows a few test requests through. If they succeed, the circuit Closes. If they fail, it Opens again.

From a user experience perspective, you can pair this with a fallback — instead of hanging, return a cached result, a default response, or a 'service temporarily unavailable' message. Users get a degraded but functional experience rather than a hung request."

---

### Q4: "How do you handle distributed transactions in microservices? What is the Saga pattern?"

**Model Answer:**

"Distributed transactions are one of the hardest problems in microservices because you can't use a single database transaction across services. The traditional solution, Two-Phase Commit, is blocking and fragile and generally avoided in microservices.

The Saga pattern handles this by breaking a distributed transaction into a sequence of local transactions, with compensating transactions to handle failures. If step 3 fails, compensating transactions undo steps 1 and 2.

There are two implementation styles. In **choreography**, services communicate via events — each service publishes an event after completing its step, and the next service reacts to that event. No central coordinator. It's loosely coupled but the overall flow is hard to follow and debug.

In **orchestration**, a central Saga Orchestrator explicitly coordinates the steps — it calls Service A, waits for success, then calls Service B, and so on. If something fails, the orchestrator calls compensating transactions. The flow is visible and easy to understand, but the orchestrator is a central point of failure and risk.

For complex flows with many compensating steps, orchestration is easier to manage. For simple, linear flows with loose coupling requirements, choreography works well. In practice, I've seen orchestration used more often because the failure handling logic is much clearer."

---

### Q5: "What is Service Discovery and how does it work in Kubernetes?"

**Model Answer:**

"Service Discovery is the mechanism by which services find each other's network locations in a dynamic environment. In microservices, service instances start and stop constantly due to scaling and deployments, so hardcoding IP addresses is not feasible.

Services register themselves with a **Service Registry** — a phone book that maps service names to their current network addresses. When Service A wants to call Service B, it queries the registry for B's address.

There are two models: **client-side discovery**, where the calling service queries the registry and does its own load balancing; and **server-side discovery**, where the client sends requests to a load balancer or router that queries the registry internally.

In **Kubernetes**, service discovery is built in and uses the server-side model. Every Kubernetes Service gets a stable DNS name — like `payment-service.default.svc.cluster.local`. The calling service just uses this DNS name without knowing which pods are behind it. Kubernetes' internal DNS server resolves the name, and kube-proxy routes the request to a healthy pod using load balancing. When pods crash or scale, Kubernetes updates the routing automatically and the DNS name remains stable. The calling service never needs to know anything changed."

---

*Day 19 Complete. Next: Day 20 — Message Queues: Kafka, RabbitMQ, Async Communication*
