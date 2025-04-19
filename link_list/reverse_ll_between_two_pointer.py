class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None

    def take_input_ll(self):
        p = input("Please enter total length for the link list")
        ss = []
        for i in range(int(p)):
            ss.append(int(input("Please enter the value one by one")))
        for i in ss:
            if not self.head:
                self.head = Node(i)
                print("self", self.head.__dict__)
                temp = self.head
            else:
                temp.next = Node(i)
                temp = temp.next

    def print_ll(self):
        temp = self.head
        while temp:
            print("Node is", temp.__dict__)
            print("Value", temp.data)
            temp = temp.next

def reverser_ll(head):
    current = head
    prev = None
    while current:
        next_ptr = current.next
        current.next = prev
        prev = current
        current = next_ptr
    return prev


if __name__ == '__main__':
    p = LinkList()
    p.take_input_ll()
    p.print_ll()
    q = reverser_ll(p.head)
    p.head = q
    p.print_ll()



