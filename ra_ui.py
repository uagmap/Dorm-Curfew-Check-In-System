#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD
import sys
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="RA",
    passwd="admin",
    database="checkinsystem"
)
            
cursor = db.cursor()
reader = SimpleMFRC522()
lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

def read_rfid_card():
    lcd.clear()
    lcd.message('Place Card to\nregister')
    global id
    id, text = reader.read()
    cursor.execute("SELECT id FROM users WHERE rfid_uid="+str(id))
    cursor.fetchone()
    if cursor.rowcount >= 1:
        return True
        lcd.clear()
        lcd.message("Overwrite\nexisting user?")
    else:
        return False
        
def overwrite_rfid():
    lcd.clear()
    lcd.message("Overwriting user.")
    time.sleep(1)
    global sql_insert
    sql_insert = "UPDATE users SET name = %s, room = %s WHERE rfid_uid=%s"

    
def write_rfid():
    global sql_insert
    sql_insert = "INSERT INTO users (name, room, rfid_uid) VALUES (%s, %s, %s)" 
    
def cursor_execute(new_name, new_room):
    cursor.execute(sql_insert, (new_name, new_room, id))
    db.commit()
    lcd.clear()
    lcd.message("User " + new_name + "\nSaved")
    time.sleep(2)
    lcd.clear()
    
def show_status_date(date):
    join = "SELECT users.name, users.room, attendance.clock_in FROM users JOIN attendance ON users.id = attendance.user_id WHERE attendance.clock_in >= '" + date + " 00:00:00' AND attendance.clock_in < '" + date + " 00:00:00' + INTERVAL 1 DAY"
    cursor.execute(join)
    output = cursor.fetchall()
    return output
 
def show_status_today():
    join = "SELECT users.name, users.room, attendance.clock_in FROM users JOIN attendance ON users.id = attendance.user_id WHERE attendance.clock_in >= CURDATE() AND attendance.clock_in < CURDATE() + INTERVAL 1 DAY"
    cursor.execute(join)
    output = cursor.fetchall()
    return output

