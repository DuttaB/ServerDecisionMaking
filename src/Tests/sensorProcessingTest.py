import unittest
import collections
import sys
sys.path.append('..')
from sensorProcessing import sensorProcessing
import sensorProcessingDummyFunctions as dummy


class TestSensorProcessing(unittest.TestCase):
    #The base sensor object
    sensor = {}
    process = sensorProcessing(dummy)
    def setUp(self):
        self.sensor['id'] = 'id'
        self.sensor['buildingId'] = 'bid'
        self.sensor['robotId'] = 'robotId'
        self.sensor['floor'] = 0
        self.sensor['room'] = 1
        self.sensor['xpos'] = 3
        self.sensor['ypos'] = 4
        self.sensor['data'] = 'data'
        self.sensor['model'] = 'model'
        self.sensor['type'] = 'type'
        self.sensor['newData'] = ''
        self.sensor['oldData'] = ''
        dummy.setUpLists()


    def test_createNewDataNoHistory(self):
        self.sensor['id'] = 'none'
        self.sensor['type'] = 'none'
        self.sensor['newData'] = '0'
        self.assertEquals(None, self.process.processNewSensorData(self.sensor))

    def test_createNewFireEventLowHeat(self):
        self.sensor['id'] = 'temp'
        self.sensor['type'] = 'temperature'
        self.sensor['newData'] = '60'
        self.sensor['oldData'] = dummy.getSensorData('temperature',\
                self.sensor['buildingId'], self.sensor['room'])
        dummy.shiftHistory('smoke', '1')
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)

    def test_createNewFireHighHeat(self):
        sensor['id'] = 'temp'
        sensor['type'] = 'temperature'
        sensor['newData'] = '101'
        sensor['oldData'] = tempArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)

    def test_createNewFireSmokeChange(self):
        tempArr.insert(0,'60')
        sensor['id'] = 'smoke'
        sensor['type'] = 'smoke'
        sensor['newData'] = '1'
        sensor['oldData'] = smokeArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)
        
    def test_noFireSmoke(self):
        sensor['id'] = 'smoke'
        sensor['type'] = 'smoke'
        sensor['newData'] = '1'
        sensor['oldData'] = smokeArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_gasLeak(self):
        sensor['id'] = 'gas'
        sensor['type'] = 'gas'
        sensor['newData'] = '1'
        sensor['oldData'] = gasArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)

    def test_noGasLeak(self):
        tempArr.insert(0,'1')
        sensor['id'] = 'gas'
        sensor['type'] = 'gas'
        sensor['newData'] = '0'
        sensor['oldData'] = gasArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_waterLeakLow(self):
        sensor['id'] = 'water pressure'
        sensor['type'] = 'water pressure'
        sensor['newData'] = '10'
        sensor['oldData'] = waterArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)

    def test_waterLeakHigh(self):
        sensor['id'] = 'water pressure'
        sensor['type'] = 'water pressure'
        sensor['newData'] = '80'
        sensor['oldData'] = waterArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)

    def test_waterNormal(self):
        sensor['id'] = 'water pressure'
        sensor['type'] = 'water pressure'
        sensor['newData'] = '45'
        sensor['oldData'] = waterArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_lowWeightNoIntruder(self):
        sensor['id'] = 'weight'
        sensor['type'] = 'weight'
        sensor['newData'] = '44'
        sensor['oldData'] = weightArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_highWeightNoIntruder(self):
        userList.insert(0,'user1')
        sensor['id'] = 'weight'
        sensor['type'] = 'weight'
        sensor['newData'] = '80'
        sensor['oldData'] = weightArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_doorClosed(self):
        doorArr.insert(0,'1')
        sensor['id'] = 'door'
        sensor['type'] = 'door'
        sensor['newData'] = '0'
        sensor['oldData'] = doorArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_doorOpenNoIntruder(self):
        userList.insert(0,'user1')
        weightArr.insert(0,80)
        sensor['id'] = 'door'
        sensor['type'] = 'door'
        sensor['newData'] = '1'
        sensor['oldData'] = doorArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_doorOpenNoIntruderChild(self):
        weightArr.insert(0,40)
        sensor['id'] = 'door'
        sensor['type'] = 'door'
        sensor['newData'] = '1'
        sensor['oldData'] = doorArr[0]
        self.assertIsNone(process.processNewSensorData(sensor))

    def test_doorOpenIntruder(self):
        weightArr.insert(0,80)
        sensor['id'] = 'door'
        sensor['type'] = 'door'
        sensor['newData'] = '1'
        sensor['oldData'] = doorArr[0]
        emergency = process.processNewSensorData(sensor)
        self.assertIsNotNone(emergency)


if __name__ == '__main__':
    unittest.main()





