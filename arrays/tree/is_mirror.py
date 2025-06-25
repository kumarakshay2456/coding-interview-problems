class Node:
    def __init__(self, data) -> None:
        self.val = data
        self.left = None
        self.right = None
    
    
def is_symmetric(root):
    if not root:
        return True

    def is_mirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (
            t1.val == t2.val and
            is_mirror(t1.left, t2.right) and
            is_mirror(t1.right, t2.left)
        )

    return is_mirror(root.left, root.right)


if __name__ == '__main__':

    """
        1
       / \
      2   2
     / \ / \
    3  4 4  3

    Yes - 
    A binary tree is symmetric if the left subtree is a mirror reflection of the right subtree.
    The tree is symmetric if:
	•	left.val == right.val
	•	left.left is a mirror of right.right
	•	left.right is a mirror of right.left
    
    """
    root = Node(1)
    root.left = Node(2)
    root.left.left = Node(3)
    root.left.right = Node(4)
    root.right = Node(2)
    root.right.left = Node(4)
    root.right.right = Node(3)
    print(is_symmetric(root))



