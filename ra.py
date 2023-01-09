#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD
import sys
from datetime import datetime

print(datetime.date(datetime.now()))

db = mysql.connector.connect(
    host="localhost",
    user="RA",
    passwd="admin",
    database="checkinsystem"
)
    
cursor = db.cursor()
reader = SimpleMFRC522()
lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

print("***MENU***")
print("1 - register new resident")
print("2 - view residents' status")
print('')
menuchoice = 0
while True:
    try:
        menuchoice = int(input("Enter your menu choice: "))
        break
    except ValueError:
        print("Please enter a valid option!")
        print('')
        time.sleep(1)
        
try:
    if menuchoice == 1:
      while True:
        lcd.clear()
        lcd.message('Place Card to\nregister')
        id, text = reader.read()
        cursor.execute("SELECT id FROM users WHERE rfid_uid="+str(id))
        cursor.fetchone()

        if cursor.rowcount >= 1:
          lcd.clear()
          lcd.message("Overwrite\nexisting user?")
          overwrite = input("Overwrite (Y/N)? ")
          if overwrite[0] == 'Y' or overwrite[0] == 'y':
            lcd.clear()
            lcd.message("Overwriting user.")
            time.sleep(1)
            sql_insert = "UPDATE users SET name = %s, room = %s WHERE rfid_uid=%s"
          else:
            continue;
        else:
          sql_insert = "INSERT INTO users (name, room, rfid_uid) VALUES (%s, %s, %s)"
        lcd.clear()
        
        lcd.message('Enter new name')
        new_name = input("Name: ")
        lcd.clear()
        
        lcd.message('Enter room number')
        new_room = input("Room: ")
        lcd.clear()

        cursor.execute(sql_insert, (new_name, new_room, id))

        db.commit()

        lcd.clear()
        lcd.message("User " + new_name + "\nSaved")
        time.sleep(2)
    if menuchoice == 2:
        date = datetime.date(datetime.now())
        print("today's date: " + str(date))
        print(' ')
        print("Resident:\tRoom:\t\tLast check-in:")
        print(' ')
        join = "SELECT users.name, users.room, attendance.clock_in FROM users JOIN attendance ON users.id = attendance.user_id WHERE attendance.clock_in >= CURDATE() AND attendance.clock_in < CURDATE() + INTERVAL 1 DAY"
        cursor.execute(join)
        output = cursor.fetchall()
        for x in range(len(output)):
            for y in range(len(output[x])):
                print(output[x][y], end = '\t | \t')
            print()
    else:
        print("Please enter a valid option!")
        print('')
        time.sleep(1)
        sys.exit()
        
finally:
    GPIO.cleanup()