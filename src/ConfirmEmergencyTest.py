import json
import unittest
import sys
sys.path.append('..')
from confirmEmergency import *
#This function gives the dummy emergencies to the confirm emergency method and checks the appropriate response
class ConfirmEmergencyTest(unittest.TestCase): 
    def test_check_fire(self):
        string1='{"msg_type": "Fire","body":{"buildingID":1,"room": 2, "floor": 2, "severity": 1}}'
        emergency1= json.loads(string1)
        self.assertEquals(True,confirmEmergency(emergency1), "Fire Event confirmed")
    
    def test_check_intruder(self):
        string2='{"msg_type": "Intruder","body":{"buildingID":2,"room": 2, "floor": 2, "severity": 1}}'
        emergency2= json.loads(string2)
        self.assertEquals(False,confirmEmergency(emergency2), "Intruder event false")
    
