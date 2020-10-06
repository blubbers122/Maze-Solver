import pygame
import sys
import time


from copy import deepcopy

from maze import Maze, GBFMaze, AStarMaze

pygame.init()

black = (0,0,0)
white = (50,0,55)
highlight = (200, 40, 0)
path_color = (0, 200, 230)
explored_color = (250, 165, 0)
options_box = (150,150,150)
button_color = (200,200,200)
start_color = (30, 220, 15)
end_color = (78, 10, 140)

small_settings = [60, [10, 10]]
medium_settings = [30, [20, 20]]
large_settings = [20, [30, 30]]
grid_position = (0, 0)

size = width, height = 800, 600

smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)

algorithms = ["Breadth First Search", "Greedy Best-First", "A*"]

class MazeInterface():
    def __init__(self):
        self.cell_size = 30
        self.grid_size = [20, 20]
        self.start = [0, 0]
        self.start_cell = None
        self.end = [19, 19]
        self.end_cell = None
        self.empty_cells = []
        self.filled_cells = []
        self.explored_cells = []
        self.wall_indices = []
        self.buttons = []
        self.path = []
        self.count = 0
        self.screen = pygame.display.set_mode(size)
        self.dragging = None
        self.show_explored = True
        self.algorithm = "Breadth First Search"


    def find_cell_under_coords(self, coords):
        for i in range(self.grid_size[1]):
            for j in range(self.grid_size[0]):
                if self.empty_cells[i][j] and self.empty_cells[i][j].x % self.cell_size != 0:
                    print("weird cell")
                    print(i, j)
                cell = self.empty_cells[i][j]
                if cell and cell.collidepoint(coords):
                    cell.x -= cell.x % self.cell_size
                    cell.y -= cell.y % self.cell_size
                    return cell
        return None

    def solve(self):
        print(self.end)
        if self.algorithm == "Breadth First Search":
            maze = Maze(self.grid_size, self.start, self.end, self.wall_indices)
        elif self.algorithm == "A*":
            maze = AStarMaze(self.grid_size, self.start, self.end, self.wall_indices)
        else:
            maze = GBFMaze(self.grid_size, self.start, self.end, self.wall_indices)
        self.path, self.count, self.explored_cells = maze.solve_maze()
        print("length of path", len(self.path))
        if self.path:
            self.path = self.indices_to_rects(self.path)
        if self.explored_cells:
            self.explored_cells = self.indices_to_rects(self.explored_cells)

        print("searched cells: ", self.count)

    def run_app(self):
        self.empty_cells = self.setup_grid()
        self.empty_cells[self.start[0]][self.start[1]] = None
        self.empty_cells[self.end[0]][self.end[1]] = None

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_cell.collidepoint(mouse):
                        self.dragging = self.start_cell
                    elif self.end_cell.collidepoint(mouse):
                        self.dragging = self.end_cell
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging == self.start_cell:
                        self.start_cell.x = mouse[0]
                        self.start_cell.y = mouse[1]
                    elif self.dragging == self.end_cell:
                        self.end_cell.x = mouse[0]
                        self.end_cell.y = mouse[1]
                elif event.type == pygame.MOUSEBUTTONUP:

                    if self.dragging:
                        hovered_cell = self.find_cell_under_coords(mouse)
                        if self.dragging == self.start_cell:
                            if not hovered_cell:
                                self.start_cell = pygame.Rect(self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size)
                            else:
                                self.start = [hovered_cell.x / self.cell_size, hovered_cell.y / self.cell_size]
                                self.start_cell = deepcopy(hovered_cell)
                        else:
                            if not hovered_cell:
                                self.end_cell = pygame.Rect(self.end[0] * self.cell_size, self.end[1] * self.cell_size, self.cell_size, self.cell_size)
                            else:
                                self.end_cell = deepcopy(hovered_cell)
                                self.end = [hovered_cell.x / self.cell_size, hovered_cell.y / self.cell_size]
                        hovered_cell = None
                    self.dragging = None


                    for button in self.buttons:
                        if self.buttons[button].collidepoint(mouse):
                            if button == "Solve":
                                self.solve()
                            elif button == "Clear":
                                self.clear_grid()
                            elif button == "Grid Size":
                                settings = large_settings
                                if self.grid_size == [20, 20]:
                                    settings = large_settings
                                elif self.grid_size == [30, 30]:
                                    settings = small_settings
                                else:
                                    settings = medium_settings
                                print("changing grid size")
                                self.change_grid_size(settings)
                                self.clear_grid()
                            elif button == "Show Explored" or button == "Hide Explored":
                                self.show_explored = not self.show_explored
                            elif button in algorithms:
                                self.algorithm = algorithms[algorithms.index(button) - 1]

            self.screen.fill(black)

            self.draw_maze()
            self.buttons = self.draw_options()

            left_click, _, right_click = pygame.mouse.get_pressed()

            if left_click and not self.dragging:
                hovered_cell = self.find_cell_under_coords(mouse)
                if hovered_cell and hovered_cell not in self.filled_cells:
                    self.filled_cells.append(hovered_cell)
                    self.wall_indices.append((int(hovered_cell.x/self.cell_size), int(hovered_cell.y/self.cell_size)))
                    hovered_cell = None
            elif right_click and not self.dragging:
                for cell in self.filled_cells:
                    if cell.collidepoint(mouse):
                        grid_index = (int(cell.x/self.cell_size), int(cell.y/self.cell_size))
                        new_rect = pygame.Rect(cell.x, cell.y, self.cell_size, self.cell_size)
                        self.filled_cells.remove(cell)
                        self.empty_cells[grid_index[1]][grid_index[0]] = new_rect
                        self.wall_indices.remove(grid_index)

            pygame.display.flip()

    def clear_grid(self):
        self.empty_cells = self.setup_grid()
        self.wall_indices = []
        self.filled_cells = []
        self.explored_cells = []
        self.path = []

    def change_grid_size(self, size_settings):
        self.cell_size = size_settings[0]
        self.grid_size = size_settings[1]
        self.start = [0, 0]
        self.end = [x-1 for x in size_settings[1]]

    def setup_grid(self):
        grid = []
        for i in range(self.grid_size[1]):
            row = []
            for j in range(self.grid_size[0]):
                rect = pygame.Rect(
                    grid_position[0] + j * self.cell_size,
                    grid_position[1] + i * self.cell_size,
                    self.cell_size, self.cell_size
                )
                row.append(rect)
            grid.append(row)

        self.start_cell = pygame.Rect(self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size)
        self.end_cell = pygame.Rect(self.end[0] * self.cell_size, self.end[1] * self.cell_size, self.cell_size, self.cell_size)
        return grid

    def draw_maze(self):
        for i in range(self.grid_size[1]):
            row = []
            for j in range(self.grid_size[0]):
                if self.empty_cells[i][j]:
                    rect = pygame.Rect(
                        grid_position[0] + j * self.cell_size,
                        grid_position[1] + i * self.cell_size,
                        self.cell_size, self.cell_size
                    )
                    pygame.draw.rect(self.screen, white, rect, 1)

        if self.show_explored:
            for cell in self.explored_cells:
                pygame.draw.rect(self.screen, explored_color, cell)

        for cell in self.path:
            pygame.draw.rect(self.screen, path_color, cell)

        for cell in self.filled_cells:
            pygame.draw.rect(self.screen, highlight, cell)



        pygame.draw.rect(self.screen, end_color, self.end_cell)
        pygame.draw.rect(self.screen, start_color, self.start_cell)


    def draw_options(self):
        options_position_x = self.grid_size[0] * self.cell_size
        options_rect = pygame.Rect(
                    options_position_x,
                    0,
                    width - options_position_x,
                    height
                    )
        pygame.draw.rect(self.screen, options_box, options_rect)

        buttons = {}
        button_names = ["Solve", "Clear", "Grid Size", "Show Explored" if not self.show_explored else "Hide Explored", self.algorithm]
        button_size = (160, 60)
        button_top_margin = 20

        for i, button_name in enumerate(button_names):

            button_x = (width - options_position_x) / 2 + options_position_x - button_size[0] / 2
            button = pygame.Rect(
                        button_x,
                        button_top_margin * (i + 1) + i * button_size[1],
                        button_size[0],
                        button_size[1]
                        )
            if len(button_name) <= 12:
                button_text = mediumFont.render(button_name, True, black)
            else:
                button_text = smallFont.render(button_name, True, black)
            text_rect = button_text.get_rect()
            text_rect.center = button.center
            pygame.draw.rect(self.screen, button_color, button)
            self.screen.blit(button_text, text_rect)

            buttons[button_name] = button

        return buttons

    def indices_to_rects(self, indices):
        rect_array = []
        for index in indices:
            rect_array.append(pygame.Rect(index[0] * self.cell_size, index[1] * self.cell_size, self.cell_size, self.cell_size))
        return rect_array

if __name__ == "__main__":
    app = MazeInterface()
    app.run_app()
