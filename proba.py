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


# взять
# cur.execute("SELECT file_map FROM maps")
# data = cur.fetchall()[1][0]
# file_output = open("map1.txt", "wb")
# file_output.write(data)
# file_output.close()
# con.close()
# print(choice(data)[0])