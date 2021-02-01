import sqlite3

conn = sqlite3.connect('../urls.db')
c = conn.cursor()

c.execute('''CREATE TABLE images (url text UNIQUE)''')