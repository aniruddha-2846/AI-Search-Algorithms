class Stack():
    def __init__(self):
        self.list = []

    def add(self, node):
        self.list.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.list)

    def empty(self):
        return len(self.list) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Stack")
        else:
            node = self.list[-1]
            self.list = self.list[:-1]
            return node

class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception("Empty Queue")
        else:
            node = self.list[0]
            self.list = self.list[1:]
            return node