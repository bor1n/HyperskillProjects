def print_table():
    print('---------')
    i = 0
    for k in range(3):
        print("| " + string[i] + " " + string[i + 1] + " " + string[i + 2] + " |")
        i += 3
    print('---------')


def check_state(string):

    def is_x(symbol):
        if symbol == 'X':
            return True
        return False

    def is_o(symbol):
        if symbol == 'O':
            return True
        return False

    # x_counter = 0
    # o_counter = 0
    # for symbol in string:
    #     if symbol == 'X':
    #         x_counter += 1
    #     if symbol == 'O':
    #         o_counter += 1
    # if o_counter > x_counter + 1 or x_counter > o_counter + 1:
    #     print('Impossible')
    #     exit(0)

    x_win_counter = 0
    o_win_counter = 0
    index = 0
    for counter in range(3):
        if is_x(string[index]) and is_x(string[index + 3]) and is_x(string[index + 6]):
            x_win_counter += 1
        if is_o(string[index]) and is_o(string[index + 3]) and is_o(string[index + 6]):
            o_win_counter += 1
        index += 1
    index = 0
    for counter in range(3):
        if is_x(string[index]) and is_x(string[index + 1]) and is_x(string[index + 2]):
            x_win_counter += 1
        if is_o(string[index]) and is_o(string[index + 1]) and is_o(string[index + 2]):
            o_win_counter += 1
        index += 2
    if is_x(string[0]) and is_x(string[4]) and is_x(string[8]):
        x_win_counter += 1
    if is_o(string[0]) and is_o(string[4]) and is_o(string[8]):
        o_win_counter += 1
    if is_x(string[6]) and is_x(string[4]) and is_x(string[2]):
        x_win_counter += 1
    if is_o(string[6]) and is_o(string[4]) and is_o(string[2]):
        o_win_counter += 1

    # if o_win_counter > 1 or x_win_counter > 1 or (o_win_counter == 1 and x_win_counter == 1):
    #     print('Impossible')
    #     exit(0)

    if x_win_counter == 1:
        print('X wins')
        exit(0)

    if o_win_counter == 1:
        print('O wins')
        exit(0)

    if not string.__contains__(' '):
        print('Draw')
        exit(0)

    # if o_win_counter == 0 and x_win_counter == 0:
    #     print('Draw')
    #     exit(0)


def get_coordinates(symbol):
    global string
    coordinates = input('Enter the coordinates: ').split()
    try:
        coordinates = [int(position) for position in coordinates]
    except ValueError as ve:
        print('You should enter numbers!')
        get_coordinates(symbol)
        return
    pos_y = coordinates[0]
    pos_x = coordinates[1]

    if pos_y < 1 or pos_y > 3 or pos_x < 1 or pos_x > 3:
        print('Coordinates should be from 1 to 3!')
        get_coordinates(symbol)
    elif string[(pos_y - 1) * 3 + pos_x - 1] == ' ':
        string_in_list = list(string)
        string_in_list[(pos_y - 1) * 3 + pos_x - 1] = symbol
        string = "".join(string_in_list)
        print_table()
    else:
        print("This cell is occupied! Choose another one!")
        get_coordinates(symbol)


string = "         "
print_table()

while True:
    get_coordinates('X')
    check_state(string)
    get_coordinates('O')
    check_state(string)
