import mysql.connector as sql
import pandas as pd
import os
import time

mydb = sql.connect(
    host="localhost",
    user="root",
    password="danghari2707",
    database="dagharitr_database"
    )

my_data = pd.read_sql("SELECT * FROM sensors11 where DATE(Time) = CURRENT_DATE()", mydb)


while True: 
    with open(os.path.join("C:/Users/Admin/Desktop/testcode/danhnhau", "data.txt"), 'w', encoding='utf-8') as file:
        print(my_data.to_dict('index'))
        file.write(str(my_data.to_dict('index')))
        time.sleep(10)