# importing libraries
import paho.mqtt.client as paho
import ssl
from time import sleep
import requests
import json
from datetime import datetime
import random
from array import *


global county
RFID = [1,2,3,4,5,6,7,8,9,10]             #registered valid RFID card numbers
bus = [201,202,203,204,205,206]           #Bus numbers
new=[]                                    #will contain valid RFID card holders present in the bus

max_count=10                              #maximum bus capacity
opt_count=5                               #optimum bus capacity
county = 0
exe = 0

bus_number = random.choice(bus)

 
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    #if connection is successful, rc value will be 0
    print("Connection returned result: " + str(rc) )
    #print(flags)
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()    
#create an mqtt client object
#attach call back function
mqttc.on_connect = on_connect
#attach on_connect function written in the
#mqtt class, (which will be invoked whenever
#mqtt client gets connected with the broker)
#is attached with the on_connect function
#written by you.


mqttc.on_message = on_message                               # assign on_message func
#attach on_message function written inside
#mqtt class (which will be invoked whenever
#mqtt client gets a message) with the on_message
#function written by you






#### Change following parameters #### 
awshost = "ajq7vdimckork-ats.iot.us-east-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "myLaptop"                                     # Thing_Name
thingName = "myLaptop"                                    # Thing_Name
caPath = "AmazonRootCA1san.pem.crt" #Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
certPath = "bf5debdd98-certificate.pem.crt"   # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
keyPath = "bf5debdd98-private.pem.key"        # <Thing_Name>.private.key Thing's private key from Amazon
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
while 1:
    sleep(5)
    if connflag == True:
        key ='lCjtPeawYr7eGGxB5g1qTclW9lCHaTfC'
        url ='http://www.mapquestapi.com/geocoding/v1/address?key='
        loc = 'Birla Institute of Technology and Science, Pilani – Goa Campus'
        main_url= url + key +'&location=' + loc

        r = requests.get(main_url)
        data = r.json()['results'][0]
        location =data['locations'][0]
        lat = location['latLng']['lat']                       #latitude and longitude for given input address
        lon = location['latLng']['lng']


        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")               #timestamp

        def entry():
             global county 
             pas_id = random.randint(1,13)
    
             if pas_id in RFID:
                 RFID.remove(pas_id)
        #print('entered id:',pas_id)
        #print(RFID)
                 county +=1
                 new.append(pas_id)
        #print(new)
        #print(county)

    #else:
        #print('entered id:',pas_id)
        
    

        def leave():
            global exe
            exit_id= random.choice(new)
            RFID.append(exit_id)
            new.remove(exit_id)

    #print(RFID)
    #print(new)
            exe +=1
    #print(exe)
        
        
        entry()                                             #representation for people entering and exiting bus using RFID cards
        entry()
        entry()
        entry()
        entry()
        leave()
        leave()

        message1 = '{"Number of passenger":'+str(county-exe)+'}'
        mqttc.publish("countTopic", message1, 1)                            # Publishing Number of passenger values
        message2 = '{"Bus Number":'+str(bus_number)+'}'
        mqttc.publish("busTopic", message2, 1)                              # Publishing Bus Number values
        message3 = '{"current_time":"'+str(current_time)+'"}'
        mqttc.publish("timeTopic", message3, 1)                             # Publishing timestamp
        message4 = '{"latitude":'+str(lat)+'}'
        mqttc.publish("latitudeTopic", message4, 1)                         # Publishing latitude values
        message5 = '{"longitude":'+str(lon)+'}'
        mqttc.publish("longitudeTopic", message5, 1)                        # Publishing longitude values
        message6 = '{"Current Time":'+'"'+str(current_time)+'",'+'"Number of passenger":'+str(county-exe)+'}'
        mqttc.publish("commontestTopic", message6, 1)
        #message6 = '{"Current Time":'+'"'+str(current_time)+'",'+'"Number of passenger":'+str(county-exe)+'}'
        #mqttc.publish("commonTopic", message6, 1)
        # topic: temperature # Publishing Temperature values

        print('Number of passenger:',county-exe)
        print('Bus Number ' + str(bus_number) +' arrived')
        if county > opt_count and county < max_count:
            print("over loading")
        elif county < opt_count:
            print("under loading")
        else:
            print("balance loading")

        print("Current Time =", current_time)
        print('latitude :',lat)
        print('longitude :',lon) 


         # Print sent temperature msg on console
    else:
        print("waiting for connection...")                   
