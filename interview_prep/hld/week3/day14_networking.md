# Week 3 - Day 14: Networking Basics
# Topic: DNS, CDN, Load Balancer, Reverse Proxy, API Gateway

---

## Why Networking Knowledge Matters in HLD Interviews

In almost every HLD interview, you will draw a diagram with boxes representing components.
Between those boxes are arrows. Those arrows are not magic — they represent real
networking infrastructure that makes large-scale systems function.

When you say "the client sends a request to the server," an interviewer is silently
asking: "But how does the client find the server? What if the server is overloaded?
What if a hacker sends 10,000 requests per second? Who terminates the SSL? Who
authenticates the request before it even reaches your service?"

Today's components answer all of those questions.

By the end of this day, you will be able to explain the networking layer of
any large system — and that explanation is what separates a junior-level answer
from a senior-level answer.

---

## Section 1: DNS — The Phone Book of the Internet

### The Problem DNS Solves

Computers do not understand names like `www.google.com`.
They understand IP addresses like `142.250.195.68`.

An IP address is a unique numerical label assigned to every device connected
to the internet. Think of it like a home address — precise, unambiguous,
machine-readable. But nobody wants to memorize `142.250.195.68` every time
they want to use Google.

DNS is the system that bridges this gap.

### The Phone Book Analogy

Before smartphones, people had physical phone books.
You look up "Sharma, Priya" and find the number `+91-98765-43210`.
You did not memorize the number — you memorized the name and used the book to get the number.

DNS works identically:
- **Domain name** (`www.google.com`) = the person's name in the phone book
- **IP address** (`142.250.195.68`) = the phone number
- **DNS Server** = the phone book itself

### How DNS Resolution Works — Step by Step

When you type `www.amazon.com` and press Enter:

```
Step 1: Browser Cache Check
Your browser first checks its own cache.
Did I resolve this domain recently? If yes, use the cached IP. Skip all other steps.

Step 2: Operating System Cache Check
Browser asks the OS: "Do you have this?"
The OS checks its own DNS cache (and the hosts file).
If found, return it. If not, continue.

Step 3: Recursive Resolver (Your ISP)
The OS contacts your ISP's Recursive DNS Resolver.
Think of this resolver as a researcher who will do all the legwork for you.
It's also called a Recursive Resolver or DNS Recursor.

Step 4: Root Name Server
The Recursive Resolver contacts a Root Name Server.
There are 13 sets of root servers globally (operated by ICANN, Verisign, etc.).
The root server says: "I don't know amazon.com specifically, but .com domains
are handled by these TLD servers."

Step 5: TLD (Top-Level Domain) Name Server
The Recursive Resolver contacts the .com TLD name server.
The TLD server says: "I don't know the exact IP either, but Amazon's authoritative
name server is ns1.amazon.com."

Step 6: Authoritative Name Server
The Recursive Resolver contacts Amazon's authoritative name server.
THIS server knows the actual IP address. It responds: "www.amazon.com = 52.94.236.248"

Step 7: Response Returned
The Recursive Resolver returns the IP to your OS.
The OS returns it to the browser.
The browser caches it.
The browser now connects to 52.94.236.248.
```

Visually:

```
Browser
  |
  | (cache miss)
  v
OS Cache
  |
  | (cache miss)
  v
ISP Recursive Resolver
  |
  |---> Root Name Server:   "Who handles .com?"
  |<--- Root Name Server:   "TLD Server at a.gtld-servers.net"
  |
  |---> TLD Name Server:    "Who handles amazon.com?"
  |<--- TLD Name Server:    "ns1.amazon.com"
  |
  |---> Authoritative NS:   "What is www.amazon.com?"
  |<--- Authoritative NS:   "52.94.236.248"
  |
  v
Browser now connects to 52.94.236.248
```

### DNS Record Types

Not all DNS records are IP addresses. There are different types for different purposes:

| Record Type | Purpose | Example |
|---|---|---|
| **A** | Maps domain to IPv4 address | `google.com -> 142.250.195.68` |
| **AAAA** | Maps domain to IPv6 address | `google.com -> 2607:f8b0::200e` |
| **CNAME** | Alias — points one domain to another domain | `www.google.com -> google.com` |
| **MX** | Mail server for this domain | `gmail.com -> smtp.google.com` |
| **TXT** | Arbitrary text (verification, SPF, etc.) | `"v=spf1 include:google.com"` |
| **NS** | Authoritative name servers for this domain | `amazon.com -> ns1.amazon.com` |

In interviews, A, CNAME, and MX come up most often.

### DNS Caching and TTL

DNS results are cached at every level (browser, OS, ISP resolver) to avoid
repeating this expensive lookup chain on every single request.

**TTL (Time To Live)** is a number (in seconds) that tells each cache:
"You can use this DNS record for this many seconds. After that, throw it away
and re-fetch the latest version."

Set by the domain owner in the authoritative DNS server.

```
amazon.com A record:
  IP: 52.94.236.248
  TTL: 300  (= 5 minutes — re-check every 5 minutes)

github.com A record:
  IP: 140.82.121.4
  TTL: 3600 (= 1 hour — re-check every hour)
```

**Why this matters in design:**

- **High TTL (hours/days)**: fewer DNS queries, faster for users, but changes take time to propagate.
  If Amazon changes their server IP, users who have the old IP cached will fail for up to the TTL duration.

- **Low TTL (seconds/minutes)**: changes propagate quickly, but more DNS traffic and slightly slower
  for users who don't have a cached result.

**Interview insight:** When doing a major migration (changing servers, moving regions),
engineers lower the TTL days in advance (e.g., from 86400 to 60 seconds) so they can
switch DNS records quickly and have the change propagate within minutes, not days.

### DNS as a Traffic Management Tool

DNS is not only about resolving names to IPs. It is also used to:

- **Geographic routing**: return different IPs to users in different countries
  (India users get Mumbai servers, US users get Virginia servers)
- **Failover**: if the primary IP stops responding, DNS health checks switch to a backup IP
- **Load balancing**: return multiple IPs in rotation (Round Robin DNS)

Services like **AWS Route 53** and **Cloudflare DNS** offer all of these features.

---

## Section 2: CDN — The Global Warehouse Network

### The Problem CDN Solves

Imagine your servers are in Mumbai. A user in New York visits your website.
Their request travels ~13,500 km to Mumbai and back — at the speed of light
through undersea fiber cables, this takes ~130-170 milliseconds for the round trip.

Now imagine your website has images, CSS files, JavaScript bundles, and video content.
Every single one of those files makes a round trip to Mumbai.
The page feels slow, laggy, and frustrating.

A CDN solves this by **bringing your content closer to your users.**

### The Warehouse Analogy

Imagine a book publisher in Delhi.
When someone in Chennai, Kolkata, or Mumbai orders a book, it ships from Delhi
and arrives in 5-7 days.

The publisher's logistics team gets smart: they create regional warehouses.
- Warehouse in Chennai
- Warehouse in Kolkata
- Warehouse in Mumbai

Popular books are stocked in all regional warehouses.
When a customer in Chennai orders, the book ships from the Chennai warehouse
and arrives the same day.

The CDN is exactly this. Your origin server (Delhi publisher) holds the
master copy. CDN **edge servers** (regional warehouses) hold copies of
your static content, positioned close to your users around the world.

### How a CDN Works

```
Origin Server (Mumbai)
        |
        |  CDN pre-pulls (or lazily caches) content
        |
   +----+----+----+----+
   |    |    |    |    |
   v    v    v    v    v
Edge  Edge  Edge  Edge  Edge
(NY)  (LA) (London)(Singapore)(Sydney)

When user in London requests your logo:
  User --> CDN Edge Server (London) --> Returns logo in ~10ms
  [NOT: User --> Mumbai server --> ~200ms]
```

### CDN Request Flow in Detail

**First request (cache miss):**
```
1. User in London requests: cdn.myapp.com/images/logo.png
2. London edge server checks its cache: NOT FOUND
3. Edge server fetches from origin (Mumbai): logo.png
4. Edge server caches the file locally with a TTL (e.g., 24 hours)
5. Edge server returns the file to the user
```

**Subsequent requests (cache hit):**
```
1. Another user in London requests: cdn.myapp.com/images/logo.png
2. London edge server checks its cache: FOUND (cached)
3. Returns immediately from London cache — no origin fetch needed
4. Response time: ~5-20ms instead of ~200ms
```

### What CDNs Cache (and What They Don't)

**CDN is great for static, rarely-changing content:**
- Images (JPEG, PNG, WebP, SVG)
- CSS and JavaScript files
- Fonts
- Video files
- HTML files (if content doesn't change per user)
- Software downloads

**CDN is NOT suitable for:**
- Dynamic, personalised content (your specific user feed, your shopping cart)
- Real-time data (live stock prices, live sports scores)
- Anything that must be different per user per request

### Cache Invalidation — The Hard Problem

What if you deploy a new version of your JavaScript file?
The old version is cached on 200 edge servers globally.
Users will see the old version until the TTL expires.

**Solution 1: Long TTL + URL versioning**
```
# Old file
cdn.myapp.com/app.js           (TTL: 365 days)

# New deployment — new filename includes hash
cdn.myapp.com/app.a3f9c2.js    (TTL: 365 days)
```
The HTML references the new filename. Browsers fetch the new file because the URL changed.
The old file can stay cached (harmless, it's just never referenced again).

**Solution 2: Purge the CDN cache**
Most CDN providers (Cloudflare, AWS CloudFront) offer a Cache Purge API.
Your CI/CD pipeline calls this API on every deployment.
Forces all edge servers to discard their cached copies and re-fetch from origin.

**Interview tip:** When a candidate designs a system with a CDN, a sharp interviewer
will ask "how do you handle cache invalidation?" This is one of the two hardest
problems in computer science. Have an answer ready.

### CDN Providers

- **Cloudflare**: the most widely used globally
- **AWS CloudFront**: integrates deeply with AWS infrastructure
- **Akamai**: enterprise-grade, used by major banks and governments
- **Fastly**: popular with startups, strong real-time purging capabilities

---

## Section 3: Load Balancer — The Traffic Police

### The Problem Load Balancers Solve

Your application is a hit. Traffic grows from 100 requests/second to 50,000 requests/second.
You spin up 20 servers to handle the load.

But how do users' requests get distributed across those 20 servers?
If all traffic still goes to Server 1, you have 19 idle servers and one dead one.

A **Load Balancer** sits in front of all your servers and distributes incoming
requests across them intelligently.

### The Traffic Police Analogy

Imagine a busy intersection with 8 lanes of traffic merging from a highway.
Without traffic police, every driver would choose the same lane (probably the
leftmost one), causing a massive jam.

A traffic police officer stands at the junction and directs:
- "You, go to Lane 3"
- "You, Lane 7"
- "You, Lane 1"

The officer distributes vehicles evenly, preventing any single lane from
becoming overwhelmed. The officer also knows if a lane is blocked and
stops routing cars into it.

A load balancer does exactly this with HTTP requests and servers.

### Load Balancing Algorithms

Not all traffic distribution strategies are equal. Different situations call
for different algorithms.

#### 1. Round Robin

The simplest strategy. Requests are distributed one by one, in order, cycling
through all servers.

```
Request 1  --> Server 1
Request 2  --> Server 2
Request 3  --> Server 3
Request 4  --> Server 1 (cycles back)
Request 5  --> Server 2
...
```

**Analogy**: A teacher handing out papers one by one to each student in row order.

**Best used when:** All requests take roughly the same time to process,
and all servers have equal hardware capacity.

**Problem:** If some requests are "heavy" (e.g., generating a video) and some are "light"
(e.g., fetching a user profile), a server could end up with all the heavy requests
while others sit idle.

#### 2. Least Connections

Route each new request to the server that currently has the fewest active connections.

```
Server 1: 120 active connections
Server 2: 43 active connections  <-- Route here
Server 3: 87 active connections
```

**Analogy**: A bank with multiple teller windows. You join the shortest queue.

**Best used when:** Requests vary significantly in processing time.
Heavy requests stay on one server, the load balancer naturally compensates
by sending fewer new requests to it.

#### 3. IP Hash (Sticky Sessions)

A hash function is applied to the client's IP address.
The result determines which server handles ALL requests from that IP.

```
Client IP: 192.168.1.45
Hash: 45 % 3 = 0  --> Always Server 1

Client IP: 203.0.113.12
Hash: 12 % 3 = 0  --> Always Server 1

Client IP: 198.51.100.7
Hash: 7 % 3 = 1   --> Always Server 2
```

**Why would you want this?** If your servers ARE stateful (they store session data
in memory), you need the same user to always hit the same server.
This is called **session affinity** or **sticky sessions**.

**Problem:** This breaks horizontal scaling. If Server 1 crashes, all Client A's
sessions are lost. And if Client A is unusually heavy, Server 1 gets overloaded
while others are idle.

**Best used when:** You cannot redesign your app to be stateless (legacy system),
or for WebSocket connections (which require persistent server affinity).

#### 4. Weighted Round Robin

Like Round Robin, but you assign a **weight** to each server based on its capacity.
Servers with more capacity get proportionally more requests.

```
Server 1: weight 3 (powerful machine)  -> Gets 3 out of every 6 requests
Server 2: weight 2 (medium machine)    -> Gets 2 out of every 6 requests
Server 3: weight 1 (weak machine)      -> Gets 1 out of every 6 requests
```

**Best used when:** Your server fleet is heterogeneous — some servers are more powerful
than others (e.g., during a gradual hardware upgrade).

#### 5. Least Response Time

Routes to the server with the **lowest current response time**.
The load balancer actively monitors how long each server takes to respond
and favors the fastest ones.

**Best used when:** You have very strict latency requirements and want to avoid
routing to servers that are under momentary CPU spikes.

### Algorithm Comparison Table

| Algorithm | Distribution Basis | Best For |
|---|---|---|
| Round Robin | Turn-based | Uniform requests, equal servers |
| Least Connections | Current connection count | Variable request durations |
| IP Hash | Client IP address | Stateful apps (legacy), WebSockets |
| Weighted Round Robin | Server capacity | Heterogeneous server fleet |
| Least Response Time | Measured latency | Strict latency SLAs |

---

## Section 4: L4 vs L7 Load Balancing

Load balancers operate at different layers of the OSI networking model.
The two most relevant are Layer 4 and Layer 7.

### Layer 4 (Transport Layer) Load Balancing

L4 load balancers operate at the **TCP/UDP** level.
They see: source IP, destination IP, port number.
They do NOT see the actual content of the request.

Think of an L4 load balancer like a **postal sorting facility**.
Packages arrive, the facility looks at the address label (IP + port)
and routes the package to a delivery truck. It does NOT open the package
to see what's inside.

```
L4 sees:  [IP: 203.0.113.1] [Port: 443] --> Route to Server Cluster A
L4 does NOT see:  "GET /admin/delete-user" or "POST /api/login"
```

**Characteristics:**
- Extremely fast — no deep packet inspection
- Cannot make routing decisions based on content (URL path, headers, cookies)
- Used when raw throughput and speed are the priority
- Works for any TCP/UDP traffic (not just HTTP)

**Examples:** AWS Network Load Balancer (NLB), HAProxy in TCP mode

### Layer 7 (Application Layer) Load Balancing

L7 load balancers operate at the **HTTP/HTTPS** level.
They can read the full request: URL path, HTTP headers, cookies, request body.
They make intelligent routing decisions based on this content.

Think of an L7 load balancer like a **hotel concierge**.
When you arrive, the concierge reads your entire situation:
- "You are here for a business conference" → directs you to the conference center
- "You are checking in" → directs you to the front desk
- "You need room service" → connects you to the kitchen

The concierge understands the CONTENT of your request and routes you accordingly.

```
L7 sees the full request:
GET /api/images/profile.jpg HTTP/1.1
Host: api.myapp.com
Authorization: Bearer eyJ...

L7 can decide:
- Requests to /api/images/* --> Route to Image Service
- Requests to /api/users/* --> Route to User Service
- Requests to /api/orders/* --> Route to Order Service
- Requests with invalid Authorization --> Return 401 immediately
```

**Characteristics:**
- Slower than L4 (has to inspect packets, terminate SSL)
- Can route by URL path, HTTP headers, cookies, query params
- Can perform SSL/TLS termination (decrypt HTTPS here, forward plain HTTP internally)
- Can modify headers, add caching, compress responses
- Essential for microservices (different paths → different services)

**Examples:** AWS Application Load Balancer (ALB), Nginx, HAProxy in HTTP mode

### When to Use Each

| Use L4 when... | Use L7 when... |
|---|---|
| You need maximum throughput | You need content-based routing |
| Non-HTTP traffic (e.g., game servers, SMTP) | You are routing microservices by path |
| Minimal latency is critical | You need SSL termination at the LB |
| Simple TCP forwarding is sufficient | You want to inspect headers/cookies |

In most web application HLD answers, **L7 is the right choice** because it enables
the path-based routing that microservices require.

---

## Section 5: Reverse Proxy — The Security Guard at the Gate

### What is a Proxy?

First, understand a **forward proxy**.

A forward proxy sits between clients and the internet.
The client talks to the proxy; the proxy talks to the internet on the client's behalf.

**Analogy**: A travel agent. You (the client) tell the travel agent what you want.
The travel agent contacts hotels, airlines, and tour companies (the internet)
on your behalf. They know what you want, but the hotels don't know who you are directly.

Forward proxies are used to:
- Hide the client's identity (anonymity — like VPNs)
- Block certain websites (corporate firewalls)
- Cache responses for a group of clients (school network)

### Reverse Proxy

A **reverse proxy** flips the picture. It sits in front of servers, not clients.

The client talks to the reverse proxy thinking it is talking to the server.
The reverse proxy forwards the request to the actual server and returns the response.

**Analogy**: A security guard / receptionist at a corporate office.

Visitors (clients) do not walk directly into the office to find whoever they need.
They go to the reception desk. The receptionist:
- Checks your ID (authentication)
- Decides if you are allowed in (authorization)
- Calls the right department (routing)
- Records your visit (logging)
- Returns results to you

The visitor never directly interacts with the actual employees. The receptionist is the
single, controlled entry point. Employees are protected behind the receptionist.

```
Without Reverse Proxy:
Client --> Server 1 directly (server's IP exposed, no protection)

With Reverse Proxy:
Client --> Reverse Proxy --> Server 1 (server's IP hidden, one controlled entry)
                        --> Server 2
                        --> Server 3
```

### Benefits of a Reverse Proxy

**1. SSL/TLS Termination**
HTTPS encryption/decryption is computationally expensive.
Rather than every backend server managing SSL certificates and doing encryption,
the reverse proxy handles all of it. Backend servers receive plain HTTP internally.
This is simpler and faster.

**2. Security and Anonymity**
The actual server IPs and infrastructure are never exposed to the internet.
A DDoS attack hits the reverse proxy — the backend servers are shielded.
The reverse proxy can also block known malicious IPs.

**3. Load Balancing**
A reverse proxy can distribute requests across multiple backend servers —
combining the functionality of a load balancer.

**4. Caching**
The reverse proxy can cache responses to frequently-requested content.
If 10,000 users request the homepage in one second, the reverse proxy can
serve it from cache without touching the backend server at all.

**5. Compression**
Responses can be compressed (gzip, brotli) at the reverse proxy level before
sending to clients, reducing bandwidth.

**6. Rate Limiting**
Limit how many requests a single client can make per second/minute.
Protects backend servers from being overloaded by a single aggressive client.

**Popular Reverse Proxy Software**: Nginx, Apache HTTPD, HAProxy, Caddy, Envoy

### Forward Proxy vs Reverse Proxy — Side by Side

| Aspect | Forward Proxy | Reverse Proxy |
|---|---|---|
| **Sits between** | Clients and internet | Servers and internet |
| **Who configures it** | The client side | The server side |
| **Hides** | Client identity | Server identity |
| **Used by** | Individuals, corporate networks | Businesses protecting servers |
| **Examples** | VPN, corporate web filter | Nginx, CDN edge server |

---

## Section 6: API Gateway — The Hotel Concierge

### What is an API Gateway?

In a microservices architecture, you might have 20 different services:
- User Service on port 8001
- Order Service on port 8002
- Payment Service on port 8003
- Inventory Service on port 8004
- Notification Service on port 8005
- ... and so on

Should your mobile app know about all 20 services? Should it call each one directly?
Should it manage authentication with each one separately?

Absolutely not. That would be an architectural nightmare.

An **API Gateway** is a single entry point for all client requests.
Clients only ever talk to the API Gateway. The gateway handles everything else.

### The Hotel Concierge Analogy

Imagine a 5-star hotel with 30 departments:
room service, spa, restaurant, gym, laundry, pool, valet, business center...

As a guest, you do NOT call each department's direct line.
You call the **concierge**. You say: "I need a massage at 3pm, dinner reservation at 7pm,
and my car ready at 9pm."

The concierge:
- Verifies you are a registered hotel guest (authentication)
- Takes your requests
- Routes each request to the right department (spa, restaurant, valet)
- Coordinates the responses
- Returns a unified confirmation to you

You interact with one person. That one person knows the entire hotel.

The API Gateway is the concierge. Clients interact with one URL.
The gateway knows the entire system.

### What an API Gateway Does

**1. Authentication and Authorization**

Every incoming request carries a token (e.g., JWT in the Authorization header).
The API Gateway validates the token ONCE before passing the request to any backend service.

Without a gateway:
- Each service must validate the token itself
- Duplicated code across 20 services
- If the auth logic changes, update 20 services

With a gateway:
- Gateway validates the token once
- Passes user identity to backend services (as a header or context)
- Auth logic lives in one place

```
Client Request --> API Gateway
                   [Validate JWT]
                   [Token invalid? Return 401 immediately]
                   [Token valid? Add user_id to header, forward request]
                        --> User Service
```

**2. Rate Limiting**

Prevent any single client from overwhelming the system.

```
Rule: Max 100 requests per minute per user

Client A: 200 requests in 1 minute
  - First 100: allowed and forwarded
  - Remaining 100: rejected with HTTP 429 Too Many Requests

Client B: 50 requests in 1 minute
  - All 50: allowed
```

This protects backend services from abuse, accidental loops in client code,
or deliberate denial-of-service attacks.

**3. Request Routing**

Based on the URL path (and sometimes headers), the gateway routes requests
to the correct backend service.

```
GET  /users/42          --> User Service
POST /orders            --> Order Service
POST /payments/process  --> Payment Service
GET  /products/search   --> Product/Search Service
GET  /notifications     --> Notification Service
```

All of these go to the same gateway URL (`api.myapp.com`) from the client's perspective.

**4. SSL Termination**

Just like a reverse proxy, the API Gateway handles HTTPS termination.
Internal services communicate over HTTP for speed.

**5. Request/Response Transformation**

The gateway can modify requests before sending them to services, or modify
responses before returning them to clients:
- Add headers
- Strip sensitive fields from responses
- Translate between API versions
- Aggregate responses from multiple services into one

**6. Logging and Monitoring**

Every request that enters the system passes through the gateway —
making it the perfect place to log all activity, measure response times,
and emit metrics.

**7. Circuit Breaking**

If a backend service starts failing, the gateway can stop routing requests
to it and return a graceful error — rather than hammering a failing service
with more requests.

### API Gateway vs Load Balancer — The Difference

Students often confuse these. Here is the clear distinction:

| Aspect | Load Balancer | API Gateway |
|---|---|---|
| **Primary purpose** | Distribute traffic across identical instances | Single entry point for all services |
| **Awareness** | Which servers are healthy | Which services handle which routes |
| **Features** | Traffic distribution, health checks | Auth, rate limiting, routing, transformation |
| **Layer** | L4 or L7 | L7 (always HTTP-aware) |
| **Analogy** | Traffic police at an intersection | Hotel concierge |

In practice, they are often used together:
- API Gateway routes to the correct service
- Load Balancer distributes traffic within each service's instance pool

### Popular API Gateway Solutions

| Tool | Common Context |
|---|---|
| **AWS API Gateway** | Native AWS managed service |
| **Kong** | Open-source, highly extensible |
| **Nginx** | Can function as API gateway with plugins |
| **Traefik** | Popular in Kubernetes environments |
| **Apigee** | Enterprise-grade (Google Cloud) |

---

## Section 7: How All of These Fit Together — The Complete Picture

Let us now draw the complete networking layer for a production web application.
Every component we covered today has a place in this diagram.

```
+------------------+        +------------------+
|   Web Browser    |        |   Mobile App     |
+--------+---------+        +--------+---------+
         |                           |
         |          HTTPS            |
         +------------+--------------+
                      |
                      v
          +-----------+-----------+
          |        CDN             |
          | (Cloudflare / CloudFront)|
          | Serves static files from|
          | nearest edge server    |
          +-----------+-----------+
                      |
          (Dynamic requests pass through)
                      |
                      v
          +-----------+-----------+
          |      API Gateway       |
          |  - SSL Termination     |
          |  - JWT Authentication  |
          |  - Rate Limiting       |
          |  - Request Routing     |
          |  - Logging / Metrics   |
          +-----------+-----------+
                      |
         +------------+------------+
         |            |            |
         v            v            v
  +------+----+  +----+------+  +--+--------+
  |   User    |  |   Order   |  |  Payment  |
  |  Service  |  |  Service  |  |  Service  |
  +------+----+  +----+------+  +--+--------+
         |            |            |
    +----+----+  +----+----+  +---+----+
    |  LB (3  |  |  LB (3  |  | LB (2 |
    |instances)|  |instances)|  |instances)
    +----+----+  +----+------+  +---+----+
         |            |            |
         v            v            v
    +----+----+  +----+----+  +---+----+
    | Users DB|  |Orders DB|  | Pay DB |
    |(Postgres)|  |(Postgres)|  |(Postgres)
    +---------+  +---------+  +--------+
                      |
                      v
             +--------+--------+
             |  Message Queue  |
             |    (Kafka)      |
             +--------+--------+
                      |
                      v
             +--------+--------+
             | Notification    |
             | Service         |
             | (SMS, Email)    |
             +-----------------+
```

**The request journey:**

1. User types `myapp.com` in the browser
2. **DNS** resolves `myapp.com` to the IP of the CDN/API Gateway
3. If requesting a static file (logo, CSS): **CDN** edge server responds directly
4. If requesting dynamic data (user feed, orders): CDN passes to **API Gateway**
5. **API Gateway** validates the JWT token, applies rate limiting, determines target service
6. Gateway routes to the correct microservice (User, Order, Payment)
7. Each service has its own **Load Balancer** distributing traffic across multiple instances
8. Service runs business logic, queries its **database**
9. For async work (send confirmation email): service publishes to **Kafka**
10. **Notification Service** consumes the Kafka event and sends the email/SMS
11. Response travels back: Service → Load Balancer → API Gateway → CDN → Browser

Every arrow in this diagram that you can explain is a point you earn in the interview.

---

## Interview Q&A

**Q1: What is DNS and what happens when you type a URL into a browser?**

> DNS (Domain Name System) translates human-readable domain names into IP addresses
> that computers use to locate servers.
>
> When I type `www.example.com`:
> First, the browser checks its local DNS cache. If not found, it checks the OS cache.
> If still not found, the request goes to the ISP's recursive resolver.
> The resolver queries the root name server, which points to the TLD (.com) name server.
> The TLD server points to the authoritative name server for `example.com`.
> The authoritative server returns the actual IP address.
> The resolver caches this with the record's TTL and returns it to the browser.
> The browser then opens a TCP connection to that IP address and sends the HTTP request.
>
> The entire DNS lookup typically takes 20-120ms on a cold start, but cached
> lookups are nearly instant (sub-millisecond).

---

**Q2: What is a CDN and how does it improve performance? What are the challenges?**

> A CDN is a globally distributed network of servers (edge servers) that cache
> static content close to end users. Instead of every request traveling to a central
> origin server, users are served from the nearest edge server — reducing latency
> from hundreds of milliseconds to single digits.
>
> A CDN works by either:
> - Pull model: edge server fetches from origin on first cache miss, then serves from cache
> - Push model: you proactively upload content to all edge servers (good for large files)
>
> CDNs dramatically improve page load times for static assets (images, CSS, JS, fonts)
> and reduce origin server load.
>
> The main challenges are:
> - **Cache invalidation**: when you update a file, cached copies on hundreds of edge
>   servers become stale. Solutions include URL versioning (hash in filename) or CDN purge APIs.
> - **Dynamic content**: CDN cannot cache personalised, user-specific content.
>   This content must always go to the origin server.
> - **Cost**: CDN providers charge per GB of data transferred.
> - **Geographic coverage gaps**: remote regions may not have nearby edge servers.

---

**Q3: Explain the difference between a Round Robin and Least Connections load balancing algorithm. When would you use each?**

> **Round Robin** distributes requests one by one in a fixed rotation.
> Request 1 goes to Server 1, Request 2 to Server 2, Request 3 to Server 3,
> Request 4 back to Server 1, and so on.
>
> Round Robin is ideal when all requests take roughly the same amount of time to process
> and all servers have identical hardware. It is simple, predictable, and has zero overhead.
>
> **Least Connections** routes each new request to whichever server currently has
> the fewest active connections — the "least busy" server.
>
> Least Connections is ideal when requests vary widely in processing time.
> For example, if some users trigger a lightweight profile fetch (10ms) while
> others trigger a heavy report generation (3 seconds), Round Robin would overload
> the server that gets all the heavy requests. Least Connections naturally
> compensates — fewer new requests are sent to the busy server.
>
> In a video streaming service where some users stream 4K and others stream 360p,
> I would use Least Connections. For a simple REST API with uniform request times,
> Round Robin is sufficient.

---

**Q4: What is a reverse proxy and how is it different from a load balancer?**

> A **reverse proxy** is a server that sits in front of one or more backend servers
> and acts as an intermediary for all incoming requests. Clients talk to the reverse proxy;
> they never directly reach backend servers.
>
> Benefits of a reverse proxy include: SSL termination, hiding backend server IPs,
> caching, compression, DDoS protection, and adding security headers.
>
> A **load balancer** is specifically about distributing traffic across multiple
> instances of the SAME service to prevent any single instance from being overwhelmed.
>
> The key distinction: a reverse proxy can serve a single backend server and still
> provide value (security, caching, SSL). A load balancer only makes sense with
> multiple backend instances — its sole purpose is traffic distribution.
>
> In practice, many tools do both. Nginx is primarily a reverse proxy but also
> does load balancing. AWS Application Load Balancer is primarily a load balancer
> but also terminates SSL (a reverse proxy function). The concepts overlap,
> but their primary purposes differ.

---

**Q5: What does an API Gateway do that a load balancer cannot? When would you use both together?**

> An API Gateway and a load balancer solve different problems and operate at different
> levels of abstraction.
>
> A load balancer distributes traffic across multiple instances of the SAME service.
> It knows nothing about the business logic — it just routes to healthy instances.
>
> An API Gateway understands the MEANING of requests. It knows that `/users/*` should
> go to the User Service and `/orders/*` should go to the Order Service. Beyond routing,
> it handles authentication (validate JWT once for all services), rate limiting,
> request transformation, logging, and SSL termination at the application level.
>
> In a real microservices system, I would use both together:
>
> Client requests hit the API Gateway first. The gateway authenticates, rate-limits,
> and routes to the correct service. Within each service, a load balancer distributes
> traffic across that service's multiple instances.
>
> So the flow is:
> `Client → API Gateway → Service Load Balancer → Service Instance`
>
> The API Gateway handles "which service?", the load balancer handles "which instance
> of that service?" — they answer different questions.

---

## Practice Exercise: Design the Networking Layer for a Food Delivery App

Using everything you learned today, draw the complete networking layer for
a food delivery app like Swiggy or Zomato.

Work through each of the following:

**1. DNS Design**
- What DNS record type does `api.swiggy.com` use?
- How would you use DNS for geographic routing? (Mumbai users hit Mumbai servers, Delhi users hit Delhi servers)
- What TTL would you set, and why?

**2. CDN Design**
- What content would you serve from CDN? (restaurant photos, app JS/CSS, menu images)
- What would NOT go through CDN? (live order status, your personalised feed, payment)
- How would you handle cache invalidation when a restaurant updates its menu photo?

**3. Load Balancer Design**
- Which load balancing algorithm would you use for the Order Service, and why?
- Would you use L4 or L7 load balancing? Justify your choice.
- How does the load balancer detect that a server is unhealthy and stop routing to it?

**4. Reverse Proxy / API Gateway Design**
- List 4 things the API Gateway does before a request reaches any microservice.
- A user places 500 orders per second from a script (abuse). Which component stops this?
- The Payment Service is slow. Which component would implement a circuit breaker?

**5. Draw the Complete Diagram**
- Draw boxes for: Mobile App, DNS, CDN, API Gateway, at least 3 services
  (Order, Restaurant, Delivery), their databases, a message queue, and Notification Service.
- Draw arrows showing the path of these two requests:
  - User opens the app → sees the home screen (restaurant list + banner image)
  - User places an order → payment is processed → restaurant is notified

**Time yourself: 35-40 minutes to complete this exercise.**
Then explain it out loud as if you were presenting it in an interview.
You should be able to justify every component and every arrow.

---

*Next: Day 15 — Databases in HLD: SQL vs NoSQL, CAP Theorem, Replication, Sharding*
