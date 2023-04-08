class Stack:
    def __init__(self, size):
        self.data = [None for _ in range(size)]
        self.size = size
        self.top = 0

    def add(self, item):
        if self.is_full():
            raise RuntimeError("Stack is full")
        self.data[self.top] = item
        self.top += 1

    def take(self):
        if self.is_empty():
            raise RuntimeError("Stack is empty")
        self.top -= 1
        return self.data[self.top]

    def is_full(self):
        return self.top == self.size

    def is_empty(self):
        return self.top == 0
