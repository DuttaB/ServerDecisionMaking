# This function checks if the input location has an intruder or a
# genuine person by checking if there exists a person in that particular
# location.
# Inputs are building_id, floor_id, room_id, xpos_id, ypos_id
# It returns TRUE in case its an intruder, else it returns false.
# It raises exception, in case of errors and returns none.

import httplib
import json
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
