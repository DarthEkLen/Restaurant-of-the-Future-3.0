import paho.mqtt.client as mqtt #import the client1
import time
import json
import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="*Password*",
database="*DataBase Name*"
)
##############################################
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    y=message.payload.decode("utf-8")
    f=json.loads(y)
    a=f["name"]
    b=f["category"]
    c1=f["time stamp"]
    c=(c1[11:13]+ c1[14:16]+ c1[17:19])
    d=(f["table"])
    
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    mycursor = mydb.cursor()
    sql = "INSERT INTO mars_iot_not_received (name, category, order_time, table_no) VALUES (%s, %s, %s,%s)"
    val = (a, b, c, d)
    mycursor.execute(sql, val)
    mydb.commit()
    print(a) 
    print(b)
    print(c)
    print(d)
##############################################
# broker_address="local host"
# test.mosquitto.org
# broker.hivemq.com
# iot.eclipse.org
##############################################

broker_address="localhost"
print("creating new instance")
client = mqtt.Client("P2") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

print("Subscribing to topic","IOT/CK")
client.subscribe("IOT/CK")
time.sleep(5)
client.loop_forever() #start the loop
