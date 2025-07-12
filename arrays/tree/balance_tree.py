class Tree:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None

def get_node_height(root):
    if not root:
        return 0, 0
    left_height = 0 
    right_height = 0
    if root.left:
        left_height = 1 + max(get_node_height(root.left))
    if root.right:
        right_height = 1 + max(get_node_height(root.right))


    return left_height, right_height

# T(n) = O(n^2)
# Space Complexity S(n) = O(h)

def is_tree_balanced(root):
    if not root:
        return True
    left , right = get_node_height(root)
    if left - right > 1 or right - left > 1:
        return False
    return is_tree_balanced(root.left) and is_tree_balanced(root.right)

# T(n) = O(n)
# Space Complexity S(n) = O(h)
def is_tree_balanced_v2(root):
    def check_height(node):
        if not node:
            return 0  # height of null node is 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1  # left subtree is unbalanced

        right_height = check_height(node.right)
        if right_height == -1:
            return -1  # right subtree is unbalanced

        if abs(left_height - right_height) > 1:
            return -1  # current node is unbalanced

        return 1 + max(left_height, right_height)

    return check_height(root) != -1

# Ex - 1
# root = Tree(1)
# root.left = Tree(2)
# root.right = Tree(2)
# root.left.left = Tree(3)
# root.left.right = Tree(3)
# root.left.left.left = Tree(4)
# root.left.left.right = Tree(4)

# EX - 2
root = Tree(3)
root.left = Tree(9)
root.right = Tree(20)
root.right.left = Tree(15)
root.right.right = Tree(7)
print(f"Is three balanced -> {is_tree_balanced(root)}")


