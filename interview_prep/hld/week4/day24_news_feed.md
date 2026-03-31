# Day 24 — HLD Problem: News Feed System (like Twitter/Instagram)

---

## What Is a News Feed?

When you open Twitter, Instagram, or Facebook, the first thing you see is a feed — a personalized list of posts from people you follow. Building this at scale is one of the most well-known system design problems because it sits at the intersection of massive read volume, complex write patterns, real-time requirements, and personalization.

Think of it like a newspaper — except instead of one newspaper for millions of people, you're printing a custom newspaper for each of 300 million people, several times a day, in under 200 milliseconds.

---

## Step 1: Clarify Requirements

Ask the interviewer these questions before drawing a single box on the whiteboard.

### What types of posts exist?

- Text only (tweets)
- Text + images (Instagram posts)
- Text + video (TikTok, Reels)
- Reposts / Retweets (content from someone else shared by a user)
- Stories (ephemeral, expire after 24 hours)

For this design, we'll focus on text and image posts (the Twitter/Instagram core case).

### Follower model or friend model?

- **Follower model (Twitter/Instagram)**: Asymmetric. I can follow you without you following me back. A celebrity might have 50M followers but follow 200 people.
- **Friend model (Facebook)**: Symmetric. Both parties must accept to see each other's posts.

These models have dramatically different write fan-out patterns. We'll design for the follower model.

### Feed ordering: Chronological or ranked?

- **Chronological**: Newest posts first. Simple to compute. Early Twitter, early Instagram.
- **Ranked**: ML model scores each post for each user based on predicted engagement. Modern Twitter ("For You"), Instagram, TikTok.

We'll design for chronological first, then discuss ranking as an optimization.

### Scale requirements:

- 300M Daily Active Users (DAU)
- Users check feed ~5 times per day
- ~1M posts published per day
- Users follow an average of 300 people
- Read-heavy system (far more reads than writes)

---

## Step 2: Capacity Estimation

Getting numbers on paper early forces you to make real design decisions. An architecture that works for 1,000 users fails at 300M.

### Read Volume

```
300M DAU * 5 feed loads/day = 1.5 Billion feed loads/day
1.5B / 86,400 seconds = ~17,400 feed reads/second
Peak (2x average) = ~35,000 reads/second
```

### Write Volume

```
1M posts/day / 86,400 seconds = ~12 posts/second
Peak (2x) = ~24 posts/second
```

This confirms the system is **read-heavy** — reads outnumber writes by roughly 1,500:1. This fundamentally shapes every design decision: optimize aggressively for reads, accept more complexity on the write path.

### Fan-out Volume

When someone with 1M followers posts, their post needs to reach 1M feed caches:

```
1M posts/day * 300 average followers = 300M fan-out writes/day
= 3,472 fan-out writes/second on average
Peak celebrity post = 1M fan-out writes in seconds
```

### Storage for Posts

```
Text post: ~300 bytes average
1M posts/day * 300 bytes = 300 MB/day of raw text
300 MB * 365 days = ~110 GB/year (text only, trivial)

Images: average 500KB per post, 50% of posts have images
500,000 posts/day * 500KB = 250 GB/day of images
250 GB * 365 = ~91 TB/year of images
```

Images dominate storage. This tells us we need an object storage service (S3) with a CDN, not a database, for media.

### Feed Cache Size

```
Each user's feed = 200 posts * 8 bytes (post ID) = 1.6 KB per user
300M users * 1.6 KB = 480 GB of feed cache (if we cache everyone)
```

480 GB is expensive but feasible for a Redis cluster. In practice, we only cache active users' feeds.

---

## Step 3: Define APIs

Keep APIs simple and REST-like. Define the contract before the internals.

### Post a Tweet / Create a Post

```
POST /v1/posts
Headers: Authorization: Bearer {token}
Body: {
  "content": "Hello world",
  "media_ids": ["img_abc123"],   // optional, pre-uploaded
  "reply_to_post_id": null       // optional, for replies
}
Response 201: {
  "post_id": "post_xyz789",
  "created_at": "2026-03-31T10:00:00Z"
}
```

### Get News Feed

```
GET /v1/feed?cursor={cursor}&limit={limit}
Headers: Authorization: Bearer {token}
Response 200: {
  "posts": [ ...post objects... ],
  "next_cursor": "cursor_abc123",  // for pagination
  "has_more": true
}
```

### Follow a User

```
POST /v1/users/{user_id}/follow
Headers: Authorization: Bearer {token}
Response 200: { "following": true }
```

### Like a Post

```
POST /v1/posts/{post_id}/like
Headers: Authorization: Bearer {token}
Response 200: { "liked": true, "total_likes": 1842 }
```

---

## Step 4: The Core Design Decision — Push vs. Pull vs. Hybrid

This is the most important section. Every other design decision flows from this one. Interviewers specifically want to see that you can articulate the trade-offs here.

---

### Option A: Pull Model (Fan-out on Read)

**Analogy**: Instead of the newspaper being delivered to your door each morning, you drive to the newsstand, pick up a paper from each person you follow, and read them all yourself.

**How it works**:
- When a user opens their feed, the system queries the database for recent posts from everyone they follow.
- The feed is computed fresh at read time.

```
User opens feed
  --> Feed Service queries Follow table: "Who does user_123 follow?"
  --> Gets list of 300 followed user IDs
  --> Queries Post table: "Get latest 20 posts from these 300 users"
  --> Merges and sorts by timestamp
  --> Returns feed
```

**Pros**:
- Write path is simple: just store the post, no fan-out needed.
- No wasted work — only compute feed for users who actually open the app.
- Celebrities' posts are just another post in a database.

**Cons**:
- Read path is slow. Querying posts from 300 users and merging them on every feed load is expensive — especially at 35,000 reads/second.
- Heavy database load on reads.
- Latency increases with number of followed users.

**When to use**: Small scale, or when writes are much more expensive than reads.

---

### Option B: Push Model (Fan-out on Write)

**Analogy**: When a newspaper writes a story, they print and deliver a copy to every subscriber's doorstep before they wake up. Reading is instant — it's already there.

**How it works**:
- When a user posts, the system immediately pushes the post ID to every follower's pre-computed feed cache.
- When a user opens their feed, you just read their pre-computed feed from cache.

```
User posts a tweet
  --> Post stored in Post table
  --> Fan-out Service reads Follow table: "Who follows user_123?"
  --> Gets 300 follower IDs
  --> Writes post_id to feed cache for all 300 followers
  --> Feed cache is now pre-populated

User opens feed
  --> Read pre-computed feed from Redis
  --> Instant. No computation needed.
```

**Pros**:
- Feed reads are extremely fast (just a cache lookup).
- Read path is simple and consistent regardless of following count.
- Perfect for read-heavy systems.

**Cons**:
- **The celebrity problem**: A user with 50M followers posts. The system must write to 50M feed caches synchronously or near-synchronously. That's catastrophic. If it's done synchronously, the post takes minutes to appear. If async, the message queue gets flooded.
- Wasted work: Users who haven't opened the app in a week still get their feed updated.
- More storage: Every follower stores the post_id in their feed cache.

---

### Option C: Hybrid Model (Recommended — What Real Systems Use)

**Analogy**: The newspaper delivers to regular subscribers proactively. But for the President's speech (which everyone wants), they don't try to pre-print 330M copies — they put it on TV (pull) and let people tune in.

**How it works**:
- **For regular users** (< 1M followers): Use Push model. Fan-out happens asynchronously to all followers' feed caches.
- **For celebrities** (> 1M followers, configurable threshold): Do NOT fan-out. Instead, when a regular user opens their feed, the system:
  1. Reads from their pre-computed feed cache (contains posts from regular users they follow)
  2. Fetches the latest posts from any celebrities they follow directly from the Post table
  3. Merges the two results

This means celebrity posts are pulled at read time, but only their posts — not the posts of 300 regular users.

```python
def get_feed(user_id):
    # Step 1: Get pre-computed feed for posts from regular follows
    cached_feed = redis.get_feed(user_id)  # Fast

    # Step 2: Get celebrity follows
    celebrities = db.get_celebrity_follows(user_id)  # Cached in user's profile

    # Step 3: Fetch latest posts from celebrities directly
    celebrity_posts = []
    for celebrity_id in celebrities:
        posts = db.get_recent_posts(celebrity_id, limit=20)  # Hot in DB cache
        celebrity_posts.extend(posts)

    # Step 4: Merge and sort
    all_posts = merge_and_sort(cached_feed, celebrity_posts)
    return all_posts[:20]
```

**Why celebrity posts are still fast even on pull**:
- Celebrities' posts are frequently accessed, so they're hot in database caches (read replicas, Redis object cache).
- You're only fetching from a handful of celebrities, not 300 regular users.

**Celebrity threshold**: Usually set at 1M followers, but it's configurable. You can also dynamically adjust based on load.

---

## Step 5: Data Models

### User Table (SQL — PostgreSQL)

```sql
CREATE TABLE users (
    user_id      BIGINT PRIMARY KEY,    -- Snowflake ID for global uniqueness
    username     VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    bio          TEXT,
    follower_count   INT DEFAULT 0,     -- Denormalized for fast reads
    following_count  INT DEFAULT 0,
    is_celebrity BOOLEAN DEFAULT FALSE, -- Pre-computed flag (follower_count > 1M)
    created_at   TIMESTAMP DEFAULT NOW()
);
```

### Post/Tweet Table (SQL — PostgreSQL with partitioning)

```sql
CREATE TABLE posts (
    post_id      BIGINT PRIMARY KEY,    -- Snowflake ID (time-sortable)
    user_id      BIGINT NOT NULL REFERENCES users(user_id),
    content      TEXT,
    media_ids    TEXT[],                -- Array of S3 object keys
    like_count   INT DEFAULT 0,         -- Denormalized counter
    repost_count INT DEFAULT 0,
    reply_count  INT DEFAULT 0,
    reply_to_id  BIGINT REFERENCES posts(post_id),  -- NULL if original post
    created_at   TIMESTAMP DEFAULT NOW(),
    is_deleted   BOOLEAN DEFAULT FALSE  -- Soft delete

    -- Partition by created_at (monthly) for efficient range queries
) PARTITION BY RANGE (created_at);

-- Index for user's posts (for fan-out and profile page)
CREATE INDEX idx_posts_user_created ON posts (user_id, created_at DESC);
```

### Follow/Friendship Table (SQL)

```sql
CREATE TABLE follows (
    follower_id  BIGINT NOT NULL,       -- The person who follows
    followee_id  BIGINT NOT NULL,       -- The person being followed
    created_at   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (follower_id, followee_id)
);

-- Index for "who follows user X" (needed for fan-out)
CREATE INDEX idx_follows_followee ON follows (followee_id, follower_id);

-- Index for "who does user X follow" (needed for feed construction)
CREATE INDEX idx_follows_follower ON follows (follower_id, followee_id);
```

**Note on scale**: The follows table for Twitter has billions of rows. Consider sharding by `followee_id` for fan-out queries and by `follower_id` for feed-construction queries. You may need two separate tables or a graph database (like Cassandra for fan-out).

### Feed Cache (Redis Sorted Set)

Redis Sorted Sets are perfect for feeds. The **score** is the Unix timestamp of the post, and the **member** is the post ID. This gives you automatic chronological ordering with O(log N) inserts and O(log N) range queries.

```
Key: feed:{user_id}
Type: Sorted Set (ZSET)
Score: Unix timestamp (for ordering)
Member: post_id

Operations:
  ZADD feed:user_123 1711929600 post_xyz789    # Add post to feed
  ZREVRANGE feed:user_123 0 19                  # Get latest 20 posts
  ZREMRANGEBYRANK feed:user_123 200 -1           # Trim to 200 posts max
  ZCARD feed:user_123                            # Count posts in feed
```

Each user's feed sorted set is capped at ~200–500 post IDs (8 bytes each). Reading the feed means a single Redis `ZREVRANGE` command — no database joins.

---

## Step 6: Component Design

### Post Service

Handles creating, reading, updating, and deleting posts.

- Validates content (length, spam detection).
- Assigns a Snowflake ID (time-sortable unique ID).
- Stores the post in the Posts database.
- If post has media, stores media metadata and returns pre-signed S3 URL for media upload.
- Publishes a `PostCreated` event to the message queue (Kafka topic: `post-events`).

### Feed Generation Service

Reads a user's feed from Redis. Falls back to database if cache miss.

```
Cache hit (99% of cases):
  ZREVRANGE feed:{user_id} 0 19 → returns post IDs
  MGET post:{id} for each post_id → returns post data (from another Redis layer)
  Return to client

Cache miss:
  Query Post table directly (expensive, should be rare)
  Rebuild feed cache for this user
  Return to client
```

### Fan-out Service (The Core Write Path)

Triggered by `PostCreated` events from Kafka. This is where the hybrid model lives.

```
1. Consume PostCreated event { post_id, author_id, timestamp }
2. Look up author's follower count
   - If follower_count < 1M (regular user):
       a. Query Follow table: get all follower IDs (can be millions of rows for popular but not celebrity)
       b. For each follower:
            ZADD feed:{follower_id} {timestamp} {post_id}
            ZREMRANGEBYRANK feed:{follower_id} 200 -1  (trim old posts)
   - If follower_count >= 1M (celebrity):
       Skip fan-out. Feed reads will pull celebrity posts dynamically.
3. Publish notification events for mentions, hashtags, etc.
```

**Why Kafka and not synchronous?**: Fan-out for a user with 500K followers would take seconds synchronously, and block the Post Service. Kafka decouples the write from the fan-out. The post appears to the author instantly; followers see it within seconds as the fan-out processes.

**Kafka consumer groups**: Run multiple Fan-out Service instances as a consumer group. Each instance processes a partition. Scale horizontally for higher throughput.

### Notification Service

Consumes events and sends push notifications, emails, in-app alerts.

- Subscribes to Kafka topics: `post-events`, `like-events`, `follow-events`
- Filters by user notification preferences (in a NoSQL store for fast reads)
- Calls push notification services (APNs for iOS, FCM for Android)
- Rate limits notifications to avoid spamming users

### Media Service (S3 + CDN)

Images and videos are never stored in your database or served from your application servers.

```
Upload flow:
  Client --> Post Service: "I want to upload a photo"
  Post Service --> Media Service: generate pre-signed S3 URL
  Media Service --> Client: {upload_url: "https://s3.amazonaws.com/..."}
  Client --> S3: PUT image directly (bypasses your servers entirely)
  S3 --> Media Processing Service: trigger image resizing, thumbnail generation
  Media Processing --> Post Service: "media_id abc123 is ready"

Serve flow:
  Client requests image
  --> CDN edge node (geographically close to user)
  --> CDN checks cache (hit 95%+)
  --> Serve from CDN edge (sub-100ms globally)
  --> CDN cache miss: fetch from S3 origin, cache at edge
```

**Why CDN?**: Serving images from S3 directly for 1.5B feed loads/day would cost a fortune and be slow. A CDN caches images at edge nodes globally, serving from the closest server to the user.

---

## Step 7: Feed Ranking

### Chronological Ordering

Simple: sort by `created_at` descending. This is what Redis Sorted Sets give you for free (score = timestamp).

**Problem**: Chronological feeds are dominated by high-volume posters. If someone you follow posts 50 times a day, they push out everyone else. Users miss posts from people they actually care about.

### ML-Based Ranking

Modern feed systems (Twitter's "For You", Instagram's main feed) use a machine learning ranking model to score posts for each user.

**Signals used in ranking**:

| Signal | Examples |
|---|---|
| Engagement signals | How often you like, comment, repost this author |
| Content signals | Post type (video scores higher), hashtags, language |
| Recency | Newer posts get a time-decay boost |
| Social signals | People you follow engaging with this post |
| User behavior | How long you dwell on similar posts (session features) |
| Negative signals | "See less like this", mute, unfollow after seeing post |

**Two-stage ranking**:

1. **Candidate generation**: Fast retrieval of ~1,000 candidate posts (from feed cache, trending, social graph). Cannot rank all posts ever made.
2. **Ranking model**: Score each candidate (neural network or gradient boosted tree). Return top 20.

**Why not rank in Redis?**: You can't easily rank by ML score in Redis Sorted Sets. Options:
- Score = ML score instead of timestamp (updated periodically by a ranking job).
- Use Redis as candidate pool, do ranking in application layer before returning.
- Use a vector database or specialized ranking service for complex ranking.

---

## Step 8: Optimizations

### Caching Hot Feeds

Not all feeds are equal. A user with 10M followers will have their own feed loaded by... just them. But the fan-out means their 10M followers all need their feeds updated when this person posts. The hot path is fan-out and feed reads for active users.

- **L1 cache**: Application server in-memory cache for the most recently loaded feeds (LRU, tiny — just last ~1000 feeds per server).
- **L2 cache**: Redis cluster for all active users' feeds (TTL = 24 hours, refresh on access).
- **L3**: Database (cold path, only on cache miss).

### Preloading Feeds

When a user is inactive for a while, their feed cache expires. When they open the app, they hit a cold start — the feed must be rebuilt from scratch. This is slow.

**Preloading**: A background job identifies users who are likely to return soon (e.g., based on historical patterns — "this user checks the app every morning at 8am"). Pre-compute and cache their feed before they open the app.

### Pagination with Cursors (Not Offset)

Never paginate with `OFFSET`. It gets slower as offset increases — the database scans all skipped rows.

**Cursor-based pagination**:

```
First request: GET /v1/feed
Response: {
  "posts": [...20 posts...],
  "next_cursor": "post_id:1711929400"  // ID of last post returned
}

Next request: GET /v1/feed?cursor=post_id:1711929400
  --> Redis: ZREVRANGEBYSCORE feed:{user_id} {cursor_score} -inf LIMIT 0 20
Response: {
  "posts": [...next 20 posts...],
  "next_cursor": "post_id:1711928900"
}
```

Cursor-based pagination is O(log N) in Redis Sorted Sets regardless of page depth. It also handles real-time inserts gracefully: new posts inserted at the top don't shift your cursor position.

### Handling Inactive Users

Don't waste fan-out on users who haven't opened the app in 30 days. During fan-out, skip users whose `last_active_at` is older than your threshold. When they return, compute their feed on demand (pull model fallback).

This dramatically reduces the fan-out queue depth for viral posts.

---

## Step 9: Full Architecture Diagram

```
                              INTERNET
                                 |
                         [CDN — Images/Video]
                                 |
                      [Load Balancer (L7)]
                                 |
              ┌──────────────────┼──────────────────┐
              |                  |                  |
       [Post Service]    [Feed Service]    [User Service]
              |                  |                  |
              |           [Redis Cluster]            |
              |        (Feed Sorted Sets)            |
              |                  |                  |
       [Kafka — post-events]     |            [PostgreSQL]
              |                  |            (users, follows,
       [Fan-out Service]         |              posts metadata)
        (consumer group)         |
              |                  |
        ┌─────┴─────┐            |
        |           |            |
   [Follow DB]  [Redis]          |
   (Cassandra)  (feed cache)     |
   Who follows  update all       |
   celebrity X? follower feeds   |
                                 |
       [Notification Service] ───┘
              |
    [APNs / FCM / Email]

Media path:
  Client --> [Media Service] --> [S3 Origin]
  Client reads: [CDN Edge] --> [S3] (cache miss only)
  [S3 Event] --> [Image Processing Lambda] --> thumbnails, resizing

Ranking (for ML feeds):
  [Feed Service] --> [Candidate Pool (Redis)] --> [Ranking Service (ML model)]
                                                        |
                                               [Ranked feed response]

Data stores:
  PostgreSQL: users, posts, follows (primary source of truth)
  Cassandra: follower/following lists (optimized for fan-out scale)
  Redis Cluster: feed sorted sets, post cache, session cache
  S3: all media storage
  CDN (CloudFront/Akamai): media delivery globally
  Kafka: async event bus (post events, notification events)
```

---

## Interview Q&A

### Q1: Why do you use a hybrid Push/Pull model instead of pure Push for a news feed?

**Model Answer**: Pure Push (fan-out on write) breaks catastrophically when accounts with millions of followers post. If a celebrity with 50M followers tweets, you'd need to write to 50M Redis keys synchronously or near-synchronously — flooding your message queue, delaying the fan-out, and wasting enormous compute and storage on users who may be inactive. The hybrid model solves this elegantly: for regular users (under a threshold, say 1M followers), we fan-out to all followers' feed caches asynchronously via Kafka — this is fast and the queue processes at scale. For celebrities, we skip the fan-out entirely. Instead, when any of their followers opens the feed, we do a targeted pull of just the celebrity's recent posts directly from the posts database. Since celebrities' posts are hit extremely frequently by millions of users, these rows are hot in the database cache (read replicas, Redis object cache) and return in milliseconds. The user experiences no slowdown, the fan-out queue stays manageable, and the system is resilient to viral moments.

---

### Q2: Why use Redis Sorted Sets for the feed cache, and what's the data structure doing?

**Model Answer**: A Redis Sorted Set stores members with an associated float score, ordered by that score. For a news feed, each member is a post ID (8 bytes, very small), and the score is the Unix timestamp of the post. This gives us automatic chronological ordering for free. We can retrieve the latest 20 posts with a single `ZREVRANGE` command — O(log N + K) where K is the number of posts returned. We cap each user's feed at ~200 post IDs by trimming with `ZREMRANGEBYRANK`, so each user's feed sorted set costs at most 200 * 8 bytes = 1.6 KB. For 100M active users, that's only 160 GB — very manageable in a Redis cluster. Adding a new post to a feed is `ZADD` — O(log N). There's no scanning, no joins, no sorting at read time. The structure is perfect for this use case. One subtlety: if we use ML ranking, we'd update the score field to reflect the ranking score instead of the timestamp, and re-run ranking periodically as user behavior data changes.

---

### Q3: How would you handle someone who follows 5,000 accounts — their feed construction could be complex?

**Model Answer**: In the pure Pull model (fan-out on read), following 5,000 accounts is devastating — you'd need to query posts from 5,000 users and merge them, which is both slow and database-intensive. The Push model makes this irrelevant: every post from every followed account is already written to this user's feed cache asynchronously. Opening the feed is just `ZREVRANGE feed:{user_id} 0 19` — a single Redis command that returns 20 post IDs in microseconds, regardless of whether they follow 50 or 5,000 people. The work happens at write time (fan-out), distributed across all posts as they're created, rather than at read time when the user is waiting. The trade-off is that following 5,000 people means this user is included in up to 5,000 different fan-out operations per post, but since fan-out is async via Kafka, this doesn't affect the posting user's experience. The one thing we must handle: cap the feed cache size (e.g., at 500 posts). If someone follows very active accounts, we trim old posts from their cache regularly. When they scroll past the cache boundary, we fall back to database queries for older posts — acceptable because deep scrolling is rare.

---

### Q4: How do you handle "delete a post" across a distributed feed system?

**Model Answer**: This is a subtle problem. In the Push model, when a user deletes a post, that post ID may already be written to thousands or millions of followers' feed caches. You can't efficiently remove a post ID from millions of Redis Sorted Sets — it would take as long as the original fan-out. The solution is lazy deletion: instead of removing the post ID from all feed caches immediately, mark the post as deleted in the Posts database (soft delete — set `is_deleted = true`). When the Feed Service retrieves post IDs from a user's feed cache and fetches the actual post data, it filters out any posts where `is_deleted = true`. The deleted post may briefly appear in the list of post IDs in cache, but it never returns actual content to the user. The cached post IDs naturally expire as newer posts push them out (we trim the sorted set to 200 entries). For hard deletion requirements (legal compliance, GDPR), you run a background cleanup job to remove the post from all caches and permanent storage, and you track which users had this post in their cache by maintaining a reverse index during fan-out.

---

### Q5: How would you scale the Fan-out Service to handle a viral post getting 100M impressions?

**Model Answer**: When a post from a user with 100M followers goes viral, the fan-out requirement is enormous — writing to 100M feed caches. With a celebrity threshold, we skip the fan-out entirely for this user, so the fan-out itself isn't the problem. But even for a "regular" user who becomes suddenly viral, the system must be resilient. First, since fan-out is async via Kafka, the posting user's experience is unaffected — the post is stored immediately and their own feed shows it. The fan-out queue just grows. Second, fan-out workers scale horizontally — we can auto-scale the consumer group to deploy more Fan-out Service instances that consume from the Kafka partitions in parallel. Third, we can prioritize the fan-out queue by user tier: if you're approaching celebrity status, the system can dynamically reclassify you and switch to the pull model on the fly. Fourth, for the celebrity's followers reading their feed during the viral moment, caching is critical — the celebrity's recent posts should be in a hot Redis object cache so pull fetches are fast. The underlying insight is that Kafka acts as a buffer absorbing bursty write load, and the fan-out eventually catches up — the SLA is not "all 100M followers see it in 1 second" but "all followers see it within a reasonable time window" (e.g., 30 seconds).

---

*End of Day 24 — News Feed System*
