# Day 15 — Databases: SQL vs NoSQL, Indexing, Replication, Sharding

---

## 1. What Is a Database?

Think of a database as a **filing cabinet system** for your application.

Without a filing cabinet, documents are scattered everywhere — on desks, floors, in random drawers. Finding anything takes forever. A filing cabinet organizes everything into labeled folders so you can find what you need quickly, store new things reliably, and remove things you no longer need.

A database does the same thing for data. It gives your application a structured, reliable, and fast way to:
- **Store** data persistently (it survives power outages, restarts)
- **Retrieve** data efficiently (you can find one user out of 500 million in milliseconds)
- **Update** data safely (two people editing the same thing at the same time doesn't corrupt it)
- **Delete** data cleanly

Every significant application uses at least one database. Instagram stores posts, users, and likes. Netflix stores your watch history and account info. Your banking app stores every transaction you've ever made.

The two major families of databases you must understand for system design interviews are **SQL (relational)** and **NoSQL (non-relational)**.

---

## 2. SQL (Relational) Databases

### The Basic Idea

SQL databases organize data into **tables** — think of them as spreadsheets with strict rules. Each table has named columns (fields), and each row is one record.

Example — a `users` table:

| id  | name         | email               | created_at          |
|-----|--------------|---------------------|---------------------|
| 1   | Alice Smith  | alice@example.com   | 2024-01-15 09:00:00 |
| 2   | Bob Jones    | bob@example.com     | 2024-01-16 14:30:00 |
| 3   | Carol White  | carol@example.com   | 2024-02-01 11:00:00 |

Tables **relate** to each other. An `orders` table might reference the `users` table by storing `user_id`. This relationship is why these are called relational databases.

You query SQL databases using **SQL (Structured Query Language)**:

```sql
SELECT name, email FROM users WHERE id = 1;
-- Returns: Alice Smith, alice@example.com

SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.total > 100;
-- Returns all users who have orders over $100
```

### ACID Properties — Why Banks Love SQL

ACID is not about the chemical — it's an acronym describing the four guarantees that make SQL databases trustworthy for critical data.

Think about a **bank transfer**: Alice sends $500 to Bob. This requires two operations:
1. Subtract $500 from Alice's account
2. Add $500 to Bob's account

What if the server crashes between step 1 and step 2? Without guarantees, Alice loses $500 and Bob never receives it. This would be catastrophic. ACID prevents this.

**A — Atomicity: "All or nothing"**

The entire transaction either completes fully or doesn't happen at all. If step 2 fails, step 1 is automatically reversed. Alice's money is returned. No partial states.

Real-world analogy: Think of it like a vending machine. You either get your snack and the machine takes your money, or you get your money back and receive nothing. The machine never takes your money and gives you nothing (well, a good one doesn't).

**C — Consistency: "Data is always valid"**

The database enforces rules. If a rule says "account balance can never be negative," the database refuses any transaction that would break this rule. Data transitions from one valid state to another valid state — never to an invalid state.

**I — Isolation: "Transactions don't interfere with each other"**

If 1,000 transactions are happening simultaneously, each one behaves as if it's running alone. Two people booking the last seat on a flight don't both successfully book it — isolation ensures only one wins.

**D — Durability: "Committed data survives failures"**

Once the bank says "transfer complete," that data is written to disk. Even if the server immediately crashes, the data is not lost. When the server restarts, the transfer is still recorded.

### When to Use SQL

- You have **structured, consistent data** that fits neatly into tables
- You need **complex queries** joining multiple tables
- **Data integrity is critical** (financial transactions, medical records, inventory)
- Your data has **clear relationships** between entities
- You need **ACID compliance** (banking, e-commerce orders)

**Popular SQL databases:** PostgreSQL, MySQL, SQLite, Oracle, Microsoft SQL Server

---

## 3. NoSQL Databases

### The Basic Idea

NoSQL means "Not Only SQL" — these databases don't use the rigid table structure of SQL. They trade some guarantees (like strong ACID compliance) for **flexibility, scale, and speed** in specific use cases.

There are four main types. Each solves a different problem.

---

### Type 1: Document Databases (MongoDB, CouchDB)

**Analogy: Filing folders with flexible documents**

Imagine a filing cabinet where each folder can hold any kind of document — a typed letter, a handwritten note, a photo, a form with 50 fields or just 3 fields. No two folders have to contain the same kind of document.

That's a document database. Each "record" is a document (usually JSON), and documents in the same collection don't have to have the same fields.

```json
// User document — rich, nested, flexible
{
  "_id": "user_123",
  "name": "Alice Smith",
  "email": "alice@example.com",
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "zip": "10001"
  },
  "preferences": ["dark_mode", "email_notifications"],
  "subscription": {
    "plan": "premium",
    "expires": "2025-12-31"
  }
}
```

Notice how this single document contains everything about a user — including nested objects and arrays. In SQL, you'd need 3-4 separate tables and JOIN queries to get this same information.

**Best for:** Content management systems, e-commerce product catalogs (products with varying attributes), user profiles, blog posts with comments

---

### Type 2: Key-Value Stores (Redis, DynamoDB, Memcached)

**Analogy: Locker room with numbered keys**

Imagine a gym locker room. Each locker has a unique number (the key). You put something inside (the value). To retrieve it, you only need the locker number. It's extremely fast — there's no searching, no scanning, just direct access.

```
SET session:user_123  {"userId": 123, "loggedIn": true, "cart": [...]}
GET session:user_123  → returns the whole session object

SET rate_limit:ip_192.168.1.1  47
GET rate_limit:ip_192.168.1.1  → returns 47
```

The tradeoff: you can only look things up by key. You can't say "give me all sessions where the user is logged in" — there's no querying by value.

**Best for:** User sessions, caching frequently accessed data, rate limiting, leaderboards, real-time counters

---

### Type 3: Column-Family Stores (Apache Cassandra, HBase)

**Analogy: A spreadsheet optimized for reading entire columns**

Imagine a massive spreadsheet tracking sensor readings from millions of IoT devices. Traditional databases store data row by row (all fields of one record together). Column-family stores group data **by column** — all temperature readings are stored together, all humidity readings are stored together.

This is extremely fast when you want to analyze one metric across millions of records: "Give me all temperature readings from January" — because all temperature data is physically together on disk.

```
Sensor readings table:
Row Key         | timestamp           | temperature | humidity | pressure
sensor_001      | 2024-01-01 00:00:00 | 22.5        | 45       | 1013
sensor_001      | 2024-01-01 00:01:00 | 22.6        | 46       | 1013
sensor_002      | 2024-01-01 00:00:00 | 19.1        | 60       | 1011
```

Cassandra is designed to handle enormous write volumes (millions of writes per second) and is masterless — no single point of failure.

**Best for:** Time-series data (sensor data, logs, metrics), write-heavy workloads, analytics, data that's read by time range (IoT, financial tick data)

---

### Type 4: Graph Databases (Neo4j, Amazon Neptune)

**Analogy: A physical social network map on a wall**

Imagine a detective's wall with photos of people connected by strings — "Alice knows Bob," "Bob works with Carol," "Carol is related to Dave." This is a graph: nodes (people) connected by edges (relationships).

Relational databases can model this with JOIN tables, but finding "all friends of friends of Alice within 3 degrees of separation" requires complex, slow, recursive SQL queries. Graph databases are built specifically for traversing relationships.

```
Nodes: (Alice)-[:FOLLOWS]->(Bob)-[:FOLLOWS]->(Carol)
                                    ↑
               (Alice)-[:FOLLOWS]---+

Query: Find all people Alice follows who also follow Carol
MATCH (alice:User {name: "Alice"})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(carol:User {name: "Carol"})
RETURN friend.name
```

**Best for:** Social networks (friend recommendations), fraud detection (suspicious transaction patterns), recommendation engines, knowledge graphs

---

## 4. SQL vs NoSQL — When to Choose Each

| Factor | SQL | NoSQL |
|---|---|---|
| **Data structure** | Structured, consistent schema | Flexible, schema-less or dynamic |
| **Relationships** | Complex relationships between entities | Simple relationships or self-contained documents |
| **Consistency** | Strong ACID guarantees | Often eventual consistency |
| **Scale** | Scales vertically (bigger machine) | Scales horizontally (more machines) |
| **Query complexity** | Complex queries, JOINs, aggregations | Simple lookups, usually by key |
| **Write throughput** | Moderate | Extremely high (Cassandra, DynamoDB) |
| **Use cases** | Banking, e-commerce, ERP, CRM | Social feeds, sessions, caching, IoT, recommendations |
| **Examples** | PostgreSQL, MySQL, Oracle | MongoDB, Redis, Cassandra, Neo4j |

**The honest answer for interviews:** Most large systems use both. PostgreSQL for user accounts and orders, Redis for caching and sessions, Cassandra for activity feeds and time-series data, Neo4j for friend graphs. This is called **polyglot persistence**.

---

## 5. Indexing

### The Problem Without Indexes

Imagine a library with one million books, but **no catalog**. To find a book about "distributed systems," a librarian would have to pull every single book off the shelf, read the title, and check if it matches. That's called a **full table scan** — it works but it's incredibly slow.

With a **card catalog** (index), the librarian looks up "distributed systems" alphabetically in a small catalog, finds the exact shelf location, and walks directly there. This is what database indexes do.

### How Indexes Work — B-Tree Index

The most common index type is the **B-Tree (Balanced Tree)**. Think of it as a phone book:

- Entries are sorted alphabetically
- You can quickly binary-search to find any name
- You can efficiently find ranges ("all names between Smith and Taylor")

```sql
-- Without an index, this scans all 50 million rows:
SELECT * FROM users WHERE email = 'alice@example.com';

-- Create an index:
CREATE INDEX idx_users_email ON users(email);

-- Now the same query uses the index and finds the row in milliseconds
SELECT * FROM users WHERE email = 'alice@example.com';
```

The index is a separate data structure that stores the indexed column values in sorted order, along with pointers to the actual rows. The database maintains this structure automatically.

### When Indexes Hurt — Write Performance

Indexes are not free. Every time you **insert, update, or delete** a row, the database must also update every relevant index. It's like a library that updates its card catalog every time a new book arrives or an existing book changes.

If a table has 5 indexes and you insert 1 row, the database actually performs 6 writes (1 for the row + 5 for indexes). For write-heavy tables with many indexes, this overhead becomes significant.

**Rule of thumb:**
- Add indexes on columns you frequently search or filter by (WHERE clauses)
- Add indexes on foreign key columns used in JOINs
- Don't add indexes on every column — it hurts write performance
- Write-heavy tables should have fewer indexes

### Composite Indexes

A composite index covers **multiple columns**. Critically, **order matters**.

```sql
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

This index efficiently supports:
- `WHERE user_id = 5` (uses the index — leading column matches)
- `WHERE user_id = 5 AND created_at > '2024-01-01'` (uses full index)

But NOT:
- `WHERE created_at > '2024-01-01'` (can't use this index — skips the leading column)

Think of it like a phone book organized by Last Name, then First Name. You can look up "Smith" or "Smith, John" quickly. But you can't look up everyone named "John" without reading the entire book.

---

## 6. Database Replication

### What Is Replication?

Replication means **keeping copies of your database on multiple machines**. The most common pattern is **Primary-Replica** (also called Master-Slave, though the modern term is Primary-Replica or Leader-Follower).

```
                    ┌─────────────────────┐
    Writes ────────►│   PRIMARY (Leader)  │
                    └──────────┬──────────┘
                               │ Replicates data
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ Replica 1│    │ Replica 2│    │ Replica 3│
        └──────────┘    └──────────┘    └──────────┘
             │               │               │
             └───────────────┴───────────────┘
                         Reads spread across replicas
```

**How it works:**
1. All **writes** go to the Primary
2. The Primary logs every change to a replication log
3. Each Replica reads the log and applies the same changes
4. **Reads** can be served by any Replica (or the Primary)

### Why Replication Helps

**1. Read Scaling**
If your application has 95% reads and 5% writes (very common — think Instagram where 95% of users are scrolling, not posting), you can distribute those reads across multiple replicas. Three replicas means roughly 3x your read throughput.

**2. High Availability / Failover**
If the Primary dies, one of the Replicas can be promoted to become the new Primary. Your database is still available. Without replication, your Primary going down means total outage.

**3. Geographic Distribution**
You can put replicas in different data centers or regions. Users in Europe read from a European replica instead of hitting a US primary — much lower latency.

### The Replication Lag Problem

Replication is not instantaneous. There's a small delay between when data is written to the Primary and when it appears on the Replicas. This is called **replication lag**.

**Scenario that breaks things:**
1. Alice posts a photo (write goes to Primary)
2. Alice immediately refreshes her feed
3. Her request is routed to a Replica
4. The Replica hasn't received the photo yet (it's 50ms behind)
5. Alice doesn't see her own photo — she thinks it didn't post

**Solutions:**
- **Read-your-own-writes consistency:** After a write, route that specific user's reads to the Primary for a short window
- **Sync replication:** Wait for at least one replica to confirm before acknowledging the write (slower but consistent)
- **Accept eventual consistency:** Tell the user "your post is processing" — most social apps do this

---

## 7. Database Sharding

### The Problem Replication Doesn't Solve

Replication solves **read scaling** and **availability**, but not **write scaling**. All writes still go to one Primary. If you're handling 100,000 writes per second, one machine must process all of them. Eventually, one machine isn't enough.

Sharding splits your data **horizontally** across multiple independent databases. Instead of one database with 1 billion users, you have 10 databases each with 100 million users.

```
                     ┌─────────────────┐
    Application  ────► Shard Router   │
                     └────────────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Shard 0 │   │  Shard 1 │   │  Shard 2 │
        │ Users    │   │ Users    │   │ Users    │
        │ 0-33M    │   │ 33M-66M  │   │ 66M-100M │
        └──────────┘   └──────────┘   └──────────┘
```

### Shard Key Selection — The Most Critical Decision

A **shard key** is the field used to decide which shard a record lives on. Choosing it wrong can make your system slower than having no sharding at all.

**Common shard strategies:**

1. **Range-based sharding:** Users with IDs 1-1,000,000 go to Shard 1, 1,000,001-2,000,000 go to Shard 2, etc.
   - Simple to understand
   - Problem: New users all get IDs at the high end — one shard gets all the new traffic while others sit idle

2. **Hash-based sharding:** `shard = hash(user_id) % number_of_shards`
   - Distributes data evenly
   - Problem: Adding a new shard changes the formula — almost all data must be redistributed

3. **Geographic sharding:** US users on US shards, EU users on EU shards
   - Low latency for regional users
   - Uneven if one region is much larger than others

### The Hotspot Problem

A **hotspot** is when one shard gets dramatically more traffic than others, making that shard the bottleneck.

**Example:** A social media app shards by `created_at` (time-based). All new posts go to the "recent" shard. During breaking news or a viral event, millions of users post at once — all hitting the same shard.

**Solutions:**
- Choose a shard key with high cardinality (many possible values) and even distribution
- Add randomness: `shard = hash(user_id + random_suffix) % shards`
- For celebrities/viral content: replicate their data to multiple shards

### Consistent Hashing — Brief Introduction

Consistent hashing solves the "adding a new shard requires redistribution" problem. Imagine all possible hash values arranged in a circle (ring) from 0 to 2^32. Each shard owns a portion of this ring.

When you add a new shard, it takes over a portion of the ring from adjacent shards — only data in that portion moves. You go from redistributing ~100% of data to redistributing ~1/n of data.

This is what Redis Cluster, Cassandra, and DynamoDB use internally.

---

## 8. Read Replicas vs Sharding — When to Use Each

| | Read Replicas | Sharding |
|---|---|---|
| **Solves** | Read throughput, availability | Write throughput, storage limits |
| **Complexity** | Low — just add replicas | High — application must know which shard to query |
| **When to use** | Reads vastly outnumber writes | Writes are the bottleneck, or dataset too large for one machine |
| **JOINs** | Work normally | Cross-shard JOINs are complex or impossible |
| **Start here?** | Yes — try replicas first | Only after replicas aren't enough |

**The practical advice:** Don't shard prematurely. It adds enormous operational complexity. Start with one database, add read replicas when reads are the bottleneck, add caching (covered in Day 16), and only shard when the write throughput or data size genuinely requires it.

Instagram didn't shard its database until it had millions of users. Most startups never need to.

---

## 9. Interview Q&A

**Q1: What's the difference between SQL and NoSQL, and how do you choose?**

"SQL databases store data in structured tables with a fixed schema and provide ACID guarantees — making them ideal for financial transactions, e-commerce, and any domain where data relationships are complex and consistency is critical. NoSQL databases sacrifice some consistency for flexibility and horizontal scalability. I'd choose NoSQL when the data model is document-like with varying attributes (MongoDB for product catalogs), when I need extreme write throughput (Cassandra for activity feeds), or when I need fast key-based lookups (Redis for sessions). In practice, most large systems use both — SQL for core transactional data, NoSQL for specific high-scale components."

---

**Q2: Explain database indexing. When would adding an index hurt performance?**

"An index is a separate data structure — typically a B-tree — that stores column values in sorted order with pointers to the actual rows. It's like a book's index: instead of reading every page to find a topic, you look it up in the index and jump directly to the right page. This dramatically speeds up SELECT queries on indexed columns. However, every write operation (INSERT, UPDATE, DELETE) must also update all relevant indexes. A table with 10 indexes requires 11 writes per inserted row. On write-heavy tables like an activity log receiving millions of inserts per minute, too many indexes become a significant bottleneck. I always index foreign keys and frequently-queried columns, but I evaluate the write cost before adding indexes to hot tables."

---

**Q3: What is database replication and what problem does replication lag cause?**

"Replication maintains copies of a database across multiple machines. In a primary-replica setup, all writes go to the primary, which asynchronously replicates changes to replicas. Replicas then serve read traffic, distributing load and providing failover if the primary fails. Replication lag is the delay between a write being committed on the primary and it appearing on replicas — typically milliseconds, but can be seconds under high load. This creates a 'read-your-own-writes' problem: a user writes data, immediately reads it from a replica that hasn't caught up yet, and sees stale data. I'd solve this by routing that user's reads to the primary for a short window after a write, or by using synchronous replication for critical writes at the cost of higher latency."

---

**Q4: When would you shard a database, and what makes a good shard key?**

"I'd consider sharding when write throughput exceeds what a single machine can handle or when the dataset is too large to store on one machine — even with optimization and replicas. A good shard key distributes data and load evenly across shards, is present in most queries (so the router knows which shard to hit), and doesn't require cross-shard JOINs for common operations. User ID is often a good shard key for user-centric applications because traffic is naturally spread across users. Poor shard keys create hotspots — for example, sharding by created_at means all new writes hit the same shard. Geographic or status-based keys are also risky if data concentrates in one value."

---

**Q5: A startup's database is getting slow. What's your approach to fixing it?**

"I'd diagnose before optimizing. First, identify whether the bottleneck is reads or writes by looking at slow query logs and database metrics. For reads: check if appropriate indexes exist on WHERE clause columns and JOIN columns — missing indexes are usually the first culprit and cheapest fix. If reads are still slow, add a caching layer (Redis) for frequently read, rarely-changed data. If reads still overwhelm one machine, add read replicas to distribute load. For writes: first look for unnecessary indexes on the write-heavy table and remove them. Consider connection pooling if many connections are being created and destroyed. If write throughput genuinely exceeds one machine's capacity, consider sharding — but this is a significant step with real complexity costs, so it's a last resort. I'd also verify we're on appropriate hardware and the database is properly tuned (connection limits, buffer pool size, etc.)."

---

## 10. Practice Scenario

**"Which database would you use for Instagram's core systems? Explain your reasoning."**

Think through each component:

**Post data (photos, captions, metadata):**
The post itself (caption, timestamp, user_id, location) is structured and benefits from relational integrity — PostgreSQL makes sense. The actual image files are stored separately in object storage (S3), with only the URL stored in the database.

**User sessions:**
Redis. Sessions are key-value lookups (session_id → user data), need to be extremely fast, and have natural expiration (TTL). Storing 500 million sessions in a SQL database would be wasteful and slow.

**Friend/follow graph:**
A graph database like Neo4j is ideal for relationship traversal queries ("suggest friends"), but at Instagram's scale they actually use a custom solution. For an interview, mentioning Neo4j for friend-of-friend queries or "who to follow" recommendations demonstrates solid understanding. Alternatively, this can be modeled in Cassandra as a followers/following list per user.

**Activity feed (what your friends posted recently):**
Cassandra. This is a write-heavy, time-series workload — millions of posts per minute. Cassandra handles extreme write throughput and time-range queries efficiently. It also scales horizontally across data centers, providing geographic redundancy.

**Search (find users by name, find posts by hashtag):**
Elasticsearch. This is a specialized search engine optimized for full-text search and inverted indexes — neither SQL nor typical NoSQL handles this well at scale.

**The complete answer:** Instagram uses PostgreSQL for core relational data, Redis for caching and sessions, Cassandra for feeds and activity data, and Elasticsearch for search — a classic polyglot persistence architecture where each database is chosen for its strengths.

---

*Next up: Day 16 — Caching: Redis, Eviction Policies, and Cache Patterns*
