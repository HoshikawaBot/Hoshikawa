import os
import sys
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
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

def dropPostTable():
    sql = 'drop table post if exists'
    c.execute(sql)
    conn.commit()

def createPostTable():
    sql = 'create table if not exists post (name varchar(255) primary key, writer_id varchar(255), context text)'
    c.execute(sql)
    conn.commit()

def connect(dbPath=dbPath):
    global conn, c
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

def disconnect():
    conn.close()

def getPostByName(name):
    sql = 'select * from post where name=(?)'
    c.execute(sql, [name])
    res = c.fetchone()
    return res

def getPostById(writer_id):
    sql = 'select * from post where writer_id=(?)'
    c.execute(sql, [writer_id])
    res = c.fetchall()
    return res

def appendPost(name, writer_id, text):
    if not isinstance(writer_id, str):
        raise TypeError("writer_id is not str but it must be.")
    finder = 'select EXISTS (select * from post where name=(?)) as success'
    c.execute(finder, [name])
    exists = c.fetchone()
    if exists == 1:
        return False
    sql = 'insert into post values (?, ?, ?)'
    c.execute(sql, [name, writer_id, text])
    conn.commit()
    return True

def updatePost(name, text):
    sql = 'update post set context=(?) where name=(?)'
    c.execute(sql, [text, name])
    conn.commit()
    return True

def deletePost(name):
    c.execute('delete from post where name=(?)', [name])
    conn.commit()
    return True