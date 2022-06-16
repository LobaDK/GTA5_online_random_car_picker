import os
import sqlite3
import sys
import platform
import random
from time import sleep
def clear(): #function to clear the terminal
    if sys.platform.startswith('win'):
        os.system('CLS')
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        os.system('clear')

if not os.path.exists(os.path.join(os.getcwd(),"ownedvehicles.db")): #if database file is not found
    while(True):
        clear()
        nd = input('No database was found. If you moved the script, remember to move the "ownedvehicles.db" file with it. Create new database? Y/N: ').upper()
        if nd == 'N': #if user does not wish to create new database
            print('Exiting as a database is required...')
            sleep(3)
            sys.exit()
        elif nd == 'Y': #if user wishes to create new database
            con = sqlite3.connect(os.path.join(os.getcwd(),"ownedvehicles.db")) #create database named "ownedvehicles.db"
            cur = con.cursor()
            #create table named "vehicles" with ID as integer, VehicleName as text, cannot be empty and has to be unique, VehicleClass as text and cannot be empty, and add primary key with autoincrement to "ID"
            cur.execute('CREATE TABLE vehicles ("VehicleName" TEXT NOT NULL UNIQUE collate nocase, "VehicleClass" TEXT NOT NULL collate nocase)') 
            con.commit()
            con.close()
            break
        else:
            print('Invalid option')
            sleep(2)
            continue

con = sqlite3.connect(os.path.join(os.getcwd(),"ownedvehicles.db"))
cur = con.cursor()
while(True):
    DisplayID = 1
    addmore = False
    clear()
    mm = input('(R)random vehicle or (M)odify list?: ').upper()
    if mm == 'M':
        while(True):
            clear()
            dm = input('(A)dd, (V)iew or (R)emove?: ').upper()
            if dm == 'A':
                while(True):
                    clear()
                    vn = input('Please input vehicle name: ')
                    if not vn:
                        print('Input cannot be empty')
                        continue
                    vc = input('\nPlease input vehicle class: ')
                    if not vc:
                        print('Input cannot be empty')
                        continue
                    if vc.casefold() == 'sport':
                        vc = 'Sports'
                    cur.execute('INSERT INTO vehicles (VehicleName, VehicleClass) VALUES (?, ?)',(vn,vc,))
                    con.commit()
                    while(True):
                        am = input('Add more? Y/N: ').upper()
                        if am == 'Y':
                            addmore = True
                            break
                        elif am == 'N':
                            addmore = False
                            break
                        else:
                            print('Invalid option')
                            sleep(2)
                            continue
                    if addmore == True:
                        continue
                    else:
                        break
            elif dm == 'V':
                while(True):
                    DisplayID = 1
                    clear()
                    vm = input('List (A)ll or (S)earch?: ').upper()
                    if vm == 'A':
                        print('\n')
                        for allrow in cur.execute('SELECT * FROM vehicles ORDER BY ROWID ASC'):
                            print(DisplayID, allrow)
                            DisplayID += 1
                            print('--------------------------------------------------------------')
                        input('\nPress enter to continue...')
                        break
                    elif vm == 'S':
                        while(True):
                            clear()
                            sm = input('Search (C)lass or (N)ame?: ').upper()
                            if sm == 'C':
                                while(True):
                                    DisplayID = 1
                                    clear()
                                    cs = input("Please enter vehicle class you're searching for: ")
                                    if not cs:
                                        print('Input cannot be empty')
                                        continue
                                    else:
                                        for classrow in cur.execute('SELECT * FROM vehicles WHERE VehicleClass like ? ORDER BY ROWID ASC',(cs+'%',)):
                                            print(DisplayID, classrow)
                                            DisplayID += 1
                                            print('--------------------------------------------------------------')
                                        input('\nPress enter to continue...')
                                        break
                            elif sm == 'N':
                                while(True):
                                    DisplayID = 1
                                    clear()
                                    ns = input("Please enter vehicle name you're searching for: ")
                                    if not ns:
                                        print('Input cannot be empty')
                                        continue
                                    else:
                                        for namerow in cur.execute('SELECT * FROM vehicles WHERE VehicleName like ? ORDER BY ROWID ASC',('%'+ns+'%',)):
                                            print(DisplayID, namerow)
                                            DisplayID += 1
                                            print('--------------------------------------------------------------')
                                        input('\nPress enter to continue...')
                                        break
                            else:
                                print('Invalid option')
                                sleep(2)
                                continue
                            break
                    break
            elif dm == 'R':
                while(True):
                    DisplayID = 1
                    clear()
                    for allrow in cur.execute('SELECT * FROM vehicles ORDER BY ROWID ASC'):
                        print(DisplayID, allrow)
                        DisplayID += 1
                        print('--------------------------------------------------------------')
                    di = input('Please specify the ID of the entry you wish to delete, or type "back" to return: ')
                    if di.isdigit():
                        while(True):
                            print('Are you sure you wanna delete the following entry?\n')
                            for deleterow in cur.execute('SELECT * FROM vehicles WHERE ROWID == ?',(di,)):
                                print(deleterow)
                            dc = input('\nY/N: ').upper()
                            if dc == 'Y':
                                cur.execute('DELETE FROM vehicles WHERE ROWID == ?',(di,))
                                con.commit()
                            elif dc == 'N':
                                break
                            else:
                                print('Invalid option')
                                sleep(2)
                                continue
                            break
                    elif di == 'back':
                        break
                    else:
                        print('ID cannot be empty and not a number')
                        sleep(2)
                        continue
                break

            else:
                print('Invalid option')
                sleep(2)
                continue
            break
    elif mm == 'R':
        while(True):
            rm = input('Chose class? Y/N: ').upper()
            if rm == 'Y':
                rc = input('Input vehicle class: ')
                con.row_factory = lambda cursor, row: row[0]
                c = con.cursor()
                cars = c.execute('SELECT VehicleName FROM vehicles WHERE VehicleClass like ?',(rc,)).fetchall()
                RNG = random.randint(0,len(cars))
                print(cars[RNG])
            elif rm == 'N':
                con.row_factory = lambda cursor, row: row[0]
                c = con.cursor()
                cars = c.execute('SELECT VehicleName FROM vehicles').fetchall()
                RNG = random.randint(0,len(cars))
                print(cars[RNG])
                input('Press enter to continue...')
                break
            else:
                print('Invalid option')
                sleep(2)
                continue
    else:
        print('Invalid option')
        sleep(2)
        continue