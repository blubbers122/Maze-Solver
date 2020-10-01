from util import StackFrontier, QueueFrontier, Node

class Maze():
    def __init__(self, grid_size, walls):
        self.grid_size = grid_size
        self.walls = walls

    def solve_maze(self):
        print("solving maze")
