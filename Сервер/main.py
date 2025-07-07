import sqlite3
from fastapi import FastAPI

app = FastAPI()

def get_connection():
    return sqlite3.connect("bd.db")

@app.get("/list")
def list_notice():
    conn = get_connection()
    cursor = conn.cursor()
    l=[]
    for row in cursor.execute('SELECT name FROM notes').fetchall():
        l.append(row[0])
    return l

@app.get("/new")
def new_notice(name:str):
    if not(name):
        return 0
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (name) VALUES (?)', (name,))
    conn.commit()
    return 1

@app.get("/save")
def save_notice(name:str, text:str):
    if not name or not text:
        return 0
    conn = get_connection() 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM notes WHERE name = ?', (name,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute('UPDATE notes SET text = ? WHERE name = ?', (text, name))
    else:
        cursor.execute('INSERT INTO notes (name, text) VALUES (?, ?)', (name, text))

    conn.commit()
    return 1



@app.get("/del")
def del_notice(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    if not name:
        return 0
    if not(name in list_notice()):
        return 0
    cursor.execute('DELETE FROM notes WHERE name = ?', (name,))
    conn.commit()
    return 1

@app.get("/get")
def get_notice(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM notes WHERE name = ?', (name,))
    rows = cursor.fetchall()
    return rows[0][0]
