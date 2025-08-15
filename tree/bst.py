class Tree:
    def __init__(self,  data):
        self.data = data
        self.left = None
        self.right = None


def insert_bst(root, data):
    if not root:
        return Tree(data)
    if root.data > data:
        root.left = insert_bst(root.left, data)
    elif root.data < data:
        root.right = insert_bst(root.right, data)
    return root

# Without recursion
def insert_bst(root, data):
    new_node = Tree(data)
    if not root:
        return new_node

    current = root
    while True:
        if data < current.data:
            if current.left:
                current = current.left
            else:
                current.left = new_node
                break
        elif data > current.data:
            if current.right:
                current = current.right
            else:
                current.right = new_node
                break
        else:
            # If duplicates are ignored, break here
            break

    return root

# Search Element
def search_bst(root, key):
    if not root:
        return None  # Not found
    if root.data == key:
        return root
    elif key < root.data:
        return search_bst(root.left, key)
    else:
        return search_bst(root.right, key)

# Find minimum
# Left most element will be the minimum
def find_minimum(root):
    if not root:
        return None
    current = root
    while current.left:
        current = current.left
    return current

# Find maximum
# Right most element will be the minimum
def find_maximum(root):
    if not root:
        return None
    current = root
    while current.right:
        current = current.right
    return current


def print_inorder(root):
    if not root:
        return
    print_inorder(root.left)
    print(root.data, end=" ")
    print_inorder(root.right)


arr = [2,6,3,4,5,8]
root =  None
for i in arr:
    root = insert_bst(root, i)
print_inorder(root)
print("elment found", search_bst(root, 4))

print("minimum element is -> ", find_minimum(root).data)
print("maximum element is -> ", find_maximum(root).data)


