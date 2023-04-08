class Path:
    def __init__(self):
        self.data = []
        self.num_items = 0
    
    def add(self, item):
        self.data.append(item)
        self.num_items += 1
    
    def take(self):
        if self.is_empty():
            raise RuntimeError("Path is empty")

        self.num_items -= 1
        return self.data[self.num_items]
    
    def is_empty(self):
        return self.num_items == 0
    
    def __repr__(self):
        return str(self.data[:self.num_items])
