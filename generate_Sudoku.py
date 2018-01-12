# создаёт базовый пазл
grid = [[str((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)]


def transposing(grid):  # функция транспонирует паззл, то есть строки становятся столбцами и наоборот
    return list(map(list, zip(*grid)))
    # zip составит кортеж из всех 1ых, 2ых, 3их и т.д. элементов списков в grid
    # map исп-ся для каждого кортежа, полученного с помощью zip и преобразует в список; вернёт кортеж
    # полученный кортеж нужно преобразовать в список


import random


def swap_rows_small(grid):  # обмен двух строк !в пределах одного района!
    area = random.randrange(0, 2, 1)  # получение случайного района
    line1 = random.randrange(0, 2, 1)  # получение случайной строки
    n1 = area * 3 + line1  # номер 1 строки для обмена
    line2 = random.randrange(0, 2, 1)
    while (line1 == line2):  # чтобы выбранные строки были разными
        line2 = random.randrange(0, 2, 1)
    n2 = area * 3 + line2  # номер 2 строки для обмена
    grid[n1], grid[n2] = grid[n2], grid[n1]
    return grid


def swap_colums_small(grid):
    grid = transposing(grid)
    grid = swap_rows_small(grid)
    grid = transposing(grid)
    return grid


def swap_rows_area(grid):
    area1 = random.randrange(0, 2, 1)  # получение случайного района
    area2 = random.randrange(0, 2, 1)  # получение второго случайного района
    while (area1 == area2):  # чтобы выбранные районы были разными
        area2 = random.randrange(0, 2, 1)
    for i in range(0, 2):  # меняем строки в этом районе
        n1, n2 = area1 * 3 + i, area2 * 3 + i
        grid[n1], grid[n2] = grid[n2], grid[n1]
    return grid


def swap_colums_area(grid):
    grid = transposing(grid)
    grid = swap_rows_area(grid)
    grid = transposing(grid)
    return grid


def mix(grid, count=5):  # функция, выполняющая 10 рандомных преобразований над паззлом
    mix_func = ['transposing(grid)', 'swap_rows_small(grid)', 'swap_colums_small(grid)', 'swap_rows_area(grid)',
                'swap_colums_area(grid)']
    for i in range(1, count):
        id_func = random.randrange(0, len(mix_func), 1)
        eval(mix_func[id_func])  # выполняет строку программного кода.
    return grid


def insert_point(grid):
    zero = [['0' for j in range(3 * 3)] for i in range(3 * 3)]
    iterator = 0
    difficult = 40  # Первоначально все элементы на месте
    while iterator <= 40:
        i, j = random.randrange(0, 9, 1), random.randrange(0, 9, 1)  # Выбираем случайную позицию
        if zero[i][j] == '0':  # Если её не смотрели
            iterator += 1
            zero[i][j] = '1'  # Посмотрели
            temp = grid[i][j]  # Сохраним элемент на случай если без него нет решения или их слишком много
            grid[i][j] = '.'
            table_solution = []
            for copy_i in range(0, 3 * 3):
                table_solution.append(grid[copy_i][:])  # Скопируем в отдельный список
    return grid


def get_row(values, pos):
    return values[pos[0]]


def get_col(values, pos):
    list = []
    for i in range(9):
        list.append(values[i][pos[1] % 9])
    return list


def get_block(values, pos):
    list_rows = []
    if pos[0] in range(3):
        for i in range(0, 3):
            list_rows.append(values[i])
    elif pos[0] in range(3, 6):
        for i in range(3, 6):
            list_rows.append(values[i])
    else:
        for i in range(6, 9):
            list_rows.append(values[i])
    control_list = []
    if pos[1] in range(3):
        for list in list_rows:
            for j in range(3):
                control_list.append(list[j])
    elif pos[1] in range(3, 6):
        for list in list_rows:
            for j in range(3, 6):
                control_list.append(list[j])
    else:
        for list in list_rows:
            for j in range(6, 9):
                control_list.append(list[j])
    return control_list


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    flag = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            in_col = get_col(solution, (i, j)).count(solution[i][j])
            in_row = get_row(solution, (i, j)).count(solution[i][j])
            in_block = get_block(solution, (i, j)).count(solution[i][j])
            if in_col + in_row + in_block > 3:
                flag = 1
                break
            if flag == 1:
                break
    if flag == 1:
        return False
    else:
        return True


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)


solution = mix(grid)

while check_solution(solution) is False:
    solution = mix(grid)
print(solution)

print(check_solution(solution))

display(insert_point(solution))
