import os.path

def read_sudoku(filename: object):
    """ Прочитать Судоку из файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    control_list = []
    jo = 0
    je = n
    list = []
    i = 0
    while i in range(len(values)):
        for j in range(jo, je):
            try:
                list.append(values[j])
            except:
                pass
        control_list.append(list)
        list = []
        jo += n
        je += n
        i += n
    return control_list


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


def find_empty_positions(grid):
    row, col, flag = 0, 0, 0
    for i in range(len(grid)):
        for number in grid[i]:
            if str(number) == '.':
                row, col, flag = i, col % 9, 1
                break
            else:
                col += 1
        if flag == 1:
            break
    if flag == 1:
        empty_pos = (row, col)
    else:
        empty_pos = None
    return empty_pos


def find_possible_values(grid, pos):
    many = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    possible_row = [str for str in many if str not in get_row(grid, pos)]
    possible_col = [str for str in many if str not in get_col(grid, pos)]
    possible_block = [str for str in many if str not in get_block(grid, pos)]
    control_possible = [str for str in possible_row if str in possible_col and str in possible_block]
    return control_possible


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    flag = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            in_col = get_col(solution, (i, j)).count(solution[i][j])
            in_row = get_row(solution, (i, j)).count(solution[i][j])
            in_block = get_block(solution, (i, j)).count(solution[i][j])
            if not (in_col == 1 and in_row == 1 and in_block == 1):
                flag = 1
                break
            if flag == 1:
                break
    if flag == 1:
        return False
    else:
        return True


def solve(grid):
    if find_empty_positions(grid) is None:
        return grid
    empty_pos = find_empty_positions(grid)
    if find_possible_values(grid, empty_pos):
        for possible_value in find_possible_values(grid, empty_pos):
            grid[empty_pos[0]][empty_pos[1]] = possible_value
            s = solve(grid)
            if s:
                return grid
            grid[empty_pos[0]][empty_pos[1]] = '.'


if __name__ == '__main__':
    for name in ['sudoku.txt', ]:
        scriptpath = os.path.dirname(__file__)
        fname = os.path.join(scriptpath, name)
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
        print(check_solution(solution))