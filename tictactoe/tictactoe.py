def print_table():
    print('---------')
    i = 0
    for row in range(3):
        print("| " + table[row][0] + " " + table[row][1] + " " + table[row][2] + " |")
        i += 3
    print('---------')


def check_state(table):

    winter = {'O': 0, 'X': 0}

    for column in range(3):
        if table[0][column] == table[1][column] == table[2][column] != ' ':
            winter[table[0][column]] += 1
    for row in range(3):
        if table[row][0] == table[row][1] == table[row][2] != ' ':
            winter[table[row][0]] += 1
    if table[0][0] == table[1][1] == table[2][2] != ' ':
        winter[table[0][0]] += 1
    if table[2][0] == table[1][1] == table[0][2] != ' ':
        winter[table[2][0]] += 1

    if winter['X'] == 1:
        print('X wins')
        exit(0)

    if winter['O'] == 1:
        print('O wins')
        exit(0)

    for row in table:
        if row.__contains__(' '):
            return
    print('Draw')
    exit(0)


def get_coordinates(symbol):
    global table
    coordinates = input('Enter the coordinates: ').split()
    try:
        coordinates = [int(position) for position in coordinates]
    except ValueError as ve:
        print('You should enter numbers!')
        get_coordinates(symbol)
        return
    pos_y = coordinates[0] - 1
    pos_x = coordinates[1] - 1

    if pos_y < 0 or pos_y > 2 or pos_x < 0 or pos_x > 2:
        print('Coordinates should be from 1 to 3!')
        get_coordinates(symbol)
    elif table[pos_y][pos_x] == ' ':
        table_row = list(table[pos_y])
        table_row[pos_x] = symbol
        table[pos_y] = "".join(table_row)
        print_table()
    else:
        print("This cell is occupied! Choose another one!")
        get_coordinates(symbol)


table = ['a'] * 3
for row in range(3):
    table[row] = ' ' * 3
print_table()

while True:
    get_coordinates('X')
    check_state(table)
    get_coordinates('O')
    check_state(table)
