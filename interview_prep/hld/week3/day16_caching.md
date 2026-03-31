# Day 16 — Caching: Redis, Eviction Policies, Cache Patterns

---

## 1. What Is Caching?

**The Bakery Analogy**

Imagine a bakery that bakes bread fresh every morning. The bread takes 45 minutes to bake. If every customer who walks in has to wait 45 minutes while the baker bakes a new loaf specifically for them, the line would be out the door and customers would leave.

Smart bakeries keep fresh bread on the counter — already baked, ready to grab. Most customers take bread from the counter (fast, instant). Only when the counter runs out does the baker start a new batch.

That counter is a **cache**. It's a small, fast, temporary storage layer that holds the results of expensive operations so future requests can be served instantly.

In software:
- **Baking bread** = running a complex database query, calling an external API, or doing a heavy computation
- **The counter** = in-memory cache (like Redis)
- **Customers** = incoming requests from users

The cache sits between your application and the slower data source. When the same data is requested repeatedly, you serve it from the fast cache instead of hitting the slow database each time.

---

## 2. Why Cache? — Latency Numbers Every Engineer Should Know

The reason caching matters so much comes down to physics. Different storage layers have wildly different speeds:

| Storage Layer | Approximate Latency | Real-World Analogy |
|---|---|---|
| L1 CPU cache | ~0.5 nanoseconds | Grabbing something from your hand |
| L2 CPU cache | ~5 nanoseconds | Reaching into your pocket |
| RAM (memory) | ~100 nanoseconds | Grabbing from your desk |
| SSD (local disk) | ~100 microseconds | Walking to a filing cabinet in your office |
| Network round trip (same data center) | ~500 microseconds | Calling a coworker in the same building |
| Database query (with index) | ~1–10 milliseconds | Driving to a nearby library |
| Database query (full table scan) | ~100ms–10 seconds | Driving to a library in another city |
| Cross-continent network request | ~150 milliseconds | Mailing a letter across the country |

**The key insight:** A database query (even a fast one) is roughly **10,000x slower** than reading from RAM. If your homepage makes 20 database queries, caching even half of them can make your page load feel instant instead of sluggish.

At scale, this compounds dramatically. If a database query takes 10ms and 10,000 users hit your homepage per second, you're asking your database to handle 200,000 queries per second (if each page makes 20 queries). With caching, most of those queries never touch the database at all.

---

## 3. Cache Hit vs Cache Miss

These are the two fundamental outcomes of any cache lookup:

**Cache Hit** — the data you need is in the cache
1. Request comes in asking for User #42's profile
2. Cache is checked: User #42 is there
3. Data is returned directly from cache
4. Fast — typically sub-millisecond

**Cache Miss** — the data is not in the cache
1. Request comes in asking for User #99's profile
2. Cache is checked: User #99 is not there
3. Application falls back to the database
4. Data is fetched from the database (slow)
5. Data is stored in the cache for next time
6. Data is returned to the user

**Hit Rate** = (Cache Hits) / (Total Requests)

A good cache hit rate is 80-99% depending on the use case. If your hit rate is 40%, your cache is barely helping — you're adding complexity without much benefit, and you should reconsider your caching strategy (what you're caching, TTL settings, cache size).

---

## 4. Where to Cache — The Cache Hierarchy

Caching isn't just one thing. There are multiple layers where caching can happen, from closest to the user to closest to the database:

**1. Client-Side Cache (Browser Cache)**
The user's browser stores CSS, JavaScript, images, and even API responses locally. On repeat visits, these load from disk instead of making network requests. Controlled by HTTP headers like `Cache-Control: max-age=86400` (cache for 24 hours). Free performance — costs nothing server-side.

**2. CDN (Content Delivery Network)**
A CDN is a network of servers distributed globally (Cloudflare, AWS CloudFront, Fastly). Static assets (images, videos, fonts, JS bundles) are cached on CDN servers in dozens of cities. A user in Tokyo gets your assets served from a Tokyo CDN node instead of your server in Virginia — dramatically lower latency.

CDNs are also increasingly used for API caching — caching API responses at the edge for public, non-personalized endpoints.

**3. Server-Side Application Cache (Redis / Memcached)**
Your application servers maintain an in-memory cache. This is where Redis lives. Results of expensive database queries, rendered HTML fragments, computed aggregations, and external API responses are stored here. Shared across all your application server instances.

**4. Database Query Cache**
Databases like MySQL have a built-in query cache that stores the results of recent queries. If the same query runs again with the same parameters, the database returns the cached result without re-executing the query. This is largely deprecated in MySQL 8+ because it created more problems than it solved (cache invalidation on every write to a table), but the concept is important to understand.

---

## 5. Redis Overview

### What Is Redis?

Redis stands for **Remote Dictionary Server**. It's an open-source, in-memory data structure store used as a cache, message broker, and sometimes a primary database for specific use cases.

It is the most commonly discussed caching solution in system design interviews. When an interviewer says "add a cache," you can almost always say "I'd use Redis."

### Why Redis Is Fast

Redis stores everything in **RAM** (memory) instead of on disk. Reading from RAM is orders of magnitude faster than reading from disk — that's the entire explanation. When you look something up in Redis, it's going from memory directly to your application. No disk seeks, no complex query parsing, no table scans.

Additional reasons Redis is fast:
- Single-threaded command processing (avoids locking overhead from concurrent writes)
- Uses efficient data structures internally (hash tables, skip lists)
- Network protocol is lean and low-overhead

Redis handles **hundreds of thousands to millions of operations per second** on a single instance.

### Redis Data Structures — Not Just Key-Value

Redis is often called a key-value store, but it's more accurately a **data structure store**. Each key maps to a value, but that value can be one of several rich data types.

**String** — simplest type, stores text or binary data (including integers and floats)
```
SET page_views:homepage 142591
INCR page_views:homepage       → 142592
GET page_views:homepage        → "142592"

SET user:123:name "Alice Smith"
GET user:123:name              → "Alice Smith"

SET session:abc123 "{...json...}" EX 3600   # expires in 1 hour
```
Use cases: simple caching, counters, rate limiting, storing serialized objects

**List** — ordered list of strings, supports push/pop from both ends
```
LPUSH notifications:user_123 "Bob liked your photo"
LPUSH notifications:user_123 "Carol followed you"
LRANGE notifications:user_123 0 9    → [most recent 10 notifications]
```
Use cases: activity feeds, task queues, notification lists, recent history

**Set** — unordered collection of unique strings
```
SADD online_users user_123
SADD online_users user_456
SADD online_users user_123      # duplicate, ignored
SMEMBERS online_users           → {user_123, user_456}
SISMEMBER online_users user_789 → 0 (not online)

# Intersection — users who follow both Alice and Bob
SINTERSTORE mutual_followers alice:followers bob:followers
```
Use cases: tracking unique visitors, tags on a post, membership lists, finding mutual friends

**Hash** — a map of field-value pairs within a single key (like a mini-dictionary inside Redis)
```
HSET user:123 name "Alice" email "alice@example.com" age 28 city "New York"
HGET user:123 name          → "Alice"
HGETALL user:123            → all fields and values
HINCRBY user:123 age 1      → 29
```
Use cases: storing objects with multiple fields (user profiles, product details), avoiding storing entire serialized JSON when you only need one field

**Sorted Set (ZSet)** — like a Set but each member has an associated float score. Members are automatically ordered by score.
```
ZADD leaderboard 9850 "Alice"
ZADD leaderboard 12200 "Bob"
ZADD leaderboard 7600 "Carol"

ZRANGE leaderboard 0 -1 WITHSCORES REV   → Bob(12200), Alice(9850), Carol(7600)
ZRANK leaderboard "Alice"                → 1 (0-indexed from bottom)
ZINCRBY leaderboard 500 "Alice"          → Alice now has 10350
```
Use cases: **real-time leaderboards**, priority queues, rate limiting (sliding window), trending topics sorted by score

---

## 6. Cache Eviction Policies — What Happens When the Cache Is Full

Your cache has limited memory. Eventually it gets full. The **eviction policy** determines which data gets removed to make room for new data.

Think of a **bookshelf** with limited space. When you buy a new book and the shelf is full, you have to remove one. But which one? Different strategies exist, and each makes sense in different situations.

---

**LRU — Least Recently Used**

Remove the item that was accessed the **least recently**. The assumption is that if you haven't used something in a while, you're less likely to need it in the near future.

Bookshelf analogy: You keep your most recently read books at the front of the shelf. When you need space, you remove the book at the very back — the one you read the longest ago.

```
Cache: [A, B, C, D] (D is most recently used, A is least recently used)
New item E arrives, cache is full → evict A
Cache: [B, C, D, E]
```

LRU is the most commonly used eviction policy and works well for most applications because access patterns often follow temporal locality — recently accessed data is likely to be accessed again soon.

Redis config: `maxmemory-policy allkeys-lru`

---

**LFU — Least Frequently Used**

Remove the item accessed the **fewest total times**. The assumption is that popular data (accessed many times) is more valuable to keep than data only accessed once or twice.

Bookshelf analogy: You track how many times you've read each book. When the shelf is full, you remove the book you've read the fewest times overall — even if you read it yesterday.

LFU is better than LRU when access patterns are non-uniform — some data is always popular (a celebrity's profile page) while some data is accessed once and never again (a one-time news article). LRU would keep the recent-but-rare article; LFU would keep the popular celebrity page.

Redis config: `maxmemory-policy allkeys-lfu`

---

**TTL — Time To Live**

Data automatically expires after a set duration, regardless of how often it's accessed. Not strictly an eviction policy but a fundamental cache mechanism.

```
SET session:abc123 "{...}" EX 3600       # expires in 3600 seconds (1 hour)
SET user:profile:123 "{...}" EX 300      # expires in 5 minutes
SET rate_limit:ip_x.x.x.x 47 EX 60      # rate limit window, expires in 1 minute
```

TTL is essential for:
- Session data (automatically cleaned up when sessions expire)
- Rate limiting (sliding or fixed windows)
- Data that must reflect reality after a certain time (prices, availability)

---

**FIFO — First In, First Out**

Remove the item that was **added to the cache first**, regardless of when it was last accessed or how often.

Queue analogy: The first item to enter is the first item to leave.

FIFO is simple to implement but generally not a great policy for caches — the first item added might still be the most popular item being accessed. FIFO is more common in queues than in caches.

---

## 7. Cache Patterns — The Most Important Section for Interviews

How your application **interacts** with the cache matters as much as what's in the cache. These patterns define when you read from / write to the cache vs the database.

---

### Cache-Aside (Lazy Loading)

**The most common pattern. Know this one cold.**

The application code is responsible for managing the cache. The cache is populated "lazily" — only when data is first requested.

**How it works:**

```
Read path:
1. Application checks cache for the data
2. Cache HIT → return data immediately (done)
3. Cache MISS → query the database
4. Store the database result in cache (for future requests)
5. Return the data to the caller

Write path:
1. Write new data to the database
2. Invalidate (delete) the cache entry for that data
   (so the next read will fetch fresh data from the DB)
```

**Pseudocode:**
```python
def get_user(user_id):
    # Step 1: Check cache
    cache_key = f"user:{user_id}"
    user = redis.get(cache_key)

    if user:
        return json.loads(user)  # Cache hit — return immediately

    # Step 2: Cache miss — hit the database
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # Step 3: Populate the cache for next time
    redis.setex(cache_key, ttl=300, value=json.dumps(user))

    return user

def update_user(user_id, data):
    db.query("UPDATE users SET ... WHERE id = ?", user_id, data)
    redis.delete(f"user:{user_id}")  # Invalidate cache
```

**Pros:**
- Only caches what's actually requested — no wasted space on unused data
- Database is the system of record; cache failure doesn't break the app
- Simple, resilient — if the cache goes down, the app still works (slower)

**Cons:**
- First request always misses — users after a cache flush or new deployment experience slower responses
- Risk of stale data if cache invalidation is missed
- Cache miss under high load can cause many simultaneous DB queries (see Cache Stampede below)

---

### Write-Through

Write to the **cache AND the database simultaneously** on every write. Reads always find fresh data in cache.

```
Write path:
1. Write data to cache
2. Write data to database (synchronously)
3. Return success only after BOTH succeed

Read path:
1. Check cache — almost always a hit (data was written here on write)
2. Return data
```

**Pros:**
- Cache is always up to date — no stale data problem
- Reads are always fast — data is in cache
- No complex invalidation logic

**Cons:**
- Every write is slower — must wait for both cache AND database write
- Newly added cache entries may never be read (you cache data that nobody ever requests)
- If the database write fails after the cache write, you have inconsistency

**Best for:** Read-heavy workloads where stale data is unacceptable (financial account balances, inventory counts)

---

### Write-Behind (Write-Back)

Write to the **cache immediately** and write to the database **asynchronously** (later, in the background). The application considers the write done when the cache is updated.

```
Write path:
1. Write data to cache → return success immediately (fast!)
2. Asynchronously, a background process writes cache changes to DB

Read path:
1. Check cache — data is there (it was written to cache first)
2. Return data
```

**Pros:**
- Extremely fast writes — no waiting for database
- Can batch multiple writes to the database for efficiency (write 100 updates in one DB transaction)

**Cons:**
- **Data loss risk:** If the cache goes down before the async write completes, those writes are lost
- More complex to implement and operate
- Inconsistency window between cache and database

**Best for:** Write-heavy workloads where losing a small amount of recent data is acceptable. Gaming leaderboards, analytics counters, view counts. Twitter uses this for tweet view counts — losing a few counts doesn't matter.

---

### Read-Through

Similar to Cache-Aside, but the cache itself handles the miss logic. The application always talks to the cache; the cache talks to the database on a miss.

```
Read path:
1. Application requests data from cache
2. Cache HIT → cache returns data
3. Cache MISS → cache automatically fetches from DB, stores it, returns it
   (application never needs to know this happened)

Write path:
1. Application writes to database
2. Cache entry is invalidated or updated
```

**Pros:**
- Simpler application code — the cache client library handles miss logic
- Cache is always populated on first access

**Cons:**
- Cache client must support this pattern (not all do)
- First request is always slow (same as cache-aside)
- Cache must have a way to talk to the database (adds coupling)

---

## 8. Cache Problems — The Failures to Know

### Cache Stampede (Thundering Herd)

**The problem:** A popular cache entry expires (TTL runs out). At that exact moment, 5,000 requests come in for that data simultaneously. Every request finds the cache empty. All 5,000 requests hit the database at the same time. The database, suddenly receiving 5,000 queries for the same data, gets overwhelmed and potentially crashes.

This is the **thundering herd** — a stampede of requests all hitting the DB at once.

**Real scenario:** A news site's homepage cache expires during a breaking news event. 50,000 simultaneous users trigger 50,000 database queries for the same data. Database falls over. Site goes down. The cache, designed to protect the database, accidentally caused the outage when it expired.

**Solutions:**

1. **Mutex lock / locking:** When a cache miss occurs, acquire a lock. Only the first request gets the lock and queries the database. All other requests wait. When the lock holder finishes, it populates the cache and releases the lock. All waiting requests then serve from cache. Only one DB query instead of 5,000.

2. **Probabilistic early expiration (PER):** Before the cache entry actually expires, start regenerating it probabilistically. As the TTL counts down, there's a small random chance each request will trigger a refresh. Spreads out the regeneration work instead of spiking it at expiry.

3. **Cache warming:** Pre-populate the cache before expiry. A background job refreshes popular cache entries before they expire, so there's never a cold miss.

4. **Staggered TTLs:** Instead of all entries expiring at the exact same time, add random jitter to TTLs: `TTL = base_TTL + random(0, 60 seconds)`. This prevents synchronized expiration.

---

### Cache Penetration

**The problem:** An attacker or misbehaving client repeatedly requests data that **doesn't exist** in either the cache or the database. Every request misses the cache (nothing to cache for a non-existent key) and hits the database. Millions of such requests can bring down the database.

**Example:** Someone queries `GET /api/users/99999999999` for a user ID that doesn't exist. The cache has nothing. The DB returns empty. Nothing is cached. Every subsequent identical request hits the DB.

**Solutions:**

1. **Cache null results:** When the database returns nothing for a key, cache the absence explicitly — store a special "null" or "not found" value with a short TTL. Future requests for the same non-existent key hit the cache and immediately return "not found" without hitting the DB.

```python
result = db.query(user_id)
if result is None:
    redis.setex(f"user:{user_id}", ttl=60, value="__NULL__")  # Cache the absence
else:
    redis.setex(f"user:{user_id}", ttl=300, value=json.dumps(result))
```

2. **Bloom filter:** A bloom filter is a probabilistic data structure that tells you "definitely not in the database" or "might be in the database." Check the bloom filter before querying. If it says the key definitely doesn't exist, return immediately without touching the cache or DB. False positives are possible but false negatives are not — this is exactly the property needed here.

---

### Cache Avalanche

**The problem:** A large number of cache entries expire at roughly the same time, causing a sudden flood of requests to hit the database simultaneously. Similar to Cache Stampede but at larger scale — instead of one popular entry expiring, thousands of entries expire together.

**Common cause:** After a deployment or cache flush, the cache is rebuilt. All keys are set with the same TTL. They all expire at the same time. The next day, you have an avalanche.

**Solutions:**

1. **TTL jitter:** Add randomness to every TTL so entries expire at different times:
   ```python
   import random
   base_ttl = 300  # 5 minutes
   jitter = random.randint(0, 60)  # 0-60 second random offset
   redis.setex(key, ttl=base_ttl + jitter, value=data)
   ```

2. **Multilevel caching:** Use both a local in-process cache (very fast, small) and a distributed cache (Redis). Even if Redis entries all expire, the local cache buffers some requests.

3. **Circuit breaker:** If the database detects it's overwhelmed, it stops accepting new connections and returns an error immediately rather than queuing thousands of requests that will time out anyway.

---

## 9. When NOT to Cache

Caching adds complexity and can cause subtle bugs. Don't cache blindly.

**Frequently changing data:** If data changes every second (live stock prices, real-time sports scores, live auction bids), caching will serve stale data constantly. The overhead of constant cache invalidation may exceed the benefit.

**Sensitive or personalized data:** Be thoughtful about what you cache and who can access it. Caching a user's private messages or health records in a shared cache creates privacy risks. Serving one user's cached data to another user is a serious security bug. If you cache personalized data, ensure cache keys are user-scoped and access control is enforced.

**Data with strict consistency requirements:** If your system requires reading the most up-to-date value on every request (financial balances during a transaction, inventory counts when placing an order), caching introduces lag that could cause incorrect decisions.

**Low-traffic endpoints:** If an endpoint is called 10 times per day, the overhead of checking the cache, handling misses, and managing invalidation provides no meaningful benefit. Cache popular, frequently-accessed data.

**Data that's already fast:** If the database query takes 0.5ms due to a perfect index, adding a cache layer might only save 0.4ms (Redis is 0.1ms). The added operational complexity isn't worth it. Focus caching effort on slow queries.

---

## 10. Interview Q&A

**Q1: Explain cache-aside vs write-through. When would you use each?**

"Cache-aside, also called lazy loading, populates the cache on the first read miss — the application checks the cache, and on a miss, fetches from the database and populates the cache for next time. Writes invalidate the cache entry. It's the most flexible pattern because only actually-requested data gets cached, and the system continues working even if the cache is unavailable. Write-through writes to both the cache and database on every write, so reads always find fresh data in cache. I'd use cache-aside for most scenarios — it's resilient and efficient. I'd switch to write-through when stale data is genuinely harmful, like caching user account balances or inventory levels, where serving a stale cached value could cause real problems. Write-behind is appropriate for write-heavy workloads where losing a small amount of recent writes is acceptable, like view counts or analytics events."

---

**Q2: What is cache stampede and how do you prevent it?**

"Cache stampede happens when a popular cache entry expires and many simultaneous requests all miss the cache, all fall through to the database, and all query the database for the same data simultaneously. If you have 10,000 concurrent users and a popular cache entry expires, you get 10,000 simultaneous database queries instead of 1 — the database can be overwhelmed and crash. I'd prevent it by adding random jitter to TTLs so entries don't expire simultaneously, using a mutex lock so only one cache-miss request queries the database while others wait and then serve from the repopulated cache, or by proactively refreshing cache entries before they expire using a background job — so there's never a cold miss for popular data."

---

**Q3: What Redis data structure would you use to implement a real-time leaderboard?**

"Sorted Set (ZSet). Redis Sorted Sets store members with an associated score and automatically maintain sorted order. I'd store player names as members and their scores as the numeric score. `ZADD leaderboard 9500 player_123` updates a score in O(log n) time. `ZRANGE leaderboard 0 9 REV WITHSCORES` returns the top 10 players with their scores. `ZRANK leaderboard player_123` returns a player's current rank in O(log n). This all happens in memory and is essentially instant — Sorted Sets are purpose-built for exactly this use case. For millions of players, this is far faster than any database query that would require sorting a large table."

---

**Q4: What is the difference between cache penetration and cache avalanche?**

"Cache penetration is when requests come in for data that doesn't exist anywhere — not in the cache and not in the database. Every request misses the cache and hits the database, getting nothing. An attacker can exploit this deliberately by querying fabricated IDs, causing constant DB load. I'd fix it by caching null results (storing 'not found' in the cache for a short TTL) or by using a bloom filter to detect non-existent keys before hitting the DB. Cache avalanche is when many real cache entries expire at the same time, causing a sudden spike in DB queries for real data. The fix is TTL jitter — randomizing expiration times so entries don't expire in sync. Both attack the same weakness (the cache not protecting the DB) but from different angles."

---

**Q5: When would you NOT use a cache?**

"I'd avoid caching when the data changes so frequently that cached data would be stale almost immediately, like live auction bids or real-time stock prices — you'd be adding complexity without benefit and potentially serving wrong data. I'd avoid caching when there are strict consistency requirements — if a banking transaction needs to read the absolute current balance, reading a potentially-stale cached value could overdraw an account. I'd also think carefully about caching sensitive personal data in a shared cache, as cache keys must be carefully scoped to prevent one user's data from leaking to another. Finally, there's no point caching low-traffic endpoints or queries that are already extremely fast — the added complexity isn't justified when there's no meaningful load to deflect."

---

## 11. Practice: Design the Caching Layer for a YouTube-Like Platform

**Scenario:** You're designing a video platform similar to YouTube. It has:
- 2 billion monthly active users
- 500 hours of video uploaded per minute
- Most traffic is watch/discovery (reads), not uploads (writes)
- A small number of videos account for the majority of views (power law distribution)

**Think through each component:**

---

**Video Metadata (title, description, view count, uploader, tags)**

Strategy: Cache-Aside with moderate TTL (5-10 minutes)

The title and description rarely change. View counts change constantly, but showing a slightly stale view count ("1.2M views" vs the exact "1,203,847 views") is perfectly acceptable. Cache the entire video metadata object in Redis keyed by video ID:

```
Key: video:metadata:{video_id}
Value: {title, description, channel, view_count, tags, ...}
TTL: 300 seconds (5 minutes)
```

For view counts specifically, use an in-memory counter in Redis (`INCR video:views:{video_id}`) that's periodically flushed to the database in batches — this is the Write-Behind pattern and avoids hammering the DB with millions of INCR updates.

---

**Video Files (the actual MP4/streaming chunks)**

Not Redis — this is what CDNs are built for. Video chunks are large binary files that benefit from geographic distribution. Store source videos in object storage (S3), use a CDN (CloudFront, Akamai) to cache and serve chunks globally. A viewer in Japan gets their video chunks from a CDN server in Tokyo — not from your origin server in the US.

The CDN is your cache for static media content.

---

**Homepage Feed / Recommendations**

Pre-compute and cache recommended videos per user. Recommendations are expensive to compute (collaborative filtering, machine learning models) but don't need to be real-time. Cache the pre-computed recommendation list for each user:

```
Key: recommendations:{user_id}
Value: [video_id_1, video_id_2, ..., video_id_20]
TTL: 1800 seconds (30 minutes)
```

A background job continuously refreshes recommendations. Users get the cached list immediately; slight staleness (seeing recommendations from 30 minutes ago) is acceptable.

---

**Search Results**

Cache popular search queries. "How to tie a tie" gets searched millions of times per day. Cache the first page of results:

```
Key: search:{query_hash}
Value: [list of video_ids and metadata]
TTL: 600 seconds (10 minutes)
```

Don't cache long-tail queries (searches that happen once) — they'll never be cache hits. A bloom filter or minimum-frequency threshold can prevent caching rare queries.

---

**User Sessions / Authentication**

Redis with TTL. Every authenticated request needs to verify the session:

```
Key: session:{session_token}
Value: {user_id, roles, preferences}
TTL: 86400 seconds (24 hours, or session length)
```

Session validation is on every request — this must be sub-millisecond. Redis is perfect.

---

**Trending / Top Charts**

Pre-compute trending videos hourly using a background job. Store the result as a single Redis key:

```
Key: trending:global
Value: [video_id_1, video_id_2, ..., video_id_50]
TTL: 3600 seconds (1 hour)

Key: trending:US
Key: trending:category:gaming
```

One expensive computation serves millions of users. Classic caching win.

---

**Key Architectural Decisions to Mention in the Interview:**

1. Use **Redis Cluster** for horizontal scaling of the cache layer itself — one Redis instance isn't enough at YouTube scale
2. Use **multi-region Redis deployments** for geographic distribution — cache nearest to the user
3. Apply **TTL jitter** to all cache entries to prevent synchronized avalanche expiration
4. Use **Write-Behind** for high-frequency counters (view counts, like counts)
5. Accept **eventual consistency** for most metrics — approximate counts are fine for social video
6. The **CDN is the most impactful cache** for a video platform — get this right first before over-engineering the Redis layer

---

*Next up: Day 17 — Message Queues and Async Processing*
