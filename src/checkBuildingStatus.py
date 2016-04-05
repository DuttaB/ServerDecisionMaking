import httplib
import json
def checkBuildingStatus(building_id):
    basePath = "localhost"
    userIds = []
    conn = httplib.HTTPConnection(basePath, 8080)

    conn.request("GET", "/api/users/")
    
    res = conn.getresponse()
    data = res.read()
    
    print res.status
    print data
    """

    people = json.loads(data)

    for person in people:
    	building = person["buildingID"]
    	if(building == building_id):
    		uid = person["id"]
    		userIds.append(uid)
    return userIds
    """
if __name__ == '__main__':
   	this = checkBuildingStatus("1")
   	print this