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
        print "checkIntruder(): Need to look for intruder at building, floor, room, xpos, ypos: %s %d %d %d %d" %(building_id, floor_id, room_id, xpos_id, ypos_id)
        
        for person in people:
            building = person["buildingId"]
            floor = person["floor"]
            room = person["room"]
            xpos = person["xpos"]
            ypos = person["ypos"]
            print "checkIntruder(): Intruder Comparison for, building, floor, room, xpos, ypos: %s %d %d %d %d" %(building, floor, room, xpos, ypos)            
            if(building == building_id and floor == floor_id and room == room_id and xpos == xpos_id and ypos == ypos_id):
                uid = person["id"]
                #print"MATCH %d %d" %(uid, person["id"])

        if uid != 9999:
            print"NOT FOUND intruder in the given location!!!"
            return False;
        else:
            print"FOUND intruder in the given location!!!"
            return True;
    except Exception as e:
       print('Error in checkIntruder: ', e)
    return None
