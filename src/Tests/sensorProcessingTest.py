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
        self.assertEquals('fire', emergency)

    def test_createNewFireHighHeat(self):
        self.sensor['id'] = 'temp'
        self.sensor['type'] = 'temperature'
        self.sensor['newData'] = '101'
        self.sensor['oldData'] = dummy.getSensorData('temperature',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency)

    def test_createNewFireSmokeChange(self):
        self.sensor['id'] = 'smoke'
        self.sensor['type'] = 'smoke'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('smoke',\
                self.sensor['buildingId'], self.sensor['room'])
        dummy.shiftHistory('temp', '60')
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency)

    def test_noFireSmoke(self):
        self.sensor['id'] = 'smoke'
        self.sensor['type'] = 'smoke'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('smoke',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_gasLeak(self):
        self.sensor['id'] = 'gas'
        self.sensor['type'] = 'gas'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('gas',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('gas leak', emergency)

    def test_noGasLeak(self):
        dummy.shiftHistory('gas', '0')
        self.sensor['id'] = 'gas'
        self.sensor['type'] = 'gas'
        self.sensor['newData'] = '0'
        self.sensor['oldData'] = dummy.getSensorData('gas',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_waterLeakLow(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '10'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('water leak', emergency)

    def test_waterLeakHigh(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '80'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('water leak', emergency)

    def test_waterNormal(self):
        self.sensor['id'] = 'water pressure'
        self.sensor['type'] = 'water pressure'
        self.sensor['newData'] = '45'
        self.sensor['oldData'] = dummy.getSensorData('water pressure',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_lowWeightNoIntruder(self):
        self.sensor['id'] = 'weight'
        self.sensor['type'] = 'weight'
        self.sensor['newData'] = '44'
        self.sensor['oldData'] = dummy.getSensorData('weight',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_highWeightNoIntruder(self):
        dummy.addUser('user1')
        self.sensor['id'] = 'weight'
        self.sensor['type'] = 'weight'
        self.sensor['newData'] = '80'
        self.sensor['oldData'] = dummy.getSensorData('weight',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorClosed(self):
        dummy.shiftHistory('door','1')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '0'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenNoIntruder(self):
        dummy.addUser('user1')
        dummy.shiftHistory('weight','80')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenNoIntruderChild(self):
        dummy.shiftHistory('weight','40')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        self.assertIsNone(self.process.processNewSensorData(self.sensor))

    def test_doorOpenIntruder(self):
        dummy.shiftHistory('weight','80')
        self.sensor['id'] = 'door'
        self.sensor['type'] = 'door'
        self.sensor['newData'] = '1'
        self.sensor['oldData'] = dummy.getSensorData('door',\
                self.sensor['buildingId'], self.sensor['room'])
        emergency = self.process.processNewSensorData(self.sensor)
        self.assertIsNotNone(emergency)
        self.assertEquals('intruder', emergency)


if __name__ == '__main__':
    unittest.main()





