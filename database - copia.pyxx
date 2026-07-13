import sqlite3
import os

DB_PATH = os.path.join("data", "missions.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_script(filename):
    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    conn = get_connection()
    conn.executescript(sql)
    conn.close()