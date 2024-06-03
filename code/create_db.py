import sqlite3

con = sqlite3.connect("User.db")
print("Database opened successfully")

con.execute("create table loginInformation(userId INTEGER PRIMARY KEY AUTOINCREMENT, firstName VARCHAR(225) NOT NULL, lastName VARCHAR(225) NOT NULL, email VARCHAR(225) UNIQUE NOT NULL, gender VARCHAR(225) NOT NULL,password VARCHAR(225)  NOT NULL)")

print("Table Create successfully")
con.close()