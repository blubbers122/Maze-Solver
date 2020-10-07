from util import StackFrontier, QueueFrontier, Node, PriorityNode, PQueueFrontier



class Maze():
    def __init__(self, grid_size, start, end, walls):
        self.grid_size = grid_size
        self.start = tuple(start)
        self.end = tuple(end)
        self.walls = walls
        self.frontier = QueueFrontier()

    def get_path(self, node):
        path = []

        while node.parent:
            path.append(node.state)
            node = node.parent

        return path

    def solve_maze(self):
        start_node = Node(self.start, None, None)
        self.frontier.add(start_node)

        explored = set()
        count = 0
        while True:
            if self.frontier.empty():
                print("couldn't find solution")
                return [], count, explored

            node = self.frontier.remove()
            if node.state == self.end:
                print("found solution")
                return self.get_path(node), count, explored

            #get node's neighbor cells and adds them to frontier
            x = node.state[0]
            y = node.state[1]

            neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

            for neighbor in neighbors:
                cell = None

                if self.grid_size[0] > neighbor[0] and neighbor[0] >= 0 and 0 <= neighbor[1] and neighbor[1] < self.grid_size[1]:
                    cell = neighbor

                # makes sure cell index is valid and not already queued
                if cell and cell not in explored and not self.frontier.contains_state(cell) and cell not in self.walls:
                    self.frontier.add(Node(cell, node, None))

            explored.add(node.state)
            count += 1

class DFSMaze(Maze):
    def __init__(self, grid_size, start, end, walls):
        super().__init__(grid_size, start, end, walls)
        self.frontier = StackFrontier()

class GBFMaze(Maze):
    def __init__(self, grid_size, start, end, walls):
        super().__init__(grid_size, start, end, walls)
        self.frontier = PQueueFrontier(900)

    def manhattan_distance(self, index):
        return abs(self.end[0] - index[0]) + abs(self.end[1] - index[1])

    def solve_maze(self):
        start_node = PriorityNode(self.start, None, None, self.manhattan_distance(self.start))
        self.frontier.put(start_node, 1)

        explored = set()
        count = 0
        while True:
            if self.frontier.empty():
                print("couldn't find solution")
                return [], count, explored

            node = self.frontier.get()[1]
            if node.state == self.end:
                print("found solution")
                return self.get_path(node), count, explored

            #get node's neighbor cells and adds them to frontier
            x = node.state[0]
            y = node.state[1]

            neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

            for neighbor in neighbors:
                cell = None

                if self.grid_size[0] > neighbor[0] >= 0 and 0 <= neighbor[1] < self.grid_size[1]:
                    cell = neighbor

                # makes sure cell index is valid and not already queued
                if cell and cell not in explored and not self.frontier.contains_state(cell) and cell not in self.walls:
                    distance = self.manhattan_distance(cell)
                    self.frontier.put(PriorityNode(cell, node, None, distance), distance)

            explored.add(node.state)
            count += 1

class AStarMaze(Maze):
    def __init__(self, grid_size, start, end, walls):
        super().__init__(grid_size, start, end, walls)
        self.frontier = PQueueFrontier(900)

    def manhattan_distance(self, index):
        return abs(self.end[0] - index[0]) + abs(self.end[1] - index[1])

    def cost_to_reach(self, index):
        return abs(self.start[0] - index[0]) + abs(self.start[0] - index[1])

    def solve_maze(self):
        start_node = PriorityNode(self.start, None, None, self.manhattan_distance(self.start))
        self.frontier.put(start_node, 1)

        explored = set()
        count = 0
        while True:
            if self.frontier.empty():
                print("couldn't find solution")
                return [], count, explored

            node = self.frontier.get()[1]
            if node.state == self.end:
                print("found solution")
                return self.get_path(node), count, explored

            #get node's neighbor cells and adds them to frontier
            x = node.state[0]
            y = node.state[1]

            neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

            for neighbor in neighbors:
                cell = None

                if self.grid_size[0] > neighbor[0] >= 0 and 0 <= neighbor[1] < self.grid_size[1]:
                    cell = neighbor

                # makes sure cell index is valid and not already queued
                if cell and cell not in explored and not self.frontier.contains_state(cell) and cell not in self.walls:
                    priority = self.manhattan_distance(cell) + self.cost_to_reach(cell)
                    self.frontier.put(PriorityNode(cell, node, None, priority), priority)

            explored.add(node.state)
            count += 1
