import httplib
import json

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

    """
    conn.request("GET", "/api/buildings/" + str(building) + "/robots/")
    r1 = conn.getresponse()
	
    data1 = r1.read()
    """
    """
	data1 = eval(r1.read())
	conn.close()
	for thisObject in data1:
		robotIds.append(thisObject["id"])
	"""


if __name__ == '__main__':
	findRobot('fire', '44131ffa-8e1e-494b-84b0-1e9e8bedccdd')

	"""
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
	"""