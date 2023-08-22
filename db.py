import sqlite3

connex = sqlite3.connect('motorbike.sqlite')

cursor = connex.cursor()
sql_query = """ CREATE TABLE moto (
        id integer PRIMARY KEY,
        company text NOT NULL,
        model text NOT NULL,
        cm3 integer NOT NULL,
        price integer NOT NULL,
        year integer NOT NULL
)"""
cursor.execute(sql_query)