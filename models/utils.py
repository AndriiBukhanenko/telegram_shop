import os
import pymysql

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWD = os.getenv("PASSWD")
DB = os.getenv("DB")


def db_connect():
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
    cursor = db.cursor()
    return  cursor