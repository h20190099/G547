# importing libraries
import boto3
import sys
import paho.mqtt.client as paho
import ssl
from time import sleep
import requests
import json
from datetime import datetime
import random
from array import *
import time 
global check


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
 

 
mqttc = paho.Client()    
mqttc.on_connect = on_connect
mqttc.on_message = on_message                               # assign on_message func
        

#### Change following parameters #### 
awshost = "ajq7vdimckork-ats.iot.us-east-1.amazonaws.com"        # Endpoint
awsport = 8883                                                   # Port no.   
clientId = "myLaptop"                                            # Thing_Name
thingName = "myLaptop"                                           # Thing_Name
caPath = "AmazonRootCA1san.pem.crt"                              #Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
certPath = "bf5debdd98-certificate.pem.crt"                      # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
keyPath = "bf5debdd98-private.pem.key"                           # <Thing_Name>.private.key Thing's private key from Amazon
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
while 1:
    sleep(5)
    if connflag == True:
        
        key ='lCjtPeawYr7eGGxB5g1qTclW9lCHaTfC'
        url ='http://www.mapquestapi.com/geocoding/v1/address?key='
        loc1 = 'Navy Nagar Colaba'
        loc2 = 'Afghan Church'
        loc3 = 'Sasoon Dock'
        loc4 = 'Colaba Depot'
        loc5 = 'Mantralaya'
        loc6 = 'Dhobi Ghat Colaba'
        loc7 = 'Strand Cinema'
        loc8 = 'Hutatma Chowk'
        
        main_url_1= url + key +'&location=' + loc1
        main_url_2= url + key +'&location=' + loc2
        main_url_3= url + key +'&location=' + loc3
        main_url_4= url + key +'&location=' + loc4
        main_url_5= url + key +'&location=' + loc5
        main_url_6= url + key +'&location=' + loc6
        main_url_7= url + key +'&location=' + loc7
        main_url_8= url + key +'&location=' + loc8

        r1 = requests.get(main_url_1)
        data = r1.json()['results'][0]
        location1 =data['locations'][0]
        lat1 = location1['latLng']['lat']
        lon1 = location1['latLng']['lng']

        r2 = requests.get(main_url_2)
        data2 = r2.json()['results'][0]
        location2 =data2['locations'][0]
        lat2 = location2['latLng']['lat']
        lon2 = location2['latLng']['lng']

        r3 = requests.get(main_url_3)
        data3 = r3.json()['results'][0]
        location3 =data3['locations'][0]
        lat3 = location3['latLng']['lat']
        lon3 = location3['latLng']['lng']

        r4 = requests.get(main_url_4)
        data4 = r4.json()['results'][0]
        location4 =data4['locations'][0]
        lat4 = location4['latLng']['lat']
        lon4 = location4['latLng']['lng']


        r5 = requests.get(main_url_5)
        data5 = r5.json()['results'][0]
        location5 =data5['locations'][0]
        lat5 = location5['latLng']['lat']
        lon5 = location5['latLng']['lng']


        r6 = requests.get(main_url_6)
        data6 = r6.json()['results'][0]
        location6 =data6['locations'][0]
        lat6 = location6['latLng']['lat']
        lon6 = location6['latLng']['lng']


        r7 = requests.get(main_url_7)
        data7 = r7.json()['results'][0]
        location7 =data7['locations'][0]
        lat7 = location7['latLng']['lat']
        lon7 = location7['latLng']['lng']

        r8 = requests.get(main_url_8)
        data8 = r8.json()['results'][0]
        location8 =data8['locations'][0]
        lat8 = location8['latLng']['lat']
        lon8 = location8['latLng']['lng']


        # define the countdown func. 
        def countdown(t):
            
            print('Bus registration number', str(sys.argv[1]))
            print('latitude :',lat)
            print('longitude :',lon)
            print('Number of passenger:',county-exe)
            
            if county-exe > opt_count and county-exe < max_count:
                print(" Bus is over loaded")
            elif county-exe < opt_count:
                print("Bus is under loaded")
            elif county-exe == opt_count:
                print("Bus is balancely loaded")
                
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("current_time =", current_time)
            
            
            message1 = '{"current_time":'+'"'+str(current_time)+'","Bus registration number":'+'"'+str(sys.argv[1])+'","Route number":'+'"'+str(sys.argv[2])+'","latitude":'+'"'+str(lat)+'","longitude":'+'"'+str(lon)+'",'+'"Number of passenger":'+str(county-exe)+'}'
            mqttc.publish("commontestTopic", message1, 1)
            
            while t:
                count=0
                mins, secs = divmod(t, 60) 
                timer = '{:02d}:{:02d}'.format(mins, secs) 
               # print(timer, end="\r") 
                time.sleep(1) 
                t -= 1
                



        def entry():
            global county 
            pas_id = random.randint(1,13)
            
            if pas_id in RFID:
                RFID.remove(pas_id)
                print('entered id:',pas_id)
                print('Yet to entered :',RFID)
                county +=1
                new.append(pas_id)

                print('Inside the bus:',new)
                print('\n')

            
                
        def leave():
            global exe
            exit_id= random.choice(new)
            RFID.append(exit_id)
            new.remove(exit_id)

            print('Yet to entered :',RFID)
            print('Inside the bus:',new)
            exe +=1
            print('\n')
                
        # function call
        print('Route scheduled:', str(sys.argv[2]))
        print('At Bustop 1!!')

                
        entry()
        entry()
        entry()
        entry()
        entry()
        entry()
        entry()
        leave()
        leave()


        lat=lat1
        lon=lon1
            
        countdown(int(10))
      
        ###########################################
        print('\nAt Bustop 2!!')
        
        entry()
        entry()
        entry()
        entry()
        leave()
        leave()



        if str(sys.argv[2])=='1':
            lat=lat2
            lon=lon2
        elif str(sys.argv[2])=='2':
            lat=lat3
            lon=lon3
        else:
            lat=lat4
            lon=lon4
           
        countdown(int(25))
        
        ###############################################
        print('\nAt Bustop 3!!')

        
        entry()
        entry()
        leave()


        if str(sys.argv[2])=='1':
            lat=lat5
            lon=lon5
        elif str(sys.argv[2])=='2':
            lat=lat6
            lon=lon6
        else:
            lat=lat7
            lon=lon7
            
        countdown(int(15))
        
    
        ######################################################
        print('\nAt Bustop 4!!')

        while len(new) > 0:
            leave()
            #print('empty')
            
           

        lat=lat8
        lon=lon8
        
        countdown(int(1))
        
        print('\nBus ready for rescheduling!!')
        ##########################################################

         # Print sent temperature msg on console
    else:
        print("waiting for connection...")                   
