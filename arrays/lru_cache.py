"""
LRU Cache — O(1) get and put using a doubly linked list + hashmap.

The list keeps insertion/access order: most recent at tail, least recent at head.
On every get/put, the accessed node moves to tail.
On capacity overflow, the head node (least recently used) is evicted.

Interview tip: Python's OrderedDict gives the same result in fewer lines,
but interviewers usually want the manual DLL implementation.
"""

from collections import OrderedDict


# ── Approach 1: Manual Doubly Linked List + HashMap ───────────────────────────

class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        # sentinel head and tail — never removed
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._move_to_tail(self.cache[key])
        return self.cache[key].val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key].val = value
            self._move_to_tail(self.cache[key])
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._insert_at_tail(node)
            if len(self.cache) > self.capacity:
                lru = self.head.next          # node just after sentinel head
                self._remove(lru)
                del self.cache[lru.key]

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_tail(self, node: Node) -> None:
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def _move_to_tail(self, node: Node) -> None:
        self._remove(node)
        self._insert_at_tail(node)


# ── Approach 2: OrderedDict (cleaner, same complexity) ────────────────────────

class LRUCacheOrderedDict:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # remove oldest (leftmost)


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for CacheClass in [LRUCache, LRUCacheOrderedDict]:
        print(f"\n{CacheClass.__name__}")
        cache = CacheClass(2)
        cache.put(1, 1)
        cache.put(2, 2)
        print(cache.get(1))       # 1
        cache.put(3, 3)           # evicts key 2
        print(cache.get(2))       # -1 (evicted)
        cache.put(4, 4)           # evicts key 1
        print(cache.get(1))       # -1 (evicted)
        print(cache.get(3))       # 3
        print(cache.get(4))       # 4
