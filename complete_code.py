import requests
import json
from datetime import datetime
import random
from array import *


global county
RFID = [1,2,3,4,5,6,7,8,9,10]
bus = [201,202,203,204,205,206]
new=[]

max_count=10
opt_count=5
county = 0
exe = 0

bus_number = random.choice(bus)

key ='lCjtPeawYr7eGGxB5g1qTclW9lCHaTfC'
url ='http://www.mapquestapi.com/geocoding/v1/address?key='
loc = 'Birla Institute of Technology and Science, Pilani – Goa Campus'
main_url= url + key +'&location=' + loc

r = requests.get(main_url)
data = r.json()['results'][0]
location =data['locations'][0]
lat = location['latLng']['lat']
lon = location['latLng']['lng']


now = datetime.now()
current_time = now.strftime("%H:%M:%S")

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
        
        
entry()
entry()
entry()
entry()
entry()
leave()
leave()




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
