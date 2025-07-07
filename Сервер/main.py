import sqlite3

conn = sqlite3.connect('bd.db')

def list_notice():
    cursor = conn.cursor()
    l=[]
    for row in cursor.execute('SELECT name FROM notes').fetchall():
        l.append(row[0])
    return l

def new_notice(name):
    if not(name):
        return 0
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (name) VALUES (?)', (name,))
    conn.commit()
    return 1


def save_notice(name, text):
    if not name or not text:
        return 0 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM notes WHERE name = ?', (name,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute('UPDATE notes SET text = ? WHERE name = ?', (text, name))
    else:
        cursor.execute('INSERT INTO notes (name, text) VALUES (?, ?)', (name, text))


    conn.commit()
    return 1



def del_notice(name):
    cursor = conn.cursor()
    if not name:
        return 0
    if not(name in list_notice()):
        return 0
    cursor.execute('DELETE FROM notes WHERE name = ?', (name,))
    conn.commit()
    return 1

def get_notice(name):
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM notes WHERE name = ?', (name,))
    rows = cursor.fetchall()
    return rows[0][0]
