import unittest
import collections
import sys
sys.path.append('..')
import checkIntruder as intruderC

class TestCheckIntruder(unittest.TestCase):
    def test_check_intruder(self):
        building_array = [7,9,45,22,21,16,19,2,30,20]
        floor_array =     [0,2,0,1,0,3,4,5,2,1]
        room_array = [0,2,0]
        xpos_array = [41,44,46,45,47,45,42,40,42]
        ypos_array = [0,1,0,1,0,1,0,1,0]
        for building in building_array:
            for floor in floor_array:
                for room in room_array:
                    for xpos in xpos_array:
                        for ypos in ypos_array:
                            #print (sys.path)
                            self.assertEquals(True,intruderC.checkIntruder(building, floor, room, xpos, ypos), "Could not find intruder")
    





