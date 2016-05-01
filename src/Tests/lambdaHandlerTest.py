#!/usr/bin/python

import mock
import sys
sys.path.append('..')
import holder
import unittest
from json_generators import *


def dummy_parseSensor(old, new, eventName):
    pass

def dummy_parseUser(old, new, eventName):
    pass

def dummy_parseRobot(old, new, eventName):
    pass

def dummy_emergencyLogic(message):
    pass

def dummy_newObjectLogic(message):
    pass

def dummy_processUserMessage(message):
    pass

class TestLambdaHandlerUnit(unittest.TestCase):
    @mock.patch('holder.parseSensor', return_value=None)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertSensorNoEmergency(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "sensors", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertTrue(PS.called)
        self.assertFalse(EL.called)
        self.assertFalse(PU.called)
        self.assertFalse(PR.called)
        self.assertFalse(NOL.called)
        self.assertFalse(PUM.called)

    @mock.patch('holder.parseSensor', return_value={"from":"new sensor", "id": "1", "buildingId":"0", "model":"model1", "type": "temperature"})
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertSensorNotify(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "sensors", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertTrue(PS.called)
        self.assertFalse(EL.called)
        self.assertFalse(PU.called)
        self.assertFalse(PR.called)
        self.assertTrue(NOL.called)
        self.assertFalse(PUM.called)


    @mock.patch('holder.parseSensor', side_effect=dummy_parseSensor)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', return_value=None)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertUserNoEmergency(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "users", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertFalse(PS.called)
        self.assertFalse(EL.called)
        self.assertTrue(PU.called)
        self.assertFalse(PR.called)
        self.assertFalse(NOL.called)
        self.assertFalse(PUM.called)

    @mock.patch('holder.parseUser', return_value={"from":"new user", "id": "1", "buildingId":"0", "room":1,"xpos":2, "ypos":3, "floor":4,"owner":1})
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseSensor', side_effect=dummy_parseSensor)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertUserNotify(self, PUM, NOL, PR, PS, EL, PU):
        event = generate_lambda("", "users", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertFalse(PS.called)
        self.assertFalse(EL.called)
        self.assertTrue(PU.called)
        self.assertFalse(PR.called)
        self.assertTrue(NOL.called)
        self.assertFalse(PUM.called)

    @mock.patch('holder.parseSensor', side_effect=dummy_parseSensor)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', return_value=None)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertRobotNoEmergency(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "robots", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertFalse(PS.called)
        self.assertFalse(EL.called)
        self.assertFalse(PU.called)
        self.assertTrue(PR.called)
        self.assertFalse(NOL.called)
        self.assertFalse(PUM.called)

    @mock.patch('holder.parseSensor', side_effect=dummy_parseSensor)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', return_value={"from":"new robot", "id": "1", "buildingId":"0", "room":0, "xpos":1, "ypos":2, "floor":3, "movement":"air" })
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_insertRobotNotify(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "robots", "INSERT") 
        holder.lambda_handler(event, 0)
        
        self.assertFalse(PS.called)
        self.assertFalse(EL.called)
        self.assertFalse(PU.called)
        self.assertTrue(PR.called)
        self.assertTrue(NOL.called)
        self.assertFalse(PUM.called)


    @mock.patch('holder.parseSensor', return_value=None)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_modifySensorNoEmergency(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "sensors", "MODIFY") 
        holder.lambda_handler(event, 0)
        
        self.assertTrue(PS.called)
        self.assertFalse(EL.called)
        self.assertFalse(PU.called)
        self.assertFalse(PR.called)
        self.assertFalse(NOL.called)
        self.assertFalse(PUM.called)
    
    @mock.patch('holder.parseSensor', return_value={"type":"fire","id":"1","buildingId":"0", "room": 0,"floor":1,"xpos":2,"ypos":3,"from":"sensor", "oldData":"50","newData":"101"})
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    @mock.patch('holder.parseUser', side_effect=dummy_parseUser)
    @mock.patch('holder.parseRobot', side_effect=dummy_parseRobot)
    @mock.patch('holder.newObjectLogic', side_effect=dummy_newObjectLogic)
    @mock.patch('holder.processUserMessage', side_effect=dummy_processUserMessage)
    def test_modifySensorFire(self, PUM, NOL, PR, PU, EL, PS):
        event = generate_lambda("", "sensors", "MODIFY") 
        holder.lambda_handler(event, 0)
        
        self.assertTrue(PS.called)
        self.assertTrue(EL.called)
        self.assertFalse(PU.called)
        self.assertFalse(PR.called)
        self.assertFalse(NOL.called)
        self.assertFalse(PUM.called)





suite = unittest.TestLoader().loadTestsFromTestCase(TestLambdaHandlerUnit)
unittest.TextTestRunner(verbosity=2).run(suite)
