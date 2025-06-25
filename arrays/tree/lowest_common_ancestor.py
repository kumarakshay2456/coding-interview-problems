class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None
    

def find_lca(root, node1, node2):
    if not root:
        return None
    if root == node1 or root == node2:
        return root
    left = find_lca(root.left, node1, node2)
    right = find_lca(root.right, node1, node2)
    if left and right:
        return root
    return left if left else right



if __name__ == '__main__':

    """
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
    
     LCA(5, 1) = 3
     LCA(6, 4) = 5
     LCA(7,8) = 3

     find_lca(3)
        ├── find_lca(5)
        │    ├── find_lca(6) → returns 6
        │    └── find_lca(2)
        │         ├── find_lca(7) → None
        │         └── find_lca(4) → returns 4
        │    ⇒ both left & right found → return 5
        └── find_lca(1)
            ├── find_lca(0) → None
            └── find_lca(8) → None
      
      ⇒ only left side gave result → return 5
    
    """
    root = Node(3)
    root.left = Node(5)
    root.left.left = Node(6)
    root.left.right = Node(2)
    root.left.right.left = Node(7)
    root.left.right.right = Node(4)
    root.right = Node(1)
    root.right.left = Node(0)
    root.right.right = Node(8)
    # print("LCA IS LCA(5, 1) -> ",  find_lca(root, root.left, root.right).data)
    print("LCA IS LCA(6, 4) -> ",  find_lca(root, root.left.left, root.left.right.right).data)
    # print("LCA IS LCA(7,8)  -> ",  find_lca(root, root.left.right.left, root.right.right).data)


