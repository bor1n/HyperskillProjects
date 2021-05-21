def print_table():
    print('---------')
    i = 0
    for row_ in range(3):
        print("| " + table[row_][0] + " " + table[row_][1] + " " + table[row_][2] + " |")
        i += 3
    print('---------')


def check_row(row_):
    first_row_symbol = table[row_][0]
    second_row_symbol = table[row_][1]
    third_row_symbol = table[row_][2]
    return first_row_symbol == second_row_symbol == third_row_symbol != empty


def check_column(column):
    first_column_symbol = table[0][column]
    second_column_symbol = table[1][column]
    third_column_symbol = table[2][column]
    return first_column_symbol == second_column_symbol == third_column_symbol != empty


def check_left_diagonal():
    top_left_symbol = table[0][0]
    middle_symbol = table[1][1]
    bottom_right_symbol = table[2][2]
    return top_left_symbol == middle_symbol == bottom_right_symbol != empty


def check_right_diagonal():
    top_right_symbol = table[2][0]
    middle_symbol = table[1][1]
    bottom_left_symbol = table[0][2]
    return top_right_symbol == middle_symbol == bottom_left_symbol != empty


def check_state():
    winner = {'O': 0, 'X': 0}

    for n in range(3):
        if check_column(n):
            winner[table[0][n]] += 1
        if check_row(n):
            winner[table[n][0]] += 1
    if check_left_diagonal():
        winner[table[0][0]] += 1
    if check_right_diagonal():
        winner[table[2][0]] += 1

    if winner['X'] == 1:
        print('X wins')
        exit(0)

    if winner['O'] == 1:
        print('O wins')
        exit(0)

    for row_ in table:
        if row_.__contains__(empty):
            return
    print('Draw')
    exit(0)


def get_coordinates(symbol):
    global table
    coordinates = input('Enter the coordinates: ').split()
    try:
        coordinates = [int(position) for position in coordinates]
    except ValueError:
        print('You should enter numbers!')
        get_coordinates(symbol)
        return
    pos_y = coordinates[0] - 1
    pos_x = coordinates[1] - 1

    if pos_y < 0 or pos_y > 2 or pos_x < 0 or pos_x > 2:
        print('Coordinates should be from 1 to 3!')
        get_coordinates(symbol)
    elif table[pos_y][pos_x] == empty:
        table_row = list(table[pos_y])
        table_row[pos_x] = symbol
        table[pos_y] = "".join(table_row)
        print_table()
    else:
        print("This cell is occupied! Choose another one!")
        get_coordinates(symbol)


empty = ' '
table = ['a'] * 3
for row in range(3):
    table[row] = empty * 3
print_table()

while True:
    get_coordinates('X')
    check_state()
    get_coordinates('O')
    check_state()
