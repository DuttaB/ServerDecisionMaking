"""
This is the test module for the event server. This module performs the following tests
Tests sensors where no change occurs
Tests sensors where the status is okay
Tests sensors with emergencies:
    fire
    gas leak
    flood
    intruder
    water leak
Tests robots
"""

import unittest
import sys
from io import StringIO
# import functions to be tested
from team4_modify import *
from json_generators import *
import StringIO
import http.client

# ________________________________________________________________

NUM_SENSORS_OF_BUILDING = [9, 4]
NUM_BUILDINGS = len(NUM_SENSORS_OF_BUILDING)

SENSOR_TYPES = ['IR', 'Sonar']
NUM_SENSOR_TYPES = len(SENSOR_TYPES)

NUM_ROOMS_OF_BUILDING = [3, 2]

# ________________________________________________________________

conn = http.client.HTTPConnection('localhost:8080')
buildingIds = []
sensorIds = {}

# ________________________________________________________________

class TestServerMethods(unittest.TestCase):
    #parseSensor unit testing
    def test_sensors(self):
        sensor_events = [
            generate_sensor_json("INSERT", "ok"),              # Generates a sensor where value is okay
        ]
        sensor_responses = [
            "motion detector"
        ]

        # Counter for expected responses
        i = 0
        for event in sensor_events:
            old, new, eventName = event
            if i == 1:
                self.assertEqual(parseSensor(old, new, eventName), 0)
            else:
                self.assertEqual(parseSensor(old, new, eventName)['type'], sensor_responses[i])
            i += 1

    def test_robots(self):
        #parseRobots test, relys on parseSensor
        robot_events = [
            generate_robot_json(True)
        ]

        robot_responses = [
            True
        ]

        # Counter for expected responses
        i = 0
        for event in robot_events:
            if("sensorId" in event):
                #special test case for expecting integer return
                self.assertEqual("sensorId" in parseRobot(event), robot_responses[i])
            else:
                self.assertEqual("sensorId" in parseRobot(event), robot_responses[i])
            i += 1

    def test_user(self):
        user_events = [
            generate_user_json("INSERT", "ok"),              # Generates a sensor where value is okay
        ]
        user_responses = [
            "new user"
        ]

        # Counter for expected responses
        i = 0
        for event in user_events:
            old, new, eventName = event
            if i == 1:
                self.assertEqual(parseUser(old, new, eventName), 0)
            elif i == 0:
                self.assertEqual(parseUser(old, new, eventName)['from'], user_responses[i])
            else:
                self.assertEqual(parseUser(old, new, eventName)['type'], user_responses[i])
            i += 1

    def test_find_items(self):
        test_obj = generate_find_items_json()
        test_result = findItems(test_obj)
        expected = ["attack", "vent"]

        self.assertEqual(test_result, expected)

    #BMH : This is a test of the new_object helper function for the POST function
    #The JSON structures are based on the returns of the parsing functions for an INSERT
    #We analyse the print statement from the POST function to make assertions about validity
    def test_new_object(self):
        sensor = {
                        "from": "new sensor",
                        "id": '1',
                        "buildingId": '0',
                        "model": 'KM07',
                        "type": 'motion detector'
                    }
        user = {
                        "from": "new user",
                        "id": '2',
                        "buildingId": '0',
                        "room": '0',
                        "xpos": '1',
                        "ypos": '1',
                        "floor": '2',
                        "owner": 'True'
                    }
        robot = {
                    "from": "new robot",
                    "id": '3',
                    "buildingId": '0',
                    "room": '0',
                    "xpos": '2',
                    "ypos": '2',
                    "floor": '2',
                    "movement": 'right',
                    "capabilities": 'vent',
                    "sensorId" : '1'
                }
        NO_events = [
            sensor,
            user,
            robot
        ]
        NO_responses = [
            '{"message": {"body": {"type": "motion detector", "model": "KM07", "new_id": "1", "buildingId": "0"}, "msg_type": "new sensor"}, "id": ["0"]}',
            '{"message": {"body": {"xpos": "1", "room": "0", "floor": "2", "new_id": "2", "ypos": "1", "owner": "True", "buildingId": "0"}, "msg_type": "new user"}, "id": ["0"]}',
            '{"message": {"body": {"ypos": "2", "xpos": "2", "room": "0", "floor": "2", "sensorId": "1", "new_id": "3", "buildingId": "0", "capabilities": "vent", "movement": "right"}, "msg_type": "new robot"}, "id": ["0"]}'
        ]
        # Counter for expected responses
        i = 0
        for event in NO_events:
            #do stringIO things to correctly test outputs
            sys.stdout = StringIO.StringIO()
            newObjectLogic(NO_events[i])
            sys.stdout.seek(0)
            out = sys.stdout.read()
            sys.stdout.flush()
            returned = out.split("\n")[0]
            self.assertEqual(returned, NO_responses[i])
            i += 1
			
	#The base sensor object
    sensor = {}
    process = sensorProcessing(dummy)
	
    def setUp(self):
        self.sensor['id'] = 'id'
        self.sensor['buildingId'] = 'bid'
        self.sensor['robotId'] = 'robotId'
        self.sensor['floor'] = 0
        self.sensor['room'] = 1
        self.sensor['xpos'] = 3
        self.sensor['ypos'] = 4
        self.sensor['data'] = 'data'
        self.sensor['model'] = 'model'
        self.sensor['type'] = 'type'
        self.sensor['newData'] = ''
        self.sensor['oldData'] = ''
        dummy.setUpLists()


    def test_createNewDataNoHistory(self):
        self.sensor['id'] = 'none'
        self.sensor['type'] = 'none'
        self.sensor['newData'] = '0'
        self.assertEquals(None, self.process.processNewSensorData(self.sensor))

    def test_createNewFireEventLowHeat(self):
        self.sensor['id'] = 'temp'
        self.sensor['type'] = 'temperature'
        self.sensor['newData'] = '60'
        self.sensor['oldData'] = dummy.getSensorData('temperature',\
                self.sensor['buildingId'], self.sensor['room'])
        dummy.shiftHistory('smoke', '1')
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency)

    def test_createNewFireHighHeat(self):
        self.sensor['id'] = 'temp'
        self.sensor['type'] = 'temperature'
        self.sensor['newData'] = '101'
        self.sensor['oldData'] = dummy.getSensorData('temperature',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency)

    def test_createNewFireSmokeChange(self):
        self.sensor['id'] = 'smoke'
        self.sensor['type'] = 'smoke'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('smoke',\
                self.sensor['buildingId'], self.sensor['room'])
        dummy.shiftHistory('temp', '60')
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency)

    def test_noFireSmoke(self):
        self.sensor['id'] = 'smoke'
        self.sensor['type'] = 'smoke'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('smoke',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_gasLeak(self):
        self.sensor['id'] = 'gas'
        self.sensor['type'] = 'gas'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('gas',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('gas leak', emergency)

    def test_noGasLeak(self):
        dummy.shiftHistory('gas', '0')
        self.sensor['id'] = 'gas'
        self.sensor['type'] = 'gas'
        self.sensor['newData'] = '0'
        self.sensor['oldData'] = dummy.getSensorData('gas',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_waterLeakLow(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '10'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('water leak', emergency)

    def test_waterLeakHigh(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '80'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('water leak', emergency)

    def test_waterNormal(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '45'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_lowWeightNoIntruder(self):
        self.sensor['id'] = 'weight'
        self.sensor['type'] = 'weight'
        self.sensor['newData'] = '44'
        self.sensor['oldData'] = dummy.getSensorData('weight',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_highWeightNoIntruder(self):
        dummy.addUser('user1')
        self.sensor['id'] = 'weight'
        self.sensor['type'] = 'weight'
        self.sensor['newData'] = '81'
        self.sensor['oldData'] = dummy.getSensorData('weight',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorClosed(self):
        dummy.shiftHistory('door','1')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '0'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenNoIntruder(self):
        dummy.addUser('user1')
        dummy.shiftHistory('weight','81')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenNoIntruderChild(self):
        dummy.shiftHistory('weight','40')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenIntruder(self):
        dummy.shiftHistory('weight','81')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('intruder', emergency)
		
	 def deleteAllBuildings():
        conn.request('DELETE', '/api/buildings/', headers={})
        conn.getresponse()

    def postAndGetBuildingId():
        conn.request('POST', '/api/buildings/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        return data['id']

    def deleteAllSensorsOfBuilding(x):
        conn.request('DELETE', '/api/buildings/' + buildingIds[x] + '/sensors/', headers={})
        conn.getresponse()

    def postAndGetSensorIdOfBuilding(x):
        # create sensors for building 1
        sensorIdsOfBuildingX = []
        for i in range(NUM_SENSORS_OF_BUILDING[x]):
            conn.request('POST', '/api/buildings/' + buildingIds[x] + '/sensors/', headers={})
            data = json.loads(conn.getresponse().read().decode('utf-8'))
            sensorIdsOfBuildingX.append(data['id'])
        return sensorIdsOfBuildingX

    def putSensorForBuilding(x):
        for i in range(NUM_SENSORS_OF_BUILDING[x]):
            data = {
                'type' : SENSOR_TYPES[i % NUM_SENSOR_TYPES],
                'room' : int(i / int(NUM_SENSORS_OF_BUILDING[x] / NUM_ROOMS_OF_BUILDING[x])),
                'data' : sensorIds[buildingIds[x]][i]
            }
            payload = json.dumps(data)
            conn.request('PUT', '/api/sensors/' + sensorIds[buildingIds[x]][i],
                         payload, {'content-type': 'application/json'})
            print(conn.getresponse().read().decode('utf-8'))

    print('******Creating objects for test cases******')
    for i in range(NUM_BUILDINGS):
        buildingIds.append(postAndGetBuildingId())
        print('Created building%d with id=%s' % (i, buildingIds[i]))
        deleteAllSensorsOfBuilding(i)
        print('All sensors for building%d deleted.' % (i))
        sensorIds[buildingIds[i]] = postAndGetSensorIdOfBuilding(i)
        print('Created sensors for building%d, ids=%s' % (i, sensorIds[buildingIds[i]]))
        putSensorForBuilding(i)
    print('******Finished creating objects for test cases******')


    def __init__(self, *args, **kwargs):
        super(TestGetSensorData, self).__init__(*args, **kwargs)
        createObjects()

    def test(self):
        print('******Running test cases******')
        # building 0
        # room0
        sensorData_IR_room0 = getSensorData('IR', buildingIds[0], 0)
        self.assertEqual(sensorData_IR_room0,
                         {x : x for x in [sensorIds[buildingIds[0]][0], sensorIds[buildingIds[0]][2]]})
        sensorData_Sonar_room0 = getSensorData('Sonar', buildingIds[0], 0)
        self.assertEqual(sensorData_Sonar_room0,
                         {x : x for x in [sensorIds[buildingIds[0]][1]]})
        # room1
        sensorData_IR_room1 = getSensorData('IR', buildingIds[0], 1)
        self.assertEqual(sensorData_IR_room1,
                         {x : x for x in [sensorIds[buildingIds[0]][4]]})
        sensorData_Sonar_room1 = getSensorData('Sonar', buildingIds[0], 1)
        self.assertEqual(sensorData_Sonar_room1,
                         {x : x for x in [sensorIds[buildingIds[0]][3], sensorIds[buildingIds[0]][5]]})
        # room2
        sensorData_IR_room2 = getSensorData('IR', buildingIds[0], 2)
        self.assertEqual(sensorData_IR_room2,
                         {x : x for x in [sensorIds[buildingIds[0]][6], sensorIds[buildingIds[0]][8]]})
        sensorData_Sonar_room2 = getSensorData('Sonar', buildingIds[0], 2)
        self.assertEqual(sensorData_Sonar_room2,
                         {x : x for x in [sensorIds[buildingIds[0]][7]]})

        # building 1
        # room0
        sensorData_IR_room0 = getSensorData('IR', buildingIds[1], 0)
        self.assertEqual(sensorData_IR_room0,
                         {x : x for x in [sensorIds[buildingIds[1]][0]]})
        sensorData_Sonar_room0 = getSensorData('Sonar', buildingIds[1], 0)
        self.assertEqual(sensorData_Sonar_room0,
                         {x : x for x in [sensorIds[buildingIds[1]][1]]})
        # room1
        sensorData_IR_room1 = getSensorData('IR', buildingIds[1], 1)
        self.assertEqual(sensorData_IR_room1,
                         {x : x for x in [sensorIds[buildingIds[1]][2]]})
        sensorData_Sonar_room1 = getSensorData('Sonar', buildingIds[1], 1)
        self.assertEqual(sensorData_Sonar_room1,
                         {x : x for x in [sensorIds[buildingIds[1]][3]]})

        print('******Finished running test cases******')
		
	def testFindRobot(self):
		building_id = new_building()
        
		empty_list = []
		fire_robots = findRobot('fire', building_id)
		water_robots = findRobot('water leak', building_id)
		gas_robots = findRobot("gas leak", building_id)
		intruder_robots = findRobot('intruder', building_id)
		self.assertEqual(fire_robots, empty_list)
		self.assertEqual(water_robots, empty_list)
		self.assertEqual(gas_robots, empty_list)
		self.assertEqual(intruder_robots, empty_list)

		robot1 = post_robot(building_id)		
		robot2 = post_robot(building_id)
		robot3 = post_robot(building_id)
		robot4 = post_robot(building_id)
		
		fire_robots = findRobot('fire', building_id)
		water_robots = findRobot('water leak', building_id)
		gas_robots = findRobot("gas leak", building_id)
		intruder_robots = findRobot('intruder', building_id)

		self.assertEqual(fire_robots, empty_list)
		self.assertEqual(water_robots, empty_list)
		self.assertEqual(gas_robots, empty_list)
		self.assertEqual(intruder_robots, empty_list)
		fire_robots = findRobot('fire', building_id)
		
		extinguish(robot1, building_id)
		pump(robot2, building_id)
		vent(robot3, building_id)
		attack(robot4, building_id)

		fire_robots = findRobot('fire', building_id)
		water_robots = findRobot('water leak', building_id)
		gas_robots = findRobot("gas leak", building_id)
		intruder_robots = findRobot('intruder', building_id)
		
		self.assertEqual(len(fire_robots), 1)
		self.assertEqual(len(water_robots), 1)
		self.assertEqual(len(gas_robots), 1)
		self.assertEqual(len(intruder_robots), 1)

		robot5 = post_robot(building_id)		
		robot6 = post_robot(building_id)
		robot7 = post_robot(building_id)
		robot8 = post_robot(building_id)
		

		fire_robots = findRobot('fire', building_id)
		water_robots = findRobot('water leak', building_id)
		gas_robots = findRobot("gas leak", building_id)
		intruder_robots = findRobot('intruder', building_id)



		self.assertEqual(len(fire_robots), 1)
		self.assertEqual(len(water_robots), 1)
		self.assertEqual(len(gas_robots), 1)
		self.assertEqual(len(intruder_robots), 1)


		extinguish(robot5, building_id)
		pump(robot6, building_id)
		vent(robot7, building_id)
		attack(robot8, building_id)

		fire_robots = findRobot('fire', building_id)
		water_robots = findRobot('water leak', building_id)
		gas_robots = findRobot("gas leak", building_id)
		intruder_robots = findRobot('intruder', building_id)

		self.assertEqual(len(fire_robots), 2)
		self.assertEqual(len(water_robots), 2)
		self.assertEqual(len(gas_robots), 2)
		self.assertEqual(len(intruder_robots), 2)
		
		delete_robots(building_id)
		delete_building(building_id)
		
	def test_check_fire(self):
        string1='{"msg_type": "Fire","body":{"buildingID":1,"room": 2, "floor": 2, "severity": 1}}'
        emergency1= json.loads(string1)
        self.assertEquals(True,confirmEmergency(emergency1), "Fire Event confirmed")
    
    def test_check_intruder(self):
        string2='{"msg_type": "Intruder","body":{"buildingID":2,"room": 2, "floor": 2, "severity": 1}}'
        emergency2= json.loads(string2)
        self.assertEquals(False,confirmEmergency(emergency2), "Intruder event false")
		
	def testFindOccupant(self):

        # Start connection
        basePath = "localhost"
        conn = httplib.HTTPConnection(basePath, 8080)


        # Delete all previous users.
        conn.request("DELETE", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)        

        # No users after all are deleted
        response = findBuildingOccupants("1")
        self.assertEqual(len(response), 0)

        # Post new user and get id to edit.
        conn.request("POST", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)
        the_id = people["id"]

        # New user, but not in building.
        response = findBuildingOccupants("1")
        self.assertEqual(len(response), 0)


        # Add user to building.
        headers = {
            'Content-Type': 'application/json',
            'cache-control': "no-cache",
        }
        base_obj = {
          "buildingID": "1",
          "floor": 4,
          "room": 4,
          "xpos": 4,
          "ypos": 4,
          "message": "111",
          "owner": True
        }

        json_obj = json.dumps(base_obj)
        address = "/api/users/" + the_id
        conn.request("PUT", address, json_obj, headers)
        res = conn.getresponse()
        response = findBuildingOccupants("1")
        self.assertEqual(len(response), 1)        
        

        # Post new user and get id to edit.
        conn.request("POST", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)
        the_id = people["id"]
        
        # Should have one users in the builidng
        response = findBuildingOccupants("1")
        self.assertEqual(len(response), 1)


        # Add user to building.
        headers = {
            'Content-Type': 'application/json',
            'cache-control': "no-cache",
        }
        base_obj = {
          "buildingID": "1",
          "floor": 4,
          "room": 4,
          "xpos": 4,
          "ypos": 4,
          "message": "111",
          "owner": True
        }
        json_obj = json.dumps(base_obj)
        address = "/api/users/" + the_id
        conn.request("PUT", address, json_obj, headers)
        res = conn.getresponse()
        
        # Should have two users in the builidng
        response = findBuildingOccupants("1")
        self.assertEqual(len(response), 2)        


    #BMH : Test for correct flow from lambda function entry point through subroutines to server POST routine
    #The only return we can assert against is the print from the POST routine, so we capture that and compare
    #to expected to see if the lambda function correctly governed program flow
    def test_lambda(self):
        lambda_events = [
            #make sure all parsing functions (user, sensor, robot) are reached, as well as
            #all processing functions (user message, emergency, new object)
            generate_lambda("fire", "sensors", "MODIFY"),  # no change(old status defaults to fire
            generate_lambda("ok", "sensors", "MODIFY"),  # no change(old status defaults to fire
        ]

        lambda_responses = [
            '0',
            ""
        ]

        # Counter for expected responses
        i = 0
        for event in lambda_events:
            #do stringIO things to correctly test outputs
            sys.stdout = StringIO.StringIO()
            lambda_handler(event,0)
            sys.stdout.seek(0)
            out = sys.stdout.read()
            sys.stdout.flush()
            returned = out.split("\n")[0]
            self.assertEqual(returned, lambda_responses[i])
            i += 1

suite = unittest.TestLoader().loadTestsFromTestCase(TestServerMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
