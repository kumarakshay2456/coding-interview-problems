# Day 23 — HLD Problem: Rate Limiter

---

## What Is a Rate Limiter?

Imagine you own a coffee shop. You have one barista. If 500 people show up at the same time demanding coffee, your barista collapses, the espresso machine breaks, and nobody gets coffee. So you put up a sign: "Max 10 customers per minute." That sign is your rate limiter.

In software, a rate limiter controls how many requests a user, IP address, or API key can make in a given time window. Without one, a single bad actor — or even a well-meaning but buggy client — can bring your entire service down.

---

## Step 1: Clarify Requirements

Before designing anything, ask the interviewer these questions. They seem obvious but they completely change the design.

### What are we rate limiting?

- **Per user ID** — each logged-in user gets their own counter. Good for APIs that require authentication.
- **Per IP address** — used when users aren't logged in. Problem: shared IPs (corporate offices, universities) can get blocked unfairly.
- **Per API key** — common for B2B APIs. Each partner gets a key with its own quota.
- **Per endpoint** — `/search` might allow 100 req/min, `/payment` might allow only 5 req/min.
- **Global rate limiting** — limit total traffic to your service regardless of who's sending it.

### What should happen when a request is rate limited?

- Return HTTP **429 Too Many Requests** with a `Retry-After` header.
- Return a cached/stale response (graceful degradation).
- Queue the request and serve it when capacity opens up.
- Silently drop the request (bad for user experience, avoid this).

### Distributed or single server?

- **Single server**: simple, all state lives in memory. Works for small services.
- **Distributed**: state must be shared across multiple servers. Requires a centralized store like Redis. This is the interesting design problem.

### What's the scale?

- How many requests per second?
- How many unique users?
- How strict does accuracy need to be? (Slightly over-limiting is usually acceptable.)

---

## Step 2: Where to Place the Rate Limiter

Think of this like deciding where to put a security checkpoint at an airport. You could check passengers at the door, at the gate, or in the plane. Each option has trade-offs.

### Option 1: Client Side

The client throttles its own requests before even sending them.

**Analogy**: You tell yourself "I'll only call my friend 3 times a day." The decision lives with you.

- **Pro**: No server load at all.
- **Con**: You cannot trust the client. Any malicious or buggy client will ignore this. Never rely solely on client-side rate limiting.

### Option 2: Server Side (Within Application Code)

Your API server checks a rate limit counter before processing each request.

- **Pro**: Full control, can use business logic (VIP users, endpoint-specific limits).
- **Con**: In a distributed system with 10 servers, each server has its own counter. User could send 10x their limit by hitting all 10 servers.

### Option 3: Middleware Layer

A dedicated rate-limiting middleware sits in front of your application code — same process, but before the business logic runs.

- **Pro**: Cleaner separation of concerns. Easier to update limits without touching business logic.
- **Con**: Still lives on each server in a distributed setup unless middleware talks to shared state.

### Option 4: API Gateway (Recommended for Production)

The rate limiter lives outside your application entirely, at the API gateway (e.g., AWS API Gateway, Kong, NGINX, Cloudflare).

**Analogy**: The security checkpoint at the airport entrance — before you even reach the gates. All traffic flows through it.

- **Pro**: Language-agnostic. Protects all services behind it. Centralized configuration. Can offload SSL termination, auth, and rate limiting all in one place.
- **Con**: Single point of failure if not made highly available. Latency added to every request.

**Recommendation for interview**: Place the rate limiter at the API gateway layer, backed by a centralized Redis cluster for shared state.

---

## Step 3: Rate Limiting Algorithms

This is the most technically interesting part. There are five main algorithms. Each has a real-world analogy that makes the trade-offs immediately obvious.

---

### Algorithm 1: Token Bucket

**Analogy**: Imagine a bucket that gets refilled with water droplets at a fixed rate — say, 10 drops per second. Each time you want to make a request, you scoop out one drop. If the bucket is empty, you wait or get rejected. The bucket has a maximum capacity (burst limit), so you can "save up" tokens when traffic is light and spend them all in a burst.

**How it works**:
- A bucket holds a maximum of `capacity` tokens.
- Tokens are added at a fixed `refill_rate` (e.g., 10 tokens/second).
- Each incoming request consumes 1 token (or more for expensive operations).
- If no tokens are available, the request is rejected.

**Key properties**:
- Allows bursts up to bucket capacity.
- Smooth average rate over time.
- Very memory efficient — just two numbers per user (token count, last refill time).

**Best for**: APIs where occasional bursts are acceptable (e.g., a user downloads a file and needs several quick requests).

---

### Algorithm 2: Leaky Bucket

**Analogy**: A physical bucket with a hole in the bottom. Water (requests) pours in from the top at any rate. But water only drips out of the hole at a fixed rate. If you pour in too fast, it overflows and the excess is lost. Unlike Token Bucket, you can't "save up" — the outflow rate is always fixed.

**How it works**:
- Requests enter a FIFO queue.
- Requests are processed (leak out) at a fixed rate regardless of how fast they arrive.
- If the queue is full, new requests are rejected.

**Key properties**:
- Output rate is perfectly smooth (great for protecting downstream services).
- Cannot burst — even if you've been idle, you still can't send 50 requests at once.
- Adds latency because requests wait in queue.

**Best for**: Payment processing, where you want absolutely steady load on downstream services.

---

### Algorithm 3: Fixed Window Counter

**Analogy**: A bouncer at a club who resets his clicker every hour. The limit is 100 people per hour. At minute 59, 90 people enter. At minute 61 (the new hour), another 90 people enter. In two minutes, 180 people entered — nearly double the intended limit. The bouncer reset his counter at the boundary.

**How it works**:
- Divide time into fixed windows (e.g., 1-minute buckets: 12:00–12:01, 12:01–12:02).
- Each window gets its own counter.
- Counter resets at the start of each new window.

**Key properties**:
- Simple. Very cheap in memory (one counter per user per window).
- **Critical flaw**: Burst attacks at window boundaries. A user can exhaust the limit at the end of one window and the start of the next, effectively doubling their allowed rate for a brief period.

**Best for**: Rough rate limiting where burst attacks aren't a concern (e.g., limiting email sends per day).

---

### Algorithm 4: Sliding Window Log

**Analogy**: A security guard who remembers the exact timestamp of every person who entered in the last 60 minutes. Before letting you in, she scans her list and counts how many people entered in the last 60 minutes from right now — not from when the clock hit :00.

**How it works**:
- Store a sorted set of request timestamps for each user.
- When a new request arrives, remove all timestamps older than the window (e.g., 60 seconds ago).
- Count remaining timestamps. If count < limit, allow and add the new timestamp.
- If count >= limit, reject.

**Key properties**:
- Perfectly accurate — no boundary burst problem.
- **Expensive**: Must store every request timestamp. For a user making 1,000 req/min, that's 1,000 stored entries per user.
- Memory usage scales with request volume.

**Best for**: When accuracy is critical and volume is low (e.g., financial trading APIs).

---

### Algorithm 5: Sliding Window Counter

**Analogy**: A hybrid approach. Instead of remembering every single person's exact entry time, the guard uses the fixed window counts from the current and previous window, then estimates how much of the previous window's traffic "bleeds into" the current window based on elapsed time.

**How it works**:
- Maintain two counters: current window count and previous window count.
- When a request arrives at time `t` within a window of duration `W`:
  - Calculate overlap = `(W - t) / W` (what fraction of the previous window is still relevant)
  - Estimated count = `previous_count * overlap + current_count`
  - If estimated count < limit, allow the request.

**Key properties**:
- Much more memory efficient than Sliding Window Log (just two counters per user).
- More accurate than Fixed Window (handles boundary bursts).
- Slight approximation error, but typically within 0.003% — negligible in practice.

**Best for**: Production systems that need accuracy without the memory cost of full log storage. This is what many real systems (including Cloudflare) use.

---

### Comparison Table

| Algorithm | Memory Usage | Accuracy | Burst Handling | Complexity | Best Use Case |
|---|---|---|---|---|---|
| Token Bucket | Low (2 values) | Good | Allows bursts | Low | General APIs |
| Leaky Bucket | Medium (queue) | Good | No bursts | Low | Steady downstream load |
| Fixed Window Counter | Very Low (1 value) | Poor (boundary bug) | Allows double-burst | Very Low | Coarse daily limits |
| Sliding Window Log | High (all timestamps) | Perfect | No burst at boundary | Medium | Low-volume, high-accuracy |
| Sliding Window Counter | Low (2 values) | Very Good (~99.997%) | Handles boundary well | Medium | Production systems |

---

## Step 4: Implementation — Token Bucket with Redis

### Why Redis?

Redis is an in-memory key-value store. It's fast (sub-millisecond reads/writes), supports atomic operations, and supports distributed access. It's the industry standard for rate limiter state storage.

### Redis Data Structure

For Token Bucket, store a hash per user key:

```
Key: rate_limit:{user_id}
Fields:
  - tokens: current token count (float)
  - last_refill: Unix timestamp of last refill (float)
```

### Why Atomicity Matters

Here is the bug without atomicity:

1. Server A reads user's token count: 1 token remaining.
2. Server B reads user's token count: 1 token remaining.
3. Server A decides to allow the request (1 > 0), decrements to 0.
4. Server B decides to allow the request (1 > 0), decrements to -1.

Both requests are allowed even though there was only 1 token. This is a classic **race condition**. Without atomicity, your rate limiter is broken under concurrent load.

Redis solves this with **Lua scripts**. Redis executes a Lua script as a single atomic operation — no other command can interleave with it.

### Lua Script for Atomic Token Bucket Check

```lua
-- KEYS[1] = rate limit key (e.g., "rate_limit:user_123")
-- ARGV[1] = max tokens (capacity)
-- ARGV[2] = refill rate (tokens per second)
-- ARGV[3] = current timestamp (Unix seconds, float)
-- ARGV[4] = requested tokens (usually 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- Get current state
local data = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(data[1]) or capacity       -- Default to full bucket on first request
local last_refill = tonumber(data[2]) or now

-- Calculate how many tokens to add since last refill
local elapsed = now - last_refill
local new_tokens = elapsed * refill_rate

-- Refill the bucket (cap at capacity)
tokens = math.min(capacity, tokens + new_tokens)

-- Check if request can be served
if tokens >= requested then
    -- Allow: deduct tokens
    tokens = tokens - requested
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
    redis.call('EXPIRE', key, 3600)  -- Auto-expire idle users after 1 hour
    return {1, math.floor(tokens)}  -- {allowed=true, remaining_tokens}
else
    -- Reject: update refill time but don't deduct
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
    redis.call('EXPIRE', key, 3600)
    return {0, math.floor(tokens)}  -- {allowed=false, remaining_tokens}
end
```

### Python Code Example

```python
import redis
import time

class TokenBucketRateLimiter:
    def __init__(self, redis_client, capacity: int, refill_rate: float):
        """
        Args:
            redis_client: Redis connection
            capacity: Maximum tokens in bucket (burst limit)
            refill_rate: Tokens added per second
        """
        self.redis = redis_client
        self.capacity = capacity
        self.refill_rate = refill_rate

        # Load the Lua script once (sha = script hash for EVALSHA)
        self.script = self.redis.register_script(LUA_SCRIPT)  # LUA_SCRIPT = string above

    def is_allowed(self, user_id: str, requested_tokens: int = 1) -> tuple[bool, int]:
        """
        Check if the request is allowed.

        Returns:
            (allowed: bool, remaining_tokens: int)
        """
        key = f"rate_limit:{user_id}"
        now = time.time()

        result = self.script(
            keys=[key],
            args=[self.capacity, self.refill_rate, now, requested_tokens]
        )

        allowed = bool(result[0])
        remaining = int(result[1])
        return allowed, remaining


# FastAPI middleware example
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

limiter = TokenBucketRateLimiter(
    redis_client=redis.Redis(host='redis-cluster', port=6379),
    capacity=100,        # Burst up to 100 requests
    refill_rate=10.0     # Refill 10 tokens/second = 600 req/min sustained
)

async def rate_limit_middleware(request: Request, call_next):
    user_id = request.headers.get("X-User-ID") or request.client.host
    allowed, remaining = limiter.is_allowed(user_id)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Try again later."},
            headers={
                "X-RateLimit-Limit": "100",
                "X-RateLimit-Remaining": "0",
                "Retry-After": "1"
            }
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response
```

---

## Step 5: Distributed Rate Limiting — The Hard Part

When you have a single server, rate limiting is trivial — keep a counter in memory. The moment you scale to multiple servers, everything gets complicated.

### The Race Condition Problem

Imagine you have 3 servers (S1, S2, S3) and a user is allowed 10 requests per minute.

Without centralized state:
- S1 sees: 3 requests from this user
- S2 sees: 4 requests from this user
- S3 sees: 5 requests from this user
- Total actual: 12 requests — over limit, but nobody knows

Each server only knows about the requests it personally received. The user successfully bypasses the rate limit by having their requests spread across servers.

### Solution 1: Centralized Redis (Recommended)

All servers query the same Redis instance (or Redis Cluster) for rate limit state. Since Redis is single-threaded for command execution and we use Lua for atomicity, the counter is always accurate.

```
[Server 1] ---|
[Server 2] ---+---> [Redis Rate Limit Store] ---> accurate counter
[Server 3] ---|
```

**Trade-off**: Redis becomes a bottleneck. If Redis goes down, what do you do? Options:
- **Fail open**: Allow all requests (no rate limiting). Safer for user experience.
- **Fail closed**: Reject all requests. Safer for protecting your backend.
- Most production systems fail open with monitoring alerts.

### Solution 2: Redis Cluster

Shard the rate limit keys across multiple Redis nodes. Key `rate_limit:user_123` consistently maps to the same Redis node via consistent hashing. This removes the single-node bottleneck.

```
rate_limit:user_001 --> Redis Node A
rate_limit:user_002 --> Redis Node B
rate_limit:user_003 --> Redis Node C
```

### Solution 3: Sticky Sessions (Avoid if Possible)

Route all requests from a given user to the same application server (via load balancer). Then each server only needs in-memory state.

**Problem**: Defeats the purpose of horizontal scaling. If a server goes down, all users pinned to it lose their counters. Generally not recommended.

### Solution 4: Eventual Consistency with Gossip Protocol

Each server keeps its own counter locally and periodically syncs with other servers. Accept slight over-counting as a trade-off for lower latency and no Redis dependency. Used by systems like Lyft's Ratelimit service.

**Trade-off**: Slightly less accurate — a user might exceed their limit by a small factor briefly. Usually acceptable for non-critical rate limits.

---

## Step 6: API Response Headers

When you rate limit a request, you must tell the client what happened and what to expect. These are the standard headers:

| Header | Meaning | Example |
|---|---|---|
| `X-RateLimit-Limit` | Maximum requests allowed in the window | `100` |
| `X-RateLimit-Remaining` | Requests remaining in current window | `47` |
| `X-RateLimit-Reset` | Unix timestamp when the window resets | `1711929600` |
| `Retry-After` | Seconds to wait before retrying (on 429) | `30` |

### Why These Headers Matter

A good client (SDK, retry library) reads `Retry-After` and automatically backs off. Without it, clients will aggressively retry, creating a thundering herd: you reject them, they retry immediately, you reject them again, forever — amplifying the load on your system instead of reducing it.

### Exponential Backoff

Even with `Retry-After`, recommend clients use exponential backoff with jitter:

```
wait = base_delay * (2 ^ attempt) + random_jitter
```

Without jitter, all rate-limited clients retry at the same moment when the window resets — creating a burst that immediately rate-limits them again.

---

## Step 7: Edge Cases

### VIP Customers with Higher Limits

Store rate limit configuration per user tier in a database or config service:

```python
TIER_LIMITS = {
    "free": {"capacity": 100, "refill_rate": 1},
    "pro": {"capacity": 1000, "refill_rate": 10},
    "enterprise": {"capacity": 10000, "refill_rate": 100},
    "internal": {"capacity": float('inf'), "refill_rate": float('inf')},  # No limit
}

def get_limit_config(user_id: str) -> dict:
    tier = db.get_user_tier(user_id)
    return TIER_LIMITS.get(tier, TIER_LIMITS["free"])
```

### Rate Limit by Endpoint, Not Globally

Different endpoints have different costs. `/search` is cheap; `/video/transcode` is expensive.

Use composite keys:

```
rate_limit:{user_id}:{endpoint}
e.g., rate_limit:user_123:/api/search
      rate_limit:user_123:/api/video/transcode
```

Each endpoint gets its own bucket with its own capacity and refill rate.

### Graceful Degradation

If your rate limiter itself is overloaded or Redis is down:

1. **Cache the last known rate limit state** locally in the application server for a short TTL (e.g., 5 seconds). Serve from cache while Redis is recovering.
2. **Circuit breaker**: If Redis is down, fail open (allow requests) rather than blocking all traffic.
3. **Shadow mode**: Run the rate limiter in logging-only mode first. Count violations without actually blocking. Use this data to set appropriate limits before enforcing.

### Dry Run / Testing Mode

Rate limiters should have a mode where they check and log limits without actually enforcing them. This lets you tune limits in production before you start rejecting real customers.

---

## Step 8: Full Architecture Diagram

```
                        INTERNET
                           |
                    [Load Balancer]
                           |
              [API Gateway / Rate Limiter Layer]
               /           |           \
         Check limit    Check limit    Check limit
              |              |              |
              v              v              v
    [Redis Cluster — Centralized Rate Limit State]
      Node A        Node B        Node C
    (users 0-33%) (users 34-66%) (users 67-100%)
              |              |              |
              v              v              v
         Allow/Reject   Allow/Reject   Allow/Reject
              |
              v
    [Application Servers]
       S1   S2   S3
              |
              v
    [Backend Services]
    [Databases, Caches, etc.]

Headers returned to client:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 47
  X-RateLimit-Reset: 1711929600
  Retry-After: 30 (only on 429)

Config stored in:
  [Rate Limit Config DB] --> [API Gateway] (polled periodically)
  Stores: user_id -> tier -> limits per endpoint
```

---

## Interview Q&A

### Q1: Why is the Token Bucket algorithm preferred over Fixed Window Counter?

**Model Answer**: Fixed Window Counter has a critical flaw: burst attacks at window boundaries. If a user is allowed 100 requests per minute, they can send 100 requests at second 59 and another 100 requests at second 61 — effectively 200 requests in 2 seconds without violating any per-window rule. Token Bucket avoids this because the bucket refills continuously at a fixed rate, not in discrete resets. A user can burst up to their bucket capacity, but they can only do that if they've accumulated tokens over time. There's no magical reset moment to exploit. Additionally, Token Bucket naturally handles the concept of "expensive" requests by consuming multiple tokens for heavy operations, which Fixed Window can't express.

---

### Q2: How do you handle the race condition in a distributed rate limiter without using Lua scripts?

**Model Answer**: There are a few options, each with trade-offs. First, you can use Redis transactions (MULTI/EXEC), but these are optimistic — if two clients try to modify the same key simultaneously, one will fail and need to retry, adding latency. Second, you can use Redis atomic commands directly — for Fixed Window, `INCR` combined with `EXPIRE` is atomic for that specific pattern. Third, you can use a distributed lock (like Redlock), but locks add significant latency and complexity. The cleanest solution is Lua scripts: Redis executes Lua atomically as a single command, so no interleaving is possible. It's fast, it's correct, and it doesn't require optimistic retry loops. This is what most production systems use.

---

### Q3: How would you handle a "celebrity problem" in rate limiting?

**Model Answer**: The celebrity problem in rate limiting is when you have a small number of users who generate a vastly disproportionate amount of traffic. For example, a Twitter account with 50M followers whose every tweet gets thousands of API reads per second. Standard per-user limits treat them the same as everyone else, which might be too strict. There are a few approaches. First, tiered limits — celebrities or high-traffic accounts get pre-approved higher limits stored in a config service. Second, endpoint-specific limits — reading someone's tweets might be allowed at 10,000 req/min while writing is still limited strictly. Third, cache aggressively — popular users' data should be served from cache rather than hitting the rate limiter and database on every request. The rate limiter should sit in front of the cache layer so that even 429s come from cache metadata rather than hitting Redis on every rejected request.

---

### Q4: If Redis goes down, what happens to your rate limiter? What are your options?

**Model Answer**: This is a failure mode every production rate limiter must handle. You have two fundamental choices: fail open (allow all traffic) or fail closed (reject all traffic). Most customer-facing APIs fail open — it's better for a brief period to allow slightly more traffic than to show your users a wall of errors while Redis recovers. You implement this with a circuit breaker: if Redis calls start timing out or failing beyond a threshold, the rate limiter switches to a passthrough mode and sets an alert. To reduce the blast radius, you can add a local in-process cache on each application server that stores the last known rate limit state for each user key for a short TTL (e.g., 5–10 seconds). During a brief Redis outage, each server enforces limits independently using stale data, which is slightly inaccurate but better than nothing. If Redis recovers within the TTL window, you've never exposed unchecked traffic. You should also run Redis in a replicated cluster with automatic failover so that single-node failures don't bring down the whole system.

---

### Q5: How would you design a rate limiter that limits by both user AND by endpoint simultaneously?

**Model Answer**: You need a composite key structure. Instead of just `rate_limit:{user_id}`, the key becomes `rate_limit:{user_id}:{endpoint_id}`. Each user-endpoint combination gets its own independent bucket. This means a user can exhaust their `/api/search` limit without affecting their `/api/profile` limit. The configuration system needs to store limits per endpoint category (you wouldn't want individual config for every URL path), so you'd group endpoints: `search`, `write`, `payment`, `media`. When a request comes in, the middleware looks up which category the endpoint belongs to, fetches the corresponding limit config, and checks against the composite key in Redis. The total number of Redis keys is roughly `(number of active users) * (number of endpoint categories)`. For 10M active users and 10 categories, that's 100M keys — manageable in a Redis cluster but worth planning for. You'd also set TTLs on all keys so idle users' keys expire automatically.

---

*End of Day 23 — Rate Limiter*
