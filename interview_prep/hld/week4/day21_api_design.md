# Week 4 - Day 21: REST API Design Best Practices
# Topic: Building APIs That Don't Make Developers Cry

---

## What is an API and Why Does It Exist?

API stands for **Application Programming Interface**.

That sounds intimidating. Let's break it down with a real-world analogy.

### The Electrical Socket Analogy

Think about an **electrical socket** in your wall.

You don't know — or care — what's happening behind the wall. There are wires,
circuits, transformers, power stations, and thousands of kilometers of infrastructure.
But you don't think about any of that. You just plug your phone charger in and
your phone charges.

The socket is the **interface**. It has a **standard shape** and **standard behavior**:
- Two holes (or three, depending on country)
- Delivers electricity at a fixed voltage
- Any device that follows that standard can plug in

This is exactly what an API is.

Your application is the power station. The API is the socket. Any other application —
mobile app, web frontend, third-party service — that follows your API's rules can
"plug in" and use your data or functionality. They don't need to know how your database
is structured, what language your server uses, or how your business logic works.
They just need to know the socket shape: the URL, the method, the format.

**Why this matters in interviews:**
Interviewers want to know if you understand that APIs are contracts between systems.
Breaking a contract (changing an API without versioning) is like suddenly making your
socket a different shape — every device that was plugged in stops working.

---

## The 6 REST Constraints — Explained Simply

REST (Representational State Transfer) is not a protocol or a standard. It is a set
of **architectural constraints** defined by Roy Fielding in his 2000 PhD dissertation.
An API is "RESTful" only if it follows all 6 constraints.

### Constraint 1: Stateless

**What it means:** Every request from a client to the server must contain ALL the
information needed to understand that request. The server must not store any session
state about the client between requests.

**Real-world analogy:** Think of ordering food at a restaurant using numbered tokens.
Every time you approach the counter to ask "is my food ready?", you must show your
token number. The staff does not remember your face. They do not remember what you
ordered. Your token contains everything they need. If you forget your token, they
cannot help you.

**In practice:** Instead of storing "user is logged in" on the server, the client sends
an authentication token (like a JWT) with every single request. The server reads that
token, validates it, and knows who you are — all from that one request. No memory needed.

**Why it matters:** Stateless servers are easy to scale. You can run 10 identical servers
behind a load balancer and any server can handle any request because no server holds
state. If servers held state, users would need to always hit the same server — called
"sticky sessions" — which is a scaling nightmare.

---

### Constraint 2: Client-Server

**What it means:** The client (your web browser, your mobile app) and the server
(your backend) are completely separate. The client handles the user interface. The
server handles data storage and business logic. Neither should do the other's job.

**Real-world analogy:** Think of a restaurant. The kitchen (server) handles cooking.
The waiter (interface) handles serving customers. The customer (client) handles eating.
The kitchen doesn't come to the table. The customer doesn't go into the kitchen.
Separation of concerns.

**Why it matters:** You can change your frontend completely — rewrite it in React,
build a mobile app, build a desktop app — without touching your backend. You can
also scale your backend independently of your frontend. This separation is what makes
modern microservices possible.

---

### Constraint 3: Cacheable

**What it means:** Responses from the server must label themselves as either cacheable
or non-cacheable. When a response is cacheable, the client (or an intermediary like
a CDN) can reuse that response instead of making another request.

**Real-world analogy:** Imagine calling your bank's customer service line and asking
"what is the current exchange rate for USD to INR?" The agent tells you the rate, and
adds "this rate is valid for the next 1 hour." You don't need to call back for 1 hour.
You have a cached answer.

**In practice:** A REST API returns an HTTP header like:
```
Cache-Control: max-age=3600
```
This tells the browser, CDN, or proxy: "This response is fresh for 3600 seconds.
Don't ask me again until then."

**Why it matters:** Caching reduces load on your servers dramatically. A product catalog
page that 10,000 users request every minute doesn't need 10,000 database queries per
minute if the response is cached for 60 seconds.

---

### Constraint 4: Uniform Interface

**What it means:** All interactions between client and server follow a consistent,
standardized interface. There are 4 sub-constraints here:
1. **Resource identification** — Every resource has a unique URL (URI)
2. **Manipulation through representations** — Clients interact with resources through
   JSON/XML representations, not directly with the database
3. **Self-descriptive messages** — Each message has enough information to describe
   how to process it (HTTP method, Content-Type header, etc.)
4. **HATEOAS** — Responses include links to related actions (Hypermedia As The Engine
   Of Application State — rarely enforced in practice but theoretically important)

**Real-world analogy:** Think of how every ATM in the world works the same way.
Insert card → enter PIN → choose action → get money. Whether you're in Tokyo or
Mumbai, the interface is uniform. You don't need a different skill set for each ATM.

**Why it matters:** A uniform interface means any client can talk to any RESTful server
without custom integration code. Your mobile app team doesn't need special knowledge
about your server — they just need to know REST conventions.

---

### Constraint 5: Layered System

**What it means:** The client should not know whether it's talking directly to the
final server or to an intermediary (load balancer, API gateway, cache server, CDN).
Each layer only knows about the adjacent layers.

**Real-world analogy:** When you order food on Swiggy, you don't know if your order
is being processed by a load balancer, routed through a gateway, checked by a fraud
detection service, and then sent to the restaurant. You just placed an order and
it arrived. All those layers are invisible to you.

**In practice:**
```
Client → CDN → API Gateway → Load Balancer → App Server → Database
```
The client talks only to the CDN. The CDN talks to the API Gateway. Neither the
client nor the CDN knows what's behind the Gateway.

**Why it matters:** You can add security layers, caching layers, or logging layers
without clients knowing. This is what makes modern cloud architectures possible.

---

### Constraint 6: Code on Demand (Optional)

**What it means:** Servers can optionally send executable code to clients. The most
common example is JavaScript sent from a server to be executed in a browser.

**Real-world analogy:** It's like a business sending you a form to fill out. Instead
of you calling them for every field, they gave you the form (code) that handles the
interaction locally.

**Why it matters:** This is the only **optional** constraint. Most REST APIs don't use
it explicitly, but understanding it shows architectural depth in an interview.

---

## HTTP Methods — The Verbs of REST

Every REST request uses an HTTP method. These are the "what action am I performing"
part of a request.

Think of a file cabinet in an office:
- GET = Read a file
- POST = Create a new file and put it in
- PUT = Replace an entire file with a new version
- PATCH = Make changes to specific sections of a file
- DELETE = Shred and remove a file

### GET — Read / Retrieve

Use when: You want to retrieve a resource without modifying anything.

```
GET /users/123          → Fetch user with ID 123
GET /products           → Fetch all products
GET /orders/456/items   → Fetch all items in order 456
```

Rules:
- Must be safe (should not change server state)
- Must be idempotent (calling it 10 times gives the same result as calling it once)
- Never put sensitive data in the URL — it gets logged in server logs and browser history
- Should never have a request body (technically allowed but bad practice)

---

### POST — Create

Use when: You want to create a new resource. The server determines the new resource's ID.

```
POST /users             → Create a new user
POST /orders            → Place a new order
POST /users/123/uploads → Upload a file for user 123
```

Rules:
- Not idempotent — calling POST twice creates two resources
- Returns `201 Created` with a `Location` header pointing to the new resource
- Body contains the data for the new resource
- Can also be used for operations that don't fit GET/PUT/PATCH/DELETE
  (e.g., `POST /payments/charge`)

---

### PUT — Replace (Full Update)

Use when: You want to replace an entire resource with a new version. You're sending
the complete representation.

```
PUT /users/123          → Replace user 123 with the provided data
PUT /products/456       → Replace product 456 entirely
```

Rules:
- Idempotent — calling PUT 10 times with the same data is the same as calling it once
- The body must contain the COMPLETE resource
- If a field is missing from the body, it may be set to null or default
- Returns `200 OK` or `204 No Content`

**PATCH vs PUT — The Key Difference:**
- PUT: "Here is the complete new version of this user. Replace everything."
- PATCH: "Here is just the email address. Update only that field."

Use PUT when you always send the complete object. Use PATCH for partial updates.

---

### PATCH — Partial Update

Use when: You want to update one or a few fields without sending the entire object.

```
PATCH /users/123        → Update only the fields provided (e.g., just the email)
PATCH /orders/456       → Update order status only
```

```json
PATCH /users/123
{
  "email": "newemail@example.com"
}
```
Only the email changes. Everything else stays the same.

Rules:
- Not necessarily idempotent (depends on implementation)
- More efficient than PUT for large objects where you only change one field
- Returns `200 OK` with updated resource or `204 No Content`

---

### DELETE — Remove

Use when: You want to remove a resource permanently (or soft-delete it).

```
DELETE /users/123        → Delete user 123
DELETE /orders/456       → Delete order 456
```

Rules:
- Idempotent — deleting something that's already deleted should return `404` or `200`
  (debated, but calling DELETE 10 times should not cause errors after the first success)
- Returns `200 OK`, `204 No Content`, or `404 Not Found`
- Consider soft-delete: mark as deleted rather than physically removing (set deleted_at)

---

## Resource Naming — The Art of Clean URLs

Good resource naming makes your API self-documenting. A developer can read the URL
and immediately understand what it does. Bad naming creates confusion and support tickets.

### Rule 1: Use Nouns, Not Verbs

The HTTP method IS the verb. The URL should be a noun (a thing, not an action).

| Bad (verb in URL)           | Good (noun, method is the verb)    |
|-----------------------------|------------------------------------|
| GET /getUsers               | GET /users                         |
| POST /createOrder           | POST /orders                       |
| DELETE /deleteProduct/123   | DELETE /products/123               |
| POST /updateUser/123        | PATCH /users/123                   |
| GET /fetchUserOrders/123    | GET /users/123/orders              |

**Why:** The URL describes what you're working with. The HTTP method describes what
you're doing with it. Mixing them creates redundancy and inconsistency.

---

### Rule 2: Use Hierarchical URLs for Relationships

When a resource belongs to another resource, express that in the URL structure.

```
/users                      → All users
/users/123                  → Specific user
/users/123/orders           → All orders belonging to user 123
/users/123/orders/456       → Specific order belonging to user 123
/users/123/orders/456/items → All items in that specific order
```

**Analogy:** Think of a file system. `/users/123/orders/456` is like navigating a
folder structure: Users folder → User 123 folder → Orders folder → Order 456 file.

**Rule of thumb:** Don't go deeper than 2-3 levels. If you find yourself writing
`/users/123/orders/456/items/789/reviews/abc`, consider flattening.
`/reviews/abc` with a filter `?order_item_id=789` might be cleaner.

---

### Rule 3: Use Plural Nouns Consistently

Always use plural. The confusion of "is it /user or /users?" is eliminated when
you commit to always plural.

```
/users         not /user
/products      not /product
/orders        not /order
```

Even for single resources: `GET /users/123` — still using `/users` plural.

---

### Rule 4: Use Lowercase and Hyphens

```
Good:  /user-profiles
Bad:   /userProfiles       (camelCase in URLs is inconsistent)
Bad:   /user_profiles      (underscores are less readable)
Bad:   /User-Profiles      (uppercase is ugly)
```

---

### Rule 5: Never Use File Extensions

```
Bad:  /users.json
Bad:  /products.xml
Good: /users  (use Accept header for format negotiation)
```

---

## HTTP Status Codes — The Language of Responses

Status codes are how the server communicates what happened. Think of them like
the expressions on a waiter's face after you place an order:
- 200-299: "Yes, done, here you go!" (Success)
- 300-399: "It's over there now, let me redirect you" (Redirection)
- 400-499: "You made a mistake" (Client error)
- 500-599: "We made a mistake" (Server error)

### 2xx — Success

**200 OK**
The generic success response. Use for successful GET, PUT, PATCH requests.
```
GET /users/123 → 200 OK (user found, returned in body)
PATCH /users/123 → 200 OK (updated, new state returned in body)
```

**201 Created**
Use ONLY when something new was created (POST). Must include a `Location` header.
```
POST /users → 201 Created
Location: /users/456
Body: { "id": 456, "name": "Ajmal" }
```

**204 No Content**
Success, but no body to return. Use for DELETE and PUT/PATCH when you don't need
to return the updated resource.
```
DELETE /users/123 → 204 No Content
```

---

### 4xx — Client Errors (The Client Did Something Wrong)

**400 Bad Request**
The request is malformed. Missing required fields, wrong data type, invalid JSON.
```
POST /users with body: { "name": 123, "email": "notanemail" }
→ 400 Bad Request
```

**401 Unauthorized**
"You are not authenticated." The client didn't provide credentials, or the
credentials are invalid/expired.
```
GET /users/123 with no token → 401 Unauthorized
```
The name is misleading — "Unauthorized" really means "Unauthenticated."

**403 Forbidden**
"You are authenticated but not authorized." We know who you are, but you don't
have permission.
```
Regular user trying to DELETE /admin/users/456 → 403 Forbidden
```

**401 vs 403 — The classic interview question:**
- 401: "Who are you? Please log in."
- 403: "I know who you are. You cannot do this."

**404 Not Found**
The resource does not exist.
```
GET /users/999 (user 999 doesn't exist) → 404 Not Found
```

**409 Conflict**
The request conflicts with the current state of the server.
```
POST /users with email that already exists → 409 Conflict
PUT /orders/123 with outdated version (optimistic locking conflict) → 409 Conflict
```

**422 Unprocessable Entity**
The request is well-formed (valid JSON) but semantically wrong. Validation failed.
```
POST /users with valid JSON but: age = -5, or: end_date < start_date
→ 422 Unprocessable Entity
```
**400 vs 422:**
- 400: The request body isn't even valid JSON, or a required field is missing entirely
- 422: The JSON is valid, but the values don't make logical sense

**429 Too Many Requests**
Rate limit exceeded. The client is sending too many requests.
```
→ 429 Too Many Requests
Retry-After: 60
```

---

### 5xx — Server Errors (The Server Did Something Wrong)

**500 Internal Server Error**
Something went wrong on the server that wasn't anticipated. A bug, an unhandled
exception. The catch-all server error.
```
Unhandled NullPointerException in your code → 500 Internal Server Error
```

**502 Bad Gateway**
Your server is working, but a service it depends on returned an invalid response.
```
Your API gateway couldn't get a valid response from the upstream app server → 502
```

**503 Service Unavailable**
The server is temporarily unable to handle requests. Overloaded, or down for
maintenance.
```
→ 503 Service Unavailable
Retry-After: 120
```

---

## API Versioning — Handling Change Without Breaking Clients

Your API is a contract. Once clients depend on it, you cannot change it freely.
But software evolves. You need a way to introduce breaking changes without
destroying existing integrations.

Think of it like Windows releasing Windows 11 while still supporting Windows 10 for
years. Old users are not forced to upgrade immediately.

### Strategy 1: URL Path Versioning

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Pros:**
- Extremely visible and explicit — you can see the version in the URL
- Easy to test — just paste the URL in a browser
- Easy to route at the load balancer level
- Easy to document separately

**Cons:**
- URL is supposed to identify a resource, not a version
- Makes URLs longer
- You have to maintain multiple route trees in your code

**When to use:** Most practical choice for public APIs. Used by Stripe, Twilio, GitHub.

---

### Strategy 2: Header Versioning

```
GET /users
Accept-Version: v2
```
or
```
GET /users
Accept: application/vnd.example.v2+json
```

**Pros:**
- Clean URLs — the version doesn't pollute the resource path
- More "RESTfully correct" (URLs identify resources, not versions)

**Cons:**
- Invisible — you can't see the version by looking at the URL
- Hard to test directly in a browser
- Harder for beginners to discover and use
- Caching is trickier (caches must be aware of the version header)

**When to use:** Internal APIs where developers are sophisticated enough to use headers.

---

### Strategy 3: Query Parameter Versioning

```
GET /users?version=2
GET /users?v=2
```

**Pros:**
- Visible in URL (easier than headers to discover)
- Easy to test

**Cons:**
- Query params are supposed to be for filtering/sorting, not structural versioning
- Can be accidentally omitted
- Less clean than path versioning

**When to use:** Rarely preferred. Occasionally seen in third-party integrations.

---

### The Golden Rule of API Versioning

Make a version change ONLY for breaking changes:
- Removing a field
- Renaming a field
- Changing a field's type
- Changing the URL structure

Adding new optional fields, new endpoints, or new status codes are non-breaking
and do NOT require a new version.

---

## Pagination — Handling Large Datasets

When `GET /products` might return 10 million records, you cannot send them all at once.
You need pagination.

Think of a book. You don't read all pages simultaneously. You read page by page,
and the page number tells you where you are.

### Strategy 1: Offset-Based Pagination

```
GET /products?page=3&limit=20
GET /products?offset=40&limit=20
```

The server does: `SELECT * FROM products LIMIT 20 OFFSET 40`

**Response:**
```json
{
  "data": [...],
  "total": 10000,
  "page": 3,
  "limit": 20,
  "total_pages": 500
}
```

**Pros:**
- Simple to implement
- User can jump to any page directly ("go to page 50")
- Easy to display "Page 3 of 500"

**Cons:**
- **Slow for large datasets.** `OFFSET 100000 LIMIT 20` means the database reads
  100,020 rows and discards the first 100,000. Enormously wasteful.
- **Inconsistent results.** If a new product is inserted on page 1 while you're
  on page 3, page 4 will show you a record you already saw (pages shift).

---

### Strategy 2: Cursor-Based Pagination (Keyset Pagination)

Instead of a page number, use a pointer (cursor) to the last item you saw.

```
GET /products?limit=20&cursor=eyJpZCI6MTAwfQ==
```

The cursor is a Base64-encoded value of the last record's key (e.g., `{"id": 100}`).

The server does: `SELECT * FROM products WHERE id > 100 LIMIT 20`

**Response:**
```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTIwfQ==",
  "has_more": true
}
```

**Pros:**
- Extremely fast — uses an index scan starting from a known position, no row skipping
- Consistent — new inserts don't affect your current page (you won't miss or repeat records)
- Works perfectly for infinite scroll (Instagram, Twitter feed)

**Cons:**
- Cannot jump to an arbitrary page ("go to page 50" is impossible)
- More complex to implement
- Cursor must be decoded and validated

**When to use which:**
- Admin dashboards where users navigate by page number → Offset-based
- Social media feeds, activity logs, real-time data → Cursor-based
- Large datasets (millions of records) → Always cursor-based

---

## Filtering, Sorting, and Field Selection

### Filtering

Use query parameters for filtering. Keep it simple and intuitive.

```
GET /products?category=electronics&min_price=100&max_price=500
GET /users?status=active&city=bangalore
GET /orders?created_after=2024-01-01&status=pending
```

For complex filters, some APIs accept a filter object:
```
GET /products?filter[category]=electronics&filter[in_stock]=true
```

---

### Sorting

```
GET /products?sort=price                  → sort by price ascending
GET /products?sort=-price                 → sort by price descending (- prefix)
GET /products?sort=-created_at,name       → multiple sort fields
```

Or use explicit order params:
```
GET /products?sort_by=price&order=asc
```

---

### Field Selection (Sparse Fieldsets)

Sometimes clients only need a few fields. Sending the entire object wastes bandwidth.

```
GET /users?fields=id,name,email           → return only id, name, email
GET /products?fields=id,name,price        → skip description, images, etc.
```

This is especially important for mobile clients on slow networks.

---

## Error Response Format — Consistency is Kindness

Every error response should follow the same structure. Developers integrating
your API should never have to guess what shape an error response is in.

**Recommended error body:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request contains invalid fields.",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      },
      {
        "field": "age",
        "message": "Must be a positive integer"
      }
    ],
    "request_id": "req_abc123xyz",
    "documentation_url": "https://docs.example.com/errors/VALIDATION_FAILED"
  }
}
```

Key fields to include:
- **code**: A machine-readable string your clients can `switch` on in code
- **message**: A human-readable explanation
- **details**: Field-level validation errors (array)
- **request_id**: A unique ID so your support team can find this exact request in logs
- **documentation_url**: Link to more information (optional but great for DX)

**Never expose stack traces, SQL queries, or internal paths in error responses.**
These are security vulnerabilities.

---

## Rate Limiting — Protecting Your API

Rate limiting controls how many requests a client can make in a given time window.
Without it, one misbehaving client can bring down your entire API.

Think of a highway with a speed limit. The speed limit isn't there to be mean.
It's there so 10,000 cars can share the road without chaos.

### Common Algorithms

**Fixed Window:** Allow N requests per minute. Resets at the start of each minute.
Simple but has a "boundary burst" problem — a client can make 2N requests right
at the window boundary.

**Sliding Window:** Track requests over the last 60 seconds from now (not from
the start of the minute). Smoother but more complex.

**Token Bucket:** Each client has a bucket that refills at a fixed rate. Requests
consume tokens. When the bucket is empty, requests are rejected. Allows bursting
up to bucket capacity.

**Leaky Bucket:** Requests are processed at a fixed rate regardless of burst.
Good for smoothing traffic but can drop requests during bursts.

### Rate Limit Headers to Return

Always tell the client their current rate limit status so they can back off gracefully:

```
X-RateLimit-Limit: 1000          → Max requests allowed per window
X-RateLimit-Remaining: 847       → Requests remaining in current window
X-RateLimit-Reset: 1711929600    → Unix timestamp when the window resets
Retry-After: 60                  → Seconds to wait (only when 429 is returned)
```

When the limit is exceeded, return:
```
HTTP 429 Too Many Requests
Retry-After: 60
```

---

## API Security

### Authentication — Proving Who You Are

**API Keys**
A long random string issued to each client.
```
GET /products
X-API-Key: sk_live_abc123xyz789
```
Simple, but keys don't expire by themselves. If leaked, you must rotate them.
Best for: Server-to-server integrations.

**JWT Bearer Tokens (JSON Web Token)**
A signed token containing claims (user ID, role, expiry). The server can validate
the token without a database lookup because it's cryptographically signed.
```
GET /users/123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Best for: User-facing APIs. Token expires, so security is scoped.

**OAuth 2.0**
A delegation protocol. Allows a user to grant a third-party app access to their
data without giving that app their password. This is what powers "Login with Google."

Flow:
```
1. User clicks "Login with Google"
2. App redirects user to Google's authorization server
3. User logs in to Google and grants permission
4. Google redirects back with an authorization code
5. App exchanges the code for an access token
6. App uses the access token to call Google's API on behalf of the user
```
Best for: Any time a third party needs access to user data.

---

### Authorization — What You Are Allowed to Do

Authentication = Identity ("Who are you?")
Authorization = Permissions ("What can you do?")

Common patterns:
- **RBAC (Role-Based Access Control):** Users have roles (admin, user, moderator).
  Roles have permissions. Simple and common.
- **ABAC (Attribute-Based Access Control):** Permissions based on attributes
  of the user, resource, and environment. Flexible but complex.
- **Resource Ownership:** User can only access their own resources.
  `GET /users/123/orders` → verify the authenticated user IS user 123.

---

## Idempotency Keys — Safe Retries for POST

POST is not idempotent. If a client creates an order and the network drops before
they receive the response, they don't know if the order was created or not. If they
retry, they might create a duplicate order.

**Idempotency keys solve this.**

The client generates a unique key for the operation and sends it in a header:
```
POST /orders
Idempotency-Key: a47bd6c1-9f2e-4b3e-8a1d-5c2f9d1e3b7a

{
  "product_id": 42,
  "quantity": 1
}
```

The server:
1. Checks if this idempotency key was already processed
2. If yes: return the original response (don't create a duplicate)
3. If no: process the request, store the key and response, return response

The key is typically stored in Redis with a TTL of 24 hours.

**Real-world analogy:** It's like a check number on a paper check. Even if the same
check is submitted to the bank twice, the bank recognizes the duplicate check number
and only processes it once.

Stripe's API uses idempotency keys for all payment operations. This is a great
example to bring up in interviews.

---

## API Documentation — What Makes Great Docs

Bad API documentation is one of the most common reasons developers abandon an API.

### What Great Documentation Includes

**1. Quick Start Guide**
A developer should be able to make their first successful API call in under 5 minutes.
Show a complete example: authentication, request, response.

**2. Authentication Guide**
Step-by-step: how to get credentials, how to include them in requests, how to
refresh tokens.

**3. Endpoint Reference**
For every endpoint:
- HTTP method and URL
- Path parameters, query parameters, request body — all documented with types and
  whether they're required
- Example request (copy-paste ready)
- Example response (success AND common error cases)
- Possible status codes and what each means

**4. Error Code Reference**
A complete list of error codes with explanations and how to handle each.

**5. Rate Limit Documentation**
What the limits are, how to read the headers, what to do when you hit them.

**6. SDKs and Code Samples**
Ideally in multiple languages: Python, JavaScript, Java, Go. Developers copy-paste
from docs constantly.

**Tools:** Swagger/OpenAPI (auto-generates interactive docs from annotations),
Postman collections, Redoc, Stoplight.

---

## gRPC vs REST — When to Use Each

### REST
- Uses HTTP/1.1 (or HTTP/2)
- Data format: JSON (human-readable, but larger)
- Easy to test with curl, Postman, browser
- Widely understood by developers
- Great for public APIs, browser clients, mobile apps

### gRPC
- Uses HTTP/2 exclusively
- Data format: Protocol Buffers (binary — not human-readable, but 5-10x smaller and faster)
- Strongly typed: define your API in a `.proto` file, generate client/server code
- Supports streaming (server-side, client-side, bidirectional)
- Not easy to test without special tools (like grpcurl)
- Cannot be called from a browser directly without a proxy (grpc-web)

**When to use gRPC:**
- Internal microservice-to-microservice communication where performance matters
- You need streaming (real-time updates, large data transfer)
- You have strict latency requirements
- Your team controls both the client and server

**When to use REST:**
- Public-facing APIs
- Third-party integrations
- Browser or mobile clients
- Teams need simplicity and broad tooling support

**In a typical microservices architecture:**
- External clients → REST API (API Gateway)
- Internal services talking to each other → gRPC

**Interview one-liner:** "REST for external communication where developer experience
matters. gRPC for internal services where performance and type-safety matter."

---

## Interview Q&A

### Q1: What is the difference between PUT and PATCH?

**Answer:**
PUT replaces the entire resource with the provided data. If you send a PUT with
only 3 fields but the resource has 10 fields, the other 7 fields may be set to
null or removed. PUT requires the complete representation.

PATCH is a partial update. You send only the fields you want to change, and the
server updates only those fields. The other fields remain unchanged.

Use PUT when you always have the full object and want to replace it completely.
Use PATCH when you're doing surgical updates to one or two fields, or when sending
the full object would be expensive.

---

### Q2: What is the difference between 401 and 403?

**Answer:**
401 Unauthorized means the request lacks valid authentication credentials. The user
is not logged in, or their token has expired. The message is: "I don't know who you
are. Please authenticate."

403 Forbidden means the request is authenticated but the authenticated user does
not have permission to perform this action. The message is: "I know who you are,
and you are not allowed to do this."

Example: A regular user tries to access the admin panel. They are logged in (401
does not apply), but they don't have the admin role (403 applies).

---

### Q3: How would you handle API versioning in a large system?

**Answer:**
I would use URL path versioning (`/v1/users`, `/v2/users`) for its simplicity,
visibility, and ease of routing. When introducing a new version:

1. Define what constitutes a breaking change: removing fields, renaming fields,
   changing field types, changing URL structure
2. Additive changes (new optional fields, new endpoints) do not require a new version
3. Maintain the old version for a deprecation period (typically 6-12 months)
4. Send `Deprecation` and `Sunset` headers on old version responses to warn clients
5. Document the migration guide from v1 to v2

I would avoid query parameter versioning because it's easy to accidentally omit,
and header versioning because it makes debugging and testing harder.

---

### Q4: How does cursor-based pagination work and why is it better than offset for large datasets?

**Answer:**
Cursor-based pagination uses a pointer — the cursor — to the last item seen, instead
of a page number. The cursor encodes the position of the last record, typically the
ID or timestamp of the last item returned.

When the client asks for the next page, they send the cursor. The server runs a query
like `WHERE id > {cursor_id} LIMIT 20`, which uses the database index efficiently.
It does not need to skip any rows.

Offset-based pagination does `OFFSET 100000 LIMIT 20`, which forces the database
to read 100,020 rows just to discard the first 100,000. This is O(N) work that
grows with the offset value.

Cursor-based is also more consistent: if new records are inserted during pagination,
offset-based will show duplicates or skip records (because all pages shift by one).
Cursor-based is immune to this because it works relative to a fixed reference point.

The downside of cursor-based is you cannot jump to an arbitrary page — you can only
go to the next or previous page.

---

### Q5: What is an idempotency key and when would you use it?

**Answer:**
An idempotency key is a unique identifier (usually a UUID) that the client generates
and attaches to a non-idempotent request (typically POST). It allows the client to
safely retry a request in case of a network failure without creating duplicate resources.

The server stores the idempotency key and the result of the operation. If the same
key arrives again within the TTL window, the server returns the stored result without
re-executing the operation.

This is critical for payment APIs. If a user clicks "Pay" and their network drops,
we don't know if the charge went through. With an idempotency key, the client can
retry confidently. If the payment was already processed, the server returns the
original payment confirmation. If it wasn't, it processes it now. Either way, the
user is charged exactly once.

Stripe requires idempotency keys for all POST requests. I would implement them
anywhere the consequence of a duplicate operation is significant: payments, order
creation, ticket booking.

---

## Practice: Design the REST API for a Hotel Booking System

### Requirements
- Users can search for available hotels by location, check-in date, check-out date
- Users can view hotel details and available rooms
- Users can book a room
- Users can view and cancel their bookings
- Admins can add/update/remove hotels and rooms

---

### API Endpoints

#### Hotels

```
GET    /v1/hotels
       Query params: ?city=bangalore&check_in=2024-12-01&check_out=2024-12-05&guests=2&sort=-rating&page=1&limit=20
       Response: 200 OK — list of hotels with availability and base price

GET    /v1/hotels/{hotel_id}
       Response: 200 OK — full hotel details (amenities, photos, policies)
       Response: 404 Not Found — hotel doesn't exist

POST   /v1/hotels
       Auth: Admin only
       Body: { name, address, city, star_rating, amenities, policies }
       Response: 201 Created + Location: /v1/hotels/789

PUT    /v1/hotels/{hotel_id}
       Auth: Admin only
       Body: Complete hotel object
       Response: 200 OK or 404 Not Found

DELETE /v1/hotels/{hotel_id}
       Auth: Admin only
       Response: 204 No Content or 404 Not Found
```

#### Rooms

```
GET    /v1/hotels/{hotel_id}/rooms
       Query params: ?check_in=2024-12-01&check_out=2024-12-05&type=deluxe
       Response: 200 OK — list of available rooms with price

GET    /v1/hotels/{hotel_id}/rooms/{room_id}
       Response: 200 OK — room details, availability calendar

POST   /v1/hotels/{hotel_id}/rooms
       Auth: Admin only
       Body: { room_number, type, capacity, price_per_night, amenities }
       Response: 201 Created

PATCH  /v1/hotels/{hotel_id}/rooms/{room_id}
       Auth: Admin only
       Body: { price_per_night: 4500 }
       Response: 200 OK
```

#### Bookings

```
POST   /v1/bookings
       Auth: User
       Idempotency-Key: <uuid>
       Body: {
         hotel_id: 123,
         room_id: 456,
         check_in: "2024-12-01",
         check_out: "2024-12-05",
         guests: 2,
         guest_details: { name, phone, email }
       }
       Response: 201 Created
       Body: {
         booking_id: "BK-78901",
         status: "confirmed",
         total_price: 18000,
         confirmation_code: "HB-ABC123"
       }
       Error: 409 Conflict — room is no longer available
       Error: 422 Unprocessable Entity — check_out must be after check_in

GET    /v1/bookings
       Auth: User (their own) or Admin (all)
       Query params: ?status=confirmed&from=2024-01-01
       Response: 200 OK — paginated list of bookings

GET    /v1/bookings/{booking_id}
       Auth: User (their own) or Admin
       Response: 200 OK — full booking details
       Response: 403 Forbidden — not their booking
       Response: 404 Not Found

PATCH  /v1/bookings/{booking_id}/cancel
       Auth: User (their own) or Admin
       Body: { reason: "change of plans" }
       Response: 200 OK — { status: "cancelled", refund_amount: 15000 }
       Error: 409 Conflict — booking already cancelled or past check-in date
```

#### Users

```
POST   /v1/auth/register
       Body: { name, email, password }
       Response: 201 Created

POST   /v1/auth/login
       Body: { email, password }
       Response: 200 OK — { access_token, refresh_token, expires_in }

POST   /v1/auth/refresh
       Body: { refresh_token }
       Response: 200 OK — { access_token, expires_in }

GET    /v1/users/me
       Auth: Bearer token
       Response: 200 OK — current user's profile

GET    /v1/users/me/bookings
       Auth: Bearer token
       Response: 200 OK — all bookings for current user
```

---

### Sample Error Response

```json
HTTP 409 Conflict

{
  "error": {
    "code": "ROOM_NOT_AVAILABLE",
    "message": "The requested room is no longer available for the selected dates.",
    "details": {
      "room_id": 456,
      "requested_dates": {
        "check_in": "2024-12-01",
        "check_out": "2024-12-05"
      }
    },
    "request_id": "req_9f3k2m1p",
    "documentation_url": "https://docs.hotelbooking.com/errors/ROOM_NOT_AVAILABLE"
  }
}
```

---

### Key Design Decisions to Mention in Interview

1. **Idempotency key on POST /bookings** — prevents double-booking if network fails
2. **PATCH /bookings/{id}/cancel instead of DELETE** — cancellation is a state change,
   not a deletion. Booking history must be preserved. DELETE implies removal.
3. **409 for room availability conflict** — not 400, because the request is valid but
   conflicts with current resource state
4. **Separate /users/me/bookings endpoint** — shortcut that avoids exposing the user's
   ID in the URL, safer and more convenient for mobile apps
5. **Idempotency-Key header on booking creation** — critical because a double-booking
   is a serious business problem
