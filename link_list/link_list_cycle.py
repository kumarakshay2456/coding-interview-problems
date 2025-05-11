class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def is_cycle(head):
    if not head:
        return False
    slow = head 
    fast = head.next
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False


if __name__ == '__main__':
    head = Node(2)
    head.next = Node(3)
    head.next.next = Node(4)
    head.next.next.next = Node(5)
    head.next.next.next.next = Node(6)
    head.next.next.next.next.next = Node(5)
    # head.next.next.next.next.next.next = head.next.next.next
    print("Is cycle ->", is_cycle(head))
