class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None
def return_cycle_position(head):
    

if __name__ == '__main__':
    head = Node(2)
    head.next = Node(3)
    head.next.next = Node(4)
    head.next.next.next = Node(5)
    head.next.next.next.next = Node(6)
    head.next.next.next.next.next = Node(7)
    head.next.next.next.next.next = head.next.next
        