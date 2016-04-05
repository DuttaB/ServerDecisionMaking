import httplib
import json
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

if __name__ == '__main__':
   	this = findBuildingOccupants("1")
   	print this