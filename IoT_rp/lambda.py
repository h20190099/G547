import boto3
import array

sorted_a = array.array('f', [0.0,0.0,0.0,0.0,0.0,0.0])



def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    

    
    response = client.put_item(
            TableName = 'RouteTable',
            Item={
                'current_time': {'S' :event['current_time']},
                'Route number': {'S' :event['Route number']},
                'Bus registration number ': {'S' :event['Bus registration number']}
                
            }
        )
    
    
    
    
    bus = event['Bus registration number']
    total = event['Total stops in scheduled route:']
    bus_stop = event['Bus stop']
    total_pass = event['Total passenger count ']
    avg_time = event['Route average time']
    route_no =int( event['Route number'])
    
    if total == bus_stop:
        passen = float(total_pass)
        time = float(avg_time)
        sorted_a[route_no-1] = (0.6*passen) + (0.4*time)
    print(sorted_a)
    print(route_no)
    after_sort=sorted(sorted_a)
    print("sort_arr :",after_sort)
    weight_max = after_sort[5]
    
    exists = 0.0 in sorted_a
    
    if exists:
        print("Route on which bus to be scheduled :",sorted_a.index(0.0)+1)
        
    else:
        print("Route with max. weight: ",weight_max)
        print("Route on which bus to be scheduled :",sorted_a.index(weight_max)+1)
     
    
    if bus == '201':
        
        response = client.put_item(
            TableName = 'Bus201',
            Item={
                'current_time': {'S' :event['current_time']},
                'Bus registration number ': {'S' :event['Bus registration number']},
                'latitude': {'S' :event['latitude']},
                'longitude': {'S' :event['longitude']},
                'Number of passenger': {'N' :str(event['Number of passenger'])}
                
            }
        )
        
        
    elif bus == '202':
        response = client.put_item(
            TableName = 'Bus202',
            Item={
                'current_time': {'S' :event['current_time']},
                'Bus registration number ': {'S' :event['Bus registration number']},
                'latitude': {'S' :event['latitude']},
                'longitude': {'S' :event['longitude']},
                'Number of passenger': {'N' :str(event['Number of passenger'])}
                
            }
        )
        
        
    elif bus == '203':
        response = client.put_item(
            TableName = 'Bus203',
            Item={
                'current_time': {'S' :event['current_time']},
                'Bus registration number ': {'S' :event['Bus registration number']},
                'latitude': {'S' :event['latitude']},
                'longitude': {'S' :event['longitude']},
                'Number of passenger': {'N' :str(event['Number of passenger'])}
                
            }
        )    
        
    else:
        response = client.put_item(
            TableName = 'Bus204',
            Item={
                'current_time': {'S' :event['current_time']},
                'Bus registration number ': {'S' :event['Bus registration number']},
                'latitude': {'S' :event['latitude']},
                'longitude': {'S' :event['longitude']},
                'Number of passenger': {'N' :str(event['Number of passenger'])}
                
            }
        )
        
        
   
    return 0
