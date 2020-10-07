from queue import PriorityQueue

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class PriorityNode(Node):
    def __init__(self, state, parent, action, priority):
        super().__init__(state, parent, action)
        self.priority = priority

    def __lt__(self, other):
        selfPriority = self.priority
        otherPriority = other.priority
        return selfPriority < otherPriority

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class PQueueFrontier(PriorityQueue):

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, item))

    def contains_state(self, state):
        return any(item[1].state == state for item in self.queue)
