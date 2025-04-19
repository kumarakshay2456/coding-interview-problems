def reverse_link_list(head):
    current, prev, next_ptr = head, None, None
    while current:
        next_ptr = current.next
        current.next = prev
        prev = current
        current = next_ptr
    return prev, head


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:

    def __init__(self):
        self.head = None

    def reverseLL(self, low: int, high: int):
        if low == high:
            return self.head
        temp = self.head
        rev_pr = None
        rev_cuu = None
        rev_end = None
        rev_next = None
        count = 1
        while temp and count <= high:
            if count < low:
                rev_pr = temp

            if count == low:
                rev_cuu = temp
            if count == high:
                rev_end = temp
                rev_next = temp.next
            count += 1
            temp = temp.next
        rev_end.next = None
        rev_end = reverse_link_list(rev_cuu)
        p =None
        if rev_pr:
            rev_pr.next = rev_end
        else:
            p = rev_end
        rev_cuu.next = rev_next
        return p if p else self.head

    def printll(self):
        temp = self.head
        while temp:
            print("TEMP {0}".format(temp.data))
            temp = temp.next
    def printll_with_address(self):
        temp = self.head
        ll = []
        while temp:
            p = "{0} ---> {1}".format(temp.data, temp.next)
            ll.append(p)
            temp = temp.next
        print(ll)

if __name__ == "__main__":
    llist = LinkList()
    llist.head = Node(1)
    second = Node(2)
    third = Node(3)
    llist.head.next = second
    second.next = third
    low, high = 1, 2
    llist.printll()
    llist.reverseLL(1, 2)
    print("Reverse")
    llist.printll()
