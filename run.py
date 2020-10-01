import pygame
import sys

from maze import Maze

pygame.init()

size = width, height = 800, 600

black = (0,0,0)
white = (20,0,155)
highlight = (200, 40, 0)
options_box = (150,150,150)
button_color = (0,60,140)
start_color = (30, 220, 15)
end_color = (78, 10, 140)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)

screen = pygame.display.set_mode(size)

cell_size = 20
grid_position = (0, 0)
grid_size = (30, 30)

start = (0, 0)
end = (29, 29)

def setup_grid():
    grid = []
    for i in range(grid_size[1]):
        row = []
        for j in range(grid_size[0]):
            rect = pygame.Rect(
                grid_position[0] + j * cell_size,
                grid_position[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, white, rect, 1)
            row.append(rect)
        grid.append(row)

    return grid

def draw_maze(empty_cells, filled_cells):
    for i in range(grid_size[1]):
        row = []
        for j in range(grid_size[0]):
            if empty_cells[i][j]:
                rect = pygame.Rect(
                    grid_position[0] + j * cell_size,
                    grid_position[1] + i * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, white, rect, 1)

    for cell in filled_cells:
        pygame.draw.rect(screen, highlight, cell)

    start_cell = pygame.Rect(start[0] * cell_size, start[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, start_color, start_cell)
    end_cell = pygame.Rect(end[0] * cell_size, end[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, end_color, end_cell)

def draw_options():
    options_position_x = grid_size[0] * cell_size
    options_rect = pygame.Rect(
                options_position_x,
                0,
                width - options_position_x,
                height
                )
    pygame.draw.rect(screen, options_box, options_rect)

    buttons = {}
    button_names = ["Solve", "Clear"]

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
        pygame.draw.rect(screen, button_color, button)
        screen.blit(button_text, text_rect)

        buttons[button_name] = button

    return buttons

def clear_grid():
    print("clearing grid")

def main():
    empty_cells = setup_grid()

    filled_cells = []

    buttons = []
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if buttons[button].collidepoint(mouse):
                        if button == "Solve":
                            maze = Maze(grid_size, filled_cells)
                            maze.solve_maze()
                        elif button == "Clear":
                            empty_cells = setup_grid()
                            filled_cells = []

        screen.fill(black)

        draw_maze(empty_cells, filled_cells)
        buttons = draw_options()

        left_click, _, right_click = pygame.mouse.get_pressed()

        if left_click:
            for i in range(grid_size[1]):
                for j in range(grid_size[0]):
                    if empty_cells[i][j] and empty_cells[i][j].collidepoint(mouse):
                        if empty_cells[i][j] not in filled_cells:
                            filled_cells.append(empty_cells[i][j])
                            empty_cells[i][j] = None
        elif right_click:
            for cell in filled_cells:
                if cell.collidepoint(mouse):
                    grid_index = (int(cell.x/cell_size), int(cell.y/cell_size))
                    new_rect = pygame.Rect(cell.x, cell.y, cell_size, cell_size)
                    filled_cells.remove(cell)
                    empty_cells[grid_index[1]][grid_index[0]] = new_rect

        pygame.display.flip()

if __name__ == "__main__":
    main()
