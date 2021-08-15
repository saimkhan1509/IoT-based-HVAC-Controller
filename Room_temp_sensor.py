import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json


def on_connect(client, userdata, flags, rc):
    if rc == 0:
    	print("Connected to broker")
    	global Connected  # Use global variable
    	Connected = True  # Signal connection
    else:
    	print("Connection failed Return Code : ",rc)



def on_message(client, userdata, message):
	pass
    

#Connected = False  # global variable for the state of the connection
client_name="Room_temp_sensor" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
user = "admin"
password = "hivemq"   

client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.connect(host=broker_address, port=broker_port)

print(client_name)
     	
client.loop_start()

#randomly generate a temperature andpass it to the controller
end_time=time.time()+(300 )
while time.time() < end_time:
    #randomly generating temperature between 15 and 35 and sending to the controller
	rand_temp = random.randrange(15,35)
	client.publish('location/' + client_name, str(rand_temp))
    #sending room temperaature every 30 second
	time.sleep(30)
print("exiting")
time.sleep(10)
