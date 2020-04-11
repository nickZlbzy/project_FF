class Node:
    """节点类"""
    def __init__(self,value):
        """数据区，链接区"""
        self.value = value
        self.next = None

class linkedList:
    """单链表类"""
    def __init__(self,obj=None):
        self.head = None
        if isinstance(obj,list) or isinstance(obj,tuple):
            self.array_to_linkedlist(obj)
        elif isinstance(obj,Node):
            self.head = obj

    def array_to_linkedlist(self,array):
        for i,ele in enumerate(array):
            node = Node(ele)
            if i == 0:
                self.head = node
                current = self.head
                continue
            current.next = node
            current = current.next

    def is_empty(self):
        """判断是否为空"""
        return self.head == None

    def length(self):
        """获取链表长度"""
        # current游标。移动遍历每个节点
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.next
        return count

    def travel(self):
        """遍历整个链表"""
        print("<linkedlist:",end=" ")
        current = self.head
        while current != None:
            print(current.value,end=' ')
            current = current.next
        print(">", end=' ')
        print()

    def add(self,value):
        node = Node(value)
        node.next=self.head
        self.head = node

    def append(self,value):
        """链表的尾部添加一个元素"""
        node = Node(value)

        if self.head == None:
            self.head = node
        else:
            current = self.head
            while current.next != None:
                current = current.next
            current.next = node

    def insert(self,pos,value):
        """
        再指定位置添加元素
        :param pos: 指定的下标
        :param value: 值
        :return:
        """

        if pos <= 0 :
            self.add(value)
        elif pos > self.length()-1:
            self.append(value)
        else:
            node = Node(value)
            pre = self.head
            for i in range(pos-1):
                pre = pre.next
            else:
                node.next = pre.next
                pre.next = node

    def search(self,value):
        current = self.head
        if current:
            index = 0
            while current.next != None:
                if current.value == value:
                    return index
                else:
                    index += 1
                    current = current.next
            else:
                if current.value == value:
                    return index
        return None

    def remove(self,value,count=1):
        """
        删除节点
        特殊情况1：删除头节点
        特殊情况2：删除非头节点
        :param value:
        :return:
        """
        current = self.head
        num = 0
        pre = None
        while num <count and current != None :
            if current.value == value:
                # 先判断是否为头节点
                if current == self.head:
                    self.head = current.next
                    num += 1
                else:
                    pre.next = current.next
                    num += 1
            else:
                pre = current
            current = current.next

    def __iter__(self):
        current = self.head
        while current != None:
            yield current.value
            current = current.next
        else:
            raise StopIteration

    def __str__(self):
        self.travel()