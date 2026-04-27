"""
Consistent Hashing

Solves: when adding/removing a server, only K/N keys need to remapped
        (K = keys, N = nodes), instead of all keys.

How it works:
  - Servers and keys are placed on a ring (0 to 2^32-1).
  - A key is assigned to the first server clockwise from it on the ring.
  - Virtual nodes (replicas) spread load more evenly.

Time: O(log N) lookup, O(V log V) add/remove  where V = virtual nodes per server
Space: O(N * V)
"""

import hashlib
import bisect


class ConsistentHashRing:
    def __init__(self, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring: dict[int, str] = {}   # hash_position → server_name
        self.sorted_keys: list[int] = []

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_server(self, server: str) -> None:
        for i in range(self.virtual_nodes):
            vnode_key = f"{server}#vnode{i}"
            h = self._hash(vnode_key)
            self.ring[h] = server
            bisect.insort(self.sorted_keys, h)

    def remove_server(self, server: str) -> None:
        for i in range(self.virtual_nodes):
            vnode_key = f"{server}#vnode{i}"
            h = self._hash(vnode_key)
            if h in self.ring:
                del self.ring[h]
                self.sorted_keys.remove(h)

    def get_server(self, key: str) -> str | None:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_left(self.sorted_keys, h)
        if idx == len(self.sorted_keys):
            idx = 0    # wrap around the ring
        return self.ring[self.sorted_keys[idx]]

    def get_distribution(self, keys: list[str]) -> dict[str, int]:
        dist: dict[str, int] = {}
        for key in keys:
            server = self.get_server(key)
            if server:
                dist[server] = dist.get(server, 0) + 1
        return dist


if __name__ == "__main__":
    ring = ConsistentHashRing(virtual_nodes=150)

    ring.add_server("server-A")
    ring.add_server("server-B")
    ring.add_server("server-C")

    keys = [f"user:{i}" for i in range(1000)]
    dist = ring.get_distribution(keys)
    print("Distribution across 3 servers:")
    for server, count in sorted(dist.items()):
        print(f"  {server}: {count} keys")

    # Add a new server — only a fraction of keys remapped
    ring.add_server("server-D")
    dist2 = ring.get_distribution(keys)
    moved = sum(
        1 for k in keys
        if ring.get_server(k) != (lambda s: s)(ring.get_server(k))
    )
    print("\nDistribution after adding server-D:")
    for server, count in sorted(dist2.items()):
        print(f"  {server}: {count} keys")

    print(f"\nLookup examples:")
    for k in ["user:42", "user:100", "user:999"]:
        print(f"  {k} → {ring.get_server(k)}")
