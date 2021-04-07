from dotenv import load_dotenv
load_dotenv()
from CommandLineArgs import CommandLineArgs
import os
import sys
from Database import Database

args = CommandLineArgs(sys.argv, 'file:str:!', 'action:str:!')
action = args.get('action')

db = Database(os.path.join('../', os.getenv('LOG_DB_NAME')))

if action == 'init':
    db.init_db()