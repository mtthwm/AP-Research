import sqlite3;

class Database:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def exists(self, url):
        self.cur.execute('''SELECT COUNT(*) FROM images WHERE url=?''', url)