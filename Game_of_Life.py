import pygame
from pygame.locals import *
import random


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):              # по ширине с шагом размера ячейки
            pygame.draw.line(self.screen, pygame.Color('black'),    # поверхность - экран, цвет - чёрный,
                             (x, 0), (x, self.height))              # стартовая позиция и конечная
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()                                               # инициализация всех модулей pygame
        clock = pygame.time.Clock()                                 # создание объекта для отслеживания времени
        pygame.display.set_caption('Game of Life')                  # установить заголовок окна
        self.screen.fill(pygame.Color('black'))                     # заполнить поля белым цветом
        c = CellList(self.cell_width, self.cell_height, False)
        running = True
        while running:
            for event in pygame.event.get():                        # для каждого события из полученных
                if event.type == QUIT:                              # если событие завершилось, то конец
                    running = False

            c.update()
            c.draw(self.screen, self.cell_size)
            self.draw_grid()
            pygame.display.flip()                                   # обновляем полную поверхность дисплея
            clock.tick(self.speed)                                  # обновляем время
        pygame.quit()                                               # закрываем модули


class Cell:
    def __init__(self, state):
        self.neigh_al = 0
        self.state = state

    def is_alive(self):
        return self.state

    def get_neighbours(self, cell_list, x, y):
        neighbours = [(x + i, y + j)
                      for i in range(-1, 2)
                      for j in range(-1, 2)
                      if not i == j == 0]
        count_alive = 0
        for neighbour in neighbours:
            n, m = neighbour
            if 0 <= n < len(cell_list) and 0 <= m < len(cell_list[n]):
                if cell_list[n][m].is_alive():
                    count_alive += 1
        self.neigh_al = count_alive

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)


class CellList:
    def __init__(self, cols, rows, randomize=True, f='game.txt'):
        self.cols = cols
        self.rows = rows
        self.cell_list = []
        if randomize:
            for i in range(rows):
                self.cell_list.append([])
                for j in range(cols):
                    self.cell_list[i].append(Cell(random.randint(0, 1)))
        else:
            p = open(f)
            game_list = p.readlines()
            for i in range(len(game_list)):
                self.cell_list.append([])
                for j in range(len(game_list[0]) - 1):
                    self.cell_list[i].append(Cell(int(game_list[i][j])))

    def draw(self, screen, size):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell_list[i][j].is_alive() == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (j * size, i * size, size, size))
                else:
                    pygame.draw.rect(screen, pygame.Color('red'), (j * size, i * size, size, size))

    def update(self):
        new_cell_matrix = []
        for i in range(self.rows):
            new_cell_matrix.append([])
            for j in range(self.cols):
                self.cell_list[i][j].get_neighbours(self.cell_list, i, j)
                new_cell_matrix[i].append(Cell(0))
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell_list[i][j].is_alive() == 1:
                    if 2 <= self.cell_list[i][j].neigh_al <= 3:
                        new_cell_matrix[i][j] = Cell(1)
                    else:
                        new_cell_matrix[i][j] = Cell(0)
                else:
                    if self.cell_list[i][j].neigh_al == 3:
                        new_cell_matrix[i][j] = Cell(1)
                    else:
                        new_cell_matrix[i][j] = Cell(0)
        self.cell_list = new_cell_matrix

    def __iter__(self):
        self.i = 0
        self.j = 0
        return self

    def __next__(self):
        if self.j == self.cols:
            self.j = 0
            self.i += 1
        if self.i == self.rows:
            raise StopIteration
        if self.j < self.cols:
            cell = self.cell_list[self.i][self.j]
            self.j += 1
        return cell

    def __str__(self):
        return str(self.cell_list)

    def __repr__(self):
        return str(self.cell_list)

if __name__ == '__main__':
    game = GameOfLife(360, 120, 20)
    game.run()