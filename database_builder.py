import sqlite3
import json

conn = sqlite3.connect("us_malls.db")

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS state (stateid integer primary key autoincrement, name text)")

cursor.execute("CREATE TABLE IF NOT EXISTS mall (mallid integer primary key autoincrement, name text, address text, phone text, latitude real, longitude real,\
 state integer, foreign key(state) references state(stateid) )")

cursor.execute("CREATE TABLE IF NOT EXISTS store (storeid integer primary key autoincrement, name text, mall integer, foreign key(mall) references mall(mallid) )")

conn.commit()

mallsdatafile = open("mallsdata.txt", "rb")

data = json.load(mallsdatafile)

#Populate the state table
for dicti in data:
	cursor.execute("INSERT INTO state(name) VALUES(?)", (dicti["mall_state"],))

conn.commit()
#Populate the mall table
for dicti in data:
	cursor.execute("SELECT stateid FROM state where name=?",(dicti["mall_state"],))
	stateid= cursor.fetchone()
	cursor.execute("INSERT INTO mall(name, address, phone, latitude, longitude, state) VALUES(?,?,?,?,?,?)", (dicti["mall_name"], dicti["mall_address"],\
	 dicti["mall_phone"], dicti["mall_latitude"], dicti["mall_longitude"], stateid[0]))

#populate the store table
for dicti in data:
	cursor.execute("SELECT mallid FROM mall where name=?",(dicti["mall_name"],))
	mallid = cursor.fetchone()
	storeslist = dicti["mall_stores_list"]
	for store in storeslist:
		cursor.execute("INSERT INTO store(name, mall) VALUES(?,?)", (store,mallid[0]))


mallsdatafile.close()
conn.commit()
conn.close()

