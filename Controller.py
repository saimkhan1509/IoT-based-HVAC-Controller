import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json
import ast

#default values for ac,ventilation,heating,ambient temperature
ambient_temprature = 21
ac = 21
heating = 4
ventilation = 2

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")
		global Connected  # Use global variable
		Connected = True  # Signal connection
	else:
		print("Connection failed Return Code : ",rc)


def on_message(client, userdata, message):
	#write the mechanism for AC, ventilation and heating
	global to_be_sent
	global heating
	global ac
	global ventilation
	global received_temp
	global ambient_temprature
	received_temp = int(message.payload)
	print("Received temp: " + str(received_temp) )
	
	#computing the difference between the current ambient temperature and received room temperature
	diff = abs(received_temp - ambient_temprature)

	#if the received temperature is equal to the ambient temperature, then do nothing
	if received_temp == ambient_temprature:
		pass

	#Handling the case when reveived temp from the sensor is less than ambient temperature
	elif received_temp < ambient_temprature:
		ac = ac +  (int)(math.ceil(diff/8))
		heating = heating + (int)(math.ceil(diff/10))
		#loops for controlling the overflow of range
		if(heating >10):
			heating = 9
		if(ventilation > 10):
			ventilation = 9
		if ac > 24:
			ac = 24
		if diff > 5:
			ventilation = 3
		else:
			ventilation = 2

	#Handling the case when reveived temp from the sensor is greater than ambient temperature
	elif received_temp > ambient_temprature:
		ac = ac - (int)(math.ceil(diff/8))
		heating = heating - (int)(math.ceil(diff/10))
		#loops for controlling the overflow of range
		if(heating < 0):
			heating = 1
		if diff > 5:
			ventilation = 1
		if ac < 16:
			ac = 17
		else:
			ventilation = 2

	#to_be_sent : message containing ac, heating, ventilation, and received temperature
	to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp)
	print(to_be_sent)

#function for taking the value of ambient temperature, if user want to change the ambient temperature
def temperature_to_set(client, userdata, message):
	global ambient_temprature
	ambient_temprature = int(message.payload)
	global to_be_sent
	global heating
	global ac
	global ventilation
	global received_temp
	#global ambient_temprature
	
	print("Received temp: " + str(received_temp) )
	
	#computing the difference between the current ambient temperature and received room temperature
	diff = abs(received_temp - ambient_temprature)

	#if the received temperature is equal to the ambient temperature, then do nothing
	if received_temp == ambient_temprature:
		pass

	#Handling the case when reveived temp from the sensor is less than ambient temperature
	elif received_temp < ambient_temprature:
		ac = ac +  (int)(math.ceil(diff/8))
		heating = heating + (int)(math.ceil(diff/10))
		#loops for controlling the overflow of range
		if(heating >10):
			heating = 9
		if(ventilation > 10):
			ventilation = 9
		if ac < 16:
			ac = 17
		if diff > 5:
			ventilation = 3
		else:
			ventilation = 2

	#Handling the case when reveived temp from the sensor is greater than ambient temperature
	elif received_temp > ambient_temprature:
		ac = ac - (int)(math.ceil(diff/8))
		#loops for controlling the overflow of range
		heating = heating - (int)(math.ceil(diff/10))
		if(heating < 0):
			heating = 1
		if diff > 5:
			ventilation = 1
		if ac > 24:
			ac = 24
		else:
			ventilation = 2

	#to_be_sent : message containing ac, heating, ventilation, and received temperature
	to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp)
	print(to_be_sent)
	
#Connected = False  # global variable for the state of the connection
client_name = "Controller" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
#curr=location_generator()
user = "admin"
password = "hivemq"


client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.message_callback_add('location/user-display',temperature_to_set)
client.connect(host=broker_address, port=broker_port)
client.subscribe('location/Room_temp_sensor') #channel for receiving the temperature from temperature sensor
client.subscribe('location/user-display') #channel for receiving temperature from the user
print(client_name)

client.loop_start()
time.sleep(2)

#output.txt will contain all the changes gone  through the execution of the code
f =  open("output.txt", "w") #output.txt will save the log files

#assuming every request will come after 10sec from the previous transaction
end_time=time.time()+(300 )
while time.time() < end_time:
    client.publish('location/' + client_name, to_be_sent)
    f.write("Received_temp: " + str(received_temp) + "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation) + "\n")
    time.sleep(2)   

f.close()
print("exiting")
time.sleep(10)
