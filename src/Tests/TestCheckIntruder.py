import unittest
import collections
import httplib
import json
import sys
sys.path.append('..')
import checkIntruder as intruderC

class TestCheckIntruder(unittest.TestCase):
    def test_check_intruder(self):

        print "Intruder Checking Test Started"
        
        basePath = "localhost"
        conn = httplib.HTTPConnection(basePath, 8080)

        # start by clearing up
        conn.request("DELETE", "/api/users/")
        conn.getresponse()
                
        # Insert 2 users and see that they are not intruders
        
        # Insert user 1
        conn.request("POST", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)
        the_id = people["id"]

        # Add user1 to building 1 floor 3
        headers = {
            'Content-Type': 'application/json',
            'cache-control': "no-cache",
        }
        base_obj = {
          "buildingId": "1",
          "floor": 3,
          "room": 3,
          "xpos": 3,
          "ypos": 3,
          "message": "111",
          "owner": True
        }

        json_obj = json.dumps(base_obj)
        address = "/api/users/" + the_id
        conn.request("PUT", address, json_obj, headers)
        res = conn.getresponse()
     
        # Add user2 to building 1 floor 2
        conn.request("POST", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        people = json.loads(data)
        the_id = people["id"]

        headers = {
            'Content-Type': 'application/json',
            'cache-control': "no-cache",
        }
        base_obj = {
          "buildingId": "1",
          "floor": 2,
          "room": 2,
          "xpos": 2,
          "ypos": 2,
          "message": "111",
          "owner": True
        }
        json_obj = json.dumps(base_obj)
        address = "/api/users/" + the_id
        conn.request("PUT", address, json_obj, headers)
        res = conn.getresponse()
                           
        # Now these 2 users should not be intruders
        response = intruderC.checkIntruder("1", 3, 3, 3, 3)
        self.assertEquals(False, response, "Error: A They are not supposed to be intruders")   
        
        response = intruderC.checkIntruder("1", 2, 2, 2, 2)
        self.assertEquals(False, response, "Error: B They are not supposed to be intruders")   
                        
        # Now a non existant user should be an Intruder
        response = intruderC.checkIntruder("1", 4, 3, 3, 3)
        self.assertEquals(True, response, "Error: C They are not supposed to be intruders")

        print "Intruder Checking Test Successfully Ended"

                                   
# ________________________________________________________________

if __name__ == '__main__':
    unittest.main(exit = False)

