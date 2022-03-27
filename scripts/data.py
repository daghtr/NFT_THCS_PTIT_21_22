import mysql.connector as sql
import pandas as pd
import os
import time

count = 1
path = "C:/Users/Admin/Desktop/K2N4/thcs/testtesttest/data"
mydb = sql.connect(
    host="localhost",
    user="root",
    password="danghari2707",
    database="dagharitr_database"
    )

my_data = pd.read_sql("SELECT * FROM sensors11 where DATE(Time) = CURRENT_DATE()", mydb)

while True:
    text = "Data{}.txt".format(count)
    with open(os.path.join(path, text), 'w', encoding='utf-8') as file:
        print(my_data.to_dict('index'))
        file.write(str(my_data.to_dict('index')))
        count += 1
        time.sleep(30)