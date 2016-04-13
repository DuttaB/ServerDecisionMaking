import unittest
import collections
import sys
sys.path.append('..')
import sensorProcessing as process

tempArr = []
smokeArr = []
gasArr = []
waterArr = []
doorArr = []
weightArr = []
noneArr = []

# user list is the list of users for literally whatever we care about
# the test cases will set this up.  
# If we want a list of registered users in a room, fill this in
# If we want to check for intruders, this can be left empty
userList = []

#The base sensor object
sensor = {}

def getSensorHistory(sensorID):
    '''
    Dummy function to return static sensor history until we have an actual 
    function ready to go.
    '''
    if sensorID == 'temp':
        return tempArr
    if sensorID == 'smoke':
        return smokeArr
    if sensorID == 'gas':
        return gasArr
    if sensorID == 'water pressure':
        return waterArr
    if sensorID == 'door':
        return doorArr
    if sensorID == 'weight':
        return weightArr
    if sensorID == 'none':
        return noneArr
    if sensorID == 'medhightemp':
        return medHighTempArr
    if sensorID == 'hightemp':
        return highTempArr
    if sensorID == 'yessmoke':
        return yesSmokeArr
    if sensorID == 'yesgas':
        return yesGasArr
    if sensorID == 'lowwater':
        return lowWaterArr
    if sensorID == 'highwater':
        return highWaterArr
    if sensorID == 'opendoor':
        return openDoorArr
    if sensorID == 'closedoor':
        return closeDoorArr
    if sensorID == 'heavyweight':
        return heavyWeightArr
    if sensorID == 'lightweight':
        return lightWeightArr
    if sensorID == 'noweight':
        return noWeightArr
    #if none of these sensors, just return generic list
    return [9,8,7,6,5,4,3,2,1,0]

def shiftHistory(sensorID, newData):
    '''
    Dummy function that prepends newData onto a list denoted by the sensor ID
    '''
    if sensorID == 'temp':
        tempArr.insert(0,newData)
    if sensorID == 'smoke':
        smokeArr.insert(0, newData)
    if sensorID == 'gas':
        gasArr.insert(0,newData)
    if sensorID == 'water pressure':
        waterArr.insert(0,newData)
    if sensorID == 'door':
        doorArr.insert(0,newData)
    if sensorID == 'weight':
        weightArr.insert(0,newData)
    if sensorID == 'none':
        noneArr.insert(0,newData)
    if sensorID == 'medhightemp':
        medHighTempArr.insert(0,newData)
    if sensorID == 'hightemp':
        highTempArr.insert(0,newData)
    if sensorID == 'yessmoke':
        yesSmokeArr.insert(0,newData)
    if sensorID == 'yesgas':
        yesGasArr.insert(0,newData)
    if sensorID == 'lowwater':
        lowWaterArr.insert(0,newData)
    if sensorID == 'highwater':
        highWaterArr.insert(0,newData)
    if sensorID == 'opendoor':
        openDoorArr.insert(0,newData)
    if sensorID == 'closedoor':
        closeDoorArr.insert(0,newData)
    if sensorID == 'heavyweight':
        heavyWeightArr.insert(0,newData)
    if sensorID == 'lightweight':
        lightWeightArr.insert(0,newData)
    if sensorID == 'noweight':
        noWeightArr.insert(0,newData)


def getSmokeSensorsInRoom(room):
    '''
    Dummy function for getting the smoke sensors in a particular room.  
    Just return the 'smoke' ID
    '''
    return ['smoke']

def getWeightSensorAtPos(room, floor, x, y):
    '''
    Dummy function to get a weight sensor at a particular location.
    This can be used to check the weight sensor at a door that's been opened
    to check if there's an intruder or not.

    Returns the string of the ID or None if no weight sensor present
    '''
    return 'weight'

def getUsersInRoom(room):
    '''
    Get our dummy list of users that is initialized in each test
    '''
    return userList

def getPosition(sensorID):
    '''
    Returns a dummy position for the sensor.
    '''
    Position = collections.namedtuple('Position', 'room floor x y')
    pos = Position(room=sensor['room'], floor=sensor['floor'], x=sensor['xpos'], y=sensor['ypos'])
    return pos

class TestSensorProcessing(unittest.TestCase):
    def setUp(self):
        global tempArr
        global smokeArr
        global gasArr
        global waterArr
        global doorArr
        global weightArr
        global noneArr
        global userList
        global sensor
        tempArr = ['21','20','21','22','21','20','19','18','19','20']
        smokeArr = ['0','1','0','1','0']
        gasArr = ['0','1','0']
        waterArr = ['41','44','46','45','47','45','42','40','42']
        doorArr = ['0','1','0','1','0','1','0','1','0']
        weightArr = ['0','80','0','20','85','0','15','0']
        noneArr = []
        noWeightArr = ['0']
        userList = []
        sensor['id'] = 'id'
        sensor['buildingId'] = 'bid'
        sensor['robotId'] = 'robotId'
        sensor['floor'] = 0
        sensor['room'] = 1
        sensor['xpos'] = 3
        sensor['ypos'] = 4
        sensor['data'] = 'data'
        sensor['model'] = 'model'
        sensor['type'] = 'type'


    def test_createNewDataNoHistory(self):
        sensor['id'] = 'none'
        sensor['type'] = 'none'
        sensor['newData'] = '0'
        self.assertEquals(None, process.processNewSensorData(sensor))

    def test_createNewFireEventLowHeat(self):
        smokeArr.insert(0,'1') #first elemenet set to 1, indicating smoke
        sensor['id'] = 'temp'
        sensor['type'] = 'temperature'
        sensor['newData'] = '60'
        sensor['oldData'] = tempArr[0]
        emergency = process.processNewSensorData(sensor)
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





