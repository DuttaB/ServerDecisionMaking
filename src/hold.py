import httplib
import json
def findBuildingOccupants(building_id):
    basePath = "localhost"
    userIds = []
    conn = httplib.HTTPConnection(basePath, 8080)

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

    conn.request("GET", "/api/users/", json_obj, headers=headers)
    res = conn.getresponse()
    data = res.read()
    people = json.loads(data)

    for person in people:
    	building = person["buildingID"]

    	if(building == building_id):
    		uid = person["id"]
    		userIds.append(uid)

    return userIds

if __name__ == '__main__':
   	this = findBuildingOccupants("-1")
   	print this