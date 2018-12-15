import serial 
import subprocess    
import pymongo
import datetime
import http_publish


## Database Information ##
client = pymongo.MongoClient("mongodb://localhost:27017/")
temp_db = client["tempdatabase"]     #tempdatabase the name of our database
posts = temp_db.posts 			#Collection(similar to table) name


print("The aim of this software is to record temperature in a room, format & store it in a local database and finally publish it locally and remotely\n The code is released under GPLv3")

raw_input("Press ENTER to continue")
 
arduinoSerialData = serial.Serial('/dev/ttyUSB0',9600)
while True:	 
	if(arduinoSerialData.inWaiting()>0):
		sensortemp = arduinoSerialData.readline()
		sensortemp = int(sensortemp)
		post_data = {
			'date': datetime.datetime.now(),
			'temperature': sensortemp

		}
		result = posts.insert_one(post_data)		  #Inserts data into dbase
		print sensortemp    				#Print values read from the serial output 
		
		f = open("temperature.txt", "a+")	# Open file for writing and append to it	
		shell_input = subprocess.Popen("date", stdout=subprocess.PIPE)	# Using shell command 'date' to get current local time
		shell_input = shell_input.stdout.read()
		f.write("%s = " %shell_input)
		f.write("%d degrees\n" %sensortemp)

		http_publish.local_publish_http()	
