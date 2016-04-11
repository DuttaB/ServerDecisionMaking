import unittest
import collections
import sys
sys.path.append('..')
import sensorProcessing as process

tempArr = [21,20,21,22,21,20,19,18,19,20]
smokeArr = [0,1,0,1,0]
gasArr = [0,1,0]
waterArr = [41,44,46,45,47,45,42,40,42]
doorArr = [0,1,0,1,0,1,0,1,0]
weightArr = [0,80, 0,20,85,0,15,0]
noneArr = []
medHighTempArr = [51]
highTempArr = [101]
yesSmokeArr = [1]
yesGasArr = [1]
lowWaterArr = [20]
highWaterArr = [70]
openDoorArr = [1]
closeDoorArr = [0]
heavyWeightArr = [100]
lightWeightArr = [10]
noWeightArr = [0]

# user list is the list of users for literally whatever we care about
# the test cases will set this up.  
# If we want a list of registered users in a room, fill this in
# If we want to check for intruders, this can be left empty
userList = []

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
    pos = Position(room=2, floor=1, x=20, y=10)
    return pos

class TestSensorProcessing(unittest.TestCase):
    def setUp(self):
        tempArr = [21,20,21,22,21,20,19,18,19,20]
        smokeArr = [0,1,0,1,0]
        gasArr = [0,1,0]
        waterArr = [41,44,46,45,47,45,42,40,42]
        doorArr = [0,1,0,1,0,1,0,1,0]
        weightArr = [0,80, 0,20,85,0,15,0]
        noneArr = []
        medHighTempArr = [51]
        highTempArr = [101]
        yesSmokeArr = [1]
        yesGasArr = [1]
        lowWaterArr = [20]
        highWaterArr = [70]
        openDoorArr = [1]
        closeDoorArr = [0]
        heavyWeightArr = [100]
        lightWeightArr = [10]
        noWeightArr = [0]
        userList = []
        

    def test_createNewDataNoHistory(self):
        self.assertEquals(None, process.processNewSensorData('none', 'none', 0))

    def test_createNewFireEventLowHeat(self):
        smokeArr.insert(0,1) #first elemenet set to 1, indicating smoke
        emergency = process.processNewSensorData('temp', 'temperature', 60)
        self.assertIsNotNone(emergency)

    def test_createNewFireHighHeat(self):
        emergency = process.processNewSensorData('temp', 'temperature', 101)
        self.assertIsNotNone(emergency)

    def test_createNewFireSmokeChange(self):
        tempArr.insert(0,60)
        emergency = process.processNewSensorData('smoke', 'smoke', 1)
        self.assertIsNotNone(emergency)
        
    def test_noFireSmoke(self):
        self.assertIsNone(process.processNewSensorData('smoke', 'smoke', 1))

    def test_gasLeak(self):
        emergency = process.processNewSensorData('gas', 'gas', 1)
        self.assertIsNotNone(emergency)

    def test_noGasLeak(self):
        self.assertIsNone(process.processNewSensorData('gas','gas',0))

    def test_waterLeakLow(self):
        emergency = process.processNewSensorData('water pressure', 'water pressure', 10)
        self.assertIsNotNone(emergency)

    def test_waterLeakHigh(self):
        emergency = process.processNewSensorData('water pressure', 'water pressure', 80)
        self.assertIsNotNone(emergency)

    def test_waterNormal(self):
        self.assertIsNone(process.processNewSensorData('water pressure', 'water pressure', 45))

    def test_lowWeightNoIntruder(self):
        self.assertIsNone(process.processNewSensorData('weight', 'weight', 44))

    def test_highWeightNoIntruder(self):
        userList.insert(0,'user1')
        self.assertIsNone(process.processNewSensorData('weight', 'weight', 80))

    def test_highWeightIntruder(self):
        emergency = process.processNewSensorData('weight', 'weight', 80)
        self.assertIsNotNone(emergency)

    def test_doorClosed(self):
        self.assertIsNone(process.processNewSensorData('door','door', 0))

    def test_doorOpenNoIntruder(self):
        userList.insert(0,'user1')
        weightArr.insert(0,80)
        self.assertIsNone(process.processNewSensorData('door', 'door', 1))

    def test_doorOpenNoIntruderChild(self):
        weightArr.insert(0,40)
        self.assertIsNone(process.processNewSensorData('door', 'door', 1))

    def test_doorOpenIntruder(self):
        weightArr.insert(0,80)
        emergency = process.processNewSensorData('door', 'door', 1)
        self.assertIsNotNone(emergency)

    def test_createEmergency(self):
        emergency = process.createEmergency('fire', 'fire', 10)
        #We know what the dummy values are so just check that they get returned
        self.assertIsNotNone(emergency)
        self.assertEquals('fire', emergency['msg type'])
        self.assertEquals(2, emergency['body']['room'])
        self.assertEquals(1, emergency['body']['floor'])
        self.assertEquals(20, emergency['body']['xpos'])
        self.assertEquals(10, emergency['body']['ypos'])
        self.assertEquals(10, emergency['body']['severity'])



if __name__ == '__main__':
    unittest.main()





