from datetime import date, time, timedelta, datetime
import time
from random import randint
import pyodbc


con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\user\Desktop\web\farm.accdb;'
conn = pyodbc.connect(con_string)

def insert(id):
    try:
        cursor = conn.cursor()

        flow = randint(100, 400)
        vacuum = randint(0, 1)
        now = datetime.now()

        myuser = ((id, flow, vacuum, now),)

        cursor.executemany('INSERT INTO situation VALUES (?,?,?,?)', myuser)
        conn.commit()
        print('Запись добавлена')

    except pyodbc.Error as e:
        print("Error in connection", e)

counter = 1
while True:
    insert(counter)
    counter += 1
    time.sleep(5)