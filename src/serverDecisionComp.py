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
                
            newObjectLogic(message)
    
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
	
'''
This function is currently blank because what kinds of messages users could send
was not specified. This is a placeholder so the logic can be added later.
'''
def processUserMessage(json_object):
	print("User message logic goes here")
	
'''
This function is called when a sensor determines an emergency has occurred. This
determines what robot(s) to send to handle the emergency as well as sends a 
message to all affected users about the emergency.
'''
def emergencyLogic(json_object):
	
	# Severity Levels
	FIRE = 5
	WATER_LEAK = 2
	INTRUDER = 3
	GAS_LEAK = 4

	# Message Formats				
	user_message = {
						'id':  [],
						'message': {
									'msg_type': 'notification',
									'body':{
										'buildingId':json_object['buildingId'],
										'xpos': json_object['xpos'],
										'ypos': json_object['ypos'],
										'room': json_object['room'],
										'floor': json_object['floor'],
										'message': ''
									}
						}
					}
	robot_command = {
						'id':  [],
						'message': {
									'msg_type': json_object['type'],
									'body':{
										'buildingId':json_object['buildingId'],
										'xpos': json_object['xpos'],
										'ypos': json_object['ypos'],
										'room': json_object['room'],
										'floor': json_object['floor'],
										'action': '', 
										'severity': 0
									}
						}
					}
					
	building_status = {
						'id':  [json_object['buildingId']],
						'message': {
									'msg_type': 'update status',
									'body':{
										'xpos': json_object['xpos'],
										'ypos': json_object['ypos'],
										'room': json_object['room'],
										'floor': json_object['floor'],
										'status': json_object['type']
									}
						}
					}
	
	# Send new building status if the building is not up to date
	if(~checkBuildingStatus(json_object['type'], json_object['buildingId'])):
		generatePOST(building_status)	
	
	# Get list of robots that can respond to the event
	robot_command['id'] = findRobot(json_object['type'], json_object['buildingId'])				
		
	# Generate Command/Message Content
	if len(robot_command['id']) == 0:
		return # What do we do if no robots can solve problem
	elif json_object['type'] == 'fire':	
		robot_command['message']['body']['action'] = 'Extinguish'
		robot_command['message']['body']['severity'] = FIRE
		
	elif json_object['type'] == 'intruder':
		robot_command['message']['body']['action'] = 'Attack'
		robot_command['message']['body']['severity'] = INTRUDER
		
	elif json_object['type'] == 'water leak':
		robot_command['message']['body']['action'] = 'Pump'
		robot_command['message']['body']['severity'] = WATER_LEAK
		
	elif json_object['type'] == 'gas leak':
		robot_command['message']['body']['action'] = 'Vent'
		robot_command['message']['body']['severity'] = GAS_LEAK
	else:
		return # Unhandled Event		
		
	# Send Robot Command
	generatePOST(robot_command)

	# Get list of users linked to the buildingId
	user_message['id'] = findBuildingOccupants(json_object['buildingId'])
	
	if len(user_message['id']) == 0:
		if len(robot_command['id']) == 0:
			return # No users and No robots what do we do?
		return # No users what do we do?

	# Generate user message
	user_message['message']['body']['message'] = 'Emergency: ' + json_object['type'].upper() + ' of Severity: ' + str(robot_command['message']['body']['severity'])
	
	# Send User Message
	generatePOST(user_message)

'''
This function determines which robots to send to handle an emergency.
'''
def findRobot(event_type, building):
	#get list of robot ids for a building
	return["0"]
	basepath = "localhost:8080/api/"
	robotIds = []
	conn = httplib.HTTPConnection(basepath)
	conn.request("GET", "buildings/" + building + "/robots/")
	r1 = conn.getresponse()
	data1 = eval(r1.read())
	conn.close()
	for thisObject in data1:
		robotIds.append(thisObject["id"])

	if(event_type == 'fire'):
		robot  = []
		conn = httplib.HTTPConnection(basepath)

		#search ids for the right capabilities
		for thisID in robotIds:
			conn.request("GET", "robots/" + thisID)
			r2 = conn.getresponse()
			data2 = eval(r2.read())
			if "extinguish" in data2["capabilities"]:
				robot.append(thisID)
		conn.close()

	elif(event_type == 'water leak'):
		robot  = []
		conn = httplib.HTTPConnection(basepath)

		#search ids for the right capabilities
		for thisID in robotIds:
			conn.request("GET", "robots/" + thisID)
			r2 = conn.getresponse()
			data2 = eval(r2.read())
			if "pump" in data2["capabilities"]:
				robot.append(thisID)
		conn.close()

	elif(event_type == 'gas leak'):
		robot  = []
		conn = httplib.HTTPConnection(basepath)

		#search ids for the right capabilities
		for thisID in robotIds:
			conn.request("GET", "robots/" + thisID)
			r2 = conn.getresponse()
			data2 = eval(r2.read())
			if "vent" in data2["capabilities"]:
				robot.append(thisID)
		conn.close()

	elif(event_type == 'intruder'):
		robot  = []
		conn = httplib.HTTPConnection(basepath)

		#search ids for the right capabilities
		for thisID in robotIds:
			conn.request("GET", "robots/" + thisID)
			r2 = conn.getresponse()
			data2 = eval(r2.read())
			if "attack" in data2["capabilities"]:
				robot.append(thisID)
		conn.close()
		
	return robot #returns list of robot ids
	
'''
Finds all user ids in a certain building.
'''
def findBuildingOccupants(building_id):
    return["0"]
    basePath = "localhost"
    userIds = []
    conn = httplib.HTTPConnection(basePath, 8080)

    conn.request("GET", "/api/users/")
    res = conn.getresponse()
    data = res.read()
    people = json.loads(data)

    for person in people:
        building = person["buildingID"]
        if(building == building_id):
            uid = person["id"]
            userIds.append(uid)
    return userIds
	
'''
Return true if new status equals current buildingId status else return false
'''
def checkBuildingStatus(event_type, building):
    return False
    conn = httplib.HTTPConnection("localhost:8080/api/")
	#search ids for the right capabilities
    conn.request("GET", "buildings/" + building)
    r2 = conn.getresponse()
    data2 = eval(r2.read())
    rVal = (data2["status"] == event_type)
    conn.close()
    return rVal