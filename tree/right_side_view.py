"""
Binary Tree Right Side View

Return the values of nodes visible when looking at the tree from the right side
(i.e., the rightmost node at each level).

Approach 1 — BFS: last node in each level's queue is the answer.
Approach 2 — DFS: visit right child first; first node seen at each depth is the answer.

Time: O(n)  Space: O(w) BFS / O(h) DFS
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ── BFS approach ──────────────────────────────────────────────────────────────

def right_side_view_bfs(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:       # last node in this level = rightmost
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result


# ── DFS approach (right subtree first) ────────────────────────────────────────

def right_side_view_dfs(root: TreeNode | None) -> list[int]:
    result: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth == len(result):          # first visit at this depth
            result.append(node.val)
        dfs(node.right, depth + 1)        # right first
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result


if __name__ == "__main__":
    #        1
    #       / \
    #      2   3
    #       \   \
    #        5   4
    root = TreeNode(1,
                    TreeNode(2, None, TreeNode(5)),
                    TreeNode(3, None, TreeNode(4)))

    print(right_side_view_bfs(root))   # [1, 3, 4]
    print(right_side_view_dfs(root))   # [1, 3, 4]

    # Left-skewed tree — left node is only visible from right
    root2 = TreeNode(1, TreeNode(2))
    print(right_side_view_dfs(root2))  # [1, 2]
