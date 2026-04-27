"""
Construct Binary Tree from Traversals

Problem 1: Construct from Preorder + Inorder
Problem 2: Construct from Postorder + Inorder

Key insight:
  - Preorder[0]  = root of current subtree
  - Postorder[-1] = root of current subtree
  - Root's position in Inorder splits it into left and right subtrees.

Time: O(n) with index map  Space: O(n)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_to_list(root: TreeNode | None) -> list:
    """Level-order for easy verification."""
    if not root:
        return []
    from collections import deque
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val if node else None)
        if node:
            queue.append(node.left)
            queue.append(node.right)
    while result and result[-1] is None:
        result.pop()
    return result


# ── Preorder + Inorder → Tree ─────────────────────────────────────────────────

def build_tree_pre_in(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    inorder_index = {val: i for i, val in enumerate(inorder)}
    pre_iter = iter(preorder)

    def build(left: int, right: int) -> TreeNode | None:
        if left > right:
            return None
        root_val = next(pre_iter)
        root = TreeNode(root_val)
        mid = inorder_index[root_val]
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(inorder) - 1)


# ── Postorder + Inorder → Tree ────────────────────────────────────────────────

def build_tree_post_in(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    inorder_index = {val: i for i, val in enumerate(inorder)}
    post_iter = iter(reversed(postorder))   # root is at the end of postorder

    def build(left: int, right: int) -> TreeNode | None:
        if left > right:
            return None
        root_val = next(post_iter)
        root = TreeNode(root_val)
        mid = inorder_index[root_val]
        root.right = build(mid + 1, right)  # right first (we consume from back)
        root.left = build(left, mid - 1)
        return root

    return build(0, len(inorder) - 1)


if __name__ == "__main__":
    #        3
    #       / \
    #      9  20
    #        /  \
    #       15   7

    print("── Preorder + Inorder ──")
    preorder = [3, 9, 20, 15, 7]
    inorder  = [9, 3, 15, 20, 7]
    root = build_tree_pre_in(preorder, inorder)
    print(tree_to_list(root))   # [3, 9, 20, None, None, 15, 7]

    print("── Postorder + Inorder ──")
    postorder = [9, 15, 7, 20, 3]
    root2 = build_tree_post_in(inorder, postorder)
    print(tree_to_list(root2))  # [3, 9, 20, None, None, 15, 7]
