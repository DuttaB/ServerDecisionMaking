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
