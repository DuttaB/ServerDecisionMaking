import unittest
import sensorProcessing as process


def getSensorHistory(sensorID):
    '''
    Dummy function to return static sensor history until we have an actual 
    function ready to go.
    '''
    if sensorID == 'temp':
        return [21,20,21,22,21,20,19,18,19,20]
    if sensorID == 'smoke':
        return [0,1,0,1,0]
    if sensorID == 'gas':
        return [0,1,0]
    if sensorID == 'water pressure':
        return [41,44,46,45,47,45,42,40,42]
    if sensorID == 'door':
        return [0,1,0,1,0,1,0,1,0,1, 0]
    if sensorID == 'weight':
        return [0, 80, 0, 20, 85, 0, 15, 0]
    if sensorID == 'none':
        return []
    if sensorID == 'medhightemp':
        return [51]
    if sensorID == 'hightemp':
        return [101]
    if sensorID == 'yessmoke':
        return [1]
    if sensorID == 'yesgas':
        return [1]
    if sensorID == 'lowwater':
        return [20]
    if sensorID == 'highwater':
        return [70]
    if sensorID == 'opendoor':
        return [1]
    if sensorID == 'closedoor':
        return [0]
    if sensorID == 'heavyweight':
        return [100]
    if sensorID == 'lightweight':
        return [10]
    if sensorID == 'noweight':
        return [0]
    #if none of these sensors, just return generic list
    return [9,8,7,6,5,4,3,2,1,0]

def shiftHistory(sensorID, newData):
    '''
    Dummy function that doesn't do anything because we don't really care
    '''
    pass

class TestSensorProcessing(unittest.TestCase):
    def test_createNewDataNoHistory(self):
        self.assertEquals(None, process.processNewSensorData('none', 'none', 0))

    def test_createNewFireEvent(self):
        emergency = process.processNewSensorData('temp', 'temperature', 100)
        self.assertIsNotNone(emergency)


if __name__ == '__main__':
    unittest.main()
