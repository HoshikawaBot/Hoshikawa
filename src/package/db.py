import os
import sqlite3
import fileHandler

rootDir = fileHandler.dir(__file__, 2)

dbDir = "{0}/{1}".format(rootDir, "db")
fileHandler.safeMkdir(dbDir)
dbPath = "{0}/{1}".format(dbDir, "db.db")

conn = sqlite3.connect(dbPath)
c = conn.cursor()

sql = 'create table if not exists gall_id (id varchar(255))'
c.execute(sql)

sql = 'create table if not exists post (id int, gall_id varchar(255), author varchar(255))'
c.execute(sql)

def getGallIdList():
    sql = 'select id from gall_id'
    c.execute(sql)
    return c.fetchall()

def appendGallIdList(id):
    c.execute('insert into gall_id values (?)', id)

def getPostByAuthorAndGallID(author, gallId):
    sql = 'select id from post where author=(?) and gall_id=(?)'
    c.execute(sql, author, gallId)
    return c.fetchall()