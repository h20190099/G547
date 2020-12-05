# importing libraries
import boto3
from csv import reader
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
global n
global sec



#RFID = [1,2,3,4,5,6,7,8,9,10]             #registered valid RFID card numbers
bus = [201,202,203,204]                    #Bus numbers
#new=[]                                    #will contain valid RFID card holders present in the bus
route1 =[]
route2 =[]
route3 =[]
route4 =[]
route5 =[]
route6 =[]
route=[]
latitude=[]
longitude=[]
stops =[]

max_count=10                              #maximum bus capacity
opt_count=5                               #optimum bus capacity
#county = 0
#exe = 0



 
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
        with open('rp_add.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
        
            # Pass reader object to list() to get a list of lists
            list_of_rows = list(csv_reader)
            
            for element in list_of_rows[1]:
                if element != '':
                    route1.append(element)
            for element in list_of_rows[2]:
                if element != '':
                    route2.append(element)
            for element in list_of_rows[3]:
                if element != '':
                    route3.append(element)
            for element in list_of_rows[4]:
                if element != '':
                    route4.append(element)
            for element in list_of_rows[5]:
                if element != '':
                    route5.append(element)
            for element in list_of_rows[6]:
                if element != '':
                    route6.append(element)        





                    
            print (route1)
            print(len(route1)-1)
            print (route2)
            print(len(route2)-1)
            print (route3)
            print(len(route3)-1)
            print (route4)
            print(len(route4)-1)
            print (route5)
            print(len(route5)-1)
            print (route6)
            print(len(route6)-1)
            route.append(route1[0])
            route.append(route2[0])
            route.append(route3[0])
            route.append(route4[0])
            route.append(route5[0])
            route.append(route6[0])
            print (route)
            stops.append(len(route1)-1)
            stops.append(len(route2)-1)
            stops.append(len(route3)-1)
            stops.append(len(route4)-1)
            stops.append(len(route5)-1)
            stops.append(len(route6)-1)
            print (stops)
            
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

        latitude.append(lat1)
        latitude.append(lat2)
        latitude.append(lat3)
        latitude.append(lat4)
        latitude.append(lat5)
        latitude.append(lat6)
        latitude.append(lat7)
        latitude.append(lat8)
        print (latitude)

        longitude.append(lon1)
        longitude.append(lon2)
        longitude.append(lon3)
        longitude.append(lon4)
        longitude.append(lon5)
        longitude.append(lon6)
        longitude.append(lon7)
        longitude.append(lon8)
        print (longitude)


        # define the countdown func. 
        def countdown(t,n,sec):
            
            print('Bus registration number', str(sys.argv[1]))
            
            route_max = len(route)
            Total_pass = 0
            
            print('Maximum routes for scheduled journey :', route_max)
            for i in range(1, n+1):
                
                if i != n:
                    pas_count = random.randint(1,10)
                else:
                    pas_count = 0 

                Total_pass = Total_pass + pas_count
                lat=latitude[i-1]
                lon=longitude[i-1]
                    
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")

                if i == 1:
                    start_count = current_time
                    end_count = start_count
                   
                elif i>1 :
                    end_count = current_time
                    
                     
                
                print('At Bustop :',i)
                print('latitude :',lat)
                print('longitude :',lon)
                print('Number of passenger:',pas_count)
                print('Total passenger count :',Total_pass)
                print("current_time =", current_time)
                
                while t:
                    count=0
                    mins, secs = divmod(t, 60)
                    timer = '{:02d}:{:02d}'.format(mins, secs)
                    print(timer, end="\r")
                    time.sleep(1)
                    t -= 1
                    
                FMT = '%H:%M:%S'    
                diff=datetime.strptime(end_count, FMT) - datetime.strptime(start_count, FMT)
                sec = diff.total_seconds()
               
                print('\nRoute time :',sec)
                
                
                if pas_count > opt_count and pas_count < max_count:
                    print(" Bus is over loaded")
                elif pas_count < opt_count and  pas_count >0 :
                    print("Bus is under loaded")
                elif pas_count == opt_count:
                    print("Bus is balancely loaded")
                elif pas_count == 0:
                    print('\nBus ready for rescheduling!!')
                    
                
                    
                message1 = '{"current_time":'+'"'+str(current_time)+'","Total stops in scheduled route:":'+'"'+str(n)+'","Bus registration number":'+'"'+str(sys.argv[1])+'","route_max":'+'"'+str(route_max)+'","Bus stop":'+'"'+str(i)+'","Route average time":'+'"'+str(sec)+'","Route number":'+'"'+str(sys.argv[2])+'","latitude":'+'"'+str(lat)+'","longitude":'+'"'+str(lon)+'","Total passenger count ":'+'"'+str(Total_pass)+'",'+'"Number of passenger":'+str(pas_count)+'}'
                mqttc.publish("commontestTopic", message1, 1)

                t=random.randint(10,25)
                print('\n\n')
                        
    
 
        # function call
       
        length = len(route)
        for j in range( 0,length):
            if str(sys.argv[2])== str(route[j]):
                print('\n\nRoute scheduled:',j+1)
                print('Total stops in scheduled route:',stops[j])
                countdown(int(10),stops[j],0)
               
        if str(sys.argv[2])> str(length):
            print('\nRoute does not exist!!')    
        break;  
       
        ##########################################################

        
    else:
        print("waiting for connection...")                   
