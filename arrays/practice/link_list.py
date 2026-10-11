class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LL:
    def __init__(self):
        self.head = None
    
    def add_ll(self, node):
        temp = self.head
        if not temp:
            self.head = node
            return
        while temp.next:
            temp = temp.next
        temp.next = node
        return

    def print_ll(self):
        temp = self.head
        while temp:
            print(f"{temp.data}", end=" --> ")
            temp = temp.next
        print("None")
        return

    def mid_element_link_list(self):
        temp = self.head
        slow = temp
        fast = temp
        while fast.next and fast.next.next:
            fast = fast.next.next
            slow = slow.next
        print(f"mid element is -> {slow.data}")
    
    def find_start_of_the_cycle(self):
        slow = self.head
        fast = self.head
        while slow != fast:
            slow = slow.next
            fast = fast.next.next
        print(f"Start element is {slow.next.data}")
    



    
l = [2,2,3,4]
link_list = LL()
node1 = Node(2)
link_list.add_ll(node1)
p = link_list.head
node2 = Node(2)
link_list.add_ll(node2)
node3 = Node(3)
link_list.add_ll(node3)

node4 = Node(4)
link_list.add_ll(node4)





link_list.mid_element_link_list()