import os
from datetime import datetime
import sqlite3

def start_program():
    """
    The start_program function creates a table in the database if it doesn't already exist.
    It also prints a message to let the user know that they are starting up the program.
    
    :return: Nothing
    :doc-author: Trelent
    """
    try:
        cursor.execute('''
        CREATE TABLE shiftRegister (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        manager TEXT, 
        date DATETIME, 
        cash INT, 
        shift TEXT);
        ''')
    except sqlite3.OperationalError:
        print("Welcome again to the system.")

def shift_change():
    """
    The shift_change function is used to register the start of a new shift.
    It takes no parameters and returns the name of the manager who started that shift.
    
    :return: The name of the manager that is going to be in charge of the shift
    :doc-author: Trelent
    """
    print("Welcome to IT Burguers")
    manager = input("Enter the manager's name: ")
    cursor.execute('''INSERT INTO shiftRegister (manager, date, cash, shift) VALUES (?,?,?,?)''', (manager, str(datetime.now())[:-10], cash, "IN"))
    conn.commit()
    os.system("cls")
    return manager

def select_option():
    """
    The select_option function displays a menu of options for the user to choose from.
    It returns the option that was selected.
    
    :return: The value of the input
    :doc-author: Trelent
    """
    print('''
    1 - Load order.
    2 - Shift change.
    3 - Close program.
    ''')
    return input(">>> ")

def load_order():
    """
    The load_order function allows the user to insert a new order. It will ask for the client's name,
    the products ordered and their respective amounts, and finally it will calculate the total price of 
    the order. If there is no error in any input field, it will save all this information in a database file.
    
    :return: The total price of the order
    :doc-author: Trelent
    """
    client = input("Client's name: ")
    while True:
        try:
            print("Insert the products ordered: ")
            ammounComboS = int(input("Small Combo: "))
            ammounComboM = int(input("Medium Combo: "))
            ammounComboL = int(input("Large Combo: "))
            ammounIcecream = int(input("Icecream: "))
        except ValueError:
            print("Error. Try again.")
            os.system("cls")
        else:
            break
    totalToPay = ammounComboS * burguerComboS + ammounComboM * burguerComboM + ammounComboL * burguerComboL + ammounIcecream * icecream
    print(f"Total price: U$S{totalToPay}")
    while True:
        clientPayment = int(input("Client pays with >>> U$S"))
        if totalToPay >  clientPayment:
            print("Client does not have enough money.")
            if input("Would you like to cancel this order? [y/n] >>> ").lower() == 'y':
                break
        else:
            break
    if totalToPay > 0:
        try:
            cursor.execute('''
            CREATE TABLE sells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clientName TEXT,
            ammountComboS INTEGER,
            ammountComboM INTEGER,
            ammountComboL INTEGER,
            ammountIcecream INTEGER,
            totalPaid INTEGER,
            date DATETIME,
            manager TEXT
            );''')
        except sqlite3.OperationalError:
            pass
        cursor.execute('''INSERT INTO sells (clientName, ammountComboS, ammountComboM, ammountComboL, ammountIcecream, totalPaid, date, manager) VALUES(?,?,?,?,?,?,?,?)''',(client, ammounComboS, ammounComboM, ammounComboL, ammounIcecream, totalToPay, str(datetime.now())[:-10], manager))
        conn.commit()
        os.system("cls")
    return totalToPay

def shift_ends():
    """
    The shift_ends function is used to record the end of a shift. It takes no arguments and returns nothing.
    
    :return: The cash variable
    :doc-author: Trelent
    """
    cursor.execute('''INSERT INTO shiftRegister (manager, date, cash, shift) VALUES (?,?,?,?)''', (manager, str(datetime.now())[:-10], cash, "OUT"))
    conn.commit()

# Prices list
burguerComboS = 5
burguerComboM = 6
burguerComboL = 7
icecream = 2

cash = 0
totalCashInShift = 0

conn = sqlite3.connect("data.sqlite")
cursor = conn.cursor()

start_program()
manager = shift_change()

while True:
    option = select_option()
    if option == "1":
        cash += load_order()
    elif option == "2":
        shift_ends()
        manager = shift_change()
    elif option == "3":
        os.system("cls")
        print("Program closed.")
        break
    else:
        input("Invalid option. Try again.\nEnter to continue >>>")

conn.close()