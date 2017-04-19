import sqlite3


f = open('dump.sql','rb')
sql = f.read()

connection = sqlite3.connect('source.db')
cursor = connection.cursor()
cursor.executescript(sql)
connection.close()