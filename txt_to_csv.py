import csv

mallsdatafile = open("mallsdata.txt", "r")

mallsdatacsv = open("mallsdata.csv","wb") 
writer = csv.DictWriter(mallsdatacsv, ("mall_name","mall_state", "mall_address", "mall_phone", "mall_latitude", "mall_longitude", "mall_latitude", "mall_longitude",\
	"mall_number_of_stores", "mall_stores_list"), extrasaction = "ignore", dialect="excel")

for dicti in mallsdatafile:
	print dicti
	#for key, val in dict:
	#writer.writerows(str(dicti))
	break

mallsdatafile.close()
mallsdatacsv.close()