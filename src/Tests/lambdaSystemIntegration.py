#!/usr/bin/python

import mock
import sys
sys.path.append('..')
import holder
import unittest
from json_generators import *


def dummy_newObjectLogic(message):
    pass

def dummy_emergencyLogic(message):
    pass


class TestLambdaHandlerIntegration(unittest.TestCase):
    #this mock object just used to check that it reached this stage
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    def test_multipleInsertRecords(self, NOL):
        event1 = generate_lambda("", "sensors", "INSERT") 
        event2 = generate_lambda("", "sensors", "INSERT") 
        records = {}
        records['Records'] = [event1['Records'][0], event2['Records'][0]]
        holder.lambda_handler(records, 0)

        self.assertEquals(NOL.call_count, 2)

    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    def test_multipleModifyRecords(self, CE, EL):
        event1 = generate_lambda("101", "sensors", "MODIFY", "40") 
        event1['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'temperature'
        event1['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'temperature'
        event2 = generate_lambda("101", "sensors", "MODIFY", "40") 
        event2['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'temperature'
        event2['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'temperature'
        records = {}
        records['Records'] = [event1['Records'][0], event2['Records'][0]]
        holder.lambda_handler(records, 0)

        self.assertEquals(EL.call_count, 2)
        
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    def test_insertAndModifyRecords(self, CE, EL, NOL):
        event1 = generate_lambda("", "sensors", "INSERT") 
        event2 = generate_lambda("101", "sensors", "MODIFY", "40") 
        event2['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'temperature'
        event2['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'temperature'
        records = {}
        records['Records'] = [event1['Records'][0], event2['Records'][0]]
        holder.lambda_handler(records, 0)

        self.assertEquals(EL.call_count, 1)
        self.assertEquals(NOL.call_count, 1)


    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_modifyUser(self, EL, NOL):
        event = generate_lambda("", "users", "INSERT")
        event['Records'][0]['eventName'] = 'MODIFY'

        holder.lambda_handler(event, 0)

        self.assertFalse(EL.called)
        self.assertFalse(NOL.called)


    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_modifyRobot(self, EL, NOL):
        event = generate_lambda("", "robots", "INSERT")
        event['Records'][0]['eventName'] = 'MODIFY'

        holder.lambda_handler(event, 0)

        self.assertFalse(EL.called)
        self.assertFalse(NOL.called)



suite = unittest.TestLoader().loadTestsFromTestCase(TestLambdaHandlerIntegration)
unittest.TextTestRunner(verbosity=2).run(suite)
