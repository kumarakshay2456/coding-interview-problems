"""
Binary Tree Maximum Path Sum

A path is any sequence of nodes where each pair of adjacent nodes has an edge.
Each node appears at most once. The path does not need to pass through the root.
Node values can be negative.

Key insight: same structure as diameter — at each node compute the best
"gain" contributed upward (only one branch), and the best full path through it
(both branches). Track the global max of full paths.

Time: O(n)  Space: O(h)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(root: TreeNode | None) -> int:
    max_sum = float("-inf")

    def gain(node: TreeNode | None) -> int:
        nonlocal max_sum
        if node is None:
            return 0
        left_gain = max(gain(node.left), 0)    # discard negative branches
        right_gain = max(gain(node.right), 0)
        max_sum = max(max_sum, node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)   # only one branch upward

    gain(root)
    return max_sum


if __name__ == "__main__":
    #    1
    #   / \
    #  2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    print(max_path_sum(root))   # 6

    #    -10
    #    /  \
    #   9   20
    #       / \
    #      15   7
    root2 = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(max_path_sum(root2))   # 42  (15→20→7)

    # All negative
    root3 = TreeNode(-3)
    print(max_path_sum(root3))   # -3
