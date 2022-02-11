"""
    dialogflow        0.5.1
    google-api-core   1.4.1
"""
import os
from random import randint
import dialogflow
from google.api_core.exceptions import InvalidArgument
import json
import datetime
from json import JSONEncoder

#for IOT
import paho.mqtt.client as mqtt          #import the client1
import time
import json

i=2

while i>1:
    credential_path = "*Private JSON KEY*"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    DIALOGFLOW_PROJECT_ID = '*Your Project ID*'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'me'


    text_to_be_analyzed = input ("\nEnter name :")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise


    if response.query_result.fulfillment_text == "recorded":

        #################################
        ###Creating Category for names###
        #################################

        o = text_to_be_analyzed

        if o =='chirag' or o=='apurba' or o=='abhay' or o=='yash' :
            cat='2y'
        elif o=='anfal' or o== 'vansh' :
            cat='3y'
        elif o=='shubham' or o=='sanjeev':
            cat='4y'
        
        table_value = str(randint(1,9))
        names_input = {
            "name": text_to_be_analyzed,
            "time stamp": datetime.datetime.now(),
            "category": cat,
            "table": table_value
        }
        #print(cat)


        ########################
        ##subclass JSONEncoder##
        ########################

        class DateTimeEncoder(JSONEncoder):
                #Override the default method
                def default(self, obj):
                    if isinstance(obj, (datetime.date, datetime.datetime)):
                        return obj.isoformat()

        # print("Printing to check how it will look like")
        # print(DateTimeEncoder().encode(names_input))

        # print("Encode DateTime Object into JSON using custom JSONEncoder")
        print("\nOrder: ")
        employeeJSONData = json.dumps(names_input, indent=4, cls=DateTimeEncoder)
        print(employeeJSONData)

        ##########################
        ####Internet of Things####
        ##########################


        #broker_address="local host"
        broker_address="localhost"
        # print("creating new instance")
        client = mqtt.Client("P1") #create new instance
        # client.on_message=on_message #attach function to callback
        # print("connecting to broker")
        client.connect(broker_address,1883) #connect to broker
        client.loop_start() #start the loop


        t=1
        while(t<2):
            # print("Publishing message to topic","IOT/CK")
            client.publish("IOT/CK",employeeJSONData)
            time.sleep(5)
            t=t+1 # wait
        print(" Order send to Chef. Happy Mealing :)\n")
    else:
        print(" Outside Project, Won't take order!!\n")


    # client.loop_stop() #stop the loop

    #################################################################################################################
    # CAN BE USED LATER CODE    

    # print("Query text:", response.query_result.query_text)
    # print("Detected intent:", response.query_result.intent.display_name)
    # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    # print("Fulfillment text:", response.query_result.fulfillment_text)
    i= 1+1
    print(" Next Order??")