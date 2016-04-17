from __future__ import print_function
import json
import httplib

def lambda_handler(event, context):
    for record in event['Records']:
        temp = record['dynamodb']
        
        if record['eventName'] == 'MODIFY':
            if record['eventSourceARN'].find("sensors") >= 0:
                #message = (parseSensor(temp['OldImage'], temp['NewImage'], record['eventName']))
                message = 1
                if message:
                    if message['type'] != "ok":
                        emergencyLogic(message)
    
'''
This function parses a sensor object, and determines if something
has changed. If it has, it returns a dictionary contaning all 
pertinent information to be sent in a message to whoever requires it.
'''
def parseSensor(old,new,eventName):
    if old['data']['S'] == new['data']['S']:
    #if it's the same nothing has changed
        print("0")
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
    basePath = "localhost"
    robotIds = []
    conn = httplib.HTTPConnection(basePath, 8080)
    ""
    headers = {
            'cache-control': "no-cache",
    }
    params = {
	  "buildingID": "44131ffa-8e1e-494b-84b0-1e9e8bedccdd",
	  "sensorID": [
	    "string"
	  ],
	  "capabilities": [
	    "extinguish"
	  ],
	  "movement": "string",
	  "floor": 0,
	  "room": 0,
	  "xpos": 0,
	  "ypos": 0,
	  "from": "string"
	}

    json_obj = json.dumps(params)
    conn.request("GET", "/api/buildings/44131ffa-8e1e-494b-84b0-1e9e8bedccdd/robots/", headers=headers)
    r1 = conn.getresponse()
    print r1.read()

'''
Finds all user ids in a certain building.
'''
def findBuildingOccupants(building_id):
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
def checkBuildingStatus(building_id):
    basePath = "localhost"
    userIds = []
    conn = httplib.HTTPConnection(basePath, 8080)

    conn.request("GET", "/api/users/")
    
    res = conn.getresponse()
    data = res.read()
    
    print res.status
    print data
	
def checkIntruder(building_id, floor_id, room_id, xpos_id, ypos_id):
    try:
        basePath = "localhost"
        userIds = []
        conn = httplib.HTTPConnection(basePath, 8080)
        conn.request("GET", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)
        uid = 9999; #some junk value
        for person in people:
            building = person["buildingID"]
            floor = person["floor"]
            room = person["room"]
            xpos = person["xpos"]
            ypos = person["ypos"]
            if(building == building_id and floor == floor_id and xpos == xpos_id and ypos == ypos_id):
                uid = person["id"]
        if id == 9999:
            return True;
        else:
            return False;
    except Exception as e:
       print('Error in checkIntruder: ', e)
    return None
	
#This method will return sensor ids and data of the sensors of specific type present in the given building and room
#currently some dummy code
def getSensors(buildingID, room, sensorType):
    if(buildingID==1 and room==2):
        return ["a123","b123"]
    else:
        return ["d123"]
#These methods will check if the data of a particular sensor indicates that there is Fire.
#For example, the method will return true if temperature of temperature sensor is greater than 50. currently dummy code
def ifFireTemperature(tempSensor):
    if(tempSensor=="a123" or tempSensor=="b123"):
        return True
    else:
        return False

def ifFireSmoke(smokeSensor):
    return True

#If weight>50 then there is an intruder. right now, always False.
def isIntruder(weightSensor):
    return False
#This method will receive the emergency object as the input and confirm if the emergency is real by checking other sensors in the same location
def confirmEmergency(emergency):
#Get the type of emergency and the details such as room number
    msgType=emergency['msg_type']
    buildingID=emergency['body']['buildingID']
    room=emergency['body']['room']


#Based upon the type of emergency, get the respective sensors in that room
    if(msgType=="Fire"):
        smokeSensorsArray=getSensors(buildingID, room,"Smoke")
        tempSensorsArray=getSensors(buildingID, room,"Temperature")
        smokeCount=0
        tempCount=0
        for smokeSensor in smokeSensorsArray:
            if(ifFireSmoke(smokeSensor)):
                smokeCount=smokeCount+1

        for tempSensor in tempSensorsArray:
            if(ifFireTemperature(tempSensor)):
                tempCount=tempCount+1
#If more than half of the smoke and temperature sensors detect that there is fire then fire emergency is confirmed
        if((smokeCount>len(smokeSensorsArray)/2) & (tempCount>len(tempSensorsArray)/2)):
            return True
        else:
            return False
            
    elif(msgType=="Intruder"):
        weightSensorsArray=getSensors(buildingID,room,"Weight")
        weightSensorsCount=0
        for weightSensor in weightSensorsArray:
            if(isIntruder(weightSensor)):
                weightSensorsCount=weightSensorsCount+1
#If more than half of the weight sensors detect that there is an intruder then intruder emergency is confirmed
        if(weightSensorsCount>len(weightSensorsArray)/2):
            return True
        else:
            return False
			
def getSensorData(sensor_type, buildingId, room):
    """
    Queries the database for sensor data.
    Parameters:
        sensor_type -- /string/, 'type' field of sensor object
        buildingId -- /string/, uuid of the building for the sensor
        room -- /int/, room number of the sensor
    Returns:
        dict() of (key, value) pair where key=sensorId, value=data
        e.g.
            {
                '3d33d19e-2956-4520-bce6-2bcaba48b293' : '0xFF00',
                '243f7e81-6c21-4068-9c7d-b89963e3e38c' : '0x029A'
            }
    """
    try:
        conn = http.client.HTTPConnection('localhost:8080')
        conn.request('GET', '/api/buildings/' + buildingId + '/sensors/', headers={})
        sensors = json.loads(conn.getresponse().read().decode('utf-8'))
        sensorData = {}
        for sensor in sensors:
            if sensor['type'] == sensor_type and sensor['room'] == room:
                sensorData[sensor['id']] = sensor['data']
        return sensorData
    except Exception as e:
        print('Error: ', e)
    return None
	
class sensorProcessing(object):
    def __init__(self, module=None):
        if not module:
            pass #will import other modules here to call functions
            #import getSensorData as storage 
        else:
            storage = module
            db = module
            checkEmergency = module
        self.storage = storage
        self.db = db
        self.checkEmergency = checkEmergency
        
    def processWeightSensor(self, sensor):
        '''
        Process Weight sensors by reading the sensor history and new incoming data 
        and determines if there's an emergency or not.
        The emergency this looks for is intruders (based on other sensors too,
        possibly)

        If a weight is < 45, it's asumed to be a child or robot.

        As of right now, weight sensor changes will never cause an emergency.
        The weight sensor will only be read when door sensors change.
        '''
        pass #for now

    def processTempSensor(self, sensor):
        '''
        Process the temperature sensor by reading history and determining if there 
        could be a fire.  A fire is determined if temp > 100.  If temp >50, temp 
        is only a fire if there's smoke.
        '''
        emergency = None
        if int(sensor['newData']) > 100:
            emergency = 'fire'
        elif int(sensor['newData']) > 50:
            smokeSensors = self.storage.getSensorData('smoke',\
                    sensor['buildingId'], sensor['room'])
            if smokeSensors is None:
                return None
            for val in smokeSensors.values():
                if val == '1':
                    emergency = 'fire'

        return emergency

    def processSmokeSensor(self, sensor):
        '''
        Process the smoke sensor by reading the temperature sensor history.
        If the smoke sensor, it could be a flaw.  Check the temperature history to
        judge as well.  Only fire if smoke is 1 and temp > 50
        '''
        emergency = None
        if sensor['newData'] == '1':
            tempSensors = self.storage.getSensorData('temperature',\
                    sensor['buildingId'], sensor['room'])
            if tempSensors is None:
                return None
            for val in tempSensors.values():
                if int(val) > 50:
                    emergency = 'fire'
        return emergency


    def processDoorSensor(self, sensor):
        '''
        Process the door sensor. Used for intruder detection.  
        '''
        emergency = None
        if sensor['newData'] == '1':
            #door sensor went off
            sensors = self.storage.getSensorsAtLocation(sensor['buildingId'],\
                    sensor['room'], sensor['floor'], sensor['xpos'],\
                    sensor['ypos'])
            assert sensors is not None, "sensors has to at least have a door sensor!"
            for sensor in sensors:
                if sensor['type'] == 'weight' and int(sensor['data']) > 80:
                    #weight sensor heavy
                    users = self.storage.getUsersInRoom(sensor['buildingId'], sensor['room'])
                    if users is None or not users:
                        emergency = 'intruder'
        return emergency

    def processGasSensor(self, sensor):
        '''
        If the new data is a 1, create a gas event.  If it's 0, end an existing
        gas event.
        '''
        return 'gas leak' if sensor['newData'] == '1' else None

    def processWaterSensor(self, sensor):
        '''
        If < 40 or > 65, return emergency
        '''
        newData = int(sensor['newData'])
        return 'water leak' if newData < 40 or newData > 65 else None


    #update to us passing a sensor dict object with oldData and newData already 
    #filled in.  We'll return a string 'emergency' if there is one.  'emergency'
    #can be something like 'fire' or 'gas'
    def processNewSensorData(self, sensor):
        '''
        Process new sensor data depending on the sensor type and possibly previous
        sensor data.  This "main" method acts as a switch to route sensor types
        to particular subroutines.
        If the new sensor data is the same as the last in the history, it is 
        ignored and None is returned.
        If a new emergency is detected, the emergency is created and returned.
        Otherwise, None is returned.
        '''
        sensorType = sensor['type']
        sensorID = sensor['id']
        newData = sensor['newData']
        if 'oldData' in sensor:
            oldData = sensor['oldData']
        else:
            oldData = None
        #history = db.getSensorHistory(sensorID)

        # check to see if the data has changed at all
        # Might want to check if status is still set and act accordingly
        # for now just return None
        # This should never happen so this is just a sanity check
        if oldData and oldData == newData:
            return None 

        emergency = None
        if sensorType == 'temperature':
            emergency = self.processTempSensor(sensor)
        elif sensorType == 'smoke':
            emergency = self.processSmokeSensor(sensor)
        elif sensorType == 'weight':
            emergency = self.processWeightSensor(sensor)
        elif sensorType == 'gas':
            emergency = self.processGasSensor(sensor)
        elif sensorType == 'door':
            emergency = self.processDoorSensor(sensor)
        elif sensorType == 'water pressure':
            emergency = self.processWaterSensor(sensor)
        

        self.db.shiftHistory(sensorID, newData)
        if emergency is not None:
            trueEmergency = self.checkEmergency.confirmEmergency(emergency, sensor)
            return emergency if trueEmergency else None
        return None
