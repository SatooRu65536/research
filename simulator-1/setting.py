import sys
import os
import sqlite3
import random
from cmath import sqrt

import config as cf


def main():
    print('⚡️start setting.py')
    db_init()


def db_init(table_name='control'):
    conn = sqlite3.connect(f'{cf.DB_PATH}', isolation_level=None)
    cur = conn.cursor()
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
        car_id      TEXT,
        origin      INTEGER,
        destination INTEGER,
        status      TEXT, 
        time        REAL
    )''')

    cur.execute(f'DELETE FROM {table_name}')


def db_clear():
    try:
        os.remove(cf.DB_PATH)
    finally:
        conn = sqlite3.connect(f'{cf.DB_PATH}', isolation_level=None)
        db_init()
        print('⚡️綺麗にしました')


def remove_table(table_name='control'):
    conn = sqlite3.connect(f'{cf.DB_PATH}', isolation_level=None)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE {table_name}')


if __name__ == '__main__':
    if 'clear' in sys.argv:
        db_clear()
    else:
        main()
