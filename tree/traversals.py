class Tree:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None

"""
Time - T(n) = O(n)
Space - T(n) = O(log n) if tree is balance otherwise it will take O(n) for skew treee
"""
class RecursiveTraversal:
    def print_pre_order(self, root):
        if not root:
            return
        print(root.data, end=" ")
        self.print_pre_order(root.left)
        self.print_pre_order(root.right)

    def print_post_order(self, root):
        if not root:
            return
        self.print_post_order(root.left)
        self.print_post_order(root.right)
        print(root.data, end=" ")

    def print_in_order(self, root):
        if not root:
            return
        self.print_in_order(root.left)
        print(root.data, end=" ")
        self.print_in_order(root.right)

"""
Time - T(n) = O(n)
Space - T(n) = O(log n) if tree is balance otherwise it will take O(n) for skew treee
"""
class IterativeTraversal:
    def preorder(self, root):
        stack = [root]
        while stack:
            node = stack.pop()
            print(node.data, end=" ")
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    def inorder(self, root):
        result = []
        stack = []
        current = root
        while stack or current:
            # reach the left most
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.data)
            current = current.right
        print(*result)

    def postorder(self, root):
        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            result.append(node.data)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        print(result)
        print(*result[::-1])



"""
Time - T(n) = O(n)
Space - T(n) = O(1)
Morris Traversal

"""
class MorisTraversal:

    def morris_inorder(root):
        result = []
        current = root

        while current:
            if not current.left:
                # No left child → visit and go right
                result.append(current.data)
                current = current.right
            else:
                # Find the inorder predecessor
                predecessor = current.left
                while predecessor.right and predecessor.right is not current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # Make thread to current
                    predecessor.right = current
                    current = current.left
                else:
                    # Thread already exists → break it and visit current
                    predecessor.right = None
                    result.append(current.data)
                    current = current.right
        print(*result)
        return result
    
    def morris_preorder(root):
        result = []
        current = root

        while current:
            if not current.left:
                result.append(current.data)
                current = current.right
            else:
                predecessor = current.left
                while predecessor.right and predecessor.right is not current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    result.append(current.data)  # Visit before going left
                    predecessor.right = current
                    current = current.left
                else:
                    predecessor.right = None
                    current = current.right
        print(*result)
        return result
    
    def morris_postorder(self, root):
        result = []
        dummy = Tree(0)
        dummy.left = root
        current = dummy

        while current:
            if not current.left:
                current = current.right
            else:
                predecessor = current.left
                while predecessor.right and predecessor.right is not current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    predecessor.right = current
                    current = current.left
                else:
                    # Reverse the right path from current.left to predecessor
                    self.collect_reverse_path(current.left, predecessor, result)
                    predecessor.right = None
                    current = current.right
        print(*result)
        return result

    def collect_reverse_path(self, from_node, to_node, result):
        self.reverse_path(from_node, to_node)
        node = to_node
        while True:
            result.append(node.data)
            if node is from_node:
                break
            node = node.right
        self.reverse_path(to_node, from_node)

    def reverse_path(self, start, end):
        if start is end:
            return
        prev = None
        current = start
        while True:
            nxt = current.right
            current.right = prev
            prev = current
            current = nxt
            if prev is end:
                break
    



if __name__ == '__main__':
    root = Tree(3)
    root.left = Tree(4)
    root.right = Tree(5)
    root.left.left = Tree(6)
    root.left.right = Tree(7)
    print("Preorder is ->")
    RecursiveTraversal().print_pre_order(root)
    print("\n Inorder is ->")
    RecursiveTraversal().print_in_order(root)
    print("\n Postorder is ->")
    RecursiveTraversal().print_post_order(root)
    print("\n ** Postorder is ->")
    IterativeTraversal().postorder(root)
    print("\n ** Preorder is ->")
    IterativeTraversal().preorder(root)
    print("\n ** Inorder is ->")
    IterativeTraversal().inorder(root)
    print("Moris Traversal")
    print("\n ** Postorder is ->")
    MorisTraversal().morris_postorder(root)
    print("\n ** Preorder is ->")
    MorisTraversal.morris_preorder(root)
    print("\n ** Inorder is ->")
    MorisTraversal.morris_inorder(root)




