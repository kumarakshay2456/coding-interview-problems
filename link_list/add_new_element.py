
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None

    def print_ll(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next

    def insert_start_of_ll(self, node):
        if not self.head:
            self.head = node
        else:
            temp = self.head
            self.head = node
            self.head.next = temp

    def insert_last_of_ll(self, node):
        if not self.head:
            self.head = node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = node

    def insert_node_given_node(self, node, given_node):
        if self.head:
            temp = self.head
            while temp and temp.data != given_node.data:
                temp = temp.next
            if temp and temp.data == given_node.data:
                temp1 = temp.next
                temp.next = node
                node.next = temp1
            else:
                raise ValueError("Node is not matched")
        elif not self.head and self.head == given_node:
            self.head = node
        else:
            raise ValueError("Please enter the correct given node value")


if __name__ == "__main__":
    ll = LinkList()
    """
    insert the start of the LL
    """
    ll.insert_start_of_ll(Node(1))
    ll.insert_start_of_ll(Node(2))
    ll.insert_start_of_ll(Node(3))
    ll.print_ll()

    """
    Insert the last of the LL
    """
    ll.insert_last_of_ll(Node(10))
    ll.insert_last_of_ll(Node(12))
    ll.insert_last_of_ll(Node(14))
    ll.print_ll()
    """
    Insert the node after the given node"""

    ll.insert_node_given_node(Node(20), Node(15))
    ll.print_ll()




