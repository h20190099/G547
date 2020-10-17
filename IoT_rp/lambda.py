import boto3

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