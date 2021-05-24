# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

state = "Guest"
user_card_number = ""
card_pin = ""


def parse_to_luhn_sum(card_number):
    temp = list(card_number)
    temp = [int(digit) for digit in temp]  # change list elements to int
    for index in range(0, 16, 2):
        temp[index] *= 2
    temp = [digit - 9 if digit > 9 else digit for digit in temp]
    return sum(temp)


def luhn_algorithm(card_number):
    result = parse_to_luhn_sum(card_number[:-1]) % 10 + int(card_number[-1])
    if result == 10:
        return True
    return False


def get_checksum(card_number):
    sum_ = parse_to_luhn_sum(card_number) % 10
    return card_number + str((10 - sum_) % 10)


def create_account():
    global card_pin
    print('Your card has been created')
    print('Your card number:')
    iin = '400000'
    account_identifier = str(random.randint(0, 999999999)).zfill(9)
    card_number = iin + account_identifier
    card_number = get_checksum(card_number)
    card_pin = str(random.randint(0, 9999)).zfill(4)
    print(card_number)
    print('Your card PIN:')
    print(card_pin, end='\n\n')
    cur.execute('INSERT INTO card(number, pin) VALUES("' + card_number + '", "' + card_pin + '")')
    conn.commit()


def login():
    global user_card_number
    global card_pin
    global state
    try:
        card_number = input('Enter your card number:\n')
        pin_ = input('Enter your PIN:\n')
        print()
        cur.execute('SELECT number, pin FROM card WHERE number="' + card_number + '" AND pin="' + pin_ + '";')
        account = cur.fetchone()
        if account is not None:
            print('You have successfully logged in!')
            user_card_number = card_number
            card_pin = pin_
            state = 'User'
        else:
            raise KeyError
    except KeyError:
        print('Wrong card number or PIN!')
    finally:
        print()


def exit_():
    print('Bye!')
    exit(0)


def get_balance():
    return str(
        cur.execute('SELECT balance FROM card WHERE number="' + user_card_number + '" AND pin="' + card_pin + '";').fetchone()[0])


def check_balance():
    print('Balance: ' + get_balance(), end='\n\n')


def log_out():
    global state
    global user_card_number
    global card_pin
    print('You have successfully logged out!', end='\n\n')
    state = 'Guest'
    user_card_number = ''
    card_pin = ''


def update_balance(card, value, sign):
    cur.execute(
        'UPDATE card SET balance = balance ' + sign + ' ' + value + ' WHERE number="' + card + '";')
    conn.commit()


def add_income():
    plus = '+'
    value = input('Enter income:\n')
    update_balance(user_card_number, value, plus)
    print('Income was added!', end='\n\n')


def do_transfer():
    plus = '+'
    minus = '-'
    try:
        print('Transfer')
        card_number = input('Enter card number:\n')
        if len(card_number) != 16 or not luhn_algorithm(card_number):
            print('Probably you made a mistake in the card number.')
            print('Please try again!')
            return
        cur.execute('SELECT number FROM card WHERE number="' + card_number + '";')
        account = cur.fetchone()
        if account is None:
            raise KeyError
        if account[0] == user_card_number:
            print("You can't transfer money to the same account!")
            return
        value = input('Enter how much money you want to transfer:')
        print()
        balance = get_balance()
        if int(value) <= int(balance):
            update_balance(card_number, value, plus)
            update_balance(user_card_number, value, minus)
            print('Success!')
        else:
            print('Not enough money!')
    except KeyError:
        print('Such a card does not exist.')
    finally:
        print()


def close_account():
    cur.execute('DELETE FROM card WHERE number="' + user_card_number + '";')
    print('The account has been closed!\n')
    conn.commit()


guest_menu_name = {'1': '. Create an account',
                   '2': '. Log into account',
                   '0': '. Exit'
                   }
guest_action = {'1': create_account,
                '2': login,
                '0': exit_
                }
user_menu_name = {'1': '. Balance',
                  '2': '. Add income',
                  '3': '. Do transfer',
                  '4': '. Close account',
                  '5': '. Log out',
                  '0': '. Exit'
                  }
user_action = {'1': check_balance,
               '2': add_income,
               '3': do_transfer,
               '4': close_account,
               '5': log_out,
               '0': exit_
               }


def print_user_menu():
    for key in user_menu_name:
        print(key + user_menu_name[key])


def print_guest_menu():
    for key in guest_menu_name:
        print(key + guest_menu_name[key])


while True:
    if state == 'Guest':
        print_guest_menu()
        choice = input()
        print()
        guest_action[choice]()
    else:
        print_user_menu()
        choice = input()
        print()
        user_action[choice]()
