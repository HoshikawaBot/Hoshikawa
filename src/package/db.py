import os
import sqlite3
import package.fileHandler as fileHandler

rootDir = fileHandler.dir(__file__, 3)

dbDir = "{0}/{1}".format(rootDir, "db")
fileHandler.safeMkdir(dbDir)
dbPath = "{0}/{1}".format(dbDir, "db.db")

conn = sqlite3.connect(dbPath)
c = conn.cursor()