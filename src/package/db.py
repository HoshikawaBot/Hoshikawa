import os
import sqlite3
import package.fileHandler as fileHandler

rootDir = fileHandler.dir(__file__, 2)

dbDir = "{0}/{1}".format(rootDir, "db")
fileHandler.safeMkdir(dbDir)
dbPath = "{0}/{1}".format(dbDir, "db.db")

conn = sqlite3.connect(dbPath)
c = conn.cursor()

sql = 'create table if not exists gall_id (id varchar(255))'
c.execute(sql)
conn.commit()

sql = 'create table if not exists post (id int, gall_id varchar(255), author varchar(255))'
c.execute(sql)
conn.commit()

sql = 'create table if not exists name (name varchar(255) not null primary key)'
c.execute(sql)
conn.commit()

def getGallIdList():
    sql = 'select id from gall_id'
    c.execute(sql)
    return [e[0] for e in c.fetchall()]

def appendGallIdList(id):
    c.execute('insert into gall_id values (?)', [id])
    conn.commit()

def getPostByAuthorAndGallId(author, gallId):
    sql = 'select id from post where author=(?) and gall_id=(?)'
    c.execute(sql, [author, gallId])
    return [e[0] for e in c.fetchall()]

def appendPost(author, gallId, postId):
    c.execute('insert into post values (?, ?, ?)', [postId, gallId, author])
    conn.commit()

def appendNameIfNotExists(name):
    c.execute('insert or ignore into name values (?)', [name])
    conn.commit()

def getNames():
    sql = 'select name from name'
    c.execute(sql)
    return [e[0] for e in c.fetchall()]