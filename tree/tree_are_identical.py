from collections import deque
class Tree:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None


def is_both_tree_identical(root1, root2):
    if (root1 and not root2) or (not root1 and root2):
        return False
    if not root1 and not root2:
        return True
    
    queue1 = deque([root1])
    queue2 = deque([root2])
    while queue1 and queue2:
        node1 = queue1.popleft()
        node2 = queue2.popleft()
        if node1.data != node2.data:
            return False
        if node1.left and node2.left:
            queue1.append(node1.left)
            queue2.append(node2.left)
        elif (node1.left and not node2.left) or (not node1.left and node2.left):
            return False

        if node1.right and node2.right:
            queue1.append(node1.right)
            queue2.append(node2.right)
        elif (node1.right and not node2.right) or (not node1.right and node2.right):
            return False
    return True

def recursive_version(root1, root2):
    if not root1 and not root2:
        return True
    if not root1 or not root2:
        return False
    return (root1.data == root2.data and (recursive_version(root1.left, root2.left)) and recursive_version(root1.right, root2.right))


if __name__ == '__main__':
    p = Tree(2)
    p.left = Tree(3)
    p.right = Tree(5)
    p.right.left = Tree(6)
    p.right.right = Tree(7)
    p.right.right.left = Tree(8)
    p.right.right.left.left = Tree(3)
    p.right.right.right = Tree(9)

    p1 = Tree(2)
    p1.left = Tree(3)
    p1.right = Tree(5)
    p1.right.left = Tree(6)
    p1.right.right = Tree(7)
    p1.right.right.left = Tree(8)
    p1.right.right.left.left = Tree(3)
    p1.right.right.right = Tree(9)
    print("Both tree are identical or not", recursive_version(p, p1))