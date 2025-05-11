class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None
def return_cycle_position(head):
    slow = head
    fast = head
    position = -1
    # Phase 1: Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle detected
            break
    else:
        # No cycle
        # If slow == fast happens, it means a cycle exists, and the loop breaks — the else is not run.
        # If fast or fast.next becomes None, meaning end of list — the while condition fails — the else block does run, returning None.
        return None
    
    slow = head
    position = 0
    while slow != fast:
        slow = slow.next
        fast = fast.next
        position += 1
    return position
    

if __name__ == '__main__':
    head = Node(3)
    head.next = Node(2)
    head.next.next = Node(0)
    head.next.next.next = Node(-4)
    head.next.next.next.next = Node(6)
    head.next.next.next.next.next = Node(7)
    head.next.next.next.next.next.next = head.next.next.next.next.next
    print(f"Cycle is at position {return_cycle_position(head)}")
        