from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def print_inorder(root):
    if not root:
        return
    print_inorder(root.left)
    print(root.value, end=" ")
    print_inorder(root.right)

def print_preorder(root):
    if not root:
        return
    print(root.value, end=" ")
    print_preorder(root.left)
    print_preorder(root.right)

def invert_tree(root):
    if not root:
        return None
    temp = root.right
    root.right = root.left
    root.left = temp

    invert_tree(root.left)
    invert_tree(root.right)

    return root

def list_to_tree(data):
    if not data:
        return None
    
    root = Node(data[0])
    queue = deque([root])
    i = 1
    while queue and i < len(data):
        node = queue.popleft()
        if i < len(data):
            node.left = Node(data[i])
            queue.append(node.left)
            i += 1
        if i < len(data):
            node.right = Node(data[i])
            queue.append(node.right)
            i += 1
    return root

def print_bfs_tree(root):
    if not root:
        return None
    node_list = []
    
    queue = deque([root])
    while queue:
        node = queue.popleft()
        node_list.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return node_list


    

if __name__ == '__main__':
    root = Node(4)
    root.left = Node(2)
    root.right = Node(7)
    root.left.left = Node(1)
    root.left.right = Node(3)
    root.right.left = Node(6)
    root.right.right = Node(9)
    # print_inorder(root)
    # print_preorder(root)
    # print("/n")
    root = list_to_tree([4,2,7,1,3,6,9])
    inverted = invert_tree(root)
    root_list = print_bfs_tree(inverted)
    print(root_list)