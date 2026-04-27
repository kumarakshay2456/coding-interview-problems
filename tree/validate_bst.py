"""
Validate Binary Search Tree

A valid BST satisfies: for every node, ALL nodes in its left subtree are
strictly less than it, and ALL nodes in the right subtree are strictly greater.

Common mistake: only comparing a node with its direct children.
Correct approach: pass down a valid (min, max) range for each node.

Time: O(n)  Space: O(h)

Also covers: Kth Smallest Element in a BST (inorder traversal gives sorted order).
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ── Validate BST ──────────────────────────────────────────────────────────────

def is_valid_bst(root: TreeNode | None) -> bool:
    def validate(node: TreeNode | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return (validate(node.left, lo, node.val) and
                validate(node.right, node.val, hi))

    return validate(root, float("-inf"), float("inf"))


# ── Kth Smallest Element in BST ───────────────────────────────────────────────
# Inorder traversal of a BST produces values in ascending order.
# Stop early at the kth element.
# Time: O(h + k)  Space: O(h)

def kth_smallest(root: TreeNode | None, k: int) -> int:
    count = 0
    result = 0

    def inorder(node: TreeNode | None) -> None:
        nonlocal count, result
        if node is None:
            return
        inorder(node.left)
        count += 1
        if count == k:
            result = node.val
            return
        inorder(node.right)

    inorder(root)
    return result


# Iterative version (more interview-friendly — no recursion limit risk)
def kth_smallest_iterative(root: TreeNode | None, k: int) -> int:
    stack = []
    count = 0
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        count += 1
        if count == k:
            return node.val
        node = node.right
    return -1


if __name__ == "__main__":
    #     2
    #    / \
    #   1   3
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    print(is_valid_bst(root))   # True

    #     5
    #    / \
    #   1   4
    #      / \
    #     3   6
    root2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    print(is_valid_bst(root2))  # False (4 is in right subtree of 5 but 4 < 5)

    print("\n── Kth Smallest ──")
    #       3
    #      / \
    #     1   4
    #      \
    #       2
    bst = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    print(kth_smallest(bst, 1))            # 1
    print(kth_smallest_iterative(bst, 2))  # 2
    print(kth_smallest_iterative(bst, 3))  # 3
