import sqlite3
from random import choice

con = sqlite3.connect('maps.db')
cur = con.cursor()

# вставить
file_input = open("map.txt", "rb")
file = file_input.read()
file_input.close()
binary = sqlite3.Binary(file)
cur.execute("INSERT INTO maps(file_map) VALUES (?)", (binary,))
con.commit()
