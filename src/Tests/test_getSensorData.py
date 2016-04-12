"""
This is the automatic test for function getSensorData(sensor_type, buildingId, room).
Chang Sun, 4/11/2016
"""

import http.client
import json
import unittest
from getSensorData import *

# ________________________________________________________________

NUM_SENSORS_OF_BUILDING = [9, 4]
NUM_BUILDINGS = len(NUM_SENSORS_OF_BUILDING)

SENSOR_TYPES = ['IR', 'Sonar']
NUM_SENSOR_TYPES = len(SENSOR_TYPES)

NUM_ROOMS_OF_BUILDING = [3, 2]

# ________________________________________________________________

conn = http.client.HTTPConnection('localhost:8080')
buildingIds = []
sensorIds = {}

# ________________________________________________________________

def createObjects():

    def deleteAllBuildings():
        conn.request('DELETE', '/api/buildings/', headers={})
        conn.getresponse()

    def postAndGetBuildingId():
        conn.request('POST', '/api/buildings/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        return data['id']

    def deleteAllSensorsOfBuilding(x):
        conn.request('DELETE', '/api/buildings/' + buildingIds[x] + '/sensors/', headers={})
        conn.getresponse()

    def postAndGetSensorIdOfBuilding(x):
        # create sensors for building 1
        sensorIdsOfBuildingX = []
        for i in range(NUM_SENSORS_OF_BUILDING[x]):
            conn.request('POST', '/api/buildings/' + buildingIds[x] + '/sensors/', headers={})
            data = json.loads(conn.getresponse().read().decode('utf-8'))
            sensorIdsOfBuildingX.append(data['id'])
        return sensorIdsOfBuildingX

    def putSensorForBuilding(x):
        for i in range(NUM_SENSORS_OF_BUILDING[x]):
            data = {
                'type' : SENSOR_TYPES[i % NUM_SENSOR_TYPES],
                'room' : int(i / int(NUM_SENSORS_OF_BUILDING[x] / NUM_ROOMS_OF_BUILDING[x])),
                'data' : sensorIds[buildingIds[x]][i]
            }
            payload = json.dumps(data)
            conn.request('PUT', '/api/sensors/' + sensorIds[buildingIds[x]][i],
                         payload, {'content-type': 'application/json'})
            print(conn.getresponse().read().decode('utf-8'))

    deleteAllBuildings()
    print('All buildings deleted.')

    for i in range(NUM_BUILDINGS):
        buildingIds.append(postAndGetBuildingId())
        print('Created building%d with id=%s' % (i, buildingIds[i]))
        deleteAllSensorsOfBuilding(i)
        print('All sensors for building%d deleted.' % (i))
        sensorIds[buildingIds[i]] = postAndGetSensorIdOfBuilding(i)
        print('Created sensors for building%d, ids=%s' % (i, sensorIds[buildingIds[i]]))
        putSensorForBuilding(i)

# ________________________________________________________________

class TestGetSensorData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetSensorData, self).__init__(*args, **kwargs)
        createObjects()

    def test(self):
        # building 0
        # room0
        sensorData_IR_room0 = getSensorData('IR', buildingIds[0], 0)
        self.assertEqual(sensorData_IR_room0,
                         {x : x for x in [sensorIds[buildingIds[0]][0], sensorIds[buildingIds[0]][2]]})
        sensorData_Sonar_room0 = getSensorData('Sonar', buildingIds[0], 0)
        self.assertEqual(sensorData_Sonar_room0,
                         {x : x for x in [sensorIds[buildingIds[0]][1]]})
        # room1
        sensorData_IR_room1 = getSensorData('IR', buildingIds[0], 1)
        self.assertEqual(sensorData_IR_room1,
                         {x : x for x in [sensorIds[buildingIds[0]][4]]})
        sensorData_Sonar_room1 = getSensorData('Sonar', buildingIds[0], 1)
        self.assertEqual(sensorData_Sonar_room1,
                         {x : x for x in [sensorIds[buildingIds[0]][3], sensorIds[buildingIds[0]][5]]})
        # room2
        sensorData_IR_room2 = getSensorData('IR', buildingIds[0], 2)
        self.assertEqual(sensorData_IR_room2,
                         {x : x for x in [sensorIds[buildingIds[0]][6], sensorIds[buildingIds[0]][8]]})
        sensorData_Sonar_room2 = getSensorData('Sonar', buildingIds[0], 2)
        self.assertEqual(sensorData_Sonar_room2,
                         {x : x for x in [sensorIds[buildingIds[0]][7]]})

        # building 1
        # room0
        sensorData_IR_room0 = getSensorData('IR', buildingIds[1], 0)
        self.assertEqual(sensorData_IR_room0,
                         {x : x for x in [sensorIds[buildingIds[1]][0]]})
        sensorData_Sonar_room0 = getSensorData('Sonar', buildingIds[1], 0)
        self.assertEqual(sensorData_Sonar_room0,
                         {x : x for x in [sensorIds[buildingIds[1]][1]]})
        # room1
        sensorData_IR_room1 = getSensorData('IR', buildingIds[1], 1)
        self.assertEqual(sensorData_IR_room1,
                         {x : x for x in [sensorIds[buildingIds[1]][2]]})
        sensorData_Sonar_room1 = getSensorData('Sonar', buildingIds[1], 1)
        self.assertEqual(sensorData_Sonar_room1,
                         {x : x for x in [sensorIds[buildingIds[1]][3]]})

# ________________________________________________________________

if __name__ == '__main__':
    unittest.main()
# ________________________________________________________________
