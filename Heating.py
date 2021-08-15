import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json
import ast
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")
		global Connected  # Use global variable
		Connected = True  # Signal connection
	else:
		print("Connection failed Return Code : ",rc)


def on_message(client, userdata, message):
	#write the mechanism for AC, ventilation and heating
	temp = [int(k) for k in message.payload.split() if k.isdigit()]
	heating_temp = temp[1]
	print("Received temp: " + str(heating_temp))
	

#Connected = False  # global variable for the state of the connection
client_name = "Heating" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
#curr=location_generator()
user = "admin"
password = "hivemq"


client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.connect(host=broker_address, port=broker_port)
client.subscribe('location/Controller') #subscribe to the controller
print(client_name)

client.loop_start()
time.sleep(5)

#assuming every request will come after 10sec from the previous transaction
end_time=time.time()+(300 )
while time.time() < end_time:
    time.sleep(2)   

print("exiting")	
