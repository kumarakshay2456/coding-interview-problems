# Week 4 - Day 22: HLD Problem — URL Shortener (like bit.ly)
# The Classic System Design Interview Problem, Fully Dissected

---

## Why This Problem Is Asked So Often

The URL shortener is a perfect interview problem because it is:
- Simple enough to describe in one sentence
- Complex enough to reveal whether you can think about scale
- Rich enough to test databases, caching, hashing, and distributed systems
- Realistic — bit.ly, TinyURL, and t.co process billions of requests a day

When an interviewer says "Design a URL shortener like bit.ly," they are not asking
you to write the code. They are asking you to think through a real-world system at
scale and make justified technical decisions.

Follow this 6-step framework every time.

---

## Step 1: Clarify Requirements

**Never start designing immediately.** Spend 2-3 minutes asking clarifying questions.
This shows maturity and prevents you from designing the wrong system.

### Questions to Ask

"Before I start, can I clarify a few things?"

1. **Functional scope:** Do we need only URL creation and redirection? Or also
   deletion, expiry, custom short codes, and analytics?
2. **Analytics:** Do we track clicks, geographic location, device type, referrer?
3. **Users:** Do users need to create accounts? Can anonymous users create short URLs?
4. **Custom aliases:** Can users choose their own short code? (e.g., bit.ly/my-brand)
5. **Expiry:** Do short URLs expire? Can users set an expiry date?
6. **Scale:** How many URLs are being shortened per day? What's the read/write ratio?
7. **Availability:** Is this a high-availability system? What is acceptable downtime?
8. **Consistency:** Is eventual consistency acceptable, or must redirects be instant?

### Assumed Requirements for This Design

**Functional Requirements:**
1. Given a long URL, generate a unique short URL (e.g., `https://short.ly/aB3xZ9`)
2. When a user visits the short URL, redirect them to the original long URL
3. Users can optionally set an expiry date on their short URL
4. Users can optionally request a custom short code (e.g., `short.ly/my-sale`)
5. Users can delete their short URLs
6. Analytics: track total clicks per URL

**Non-Functional Requirements:**
1. High availability — redirection must work 99.99% of the time
2. Low latency — redirection must happen in under 100ms
3. Short codes must be unique — no two long URLs share the same code
4. The system should be durable — created URLs persist for at least 5 years
5. Eventual consistency is acceptable for analytics (click counts can lag slightly)
6. The system should handle massive read traffic (read-heavy workload)

**Out of Scope (for this interview):**
- User authentication (simplify by assuming authenticated API calls)
- Billing / subscription tiers
- A/B testing of URLs

---

## Step 2: Capacity Estimation — Back of Envelope

This section demonstrates that you can think quantitatively about scale.
Interviewers love seeing this. Don't skip it.

### Write Traffic (URL Creation)

```
100 million URLs shortened per day

Per second (writes):
100,000,000 / 86,400 seconds ≈ 1,157 writes/second
Round up to: ~1,200 writes/second (write QPS)
```

### Read Traffic (Redirects)

```
Read:Write ratio = 100:1

Read QPS = 1,200 × 100 = 120,000 reads/second
Round to: ~120K reads/second
```

This is a heavily read-dominant system. Design decisions must optimize for reads.

---

### Storage Estimation (5 Years)

```
URLs per day:       100 million
URLs per year:      100M × 365 = 36.5 billion
URLs in 5 years:    36.5B × 5 = 182.5 billion ≈ 183 billion URLs
```

**Per-record size estimate:**
```
short_code:       7 characters  →   7 bytes
original_url:     avg 200 chars  → 200 bytes
user_id:          8 bytes
created_at:       8 bytes
expires_at:       8 bytes
click_count:      8 bytes
is_deleted:       1 byte
──────────────────────────────
Total per record: ~240 bytes (call it 500 bytes with overhead, indexes, metadata)
```

**Total storage:**
```
183 billion × 500 bytes = 91.5 TB ≈ ~100 TB over 5 years
```

This rules out a single machine. We need distributed storage.

---

### Bandwidth Estimation

**Write bandwidth (inbound):**
```
Assuming average request size = 500 bytes (long URL + metadata)
1,200 writes/sec × 500 bytes = 600 KB/s inbound
```

**Read bandwidth (outbound):**
```
Each redirect response = ~200 bytes (just a 302 redirect + Location header)
120,000 reads/sec × 200 bytes = 24 MB/s outbound
```

This is manageable, but with CDN caching we can reduce origin server load dramatically.

---

### Summary Table

| Metric               | Value                  |
|----------------------|------------------------|
| Write QPS            | ~1,200/sec             |
| Read QPS             | ~120,000/sec           |
| Storage (5 years)    | ~100 TB                |
| Inbound bandwidth    | ~600 KB/s              |
| Outbound bandwidth   | ~24 MB/s               |

---

## Step 3: Define the APIs

### 1. Create Short URL

```
POST /api/v1/urls

Request Headers:
  Authorization: Bearer <token>
  Idempotency-Key: <uuid>
  Content-Type: application/json

Request Body:
{
  "long_url": "https://www.example.com/some/very/long/path?with=query&params=too",
  "custom_alias": "my-sale",        // optional
  "expires_at": "2025-12-31T00:00:00Z"  // optional
}

Response: 201 Created
{
  "short_url": "https://short.ly/aB3xZ9",
  "short_code": "aB3xZ9",
  "long_url": "https://www.example.com/some/very/long/path?with=query&params=too",
  "created_at": "2024-03-15T10:30:00Z",
  "expires_at": "2025-12-31T00:00:00Z"
}

Errors:
  400 Bad Request    — invalid URL format
  409 Conflict       — custom alias is already taken
  422 Unprocessable  — expires_at is in the past
  429 Too Many Reqs  — rate limit exceeded
```

---

### 2. Redirect (The Core Feature)

```
GET /{short_code}

Example: GET /aB3xZ9

Response: 302 Found
  Location: https://www.example.com/some/very/long/path?with=query&params=too

Errors:
  404 Not Found  — short_code doesn't exist
  410 Gone       — short_code existed but has expired (HTTP 410 = permanently gone)
```

---

### 3. Get URL Info / Analytics

```
GET /api/v1/urls/{short_code}

Response: 200 OK
{
  "short_code": "aB3xZ9",
  "short_url": "https://short.ly/aB3xZ9",
  "long_url": "https://www.example.com/...",
  "created_at": "2024-03-15T10:30:00Z",
  "expires_at": "2025-12-31T00:00:00Z",
  "click_count": 14782,
  "is_active": true
}
```

---

### 4. Delete Short URL

```
DELETE /api/v1/urls/{short_code}
Authorization: Bearer <token>  (must be owner)

Response: 204 No Content
Errors:
  403 Forbidden — not the owner of this URL
  404 Not Found — short_code doesn't exist
```

---

### 5. List User's URLs

```
GET /api/v1/urls
Authorization: Bearer <token>
Query params: ?limit=20&cursor=<cursor_token>&sort=-created_at

Response: 200 OK
{
  "data": [ ... ],
  "next_cursor": "eyJpZCI6MTAwfQ==",
  "has_more": true
}
```

---

## Step 4: High-Level Design

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                              │
│    Web Browser / Mobile App / Third-party Integration               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CDN (CloudFront / Fastly)                    │
│   Caches redirects for hot short codes — serves from edge           │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ Cache miss → origin
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DNS / Load Balancer (Layer 7)                     │
│   Routes traffic to application servers, terminates TLS             │
└──────────────┬────────────────────────────────┬─────────────────────┘
               │                                │
     Read path │                      Write path│
               ▼                                ▼
┌──────────────────────────┐      ┌─────────────────────────────────┐
│  Redirect Service        │      │  URL Creation Service           │
│  (Read-optimized)        │      │  (Write path)                   │
│                          │      │                                 │
│  1. Check Redis cache    │      │  1. Validate URL                │
│  2. Cache miss → DB      │      │  2. Generate short code         │
│  3. Return 302 redirect  │      │  3. Check uniqueness            │
│  4. Async click tracking │      │  4. Write to DB                 │
└──────────┬───────────────┘      │  5. Warm cache                  │
           │                      └──────────────┬──────────────────┘
           ▼                                     │
┌──────────────────────────┐                     │
│     Redis Cache          │◄────────────────────┘
│   (Most accessed URLs)   │
│   key: short_code        │
│   value: long_url + meta │
│   TTL: 24 hours          │
└──────────┬───────────────┘
           │ Cache miss
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Database (Primary + Replicas)                     │
│    Primary: handles all writes                                       │
│    Read Replicas (3+): handle all reads on cache miss               │
└────────────────────────────────────┬────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   Analytics Service (Async)                          │
│   Kafka / SQS queue → Consumer writes click events to ClickHouse     │
└─────────────────────────────────────────────────────────────────────┘
```

### Role of Each Component

**CDN (Content Delivery Network):**
Caches the redirect response for extremely hot short URLs at edge nodes near the
user. A viral tweet's shortened link can be served entirely from the CDN without
ever hitting your origin servers. This handles traffic spikes gracefully.

**Load Balancer:**
Distributes incoming requests across multiple application server instances.
Performs health checks and removes unhealthy instances. Terminates TLS.

**Redirect Service:**
Optimized purely for speed. On every request, look up the short code in Redis.
If found (cache hit), immediately return the 302 redirect. If not found (cache miss),
query the database read replica, update the cache, then return the redirect.
Click tracking is done asynchronously — never on the critical path.

**URL Creation Service:**
Handles the write path. Generates a unique short code, validates uniqueness against
the database, writes the record, and pre-warms the cache so the first redirect is
already cached.

**Redis Cache:**
Stores the mapping of `short_code → long_url` for frequently accessed URLs.
With 120K reads/second and only ~1,200 writes/second, a well-warmed cache with
99% hit rate means only ~1,200 requests/second reach the database. This is how
you survive the scale.

**Database:**
Persistent source of truth. Primary for writes. Read replicas for cache-miss reads.
We'll pick the right database type in Step 5.

**Analytics Service:**
Click events are dropped into a message queue (Kafka) asynchronously by the
Redirect Service. A consumer reads these events and writes them to a column-store
analytics database like ClickHouse or BigQuery. This keeps analytics completely
off the critical path for redirects.

---

## Step 5: Deep Dive — The Key Technical Decisions

This is where interviewers separate senior candidates from junior ones.
Know these topics cold.

---

### Decision 1: How to Generate the Short Code

This is the central algorithmic question of the problem. You have several options.

#### Option A: MD5 / SHA-256 Hash of the Long URL

Take the long URL, hash it with MD5, and take the first 6-7 characters.

```
MD5("https://example.com/very/long/url") = "a9993e364706816aba3e25717850c26c"
Short code = "a9993e"  (first 6 chars)
```

**Problems with this approach:**
1. **Collisions are frequent.** When you take only the first 6 characters of a hash,
   different URLs can produce the same 6-character prefix. You must check for and
   handle this.
2. **Same URL always produces same hash.** Two different users shortening the same URL
   get the same short code. This may or may not be desired, but it prevents tracking
   per-user analytics on the same URL.
3. **Not truly unique.** Hash functions are deterministic, not uniqueness-guaranteed
   for short prefixes.

**Not recommended** as a standalone solution for production.

---

#### Option B: Counter-Based + Base62 Encoding (Recommended)

Maintain a global counter. Every new URL gets the next counter value. Encode that
counter value in Base62.

**What is Base62?**
Normal decimal (Base 10) uses 10 digits: 0-9.
Hexadecimal (Base 16) uses: 0-9 and a-f.
Base62 uses: 0-9 (10) + a-z (26) + A-Z (26) = **62 characters**.

```
Characters: 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

**Convert a counter value to Base62:**

```python
def to_base62(num):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        result.append(chars[num % 62])
        num //= 62
    return "".join(reversed(result))

to_base62(1)          → "1"
to_base62(61)         → "Z"
to_base62(62)         → "10"
to_base62(3521614607) → "aB3xZ9"
```

**Why 6 characters gives us enough combinations:**
```
62^6 = 56,800,235,584 ≈ 56 billion combinations
```
At 100 million URLs/day, 56 billion combinations covers:
```
56 billion / 100 million per day = 560 days ≈ 1.5 years
```

For 5+ years, use 7 characters:
```
62^7 = 3,521,614,606,208 ≈ 3.5 trillion combinations
3.5 trillion / 100 million per day = 35,000 days ≈ 95 years
```

**7 characters is plenty.**

---

#### Option C: Random Base62 String

Generate 7 random Base62 characters. Check if the code already exists in the
database. If it does (collision), regenerate.

```python
import random
import string

def generate_code(length=7):
    chars = string.ascii_letters + string.digits  # Base62
    return "".join(random.choice(chars) for _ in range(length))
```

**Problem:** At scale with billions of URLs, collision probability grows. You may
need multiple retries per creation. Also, you lose the deterministic ordering that
makes counters attractive.

---

#### Recommended Approach: Distributed Counter with Base62

Use a distributed unique ID generator instead of a single global counter
(a single counter is a bottleneck and single point of failure).

**Options for distributed unique ID generation:**
- **Twitter Snowflake:** 64-bit IDs composed of timestamp + machine ID + sequence.
  Guaranteed unique across machines. This is the industry standard.
- **UUID v4:** 128-bit random. Very low collision probability. But UUIDs are long —
  encode the lower 64 bits in Base62 to get a compact short code.
- **Database auto-increment:** Simple but creates a single-point write bottleneck.

**Best answer for interviews:** Use a Snowflake-style ID generator to get a unique
64-bit integer, then encode it in Base62.

```
Step 1: Generate unique 64-bit integer via Snowflake service
        Example: 3521614606208
Step 2: Encode in Base62
        3521614606208 → "abcXYZ7"
Step 3: Use "abcXYZ7" as the short code
Step 4: No collision check needed — Snowflake IDs are already globally unique
```

This gives you:
- No collision checking needed (huge performance win)
- No single counter bottleneck (Snowflake runs on multiple machines)
- URL-safe short codes (Base62 uses only alphanumeric characters)
- Roughly time-ordered (Snowflake IDs encode timestamp)

---

### Decision 2: Handling Hash Collisions

If you use random generation or hash-based codes:

**Strategy 1: Retry with modification**
```
attempt 1: hash(url)         → "a9f3k2" → exists in DB → retry
attempt 2: hash(url + "1")   → "b7d9x1" → not in DB → use it
```

**Strategy 2: Pre-generated code pool**
Generate millions of unique codes offline, store them in a "available codes" pool
table. When a URL is created, pop one from the pool.

```
Table: available_codes
- code VARCHAR(7)
- is_used BOOLEAN DEFAULT FALSE

On creation: SELECT code FROM available_codes WHERE is_used = FALSE LIMIT 1 FOR UPDATE
             UPDATE available_codes SET is_used = TRUE WHERE code = 'a9f3k2'
```

**Best answer:** Use Snowflake IDs + Base62 to avoid collisions entirely.
If you use random generation, use a bloom filter to check uniqueness without
hitting the database for every check.

---

### Decision 3: Database Schema

```sql
CREATE TABLE short_urls (
    id            BIGINT PRIMARY KEY,           -- Snowflake ID (also used to derive short_code)
    short_code    VARCHAR(10) UNIQUE NOT NULL,  -- The actual short code e.g. "aB3xZ9"
    original_url  TEXT NOT NULL,               -- The long URL
    user_id       BIGINT,                      -- NULL if anonymous, FK to users table
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at    TIMESTAMP,                   -- NULL means never expires
    click_count   BIGINT DEFAULT 0,            -- Approximate, updated async
    is_active     BOOLEAN DEFAULT TRUE,        -- FALSE = soft-deleted
    custom_alias  BOOLEAN DEFAULT FALSE        -- Was this code user-requested?
);

-- Critical indexes:
CREATE UNIQUE INDEX idx_short_urls_short_code ON short_urls(short_code);
CREATE INDEX idx_short_urls_user_id ON short_urls(user_id);
CREATE INDEX idx_short_urls_expires_at ON short_urls(expires_at) WHERE expires_at IS NOT NULL;

CREATE TABLE click_events (
    id           BIGINT PRIMARY KEY,
    short_code   VARCHAR(10) NOT NULL,
    clicked_at   TIMESTAMP NOT NULL,
    ip_address   VARCHAR(45),
    country      VARCHAR(2),       -- ISO country code from IP geolocation
    device_type  VARCHAR(20),      -- mobile, desktop, tablet
    referer      TEXT,             -- where the click came from
    user_agent   TEXT
);
-- click_events is a time-series table, keep in ClickHouse or separate analytics DB
```

**Which database to use?**

For `short_urls`: A relational database (PostgreSQL) works perfectly.
- The data is structured and relational (users → URLs)
- We need ACID guarantees for URL creation (no duplicate short codes)
- We need efficient lookup by `short_code` (indexed)
- PostgreSQL with a single primary + 3 read replicas handles this scale well

For `click_events`: A columnar analytics database like ClickHouse or BigQuery.
- Click events are append-only (never updated)
- We need fast aggregations (total clicks by day, by country)
- ClickHouse handles trillions of rows and aggregates them in seconds
- Don't put click events in PostgreSQL — it will destroy your write performance

---

### Decision 4: Cache Strategy

**What to cache:** The `short_code → original_url` mapping.

**Cache technology:** Redis — it is an in-memory key-value store with sub-millisecond
lookup times. Perfect for this use case.

**Cache key:** `url:{short_code}` → `"{original_url}"`
or cache the full record: `url:{short_code}` → JSON blob with URL + expiry status

**The 80/20 Rule (Pareto Principle):**
In most systems, 20% of URLs receive 80% of the traffic. A hot tweet's shortened
link will receive millions of hits. A link someone shared with 3 friends will receive
3 hits. Caching only the top 20% of hot URLs handles 80% of traffic from memory.

**Cache sizing:**
```
If 20% of URLs are hot:
20% of 100M URLs/day = 20M URLs

Each entry: short_code (10 bytes) + URL (500 bytes avg) = ~500 bytes
20M × 500 bytes = 10 GB

A single Redis instance with 32 GB RAM handles this comfortably.
```

**Cache TTL:**
- Default TTL: 24 hours (refreshed on every cache hit)
- Viral URLs will stay hot and get continuously refreshed
- Old URLs will naturally expire from cache

**Cache eviction policy:** `allkeys-lru` — evict the least recently used keys when
memory fills up. This naturally keeps the hottest URLs in cache.

**Cache warming:**
When a new URL is created, immediately write it to Redis. This prevents a cache
miss on the very first redirect, which matters for links shared immediately after
creation.

---

### Decision 5: Redirection — 301 vs 302

When the user visits `https://short.ly/aB3xZ9`, the server responds with either
a 301 or 302 redirect. This is a subtle but important choice.

**301 Moved Permanently:**
- The browser caches this redirect permanently
- Future visits to `short.ly/aB3xZ9` are resolved entirely in the browser —
  the request never reaches your server
- Pro: Zero load on your servers for repeat visitors
- **Con: You can never track clicks.** The browser never asks your server.
  If the user clicks the link 1,000 times, you record only 1 click (the first one).
- **Con: You cannot update the destination.** Once the browser caches a 301,
  even if you change the long URL, the user will still go to the old URL.

**302 Found (Moved Temporarily):**
- The browser does NOT cache the redirect
- Every visit hits your server
- Pro: **Every click is tracked accurately** — your server sees every request
- Pro: **You can change the destination** — next visit gets the updated URL
- Con: Every redirect hits your server (but you have Redis, so this is fast)

**For a URL shortener with analytics, always use 302.**

The performance difference is negligible when Redis serves the lookup in under
1ms. The benefits — accurate click tracking and the ability to update/delete URLs —
far outweigh the minor extra network hop.

**One nuance:** Some interviewers will say "use 301 to reduce server load." The
correct counter-argument is: with Redis caching, server load is already minimal.
And without 302, you fundamentally cannot provide analytics or URL management,
which are core features.

---

### Decision 6: Custom Short Codes

Allow users to choose their own alias: `short.ly/my-product-launch`

**Implementation:**
- On creation, check if the requested alias already exists in the `short_urls` table
- If not, write the record with `custom_alias = TRUE` and `short_code = "my-product-launch"`
- If yes, return 409 Conflict

**Limitations to enforce:**
- Maximum length: 50 characters
- Allowed characters: alphanumeric + hyphens (no spaces, no special characters)
- Cannot use reserved words: `api`, `admin`, `health`, `login`, `v1`, etc.
- Case-sensitive or case-insensitive? Decide and enforce consistently.

---

### Decision 7: Analytics — Click Tracking, Geo, Device

**The wrong way:** Increment `click_count` in the database on every redirect.
At 120K redirects/second, this is 120K writes/second to your primary database.
It will die immediately.

**The right way: Async event streaming**

```
Redirect Service:
1. Look up short_code in Redis → get long_url
2. Return 302 redirect to user (fast, done)
3. ASYNCHRONOUSLY push click event to Kafka:
   { short_code, timestamp, ip, user_agent, referer }
```

The user gets their redirect in <10ms. The click event is processed in the background.

**Analytics pipeline:**
```
Redirect Service
      │
      │ (async, fire-and-forget)
      ▼
   Kafka Topic: "click_events"
      │
      ├──► Consumer 1: Count aggregator → updates Redis counter (fast approximate count)
      │
      └──► Consumer 2: Event enricher
              → IP → Country (using MaxMind GeoIP database)
              → User-Agent → Device type (mobile/desktop/tablet)
              → Write enriched event to ClickHouse
```

**For the simple `click_count` displayed to users:**
Use a Redis counter that the Kafka consumer increments. This is fast and approximate.
Periodically flush the Redis counter to the database (every minute or every 1000 clicks).

**For detailed analytics (clicks by country, by device, over time):**
Query ClickHouse, which is built for this.

---

## Step 6: Scalability — How to Scale Each Component

### Scaling the Application Servers

Application servers are stateless (no session stored in memory). This means you can
run as many as you need behind a load balancer. If traffic doubles, add more instances.

Use horizontal auto-scaling:
- Monitor CPU and request queue length
- Auto-scale from 5 to 50 instances during traffic spikes
- Scale back down during low traffic to save cost

Separate the read path (Redirect Service) from the write path (URL Creation Service).
Scale them independently — the redirect service needs 100x more instances.

---

### Scaling the Database

**For reads (the bottleneck):**
Add read replicas. Route all read queries (cache misses) to replicas, not the primary.
With 3-5 read replicas, you can handle hundreds of thousands of reads/second.

**For writes (URL creation):**
Writes are only ~1,200/second. A single well-tuned PostgreSQL primary handles this
easily. No sharding needed for writes at this scale.

**For extreme scale (tens of thousands of URLs/second):**
Consider database sharding by `short_code`. Hash the short code to determine which
shard stores that URL. Route reads and writes to the correct shard.

---

### Scaling Redis

**Single Redis instance:** Handles ~100K-200K operations/second. Sufficient for our
120K read QPS at the start.

**Redis Cluster:** Automatically shards data across multiple nodes. Use this when
a single instance can no longer handle the throughput or the dataset exceeds RAM.

**Redis Sentinel:** Provides high availability. If the primary Redis fails, Sentinel
automatically promotes a replica. Use this for production.

---

### Scaling the CDN Layer

CDNs (Cloudflare, CloudFront, Fastly) have thousands of edge nodes worldwide.
They handle traffic spikes by their very nature. A viral link can receive 10 million
hits in an hour — the CDN absorbs this.

Configure CDN to cache 302 responses with a short TTL (e.g., 1 minute for dynamic
content, longer for stable URLs). This is careful — 302 is normally not cached by
CDNs unless you explicitly tell them to via `Cache-Control: s-maxage=60`.

Note: If a URL is deleted or the destination is updated, you need to invalidate the
CDN cache immediately (CDN cache purge API).

---

### Scaling the Message Queue (Kafka)

Kafka scales horizontally by adding partitions and consumers. If click event
processing falls behind (consumer lag), add more consumer instances. The queue
buffers the difference between production rate and consumption rate.

---

### Handling Hot URLs (Celebrity Problem)

A tweet from a celebrity with 50 million followers can generate millions of clicks
in seconds. This is the "thundering herd" or "hot key" problem.

**Solutions:**
1. **CDN caching** — CDN serves the hot URL from edge, zero load on origin
2. **Redis local replica** — Run a Redis replica in each data center or availability zone
3. **Consistent hash + load balancing** — Ensure hot keys are distributed, not all
   landing on one Redis shard
4. **In-memory cache in application server** — A tiny LRU cache (100 entries) on each
   app server for the hottest 100 URLs, even before hitting Redis

---

## Common Interview Follow-Up Questions

### "What if two users shorten the same long URL simultaneously?"

With Snowflake IDs + Base62, each gets a different short code (different ID). The
same long URL maps to two different short codes. This allows per-user analytics.

If you want deduplication (same URL → same short code), check for the existing URL
first with `SELECT short_code FROM short_urls WHERE original_url = ? AND user_id = ?`.
This requires a database index on `original_url`, which can be expensive for long text.
A practical solution: hash the long URL, index the hash, and store both.

---

### "How do you handle expired URLs?"

**On read:** The Redirect Service checks `expires_at` in Redis (store it with the URL).
If `expires_at < now()`, return 410 Gone instead of redirecting. Don't even hit the DB.

**Cleanup:** Run a background job (cron) every hour:
```sql
UPDATE short_urls SET is_active = FALSE WHERE expires_at < NOW() AND is_active = TRUE
```
Or physically delete them if you don't need history.
Also delete from Redis cache (immediate) when deactivating.

---

### "How do you prevent abuse (spam/malicious URLs)?"

1. **URL validation:** Check the URL format and resolve it (actually fetch the URL head
   to verify it's reachable)
2. **Blacklist check:** Compare against known phishing/malware domain lists
   (Google Safe Browsing API)
3. **Rate limiting:** Limit URL creation per user/IP (e.g., 100 URLs/day for free tier)
4. **CAPTCHA:** For anonymous users to prevent bots
5. **Manual review queue:** Flag URLs with suspicious patterns for human review
6. **Click interstitial:** For suspicious URLs, show a warning page before redirecting

---

### "How do you ensure the system stays up during a database failure?"

- **Redis as read buffer:** If the database goes down, Redis still serves redirects
  for cached URLs (hot URLs stay available for hours)
- **Database replicas:** Promote a replica to primary within seconds via automated
  failover (RDS Multi-AZ, Patroni for PostgreSQL)
- **Circuit breaker:** If DB calls fail repeatedly, short-circuit and serve from cache.
  Return 503 for cache misses rather than hanging.
- **Multi-region deployment:** Keep a replica in a second region. In a full regional
  failure, failover to the secondary region.

---

### "How would you implement analytics dashboards?"

```
ClickHouse (or BigQuery) for analytics queries:

-- Total clicks over time
SELECT toDate(clicked_at) AS day, count() AS clicks
FROM click_events
WHERE short_code = 'aB3xZ9'
GROUP BY day
ORDER BY day

-- Clicks by country
SELECT country, count() AS clicks
FROM click_events
WHERE short_code = 'aB3xZ9' AND clicked_at > now() - INTERVAL 30 DAY
GROUP BY country
ORDER BY clicks DESC
```

Pre-aggregate common queries into summary tables (materialized views) for
dashboard performance. Don't run raw scans over billions of rows on every
dashboard load.

---

## Full Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════╗
║                          URL SHORTENER ARCHITECTURE                     ║
╚══════════════════════════════════════════════════════════════════════════╝

  USER / CLIENT
      │
      │ HTTPS
      ▼
  ┌────────────────────────────────────────────────────┐
  │              CDN (CloudFront / Fastly)             │
  │   Edge nodes globally. Caches hot redirects.       │
  │   Cache miss → origin. Cache hit → instant serve.  │
  └────────────────────────┬───────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────┐
  │          Load Balancer (AWS ALB / Nginx)            │
  │   TLS termination. Route to services. Health check. │
  └──────────┬─────────────────────────┬───────────────┘
             │                         │
    ┌────────▼────────┐      ┌─────────▼──────────┐
    │ Redirect Service │      │  URL Creation Svc  │
    │ (20 instances)   │      │  (3 instances)     │
    │                  │      │                    │
    │ 1. Redis lookup  │      │ 1. Validate URL    │
    │ 2. DB on miss    │      │ 2. Gen Snowflake ID│
    │ 3. 302 redirect  │      │ 3. Base62 encode   │
    │ 4. Async track   │      │ 4. Write to DB     │
    └────────┬─────────┘      │ 5. Warm Redis cache│
             │                └─────────┬──────────┘
             │                          │
             ▼                          ▼
  ┌──────────────────────────────────────────────┐
  │          Redis Cluster (Cache Layer)          │
  │   short_code → { original_url, expires_at }  │
  │   ~10-32 GB RAM. allkeys-lru eviction.        │
  │   Read replica per AZ for HA.                 │
  └──────────────────┬───────────────────────────┘
                     │ Cache miss
                     ▼
  ┌──────────────────────────────────────────────┐
  │        PostgreSQL Database                   │
  │                                              │
  │   Primary (writes only)                      │
  │       │                                      │
  │       ├── Read Replica 1 (reads)             │
  │       ├── Read Replica 2 (reads)             │
  │       └── Read Replica 3 (reads)             │
  │                                              │
  │   Tables: short_urls                         │
  │   Indexes: short_code (unique), user_id      │
  └──────────────────────────────────────────────┘

  ASYNC ANALYTICS PATH:
  ┌────────────────┐    ┌─────────────┐    ┌──────────────────────┐
  │Redirect Service│───►│    Kafka    │───►│  Analytics Consumer  │
  │(fire & forget) │    │ click_events│    │ Enrich → ClickHouse  │
  └────────────────┘    └─────────────┘    └──────────────────────┘
                                                       │
                                                       ▼
                                            ┌──────────────────────┐
                                            │      ClickHouse      │
                                            │ Columnar Analytics DB│
                                            │ click_events table   │
                                            │ Billions of rows,    │
                                            │ sub-second queries   │
                                            └──────────────────────┘

  SUPPORTING SERVICES:
  ┌──────────────────┐  ┌────────────────────┐  ┌───────────────────────┐
  │  Snowflake ID    │  │  GeoIP Service     │  │  Cleanup Job (Cron)   │
  │  Generator       │  │  (MaxMind)         │  │  Deactivate expired   │
  │  (unique IDs)    │  │  IP → Country      │  │  URLs hourly          │
  └──────────────────┘  └────────────────────┘  └───────────────────────┘

  MULTI-REGION:
  ┌──────────────────────────┐      ┌──────────────────────────┐
  │    Region: us-east-1     │      │    Region: ap-south-1    │
  │    (Primary)             │◄────►│    (Secondary)           │
  │    Full stack            │      │    Read-only replica     │
  │    Writes here           │      │    Reads + failover      │
  └──────────────────────────┘      └──────────────────────────┘
```

---

## Summary: Key Points to Hit in the Interview

When the interviewer says "Design a URL shortener," here is the story you tell:

1. **Clarify** that it's read-heavy (100:1 ratio) → design must optimize for reads

2. **The core problem** is generating a unique, short, URL-safe code → use Snowflake ID
   + Base62 encoding, no collision checking needed

3. **The core bottleneck** is 120K redirects/second → solve with Redis cache
   (80/20 rule: cache top 20% of URLs → handle 80% of traffic from memory)

4. **Use 302 not 301** because analytics requires your server to see every click,
   and 302 responses are not cached by the browser

5. **Analytics is async** — never on the critical redirect path. Use Kafka to buffer
   click events and process them offline in ClickHouse

6. **Database**: PostgreSQL for URL records (structured, needs ACID), ClickHouse for
   click events (append-only, needs fast aggregation)

7. **Scale**: Application servers scale horizontally (stateless). Database scales with
   read replicas. Redis scales with clustering. CDN absorbs viral traffic spikes.

8. **Expiry**: Check `expires_at` in Redis, return 410 Gone for expired links.
   Background cron cleans up the database.
