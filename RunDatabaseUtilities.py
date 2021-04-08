from dotenv import load_dotenv
load_dotenv()
from utils.CommandLineArgs import CommandLineArgs
import os
import sys
from utils.Database import Database

args = CommandLineArgs(sys.argv, 'file:str:!', 'action:str:!')
action = args.get('action')

db = Database(os.getenv('LOG_DB_NAME'))

if action == 'init':
    db.init_db()
elif action == 'flush':
    db.flush()