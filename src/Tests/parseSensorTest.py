#!/usr/bin/python

import mock
import sys
sys.path.append('..')
import holder
import unittest
from json_generators import *



class TestParseSensorUnit(unittest.TestCase):
    def test_insertSensor(self):
        event = generate_lambda("", "sensors", "INSERT") 
        event['Records'][0]['dynamodb']['NewImage']['robotId'] = {'S':"robId"}
        result = holder.parseSensor(0, event['Records'][0]['dynamodb']['NewImage'], event['Records'][0]['eventName'])

        self.assertIsNotNone(result)

    def test_modifySameData(self):
        event = generate_lambda("45", "sensors", "MODIFY", "45") 
        new = event['Records'][0]['dynamodb']['NewImage']
        old = event['Records'][0]['dynamodb']['OldImage']
        result = holder.parseSensor(old, new, event['Records'][0]['eventName'])

        self.assertIsNone(result)


    @mock.patch('holder.sensorProcessing.processNewSensorData', return_value=None)
    def test_modifyDataNoEmergency(self, processData):
        event = generate_lambda("50", "sensors", "MODIFY", "45") 
        event['Records'][0]['dynamodb']['NewImage']['robotId'] = {'S':"robId"}
        new = event['Records'][0]['dynamodb']['NewImage']
        old = event['Records'][0]['dynamodb']['OldImage']
        result = holder.parseSensor(old, new, event['Records'][0]['eventName'])

        self.assertIsNone(result)
        self.assertTrue(processData.called)

    @mock.patch('holder.sensorProcessing.processNewSensorData', return_value="fire")
    def test_modifyDataFire(self, processData):
        event = generate_lambda("101", "sensors", "MODIFY", "45") 
        event['Records'][0]['dynamodb']['NewImage']['robotId'] = {'S':"robId"}
        new = event['Records'][0]['dynamodb']['NewImage']
        old = event['Records'][0]['dynamodb']['OldImage']
        result = holder.parseSensor(old, new, event['Records'][0]['eventName'])

        self.assertIsNotNone(result)
        self.assertTrue(processData.called)
        self.assertEquals(result['type'], "fire")



suite = unittest.TestLoader().loadTestsFromTestCase(TestParseSensorUnit)
unittest.TextTestRunner(verbosity=2).run(suite)
