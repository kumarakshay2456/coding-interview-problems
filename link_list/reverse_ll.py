class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None

    def add_ll(self, node:Node):
        if not self.head:
            self.head = node
            return
        key_pointer = self.head
        while key_pointer.next:
            key_pointer = key_pointer.next
        key_pointer.next = node

    def print_ll(self):
        temp = self.head
        while temp:
            print(temp.data, end="")
            if temp.next:
                print(" -> ", end="")
            temp = temp.next
    
    def reverse_ll(self):
        if not self.head.next:
            return self.head
        prev_ptr = None
        curr_ptr = self.head
        next_ptr = None
        while curr_ptr:
            next_ptr = curr_ptr.next
            curr_ptr.next = prev_ptr
            prev_ptr = curr_ptr
            curr_ptr = next_ptr
        return prev_ptr
    
    def print_ll_with_given_object(temp):
        if not temp:
            return
        if not temp.next:
            print(temp.data, end='')
        while temp:
            print(temp.data, end="")
            if temp.next:
                print(" -> ", end="")
            temp = temp.next


if __name__ == '__main__':
    ll = LinkList()
    ll.add_ll(Node(2))
    ll.add_ll(Node(3))
    ll.add_ll(Node(4))
    ll.add_ll(Node(5))
    ll.print_ll()
    curr_ptr = ll.reverse_ll()
    LinkList.print_ll_with_given_object(curr_ptr)


    
