import sqlite3
from datetime import datetime
from utils.functions import GeneratedSequence

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

    def init_db (self):
        self.cur.execute('''CREATE TABLE sequence (
            id INTEGER NOT NULL,
            bits_generated INTEGER,
            generation_time REAL,
            bit_rate REAL,
            time_started TEXT NOT NULL,
            time_finished TEXT,
            PRIMARY KEY (ID)  
        )''')
        self.cur.execute('''CREATE TABLE image (
            id INTEGER NOT NULL,
            image_key TEXT NOT NULL,
            bits_generated INTEGER NOT NULL,
            generation_time REAL NOT NULL,
            bit_rate REAL NOT NULL,
            time_generated TEXT NOT NULL,
            sequence_id INTEGER,
            FOREIGN KEY (sequence_id) REFERENCES sequence(id),
            PRIMARY KEY (ID)
        )''')
        self.conn.commit()

    def create_image (self, seq:GeneratedSequence):
        self.cur.execute('''INSERT INTO image (image_key, bits_generated, generation_time, bit_rate, time_generated, sequence_id) VALUES (?, ?, ?, ?, ?, ?)''', (seq.image_key, len(seq), seq.generation_time, seq.bit_rate, seq.time_generated, seq.sequence_id))
        self.conn.commit()
        return self.cur.lastrowid

    def start_sequence (self, time_started:datetime):
        self.cur.execute('''INSERT INTO sequence (time_started) VALUES (?)''', (time_started,))
        self.conn.commit()
        return self.cur.lastrowid

    def end_sequence (self, id:int, bits_generated:int, generation_time:float, bit_rate:float, time_finished:datetime):
        self.cur.execute('''UPDATE sequence SET bits_generated=?, generation_time=?, bit_rate=?, time_finished=? WHERE id=?''', (bits_generated, generation_time, bit_rate, time_finished, id))
        self.conn.commit()
        return self.cur.lastrowid

    def flush (self):
        if input(f'Doing this will IRREVERSIBLY DESTORY all logs in the database {self.filename}. Are you sure? Y/N ') in ('Yes', 'y', 'Y'):
            self.cur.execute('''DELETE FROM image''')
            self.cur.execute('''DELETE FROM sequence''')
            self.conn.commit()
            print('Database flushed.')
        else:
            print('Cancelled database flush.')
    