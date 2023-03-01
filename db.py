import sqlite3
conn=sqlite3.connect("user.db")
conn.execute("create table lecture")