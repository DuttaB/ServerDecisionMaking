from __future__ import print_function
import json
import httplib

def lambda_handler(event, context):
    for record in event['Records']:
        temp = record['dynamodb']
        
        if record['eventName'] == 'MODIFY':
            if record['eventSourceARN'].find("sensors") >= 0:
                message = (parseSensor(temp['OldImage'], temp['NewImage'], record['eventName']))
                if message:
                    if message['type'] != "ok":
                        emergencyLogic(message)
            elif record['eventSourceARN'].find("users") >= 0:
                message = (parseUser(temp['OldImage'], temp['NewImage'], record['eventName']))
                if message:
                    processUserMessage(message)
                
        elif record['eventName'] == "INSERT":
            if record['eventSourceARN'].find("sensors") >= 0:
                message = (parseSensor(0, temp['NewImage'], record['eventName']))
            elif record['eventSourceARN'].find("users") >= 0:
                message = (parseUser(0, temp['NewImage'], record['eventName']))
            elif record['eventSourceARN'].find("robots") >= 0:
                message = parseRobot(temp['NewImage'])
                
            #newObjectLogic(message)
    
'''
This function parses a sensor object, and determines if something
has changed. If it has, it returns a dictionary contaning all 
pertinent information to be sent in a message to whoever requires it.
'''
def parseSensor(old,new,eventName):
    if eventName == "INSERT":
        #if it is a new sensor
        emergency = {
                        "from": "new sensor",
                        "id": new['id']['S'],
                        "buildingId": new['buildingId']['S'],
                        "model": new['model']['S'],
                        "type": new['type']['S']
                    }
        if "robotId" in new:
            emergency['robotId'] = new['robotId']['S']
        return emergency
    elif old['data']['S'] == new['data']['S']:
    #if it's the same nothing has changed
        return 0
    else:
    #if it has changed there must be a problem
        emergency = {
                        "type": new['data']['S'],
                        "buildingId": new['buildingId']['S'],
                        "room": new['room']['N'],
                        "from": "sensor",
                        "xpos": new['xpos']['N'],
                        "ypos": new['ypos']['N'],
                        "floor": new['floor']['N']
                    }
        if "robotId" in new:
            emergency['robotId'] = new['robotId']['S']
        return emergency

'''
This function parses a user object, and determines if something
has changed. If it has, it returns a dictionary contaning all 
pertinent information to be sent in a message to whoever requires it.
'''
def parseUser(old, new, eventName):
    if eventName == "INSERT":
        #if it is a new sensor
        emergency = {
                        "from": "new user",
                        "id": new['id']['S'],
                        "buildingId": new['buildingId']['S'],
                        "room": new['room']['N'],
                        "xpos": new['xpos']['N'],
                        "ypos": new['ypos']['N'],
                        "floor": new['floor']['N'],
                        "owner": new['owner']['BOOL']
                    }
        return emergency
    elif old['message']['S'] == new['message']['S']:
    #if it's the same nothing has changed
        return 0
    else:
    #if it has changed there must be a problem
        emergency = {
                        "type": new['message']['S'],
                        "building": new['buildingId']['S'],
                        "room": new['room']['N'],
                        "from": "user",
                        "xpos": new['xpos']['N'],
                        "ypos": new['ypos']['N'],
                        "floor": new['floor']['N'],
                        "owner": new['owner']['BOOL']
                    }
        return emergency
        
'''
This function parses a robot object, and determines if something
has changed. If it has, it returns a dictionary contaning all 
pertinent information to be sent in a message to whoever requires it.
'''
def parseRobot(new):
    emergency = {
                    "from": "new robot",
                    "id": new['id']['S'],
                    "buildingId": new['buildingId']['S'],
                    "room": new['room']['N'],
                    "xpos": new['xpos']['N'],
                    "ypos": new['ypos']['N'],
                    "floor": new['floor']['N'],
                    "movement": new['movement']['S'],
                    "capabilities": findItems(new['capabilities']['L'])
                }
    if "sensorId" in new:
        emergency['sensorId'] = findItems(new['sensorId']['L'])
    return emergency
 
'''
This finds all items in an array of dictionaries with 'S' as the key
'''
def findItems(arr):
    sensorIds = []
    for sen in arr:
        sensorIds.append(sen['S'])
    return sensorIds

'''
Generates a POST request to the push notification team that sends a message
to them for them to store
'''
def generatePOST(message):
    params = json.dumps(message) #necessary to format message in string format
    print(params)
    return
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
        }
    conn.request("POST", "/testing", params, headers)
    response = conn.getresponse()
    data = response.read()
    print(data.decode("utf-8"))

def newObjectLogic(json_object):
    add_object = {}
    if(json_object['from'] == 'new sensor'):
        add_object = {
                        "id":  [json_object['buildingId']],
                        "message": {
                                    'msg_type': json_object['from'],
                                    'body':{
                                        'buildingId':json_object['buildingId'],
                                        'new_id': json_object['id'],
                                        'model': json_object['model'],
                                        'type': json_object['type']
                                    }
                        }
                    }
        if "robotId" in json_object:
            add_object['message']['body']['robotId'] = json_object['robotId']

    elif(json_object['from'] == 'new robot'):
        add_object = {
                        'id':  [json_object['buildingId']],
                        'message': {
                                    'msg_type': json_object['from'],
                                    'body':{
                                        'buildingId':json_object['buildingId'],
                                        'new_id': json_object['id'],
                                        'sensorId': json_object['sensorId'],
                                        'capabilities': json_object['capabilities'],
                                        'movement': json_object['movement'],
                                        'xpos': json_object['xpos'],
                                        'ypos': json_object['ypos'],
                                        'room': json_object['room'],
                                        'floor': json_object['floor']
                                    }
                        }
                    }
    elif(json_object['from'] == 'new user'):
        add_object = {
                        "id":  [json_object['buildingId']],
                        "message": {
                            "msg_type": json_object['from'],
                            "body":{ "buildingId":json_object['buildingId'],
                            "new_id": json_object['id'],
                            "xpos": json_object['xpos'],
                            "ypos": json_object['ypos'],
                            "room": json_object['room'],
                            "floor": json_object['floor'],
                            "owner": json_object['owner']
                             }
                         }
                      }

    generatePOST(add_object)
