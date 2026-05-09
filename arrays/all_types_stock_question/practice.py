from collections import deque
class Tree:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
class TreeStructure:
    def __init__(self):
        self.root = None

    def add_node_in_tree(self, data):
        new_node = Tree(data)
        
        if not self.root:
            self.root = new_node
            return
        queue = deque()
        queue.append(self.root)
        while queue:
            current_node = queue.popleft()
            if not current_node.left:
                current_node.left = new_node
                return
            else:
                queue.append(current_node.left)
            if not current_node.right:
                current_node.right = new_node
                return
            else:
                queue.append(current_node.right)
    
    def print_pre_order(self, tree):
        if not tree:
            return
        print(tree.data, end=" -> ")
        self.print_pre_order(tree.left)
        self.print_pre_order(tree.right)
    
    def print_pre_order_without_recursion(self, tree):
        if not tree:
            return
        stack = [tree]
        while stack:
            current_node = stack.pop()
            print(current_node.data, end= " -> ")
            if current_node.right:
                stack.append(current_node.right)
            if current_node.left:
                stack.append(current_node.left)
    
    def print_in_order(self, tree):
        if not tree:
            return
        self.print_in_order(tree.left)
        print(tree.data, end=" -> ")
        self.print_in_order(tree.right)

    def print_in_order_without_recursion(self, tree):
        if not tree:
            return
        stack = [tree]
        while stack:
            current_node = stack.pop()
            while current_node.left:
                stack.append(current_node.left)
            if not current_node.left:
                print(current_node.data, end=" -> ")
            if current_node.right:
                



        
    

ts = TreeStructure()
p = [2,3,4,5,6,7,8]
for i in p:
    ts.add_node_in_tree(i)

ts.print_pre_order(ts.root)
print("Without recrusion")
ts.print_pre_order_without_recursion(ts.root)





        

