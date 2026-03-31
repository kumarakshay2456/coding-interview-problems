# Day 18 — Scalability: Vertical vs Horizontal, Stateless Design, Performance Patterns

---

## The Big Picture: What is Scalability?

Scalability is the ability of a system to handle a growing amount of work by adding resources.

**The restaurant analogy:**

Imagine you open a small restaurant. You have one cook, four tables, and you serve 20 customers a day. Business is good. Word spreads. Suddenly 200 customers want to eat at your restaurant.

You have a problem. You need to scale.

**Option 1: Get a bigger, faster cook.** Hire Gordon Ramsay. He is ten times faster than your current cook. You can now serve 200 customers. But what happens when 2,000 customers want to eat? You cannot make Gordon Ramsay ten times faster. He is already at his physical limit. This is **vertical scaling** — making one machine bigger.

**Option 2: Hire more cooks.** Hire 9 more cooks just like your current one. Now you have 10 cooks serving customers in parallel. When demand grows to 2,000 customers, hire 90 more cooks. The approach scales indefinitely in theory. But now you have a new problem: the cooks need to coordinate — who cooks which order, who has which ingredients, how do they share the kitchen. This is **horizontal scaling** — adding more machines.

Every major system design decision you make in an interview traces back to this fundamental problem: how do I handle 10x, 100x, 1000x more load?

---

## 1. Vertical Scaling (Scale Up)

**Definition:** Making a single machine more powerful. Add more CPU cores, more RAM, faster SSDs, faster network cards — all in one box.

**The analogy:** Your restaurant cook is slow. You replace them with a faster, stronger, more skilled cook. One person, one kitchen station — just a better one.

### How it works in practice

Your web server is handling 1,000 requests per second and starting to struggle. You "scale up" from a server with 8 CPU cores and 16GB RAM to a server with 32 CPU cores and 128GB RAM. The software does not change — it just runs on a more powerful machine.

This is often the fastest solution. No code changes, no architectural changes. Just upgrade the instance type in AWS and restart.

### The limits of vertical scaling

**Physical ceiling:** There is a maximum size for a single machine. AWS's largest EC2 instance (u-24tb1.112xlarge) has 448 CPU cores and 24TB of RAM — and costs over $200 per hour. You hit the ceiling eventually, and it comes long before you need it if you are at serious scale.

**Diminishing returns:** Doubling the CPU cores does not double throughput. At some point, the bottleneck shifts from CPU to memory bandwidth, to disk I/O, to network — and adding more CPU helps nothing.

**The critical problem — single point of failure:** One machine means one point of failure. If that machine crashes, goes down for a kernel update, or loses power — your entire system goes down. There is no redundancy. For a service that needs 99.99% availability, having only one server is simply not acceptable.

**Downtime for upgrades:** Upgrading hardware often requires rebooting or replacing the machine. This means planned downtime. At scale, planned downtime is unacceptable.

### When to use vertical scaling

- **Early stage startups:** When you have 1,000 users, vertical scaling is the right move. It is simple, fast, and cheap. Do not build a distributed system when a bigger server solves the problem.
- **Databases:** Databases are hard to shard (split across machines). A very large single Postgres server can handle enormous workloads. Many companies run their core database on a single very large machine until they absolutely cannot anymore.
- **Stateful components:** Things that are hard to run multiple copies of (more on this later) benefit from vertical scaling.
- **The rule of thumb:** Vertical scale first. Horizontal scale when vertical scaling is no longer sufficient or when redundancy is required.

---

## 2. Horizontal Scaling (Scale Out)

**Definition:** Adding more machines to handle increased load, distributing the work across multiple servers.

**The analogy:** Instead of one superhuman cook, you hire many ordinary cooks who work in parallel. Each handles a subset of orders. The kitchen (your system) can grow by simply hiring more cooks.

### How it works in practice

You run your web server on 3 machines instead of 1. A load balancer sits in front of them. When a request comes in, the load balancer routes it to one of the three servers using round-robin (alternating between servers) or least-connections (sending to the server with fewest active requests).

When traffic spikes (say, a product launch), you spin up 10 more servers automatically (auto-scaling). When traffic drops, servers are terminated. You pay only for what you use.

### The challenges of horizontal scaling

**State management:** The killer problem. If a user logs in and their session is stored on Server 1, and their next request goes to Server 2 (because the load balancer sent it there), Server 2 does not know about their session. The user is suddenly "not logged in." This is the stateful server problem — and it is the central challenge of horizontal scaling.

**Data consistency:** When multiple servers write to the database, the database becomes the bottleneck. With multiple database servers (sharding), you have consistency problems.

**Coordination complexity:** Distributed systems require coordination: leader election, distributed locks, consensus. This adds complexity that a single server simply does not have.

**Network overhead:** Machines talking to each other adds latency. In a single machine, function calls are nanoseconds. Network calls between machines are milliseconds — a million times slower.

**Debugging difficulty:** A bug that only manifests under concurrent load across 10 servers is far harder to reproduce and debug than a bug on a single machine.

### When to use horizontal scaling

- **When you need redundancy and high availability:** Multiple servers mean no single point of failure.
- **When vertical scaling is maxed out:** At some traffic level, no single machine is big enough.
- **When you need to scale specific components independently:** Scale your image processing servers without scaling your API servers.
- **Stateless services (web servers, API servers):** If servers do not hold session state, horizontal scaling is straightforward.

---

## 3. Stateless Design — The Key to Horizontal Scaling

This is the single most important concept for making a system horizontally scalable. If your servers are stateless, adding more servers is trivially easy. If they are stateful, horizontal scaling becomes a complex, fragile mess.

### The Stateful Server Problem

**How most beginners build web apps:**

A user logs in. The server creates a session object:
```
session = {
    user_id: 12345,
    name: "Alice",
    cart: ["item_A", "item_B"],
    logged_in_at: "2024-01-15 10:00"
}
```

This session is stored in the server's memory (RAM). The server gives the user a cookie with a session ID. Every subsequent request from Alice includes this session ID, and the server looks up Alice's session from its RAM.

**The problem:**

You have three servers: Server 1, Server 2, Server 3. Alice logs in and her request goes to Server 1. Her session is in Server 1's memory.

Alice adds an item to her cart. That request goes to Server 2 (because the load balancer is doing round-robin). Server 2 looks up Alice's session ID. It checks its memory. Alice's session is not there. Server 2 has never seen Alice before. Alice is suddenly not logged in. Her cart is empty.

The server is **stateful** — it holds data (state) that is tied to a specific user. This makes horizontal scaling almost impossible without workarounds like "sticky sessions" (always sending a user to the same server), which defeats the purpose of horizontal scaling and creates uneven load.

### The Stateless Solution

**Principle:** Each request from the client contains all the information the server needs to process it. The server itself holds no memory of previous requests.

How? The state is moved out of the server and into a shared external store:
- **Session data:** Stored in Redis or Memcached (in-memory databases, extremely fast)
- **User data:** Stored in the database (Postgres, MySQL)
- **Files and uploads:** Stored in object storage (S3)
- **Authentication:** Validated via signed tokens (JWT), not server memory

Now when Alice's request hits Server 2, Server 2 does not need to have seen Alice before. It looks up Alice's session ID in Redis (which every server can access). Redis returns Alice's session data. Server 2 processes the request identically to how Server 1 would have. Alice's experience is seamless.

**The analogy:** Stateful is like each waiter in the restaurant memorizing each customer's order in their head. If a waiter goes on break, the replacement does not know anything. Stateless is like the waiter writing every order on a slip of paper and putting it in a central order queue. Any waiter can pick up any order and fulfill it.

---

## 4. How to Make a System Stateless

### Method 1: Session Tokens + External Session Store

The classic approach. When a user logs in:
1. Server generates a random session ID: `sess_a1b2c3d4e5f6`
2. Server stores the session data in Redis: `sess_a1b2c3d4e5f6 → {user_id: 12345, ...}`
3. Server sends the session ID to the client as a cookie
4. Every subsequent request, client sends the cookie
5. Any server that receives the request looks up the session ID in Redis
6. Redis returns the session data — no matter which server handles the request

Redis is the go-to choice for this because it is extremely fast (stores data in RAM), supports automatic expiry (sessions expire after 24 hours), and is designed for exactly this use case.

### Method 2: JSON Web Tokens (JWT)

A more modern approach. Instead of storing session data externally, encode it directly into the token and sign it cryptographically.

A JWT looks like this:
```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NX0.HMAC_SIGNATURE
```

This is three parts (separated by dots):
1. **Header:** Algorithm used for signing (HMAC SHA256)
2. **Payload:** The actual data — user_id, permissions, expiry time
3. **Signature:** Cryptographic proof that the token has not been tampered with

When a server receives a JWT, it does not need to look anything up. It verifies the signature using the secret key (which all servers share), and if valid, trusts the data in the payload. Zero database or cache lookups.

**The analogy:** A JWT is like a government-issued passport. The passport contains your information and has a cryptographic stamp (the photo, holograms, signatures). Any border officer anywhere in the world can verify the passport is legitimate without calling the issuing government. The information is self-contained and verifiable.

**The trade-off:** JWTs cannot be invalidated before they expire. If you need to "log out" a user everywhere immediately (their account was hacked), you have a problem. The JWT keeps working until it expires. Solutions: very short expiry times (15 minutes), plus a "refresh token" mechanism, plus a "revoked tokens" list in Redis (which partially brings back the stateful problem).

### Method 3: Pass State in Every Request

For some APIs, the client simply sends all relevant state with every request. A REST API is inherently stateless — each request includes the resource identifier, the action, and the authentication token. The server does not need to remember anything between requests.

This is why REST became dominant — it makes horizontal scaling trivial.

---

## 5. Database Scaling Patterns

The web server tier is relatively easy to scale (stateless + load balancer). The database is the hard part. Here are the main patterns.

### Read Replicas — For Read-Heavy Workloads

**Problem:** Your database handles 10,000 queries per second, but 9,000 of them are reads (SELECT) and only 1,000 are writes (INSERT/UPDATE/DELETE).

**Solution:** Create read replicas. The primary database handles all writes. Asynchronously, those writes are replicated to one or more replica databases. Reads are distributed across all replicas. The primary gets much less load.

**How replication works:** Every write on the primary generates a "replication log" (in Postgres: the WAL, Write-Ahead Log). Replicas continuously stream this log and apply the same changes. This is asynchronous — there is a small lag (milliseconds to seconds) between a write on the primary and its appearance on replicas.

**The tradeoff:** Reads from replicas may return slightly stale data (lag of a few milliseconds to seconds). For most reads (show me this product's description, load this user's profile), this is perfectly acceptable. For reads that must see the very latest data (a bank balance after a deposit), you must read from the primary.

**When to use it:**
- Social media feeds (reads vastly outnumber writes)
- Product catalogs (mostly reads)
- Analytics dashboards (heavy reads, slow queries)
- Any read:write ratio above 3:1

**Real example:** Instagram ran on Postgres with many read replicas for years. Reads of photos, profiles, and feeds all hit replicas. Write operations (posting a photo, liking) went to the primary.

---

### Sharding — For Write-Heavy Workloads

**Problem:** Your primary database is getting 50,000 write operations per second. A single PostgreSQL server can handle perhaps 10,000-20,000 writes per second. Read replicas do not help — they reduce read load, not write load. Every write still hits the single primary.

**Solution:** Sharding. Split the data across multiple databases (shards) so that writes are distributed. Each shard is an independent database that handles a subset of the total data.

**How sharding works — the hash shard key:**

You pick a "shard key" — a column used to determine which shard a row lives on. Common choices: user_id, order_id, a geographic region.

If you have 4 shards and user_id is the shard key:
- Users with ID 1-25M go to Shard 1
- Users with ID 25M-50M go to Shard 2
- Users with ID 50M-75M go to Shard 3
- Users with ID 75M-100M go to Shard 4

Or using a hash function: `shard = hash(user_id) % 4`

Every write for user 12345 goes to Shard 1. Every read for user 12345 goes to Shard 1. The application knows the formula and routes accordingly.

**The challenges of sharding:**

- **Cross-shard queries are expensive:** "Find all users who signed up in January" requires querying all 4 shards and merging results. This is slow.
- **Hot shards:** If a popular user generates enormous traffic (a celebrity on Twitter), the shard containing their data gets hammered while others are idle.
- **Rebalancing is painful:** If you start with 4 shards and need 8, you must move data around — half of each shard moves to new shards. This is a complex, risky migration.
- **No cross-shard transactions:** Atomically updating data in two shards requires distributed transactions — complex and slow.

**When to use sharding:**
- Write volume exceeds what a single primary can handle
- Data volume exceeds what fits on a single machine (terabytes to petabytes)
- Strong isolation between tenants (SaaS where each company's data is in its own shard)

**Real examples:** MongoDB sharding, Cassandra (natively sharded by partition key), MySQL sharding at Pinterest (they sharded by user_id), Uber sharded by trip_id.

---

### Denormalization — For Query Performance

**The traditional approach (normalized data):**

In a normalized database, data is split into multiple tables to eliminate redundancy. A blog post has a `posts` table and a separate `authors` table. To show a post with the author's name, you JOIN the two tables.

JOINs are expensive at scale. If you have a billion posts and ten million authors, joining these two tables for every page view is slow, even with indexes.

**Denormalization:** Deliberately store redundant data to avoid expensive JOINs. Store the author's name directly in the `posts` table, even though it also exists in the `authors` table. Now loading a post requires reading only one table.

**The cost:** When an author changes their name, you must update it in both the `authors` table and in every row of the `posts` table that author wrote. Writes become more expensive and more complex. Data integrity is harder to maintain.

**When to use denormalization:**
- Read performance is critical
- Data changes infrequently (an author's name rarely changes)
- You can accept the complexity of dual writes

**Real example:** Amazon's product catalog. A product has a seller. Instead of joining `products` and `sellers` on every page load, Amazon stores the seller name directly in the product record. When you view a product, it is one database read, not two.

---

## 6. Performance Patterns

### Connection Pooling — Why Direct DB Connections Don't Scale

**The naive approach:**

Every time your web server handles a request that needs the database, it opens a new database connection, runs the query, and closes the connection.

Opening a database connection is expensive: it involves a TCP handshake, database authentication, memory allocation on the database server. This takes 20-100 milliseconds.

If you have 1,000 requests per second, you are opening and closing 1,000 connections per second. PostgreSQL can handle about 500 concurrent connections total before performance degrades severely. At 1,000 connections/second, you are overwhelming it.

**Connection pooling:**

A connection pool maintains a set of pre-opened database connections (say, 20 connections). When a request needs the database, it borrows a connection from the pool, uses it, and returns it. The connection is not closed — it waits for the next request.

With 20 pooled connections, you can handle 10,000+ requests per second (each request uses a connection for milliseconds, then returns it). The database sees only 20 connections at any time.

**The tool:** PgBouncer is the standard connection pooler for PostgreSQL. It sits between your application and the database and manages the pool. At companies running millions of requests per second, PgBouncer is not optional — it is required infrastructure.

**Analogy:** Connection pooling is like a taxi dispatch service. Instead of manufacturing a new taxi for every passenger and then scrapping it after the ride (opening/closing connections), you have a fleet of 20 taxis that continuously pick up and drop off passengers (borrowing and returning connections).

---

### Async Processing — Offload Slow Operations to Queues

**The problem:**

A user registers on your platform. Your registration endpoint needs to:
1. Save the user to the database — 5ms
2. Send a welcome email — 500ms (slow, external email API)
3. Generate a profile thumbnail from their avatar — 1000ms (slow, CPU-intensive)
4. Notify the sales team via Slack — 200ms (slow, external API)

If you do all of this synchronously, the user waits 1,705ms for the "Registration successful" response. That is terrible. And if the email service is down, registration fails entirely.

**Async processing with a message queue:**

Instead:
1. Save the user to the database — 5ms
2. Publish a "user_registered" event to a message queue (Kafka, RabbitMQ, SQS) — 2ms
3. Return "Registration successful" to the user — total time: 7ms

Separately, worker processes (consumers) read from the queue:
- Email worker picks up the event, sends the welcome email
- Thumbnail worker picks up the event, generates the thumbnail
- Slack worker picks up the event, notifies the sales team

These happen asynchronously, after the user has already received their response.

**Benefits:**
- **Speed:** User gets a near-instant response
- **Resilience:** If the email service is down, the event stays in the queue. When the email service recovers, the worker processes all queued events. Nothing is lost.
- **Scalability:** Add more workers to process the queue faster during peak times
- **Decoupling:** The registration service does not know or care about the email service. They are decoupled through the queue.

**Real examples:** Every major tech company uses async processing. Stripe processes payments asynchronously (charge card → return transaction ID → process payment in background). YouTube processes video encoding asynchronously (upload video → return success → encode video in background, takes minutes).

---

### Batch Processing — Group Small Operations

**The problem:**

You have a logging system. Every user action is logged to the database. At peak, you have 100,000 user actions per second. That means 100,000 individual INSERT statements per second — far beyond what most databases can handle.

**Batch processing:**

Instead of inserting each log entry individually, buffer them in memory and insert them in batches:
- Collect 1,000 events (or wait 100ms, whichever comes first)
- INSERT all 1,000 events in a single SQL statement

One INSERT of 1,000 rows is roughly 100x faster than 1,000 individual INSERTs. The database overhead (parsing SQL, acquiring locks, flushing to disk) happens once for the batch, not 1,000 times.

**The trade-off:** If the server crashes after collecting 999 events but before inserting them, those 999 events are lost. Batch processing trades durability for performance.

**Real examples:**
- Kafka writes to disk in batches
- Elasticsearch bulk indexing API
- BigQuery and data warehouses batch-load millions of rows at a time
- Analytics events (Google Analytics batches events before sending to servers)

---

## 7. Back-of-Envelope Calculations — Critical for Interviews

This is one of the most tested skills in system design interviews. The ability to quickly estimate scale — "how many servers do I need, how much storage, what's the throughput" — demonstrates engineering maturity.

Interviewers are not looking for exact answers. They are looking for your ability to reason about scale, make reasonable assumptions, and arrive at a ballpark figure.

### Numbers Every Engineer Should Know

**Latency reference points:**
- L1 cache access: ~1 nanosecond
- RAM access: ~100 nanoseconds
- SSD read: ~100 microseconds
- Spinning disk read: ~10 milliseconds
- Network round trip within same data center: ~1 millisecond
- Network round trip US to Europe: ~150 milliseconds

**Data size reference points:**
- 1 character of text = ~1 byte
- An average tweet = ~300 bytes
- A high-quality photo = ~3-5 MB
- A minute of HD video = ~100 MB
- 1 day of typical user data = ~1 KB - 10 KB
- 1 billion bytes = 1 GB
- 1 trillion bytes = 1 TB
- 1 quadrillion bytes = 1 PB (petabyte)

**Time conversions (memorize these):**
- 1 day = 86,400 seconds ≈ 100,000 seconds (round up for easy math)
- 1 month ≈ 2.5 million seconds
- 1 year ≈ 30 million seconds

**Powers of two (useful for approximation):**
- 2^10 = 1,024 ≈ 1,000 (1K)
- 2^20 ≈ 1,000,000 (1M)
- 2^30 ≈ 1,000,000,000 (1B)

---

### How to Estimate QPS (Queries Per Second)

**Formula:**
```
QPS = Total requests per day / 86,400 seconds
```

Or for quick estimation, divide by 100,000 (close enough):
```
QPS ≈ Total requests per day / 100,000
```

**Example:**
- 100 million requests per day
- QPS = 100,000,000 / 86,400 = 1,157 QPS ≈ 1,000 QPS (normal load)
- Peak QPS = 2-5x average: 2,000 - 5,000 QPS

**Rule of thumb:** Peak traffic is roughly 3-5x average traffic. Always design for peak, not average.

---

### How to Estimate Storage

**Formula:**
```
Total storage = (number of records) × (size per record) × (replication factor)
```

You must also account for:
- **Replication factor:** Data stored 3x (3 copies) for redundancy
- **Growth rate:** How much new data per day/month/year
- **Overhead:** Indexes, metadata, logs add ~20-50% on top of raw data

**Example: Photo storage for a photo-sharing app**
- 10 million photos uploaded per day
- Average photo size: 3 MB
- Storage per day: 10M × 3 MB = 30 TB
- With replication factor 3: 30 TB × 3 = 90 TB per day
- Per year: 90 TB × 365 = 32,850 TB ≈ 33 PB per year

This tells you: you need petabyte-scale object storage. That is AWS S3 territory, not a local disk.

---

### How to Estimate Bandwidth

**Bandwidth = data transferred per unit time**

You need to estimate:
1. How much data is in each request/response
2. How many requests per second

**Formula:**
```
Bandwidth = QPS × average response size
```

**Example: Video streaming**
- 100,000 concurrent viewers
- Each stream is 5 Mbps (HD video)
- Total bandwidth = 100,000 × 5 Mbps = 500,000 Mbps = 500 Gbps

This tells you: you need a CDN. No single server has 500 Gbps of bandwidth. Netflix serves multiple terabits per second globally — only possible through a global CDN.

---

### Worked Example: "Design for 1 Million Users"

**Assumptions:**
- 1 million daily active users (DAU)
- Each user makes 10 requests per day (browsing, posting, etc.)
- Average request payload: 10 KB read, 1 KB write
- 80% reads, 20% writes
- User generates 1 KB of new data per day (posts, actions)

**Step 1: Calculate QPS**
```
Total requests per day = 1,000,000 users × 10 requests = 10,000,000 requests/day
Average QPS = 10,000,000 / 86,400 ≈ 115 QPS
Peak QPS (3x average) = 345 QPS
```

**Step 2: Calculate write QPS**
```
Write QPS = 345 × 20% = 69 writes/second
```

A single PostgreSQL server can easily handle 10,000+ simple writes per second. One database is fine at 1 million users.

**Step 3: Calculate storage growth**
```
New data per day = 1,000,000 users × 1 KB = 1 GB/day
Per year = 365 GB ≈ 400 GB/year
With replication (3x) = 1.2 TB/year
```

At 1 million users, you fit in a single large database server with a few read replicas for 5 years before needing to shard.

**Step 4: Calculate bandwidth**
```
Read bandwidth = QPS × 80% × 10 KB response = 345 × 0.8 × 10 KB = 2,760 KB/s ≈ 3 MB/s
```

A single server handles this trivially.

**Conclusion at 1 million users:**
- 2-3 web servers behind a load balancer (for redundancy, not capacity)
- 1 primary database + 2 read replicas (Postgres)
- Redis for session storage and caching
- CDN for static assets
- Object storage (S3) for any file uploads

Simple. You do not need Kafka, Kubernetes, or sharding at 1 million users. The biggest mistake junior engineers make in interviews is over-engineering early systems.

---

## 8. Interview Q&A

---

**Q1: What is the difference between vertical and horizontal scaling? When would you choose one over the other?**

A: Vertical scaling means making a single machine more powerful — more CPU, more RAM, faster disk. It is simple to implement (no code changes, just upgrade the machine), but has a hard ceiling and creates a single point of failure.

Horizontal scaling means adding more machines and distributing the load across them. It scales indefinitely in theory and provides redundancy — if one server fails, others absorb the traffic. The challenge is that servers must be stateless so any server can handle any request.

My decision framework:

I start with vertical scaling for most components. It is simple and avoids distributed systems complexity. When a single machine can no longer handle the load — or when I need redundancy for availability — I move to horizontal scaling.

For web/API servers: horizontal scaling is almost always the right choice because making them stateless is straightforward. Redundancy is critical.

For databases: vertical scaling as far as possible. Databases are stateful and hard to shard. A very large single Postgres server handles enormous workloads. Add read replicas for read-heavy loads. Shard only when write volume or data volume exceeds what a single machine can handle.

For memory/cache: horizontal scaling with consistent hashing (how Redis Cluster works).

---

**Q2: Why is stateless design so important for scalability? How would you make a stateful application stateless?**

A: Stateless design is the prerequisite for horizontal scaling. If your servers hold session state in memory, a load balancer routing requests to different servers breaks user sessions. You cannot add more servers without breaking the experience.

A stateless server treats every request independently — it does not rely on information stored from previous requests. This means any server in the pool can handle any request, making adding or removing servers seamless.

To make a stateful application stateless:

First, identify where state lives. The most common places: user sessions in server memory, temporary files on local disk, background jobs tracked in a local variable.

Then, externalize that state:
- Sessions go into Redis. Every server can read and write to the same Redis instance. Lookups are sub-millisecond.
- Files go into shared object storage (S3). Every server reads and writes from the same S3 bucket.
- Background job state goes into a database or message queue.

For authentication specifically: move from server-managed sessions to JWTs. A JWT is a signed token that contains the user's identity and permissions. Any server can verify a JWT without looking anything up — just verifying the cryptographic signature with the shared secret key.

Once all state is external, you can freely add or remove servers. The load balancer uses round-robin or least-connections to distribute requests. Auto-scaling groups spin up servers during traffic spikes and terminate them when traffic drops.

---

**Q3: When would you choose read replicas over sharding for database scaling?**

A: Read replicas and sharding solve different problems, so the choice depends on where your bottleneck is.

Read replicas help when your workload is read-heavy — most queries are SELECT statements and the primary database's CPU is overwhelmed by all the reads. With read replicas, you direct reads to replicas and free up the primary for writes. This is simpler: replicas automatically sync from the primary, queries do not change, and you can add replicas without changing application code significantly.

However, read replicas do not help if your bottleneck is writes. Every write still goes to the single primary. Replicas just copy those writes — they do not share the write load.

Sharding is for write-heavy workloads or when data volume exceeds what fits on a single machine. You split the data across multiple databases by a shard key (like user_id). Each shard handles writes for its subset of data. Write throughput scales linearly with the number of shards.

Sharding is significantly more complex: cross-shard queries require aggregating results, transactions spanning two shards require distributed transaction protocols, and rebalancing shards when you add more is operationally risky.

My recommendation: start with read replicas. Only shard when write volume or data volume requires it. Most applications never need sharding — they just need read replicas and query optimization.

---

**Q4: Explain connection pooling. Why is it necessary at scale?**

A: A database connection is an expensive resource. Establishing one requires a TCP handshake, database authentication, and memory allocation on the database server — adding 20-100ms of overhead and consuming a few MB of RAM.

Without connection pooling, a web application opens a new connection for every incoming request and closes it when the request is done. At 1,000 requests per second, that is 1,000 connection open/close cycles per second. Each cycle is expensive. And PostgreSQL degrades severely past roughly 500 concurrent connections — beyond that, memory pressure and context-switching overhead tank performance.

Connection pooling solves this by maintaining a fixed pool of pre-opened database connections (say, 20). When a request needs the database, it borrows a connection from the pool (takes microseconds), uses it, and returns it. The connection stays open — it just waits for the next borrower.

With 20 connections and average query time of 10ms, you can serve 2,000 requests per second (each connection handles 100 queries/second). The database sees exactly 20 connections at all times, regardless of incoming traffic volume.

The standard tool for PostgreSQL is PgBouncer. For MySQL: ProxySQL. At any company with significant traffic, a connection pooler is non-negotiable — it sits between all application servers and the database and acts as a shared pool.

---

**Q5: Walk me through how you would estimate storage requirements for a video platform that supports 1 billion users, where 1% of users upload 1 video per day at an average of 500 MB each.**

A: Let me walk through this step by step.

**Step 1: Calculate daily uploads**
```
1 billion users × 1% uploading = 10 million users uploading per day
10 million uploads × 500 MB = 5,000,000,000 MB = 5,000 TB = 5 PB per day
```

**Step 2: Account for transcoding**
Video platforms transcode every video into multiple resolutions (4K, 1080p, 720p, 480p, 360p) and formats (MP4, WebM). The total storage per video after transcoding is roughly 3-4x the original.
```
5 PB × 4 (transcoding factor) = 20 PB per day
```

**Step 3: Account for replication**
Videos are stored with geographic redundancy — at least 3 copies in different regions.
```
20 PB × 3 (replication) = 60 PB per day
```

**Step 4: Calculate annual growth**
```
60 PB/day × 365 = 21,900 PB ≈ 22 EB (exabytes) per year
```

**Step 5: Interpret the number**
22 exabytes per year is enormous — this is YouTube territory. YouTube stores roughly 1 billion hours of video. YouTube uses Google's global infrastructure with custom hardware (Colossus file system, Borg cluster manager). This cannot be done with off-the-shelf solutions.

For a startup, this means: object storage (S3 or GCS), aggressive deduplication (do not store the same video twice if two users upload identical content), tiered storage (hot storage for recently uploaded videos, cold storage for old videos rarely watched), and a global CDN for delivery.

**The key insight for the interviewer:** You demonstrate that you can turn a vague question into concrete numbers, and that you know what those numbers imply architecturally. The math does not need to be exact — the order of magnitude and the resulting architectural decisions are what matter.

---

## 9. Practice Problem

**"Twitter has 300 million daily active users, 500 million tweets per day. Estimate QPS, storage for 5 years, and bandwidth."**

Work through this yourself before reading the answer below.

---

### Model Solution

**Given:**
- 300 million daily active users (DAU)
- 500 million tweets per day
- Average tweet size: 300 bytes of text
- Let us assume 20% of tweets include a photo (2 MB average) and 5% include a video (10 MB average)
- Read:Write ratio is roughly 100:1 on Twitter (people read far more than they tweet)

---

**Step 1: Tweet Write QPS**
```
500 million tweets/day ÷ 86,400 seconds = 5,787 writes/second ≈ 6,000 writes/second (average)
Peak write QPS (3x) = 18,000 writes/second
```

**Step 2: Tweet Read QPS**
If the read:write ratio is 100:1:
```
Read QPS = 6,000 × 100 = 600,000 reads/second (average)
Peak read QPS = 1,800,000 reads/second
```

This immediately tells you: Twitter must use aggressive caching (Redis/Memcached) for home timelines. No database can serve 1.8 million reads per second without a cache layer in front of it.

---

**Step 3: Storage for Tweet Text (5 years)**
```
Text storage per day = 500 million tweets × 300 bytes = 150 GB/day
Per year = 150 GB × 365 = 54,750 GB ≈ 55 TB/year
5 years = 55 × 5 = 275 TB

With 3x replication = 825 TB ≈ 1 PB for text alone
```

---

**Step 4: Storage for Media (5 years)**

Photos:
```
Photos per day = 500M × 20% = 100 million photos
Storage per day = 100M × 2 MB = 200 TB/day
Per year = 200 TB × 365 = 73,000 TB = 73 PB/year
5 years = 365 PB
With replication (3x): 1,095 PB ≈ 1 EB
```

Videos:
```
Videos per day = 500M × 5% = 25 million videos
Storage per day = 25M × 10 MB = 250 TB/day
Per year = 91 PB/year
5 years = 455 PB
With replication (3x): 1,365 PB ≈ 1.4 EB
```

**Total media storage (5 years): approximately 2.4 EB**

---

**Step 5: Bandwidth**

Outgoing (serving reads):
```
Home timeline refresh every 30 seconds per user = 300M × 2 refreshes/minute = 10 million reads/minute = 167,000 reads/second
Each timeline response = 20 tweets × 300 bytes = 6 KB
Bandwidth = 167,000 × 6 KB = 1 GB/second outgoing for text timelines
```

Add media:
If 30% of timeline reads include a photo thumbnail (50 KB each):
```
Additional bandwidth = 167,000 × 30% × 50 KB = 2.5 GB/second
Total bandwidth ≈ 3.5 GB/second = 28 Gbps sustained
```

This requires a CDN. Twitter's CDN (via Akamai and its own servers) serves hundreds of Gbps globally.

---

**Step 6: What does this tell you architecturally?**

- **Write QPS at 18,000/second:** Cannot use a single database for tweet writes. Twitter shards tweet storage by tweet ID or user ID.
- **Read QPS at 1.8 million/second:** Requires massive caching. Twitter pre-computes home timelines (fan-out on write) and stores them in Redis clusters. A celebrity with 10 million followers tweeting causes 10 million cache updates (fan-out). Twitter uses a hybrid approach — small accounts use fan-out on write, celebrities use fan-out on read.
- **Media storage at 2.4 EB over 5 years:** Object storage (Twitter uses its own Blobstore + cloud storage). Aggressive CDN caching — most images are served from CDN edge nodes, not from origin storage.
- **Bandwidth at 28 Gbps:** CDN is mandatory. Compress all text (gzip). Use efficient binary formats for API responses (instead of verbose JSON).

**The interview takeaway:** The numbers are not the point. The point is demonstrating that you can go from "500 million tweets per day" to "we need Redis for caching, sharding for writes, a CDN for media, and a hybrid fan-out strategy." The math is the bridge between the problem statement and the architecture.

---

*End of Day 18 — Scalability: Vertical vs Horizontal, Stateless Design, Performance Patterns*
