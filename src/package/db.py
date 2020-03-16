import os
import sqlite3
import package.fileHandler as fileHandler

dbPath = ""
conn = None
c = None

def setup(dir="db", filename="db"):
    global dbPath

    rootDir = fileHandler.dir(__file__, 3)

    dbDir = "{0}/{1}".format(rootDir, dir)
    fileHandler.safeMkdir(dbDir)
    dbPath = "{0}/{1}".format(dbDir, f"{filename}.db")

    connect(dbPath)

    createPostTable()

def createPostTable():
    sql = 'create table if not exists post (name varchar(255) primary key, context text)'
    c.execute(sql)
    conn.commit()

def connect(dbPath=dbPath):
    global conn, c
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

def disconnect():
    conn.close()

def getPost(name):
    sql = 'select context from post where name=(?)'
    c.execute(sql, [name])
    res = c.fetchone()
    return res

def appendPost(name, text):
    finder = 'select EXISTS (select * from post where name=(?)) as success'
    c.execute(finder, [name])
    exists = c.fetchone()
    if exists == 1:
        return False
    sql = 'insert into post values (?, ?)'
    c.execute(sql, [name, text])
    conn.commit()
    return True

def updatePost(name, text):
    finder = 'select EXISTS (select * from post where name=(?)) as success'
    c.execute(finder, [name])
    exists = c.fetchone()
    if exists == 0:
        return False
    sql = 'update post set context=(?) where name=(?)'
    c.execute(sql, [text, name])
    conn.commit()
    return True

def deletePost(name):
    c.execute('delete from post where name=(?)', [name])
    conn.commit()
    return True