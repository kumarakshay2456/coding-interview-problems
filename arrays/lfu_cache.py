"""
LFU Cache (Least Frequently Used)

Eviction policy: when capacity is full, evict the key with the lowest access
frequency. Ties broken by LRU order (least recently used among the lowest freq).

All operations — get() and put() — must run in O(1).

Key insight: maintain two hash maps + one doubly-linked list per frequency bucket.
  key_map  : key  → (value, frequency)
  freq_map : freq → OrderedDict{key: None}   (insertion order = LRU order)
  min_freq : the current minimum frequency (to know which bucket to evict from)

Why OrderedDict per bucket?
  - O(1) add to end (most recent)
  - O(1) pop from front (least recent within bucket)
  - O(1) delete arbitrary key (on promotion)
"""

from collections import defaultdict, OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.key_map: dict[int, list] = {}          # key → [value, freq]
        self.freq_map: dict[int, OrderedDict] = defaultdict(OrderedDict)
        self.min_freq = 0

    # ── helpers ──────────────────────────────────────────────────────────────

    def _promote(self, key: int) -> None:
        """Increment key's frequency and move it to the next bucket."""
        val, freq = self.key_map[key]

        # Remove from current freq bucket
        del self.freq_map[freq][key]
        if not self.freq_map[freq]:          # bucket empty → clean up
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1           # min shifts up only if this bucket was the min

        # Insert into next freq bucket (most-recently-used end)
        new_freq = freq + 1
        self.freq_map[new_freq][key] = None
        self.key_map[key] = [val, new_freq]

    def _evict(self) -> None:
        """Remove the least-frequently (then least-recently) used key."""
        lfu_bucket = self.freq_map[self.min_freq]
        evict_key, _ = lfu_bucket.popitem(last=False)   # FIFO within bucket
        if not lfu_bucket:
            del self.freq_map[self.min_freq]
        del self.key_map[evict_key]

    # ── public API ────────────────────────────────────────────────────────────

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        self._promote(key)
        return self.key_map[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        if key in self.key_map:
            self.key_map[key][0] = value     # update value, then promote
            self._promote(key)
            return
        if len(self.key_map) >= self.cap:
            self._evict()
        # Insert new key at frequency 1
        self.key_map[key] = [value, 1]
        self.freq_map[1][key] = None
        self.min_freq = 1


# ── Comparison: FIFO Cache ────────────────────────────────────────────────────
# Evicts the oldest inserted item regardless of access frequency.
# No reordering on get — pure queue discipline.

class FIFOCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        return self.cache.get(key, -1)   # no reorder on access

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value      # update in place, no reorder
            return
        if len(self.cache) >= self.cap:
            self.cache.popitem(last=False)   # evict oldest inserted
        self.cache[key] = value


# ── Time-Based Key-Value Store (TTL / versioned cache) ────────────────────────
# set(key, value, timestamp): store value at timestamp
# get(key, timestamp): return the value with the largest ts ≤ timestamp

import bisect

class TimeMap:
    def __init__(self):
        self.store: dict[str, list] = defaultdict(list)   # key → [(ts, val)]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))   # timestamps always increasing

    def get(self, key: str, timestamp: int) -> str:
        entries = self.store.get(key, [])
        if not entries:
            return ""
        # Find rightmost ts ≤ timestamp
        idx = bisect.bisect_right(entries, (timestamp, chr(127))) - 1
        return entries[idx][1] if idx >= 0 else ""


# ── Tests ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── LFU Cache ──")
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    print(lfu.get(1))   # 1  (freq[1]=2, freq[2]=1)
    lfu.put(3, 3)       # evict key 2 (lowest freq=1)
    print(lfu.get(2))   # -1 (evicted)
    print(lfu.get(3))   # 3
    lfu.put(4, 4)       # freq[1]=2,freq[3]=2 → evict key 1 (LRU among freq=2)? No:
    print(lfu.get(1))   # -1
    print(lfu.get(3))   # 3
    print(lfu.get(4))   # 4

    print("\n── FIFO Cache ──")
    fifo = FIFOCache(2)
    fifo.put(1, 10)
    fifo.put(2, 20)
    print(fifo.get(1))  # 10
    fifo.put(3, 30)     # evict key 1 (oldest inserted)
    print(fifo.get(1))  # -1
    print(fifo.get(2))  # 20

    print("\n── Time Map ──")
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    print(tm.get("foo", 1))   # "bar"
    print(tm.get("foo", 3))   # "bar"
    tm.set("foo", "bar2", 4)
    print(tm.get("foo", 4))   # "bar2"
    print(tm.get("foo", 5))   # "bar2"
