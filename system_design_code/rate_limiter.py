"""
Rate Limiter — Two implementations

1. Token Bucket   — allows short bursts; tokens refill at fixed rate.
2. Sliding Window — more precise; counts requests in a rolling time window.

Both are asked in system design rounds AND sometimes as coding questions.

Time: O(1) per request for both.
"""

import time
import threading
from collections import deque


# ── 1. Token Bucket ───────────────────────────────────────────────────────────
# capacity  = max tokens (= max burst size)
# rate      = tokens added per second
# Thread-safe with a lock.

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, rate: float):
        self.capacity = capacity
        self.rate = rate                  # tokens per second
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now


# ── 2. Sliding Window Counter ─────────────────────────────────────────────────
# Stores timestamps of each request. Drops timestamps older than window_size.
# max_requests = allowed requests per window.

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: deque[float] = deque()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            cutoff = now - self.window
            while self.requests and self.requests[0] < cutoff:
                self.requests.popleft()
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False


# ── 3. Fixed Window Counter ───────────────────────────────────────────────────
# Simplest: count requests in the current fixed window.
# Weakness: allows 2x burst at window boundaries.

class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self.count = 0
        self.window_start = time.monotonic()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            if now - self.window_start >= self.window:
                self.count = 0
                self.window_start = now
            if self.count < self.max_requests:
                self.count += 1
                return True
            return False


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Token Bucket (5 capacity, 2 tokens/sec) ──")
    limiter = TokenBucketRateLimiter(capacity=5, rate=2)
    results = [limiter.allow() for _ in range(7)]
    print(results)   # First 5 True, last 2 False (burst exhausted)

    print("\n── Sliding Window (3 req / 1 sec) ──")
    sw = SlidingWindowRateLimiter(max_requests=3, window_seconds=1.0)
    print([sw.allow() for _ in range(5)])   # [T, T, T, F, F]
    time.sleep(1.1)
    print(sw.allow())   # True (window reset)

    print("\n── Fixed Window (3 req / 1 sec) ──")
    fw = FixedWindowRateLimiter(max_requests=3, window_seconds=1.0)
    print([fw.allow() for _ in range(4)])   # [T, T, T, F]
