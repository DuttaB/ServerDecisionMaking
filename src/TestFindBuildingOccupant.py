import httplib
import json
import unittest
import time
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



class testPost(unittest.TestCase):

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



suite = unittest.TestLoader().loadTestsFromTestCase(testPost)
unittest.TextTestRunner(verbosity=2).run(suite)
