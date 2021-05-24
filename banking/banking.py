# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

state = "Guest"
pin = ""


def checksum(card_number):
    temp = list(card_number)
    temp = [int(digit) for digit in temp]
    for index in range(14, -1, -2):
        temp[index] *= 2
    temp = [digit - 9 if digit > 9 else digit for digit in temp]
    sum_ = sum(temp) % 10
    return card_number + str((10 - sum_) % 10)


def create_account():
    global pin
    print('Your card has been created')
    print('Your card number:')
    iin = '400000'
    account_identifier = str(random.randint(0, 999999999)).zfill(9)
    card_number = iin + account_identifier
    card_number = checksum(card_number)
    pin = str(random.randint(0, 9999)).zfill(4)
    print(card_number)
    print('Your card PIN:')
    print(pin, end='\n\n')
    cur.execute('INSERT INTO card(number, pin) VALUES("' + card_number + '", "' + pin + '")')
    conn.commit()


def login():
    global state
    global pin
    try:
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin_ = input()
        print('')
        cur.execute('SELECT number, pin FROM card WHERE number="' + card_number + '" AND pin="' + pin_ + '";')
        account = cur.fetchone()
        if not account is None:
            print('You have successfully logged in!', end='\n\n')
            state = card_number
            pin = pin_
        else:
            raise KeyError
    except KeyError:
        print('Wrong card number or PIN!', end='\n\n')


def exit_():
    print('Bye!')
    exit(0)


def check_balance():
    cur.execute('SELECT balance FROM card WHERE number="' + state + '" AND pin="' + pin + '";')
    print('Balance: ' + str(cur.fetchone()[0]), end='\n\n')


def log_out():
    global state
    print('You have successfully logged out!', end='\n\n')
    state = 'Guest'


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
        print('')
        guest_action[choice]()
    else:
        print_user_menu()
        choice = input()
        print('')
        user_action[choice]()
