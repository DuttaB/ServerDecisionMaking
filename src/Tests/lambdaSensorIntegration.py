#!/usr/bin/python

import mock
import sys
sys.path.append('..')
import holder
import unittest
from json_generators import *


def dummy_emergencyLogic(message):
    pass

class TestLambdaHandlerIntegration(unittest.TestCase):
    @mock.patch('holder.sensorProcessing.getSensorData', return_value="1")
    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processingHighTempFire(self, EL, CE, GSD):
        event = generate_lambda("101", "sensors", "MODIFY", "40") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'temperature'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'temperature'
        holder.lambda_handler(event, 0)

        self.assertFalse(GSD.called)
        self.assertTrue(EL.called)
    
    @mock.patch('holder.sensorProcessing.getSensorData', return_value=None)
    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processSmokeSensor(self, EL, CE, GSD):
        event = generate_lambda("1", "sensors", "MODIFY", "0") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'smoke'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'smoke'
        holder.lambda_handler(event, 0)

        self.assertFalse(GSD.called)
        self.assertFalse(EL.called)

    @mock.patch('holder.sensorProcessing.getSensors', return_value=None)
    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processDoorSensor(self, EL, CE, GSD):
        event = generate_lambda("1", "sensors", "MODIFY", "0") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'door'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'door'
        holder.lambda_handler(event, 0)

        self.assertFalse(GSD.called)
        self.assertFalse(EL.called)


    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processWaterSensor(self, EL, CE):
        event = generate_lambda("30", "sensors", "MODIFY", "50") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'water pressure'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'water pressure'
        holder.lambda_handler(event, 0)

        self.assertTrue(EL.called)

    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processWaterSensor2(self, EL, CE):
        event = generate_lambda("45", "sensors", "MODIFY", "50") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'water pressure'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'water pressure'
        holder.lambda_handler(event, 0)

        self.assertFalse(EL.called)


    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processGasSensor(self, EL, CE):
        event = generate_lambda("1", "sensors", "MODIFY", "0") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'gas'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'gas'
        holder.lambda_handler(event, 0)

        self.assertTrue(EL.called)

    @mock.patch('holder.sensorProcessing.checkEmergency', return_value=True)
    @mock.patch('holder.emergencyLogic', side_effect=dummy_emergencyLogic)
    def test_processGasSensor2(self, EL, CE):
        event = generate_lambda("0", "sensors", "MODIFY", "1") 
        event['Records'][0]['dynamodb']['NewImage']['type']['S'] = 'gas'
        event['Records'][0]['dynamodb']['OldImage']['type']['S'] = 'gas'
        holder.lambda_handler(event, 0)

        self.assertFalse(EL.called)


suite = unittest.TestLoader().loadTestsFromTestCase(TestLambdaHandlerIntegration)
unittest.TextTestRunner(verbosity=2).run(suite)
