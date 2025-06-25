class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None

def inorder_traversal(root):
    if not root:
        return []
    return inorder_traversal(root.left) + [root.data] + inorder_traversal(root.right)

root = Node(1)
# root.left = Node(3)
root.right = Node(2)
root.right.left = Node(3)
print(inorder_traversal(root))
