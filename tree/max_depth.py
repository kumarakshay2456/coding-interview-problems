"""
Maximum and Minimum Depth of Binary Tree

Max Depth: longest path from root to any leaf.
Min Depth: shortest path from root to the nearest leaf.

Both: Time O(n)  Space O(h)  where h = tree height
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ── Max Depth (DFS) ───────────────────────────────────────────────────────────

def max_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# ── Min Depth (BFS — optimal, stops at first leaf) ────────────────────────────
# DFS works too, but BFS finds the nearest leaf faster on skewed trees.

from collections import deque

def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    #        3
    #       / \
    #      9  20
    #        /  \
    #       15   7
    root = TreeNode(3,
                    TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))

    print(max_depth(root))   # 3
    print(min_depth(root))   # 2
