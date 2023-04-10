class Queue:
    def __init__(self, size):
        self.data = [None for _ in range(size)]
        self.num_items = 0
        self.size = size
        self.head = 0
        self.rear = 0

    def add(self, item):
        if self.is_full():
            raise RuntimeError("Queue is full")
        self.data[self.rear] = item
        self.rear = (self.rear + 1) % self.size
        self.num_items += 1

    def take(self):
        if self.is_empty():
            raise RuntimeError("Queue is empty")
        item = self.data[self.head]
        self.head = (self.head + 1) % self.size
        self.num_items -= 1
        return item

    def is_empty(self):
        return self.num_items == 0
    
    def is_full(self):
        return self.num_items == self.size

