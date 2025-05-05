class Node:
    def __init__(self, data) :
        self.data = data
        self.next = None

class LinkList:
    def __init__(self) -> None:
        self.head = None
    
    def add_value_in_ll(self, node):
        if not self.head:
            self.head = node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = node
        return
    
    def print_ll(self):
        if not self.head:
            return
        temp = self.head
        while temp:
            print(temp.data, end="")
            if temp.next:
                print(" -> ", end="")
            temp = temp.next


def reverse_ll(head):   
    if not head:
        return
    prev_ptr = None
    curr_ptr = head
    while curr_ptr:
        next_ptr = curr_ptr.next
        curr_ptr.next = prev_ptr
        prev_ptr = curr_ptr
        curr_ptr = next_ptr
    return prev_ptr

def reverse_ll_group(head, group):
    temp  = head
    count = 1
    temp_head = temp_head
    while temp:
        temp



    


if __name__ == '__main__':
    """
    
    Reverse a Linked List in groups of given size

    Given a Singly linked list containing n nodes. The task is to reverse every group of k nodes in the list. 
    If the number of nodes is not a multiple of k then left-out nodes, in the end, should be considered as a group and must be reversed.

    Example: 
        Input: head: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> NULL, k = 2 
        Output: head: 2 -> 1 -> 4 -> 3 -> 6 -> 5 -> NULL 
        Explanation : Linked List is reversed in a group of size k = 2.
        
    """
    ll = LinkList()
    ll.add_value_in_ll(Node(2))
    ll.add_value_in_ll(Node(3))
    ll.add_value_in_ll(Node(4))
    ll.add_value_in_ll(Node(5))
    ll.add_value_in_ll(Node(6))
    ll.print_ll()
    group_size = 2

    
