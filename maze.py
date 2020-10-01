from util import StackFrontier, QueueFrontier, Node

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
                return [], count

            node = self.frontier.remove()
            if node.state == self.end:
                print("found solution")
                return self.get_path(node), count

            #get node's neighbor cells and adds them to frontier
            x = node.state[0]
            y = node.state[1]

            directions = {
                    "left": (x-1,y),
                    "right": (x+1,y),
                    "up": (x,y-1),
                    "down": (x,y+1)
                    }

            for direction, index in directions.items():

                cell = None

                if direction == "left" and x > 0:
                    cell = index
                if direction == "right" and x < self.grid_size[0] - 1:
                    cell = index
                if direction == "up" and y > 0:
                    cell = index
                if direction == "down" and y < self.grid_size[1] - 1:
                    cell = index

                if cell and cell not in explored and not self.frontier.contains_state(cell) and cell not in self.walls:
                    self.frontier.add(Node(cell, node, direction))

            explored.add(node.state)
            count += 1
