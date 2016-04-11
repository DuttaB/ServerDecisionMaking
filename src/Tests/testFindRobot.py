import httplib
import json
import unittest

def findRobot(event_type, building):
	#get list of robot ids for a building
    basePath = "localhost"
    robotIds = []
    conn = httplib.HTTPConnection(basePath, 8080)
    ""
    headers = {
            'cache-control': "no-cache",
    }

    conn.request("GET", "/api/buildings/" + building + "/robots/", headers=headers)
    r1 = conn.getresponse()
    data = r1.read()
    print(data, "here")
    robots = eval(data)

    print("event", event_type)

    if(event_type == 'fire'):
        for robot in robots:
            capabilities = robot["capabilities"]
            the_id = robot["id"]
            if 'extinguish' in capabilities:
                robotIds.append(the_id)                
    elif(event_type == 'water leak'):
        for robot in robots:
            capabilities = robot["capabilities"]
            the_id = robot["id"]
            if 'pump' in capabilities:
            	robotIds.append(the_id)
    elif(event_type == 'gas leak'):
        for robot in robots:
            capabilities = robot["capabilities"]
            the_id = robot["id"]
            if 'vent' in capabilities:
            	robotIds.append(the_id)
    elif(event_type == 'intruder'):
        for robot in robots:
            capabilities = robot["capabilities"]
            the_id = robot["id"]
            if 'attack' in capabilities:
            	robotIds.append(the_id)

    conn.close()
    return robotIds

def extinguish(robot_id, building_id):
	
    robot = {    
	  "capabilities": [
	    'extinguish'
	  ],
    }

    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

    json_object = json.dumps(robot)
    basePath = "localhost"
    conn = httplib.HTTPConnection(basePath, 8080)
    conn.request("PUT", "/api/robots/" + robot_id, json_object, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

def pump(robot_id, building_id):
    robot = {    
	  "capabilities": [
	    'pump'
	  ],
    }



    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

    json_object = json.dumps(robot)
    basePath = "localhost"
    conn = httplib.HTTPConnection(basePath, 8080)
    conn.request("PUT", "/api/robots/" + robot_id, json_object, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

def vent(robot_id, building_id):
    robot = {    
	  "capabilities": [
	    'vent'
	  ],
    }



    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

    json_object = json.dumps(robot)
    basePath = "localhost"
    conn = httplib.HTTPConnection(basePath, 8080)
    conn.request("PUT", "/api/robots/" + robot_id, json_object, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

def attack(robot_id, building_id):
    robot = {    
	  "capabilities": [
	    'attack'
	  ],
    }

    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

    json_object = json.dumps(robot)

    print("Obj", json_object, "\n\n")
    basePath = "localhost"
    conn = httplib.HTTPConnection(basePath, 8080)
    conn.request("PUT", "/api/robots/" + robot_id, json_object, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

def post_robot(building_id):
	basePath = "localhost"
	conn = httplib.HTTPConnection(basePath, 8080)
	conn.request("POST", "/api/buildings/" + building_id + "/robots/")
	res = conn.getresponse()
	data = res.read()
	robot = eval(data)
	robot_id = robot["id"]
	return robot_id	

def delete_building(building_id):
	basePath = "localhost"
	conn = httplib.HTTPConnection(basePath, 8080)
	conn.request("DELETE", "/api/buildings/" + building_id)
	res = conn.getresponse()
	data = res.read()

	print (data, "anything")


def new_building():

	basePath = "localhost"
	conn = httplib.HTTPConnection(basePath, 8080)
	conn.request("POST", "/api/buildings/")
	res = conn.getresponse()
	data = res.read()
	building = eval(data)
	print(building)
	the_id = building["id"]
	return the_id

def delete_robots(building_id):
	basePath = "localhost"
	conn = httplib.HTTPConnection(basePath, 8080)
	conn.request("DELETE", "/api/buildings/" + building_id + "/robots/")
	res = conn.getresponse()
	data = res.read()
	print(data, "here")


class TestServerMethods(unittest.TestCase):
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

suite = unittest.TestLoader().loadTestsFromTestCase(TestServerMethods)
unittest.TextTestRunner(verbosity=2).run(suite)