"""
This is the test module for the event server. This module performs the following tests
Tests sensors where no change occurs
Tests sensors where the status is okay
Tests sensors with emergencies:
    fire
    gas leak
    flood
    intruder
    water leak
Tests robots
"""

import unittest
import sys
from io import StringIO
# import functions to be tested
from team4_modify import *
from json_generators import *
import StringIO

class TestServerMethods(unittest.TestCase):
    #parseSensor unit testing
    def test_sensors(self):
        sensor_events = [
            generate_sensor_json("INSERT", "ok"),              # Generates a sensor where value is okay
        ]
        sensor_responses = [
            "motion detector"
        ]

        # Counter for expected responses
        i = 0
        for event in sensor_events:
            old, new, eventName = event
            if i == 1:
                self.assertEqual(parseSensor(old, new, eventName), 0)
            else:
                self.assertEqual(parseSensor(old, new, eventName)['type'], sensor_responses[i])
            i += 1

    def test_robots(self):
        #parseRobots test, relys on parseSensor
        robot_events = [
            generate_robot_json(True)
        ]

        robot_responses = [
            True
        ]

        # Counter for expected responses
        i = 0
        for event in robot_events:
            if("sensorId" in event):
                #special test case for expecting integer return
                self.assertEqual("sensorId" in parseRobot(event), robot_responses[i])
            else:
                self.assertEqual("sensorId" in parseRobot(event), robot_responses[i])
            i += 1

    def test_user(self):
        user_events = [
            generate_user_json("INSERT", "ok"),              # Generates a sensor where value is okay
        ]
        user_responses = [
            "new user"
        ]

        # Counter for expected responses
        i = 0
        for event in user_events:
            old, new, eventName = event
            if i == 1:
                self.assertEqual(parseUser(old, new, eventName), 0)
            elif i == 0:
                self.assertEqual(parseUser(old, new, eventName)['from'], user_responses[i])
            else:
                self.assertEqual(parseUser(old, new, eventName)['type'], user_responses[i])
            i += 1

    def test_find_items(self):
        test_obj = generate_find_items_json()
        test_result = findItems(test_obj)
        expected = ["attack", "vent"]

        self.assertEqual(test_result, expected)

    #BMH : This is a test of the new_object helper function for the POST function
    #The JSON structures are based on the returns of the parsing functions for an INSERT
    #We analyse the print statement from the POST function to make assertions about validity
    def test_new_object(self):
        sensor = {
                        "from": "new sensor",
                        "id": '1',
                        "buildingId": '0',
                        "model": 'KM07',
                        "type": 'motion detector'
                    }
        user = {
                        "from": "new user",
                        "id": '2',
                        "buildingId": '0',
                        "room": '0',
                        "xpos": '1',
                        "ypos": '1',
                        "floor": '2',
                        "owner": 'True'
                    }
        robot = {
                    "from": "new robot",
                    "id": '3',
                    "buildingId": '0',
                    "room": '0',
                    "xpos": '2',
                    "ypos": '2',
                    "floor": '2',
                    "movement": 'right',
                    "capabilities": 'vent',
                    "sensorId" : '1'
                }
        NO_events = [
            sensor,
            user,
            robot
        ]
        NO_responses = [
            '{"message": {"body": {"type": "motion detector", "model": "KM07", "new_id": "1", "buildingId": "0"}, "msg_type": "new sensor"}, "id": ["0"]}',
            '{"message": {"body": {"xpos": "1", "room": "0", "floor": "2", "new_id": "2", "ypos": "1", "owner": "True", "buildingId": "0"}, "msg_type": "new user"}, "id": ["0"]}',
            '{"message": {"body": {"ypos": "2", "xpos": "2", "room": "0", "floor": "2", "sensorId": "1", "new_id": "3", "buildingId": "0", "capabilities": "vent", "movement": "right"}, "msg_type": "new robot"}, "id": ["0"]}'
        ]
        # Counter for expected responses
        i = 0
        for event in NO_events:
            #do stringIO things to correctly test outputs
            sys.stdout = StringIO.StringIO()
            newObjectLogic(NO_events[i])
            sys.stdout.seek(0)
            out = sys.stdout.read()
            sys.stdout.flush()
            returned = out.split("\n")[0]
            self.assertEqual(returned, NO_responses[i])
            i += 1


    #BMH : Test for correct flow from lambda function entry point through subroutines to server POST routine
    #The only return we can assert against is the print from the POST routine, so we capture that and compare
    #to expected to see if the lambda function correctly governed program flow
    def test_lambda(self):
        lambda_events = [
            #make sure all parsing functions (user, sensor, robot) are reached, as well as
            #all processing functions (user message, emergency, new object)
            generate_lambda("fire", "sensors", "MODIFY"),  # no change(old status defaults to fire
            generate_lambda("ok", "sensors", "MODIFY"),  # no change(old status defaults to fire
        ]

        lambda_responses = [
            '0',
            ""
        ]

        # Counter for expected responses
        i = 0
        for event in lambda_events:
            #do stringIO things to correctly test outputs
            sys.stdout = StringIO.StringIO()
            lambda_handler(event,0)
            sys.stdout.seek(0)
            out = sys.stdout.read()
            sys.stdout.flush()
            returned = out.split("\n")[0]
            self.assertEqual(returned, lambda_responses[i])
            i += 1

suite = unittest.TestLoader().loadTestsFromTestCase(TestServerMethods)
unittest.TextTestRunner(verbosity=2).run(suite)