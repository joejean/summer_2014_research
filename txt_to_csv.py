import csv
import json

mallsdatafile = open("mallsdata.txt", "r")

mallsdatacsv = open("mallsdata.csv","wb") 
writer = csv.writer(mallsdatacsv, dialect='excel')
# writer = csv.DictWriter(mallsdatacsv, ["mall_name","mall_state", "mall_address", "mall_phone", "mall_latitude", "mall_longitude",\
# 	"mall_number_of_stores", "mall_stores_list"], extrasaction = "ignore", dialect="excel")

malls_data = json.load(mallsdatafile)

#Header Row
writer.writerow(["Mall Name"]+["Mall State"]+ ["Mall Address"]+["Mall Phone"]+ ["Mall Latitude"]+ ["Mall Longitude"]+\
	["Mall Number of Stores"]+ ["Mall Stores List"]) 

for dicti in malls_data:
	print dicti
	writer.writerow([dicti['mall_name']]+[dicti['mall_state']]+[dicti['mall_address']]+[dicti['mall_phone']]+[dicti['mall_latitude']]+\
		[dicti['mall_longitude']]+[dicti['mall_number_of_stores']]+[" | ".join(dicti["mall_stores_list"]).encode('utf-8', 'ignore')])
	

mallsdatafile.close()
mallsdatacsv.close()