"""
Diameter of Binary Tree

The diameter is the length of the longest path between any two nodes.
The path may or may not pass through the root.

Key insight: at every node, the longest path through it =
             left_height + right_height.
Track a global max across all nodes in a single DFS pass.

Time: O(n)  Space: O(h)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root: TreeNode | None) -> int:
    max_diameter = 0

    def height(node: TreeNode | None) -> int:
        nonlocal max_diameter
        if node is None:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        max_diameter = max(max_diameter, left_h + right_h)
        return 1 + max(left_h, right_h)

    height(root)
    return max_diameter


if __name__ == "__main__":
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(diameter_of_binary_tree(root))   # 3  (path: 4→2→1→3 or 5→2→1→3)

    #    1
    #   /
    #  2
    root2 = TreeNode(1, TreeNode(2))
    print(diameter_of_binary_tree(root2))  # 1
