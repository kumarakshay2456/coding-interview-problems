class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def add_element(head, node):
    if not head:
        return node
    temp = head
    while temp.next:
        temp = temp.next
    temp.next = node
    return head

def find_mid_element(head):
    slow_ptr = head
    fast_ptr = head
    while fast_ptr and fast_ptr.next:
        slow_ptr = slow_ptr.next
        fast_ptr = fast_ptr.next.next
    return slow_ptr.data



if __name__ == '__main__':
    head = None
    head = add_element(head, node = Node(2))
    head = add_element(head, node = Node(3))
    head = add_element(head, node = Node(4))
    head = add_element(head, node = Node(5))
    head = add_element(head, node = Node(6))
    head = add_element(head, node = Node(7))
    head = add_element(head, node = Node(9))
    print("Middle Element is", find_mid_element(head))


