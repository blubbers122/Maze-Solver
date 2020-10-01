import pygame
import sys

from maze import Maze

pygame.init()

black = (0,0,0)
white = (20,0,155)
highlight = (200, 40, 0)
path_color = (0, 200, 230)
options_box = (150,150,150)
button_color = (0,60,140)
start_color = (30, 220, 15)
end_color = (78, 10, 140)

medium_settings = [30, [20, 20]]
large_settings = [20, [30, 30]]
grid_position = (0, 0)

size = width, height = 800, 600

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)

class MazeInterface():
    def __init__(self):
        self.cell_size = 30
        self.grid_size = [20, 20]
        self.start = [0, 0]
        self.end = [19, 19]
        self.empty_cells = []
        self.filled_cells = []
        self.wall_indices = []
        self.buttons = []
        self.path = []
        self.count = 0
        self.screen = pygame.display.set_mode(size)


    def run_app(self):
        self.empty_cells = self.setup_grid()

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if self.buttons[button].collidepoint(mouse):
                            if button == "Solve":
                                maze = Maze(self.grid_size, self.start, self.end, self.wall_indices)
                                self.path, self.count = maze.solve_maze()
                                print("length of path", len(self.path))
                                if self.path:
                                    self.path = self.indices_to_rects(self.path)

                                print(self.count)

                            elif button == "Clear":
                                self.clear_grid()
                            elif button == "Grid Size":
                                _settings = large_settings if self.grid_size == [20, 20] else medium_settings
                                print("changing size")
                                self.change_grid_size(_settings)
                                self.clear_grid()

            self.screen.fill(black)

            self.draw_maze()
            self.buttons = self.draw_options()

            left_click, _, right_click = pygame.mouse.get_pressed()

            if left_click:
                for i in range(self.grid_size[1]):
                    for j in range(self.grid_size[0]):
                        cell = self.empty_cells[i][j]
                        if cell and cell.collidepoint(mouse):
                            if cell not in self.filled_cells:
                                self.filled_cells.append(cell)
                                self.wall_indices.append((int(cell.x/self.cell_size), int(cell.y/self.cell_size)))
                                cell = None
            elif right_click:
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
                pygame.draw.rect(self.screen, white, rect, 1)
                row.append(rect)
            grid.append(row)

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

        for cell in self.path:
            pygame.draw.rect(self.screen, path_color, cell)

        for cell in self.filled_cells:
            pygame.draw.rect(self.screen, highlight, cell)

        start_cell = pygame.Rect(self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, start_color, start_cell)
        end_cell = pygame.Rect(self.end[0] * self.cell_size, self.end[1] * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, end_color, end_cell)

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
        button_names = ["Solve", "Clear", "Grid Size"]

        button_size = (160, 60)
        button_top_margin = 20

        for i, button_name in enumerate(button_names):

            button_x = (width - options_position_x) / 2 + options_position_x - button_size[0] / 2
            button = pygame.Rect(
                        button_x,
                        button_top_margin * i + i * button_size[1],
                        button_size[0],
                        button_size[1]
                        )

            button_text = mediumFont.render(button_name, True, black)
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
