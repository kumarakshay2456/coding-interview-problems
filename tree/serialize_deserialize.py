"""
Serialize and Deserialize Binary Tree

Serialize: convert a tree to a string.
Deserialize: reconstruct the original tree from that string.

Approach: preorder DFS with 'N' for null nodes.
This is one of the cleanest solutions and handles any binary tree (not just BST).

Time: O(n)  Space: O(n)
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        tokens = []

        def dfs(node: TreeNode | None) -> None:
            if node is None:
                tokens.append("N")
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = deque(data.split(","))

        def dfs() -> TreeNode | None:
            val = tokens.popleft()
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


def tree_to_list(root: TreeNode | None) -> list:
    if not root:
        return []
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


if __name__ == "__main__":
    #        1
    #       / \
    #      2   3
    #         / \
    #        4   5
    root = TreeNode(1,
                    TreeNode(2),
                    TreeNode(3, TreeNode(4), TreeNode(5)))

    codec = Codec()
    serialized = codec.serialize(root)
    print("Serialized:", serialized)   # 1,2,N,N,3,4,N,N,5,N,N

    deserialized = codec.deserialize(serialized)
    print("Deserialized:", tree_to_list(deserialized))  # [1, 2, 3, None, None, 4, 5]

    # Edge cases
    print(codec.serialize(None))               # N
    print(tree_to_list(codec.deserialize("N")))  # []
