from collections import deque
class Tree:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None


def level_order_traversal(root):
    total_level = 0
    result = []
    if not root:
        return result
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level_nodes = []
        for i in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_nodes)
        total_level += 1
    print("Total level is", total_level -1 )
    return result





if __name__ == '__main__':
    p = Tree(2)
    p.left = Tree(3)
    p.right = Tree(5)
    p.right.left = Tree(6)
    p.right.right = Tree(7)
    p.right.right.left = Tree(8)
    p.right.right.left.left = Tree(3)
    p.right.right.right = Tree(9)
    print("level order traversal is -> ", *level_order_traversal(p))