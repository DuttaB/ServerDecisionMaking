"""
This is the automatic test for function getSensorsAtLocation(buildingId, room, floor, x, y).
Chang Sun, 4/18/2016
"""

import httplib
import json
import unittest
import time
from getSensorsAtLocation import *

# ________________________________________________________________


NUM_BUILDINGS = 2
NUM_ROOMS = 2
NUM_FLOORS = 2
NUM_XS = 2
NUM_YS = 2
MAX_PERMUTATION = 1
NUM_SENSORS_OF_BUILDING = [NUM_ROOMS * NUM_FLOORS * NUM_XS * NUM_YS*MAX_PERMUTATION
                           for x in range(NUM_BUILDINGS)]

# ________________________________________________________________

conn = httplib.HTTPConnection('localhost:8080')
buildingIds = []
sensorIds = {}
sensorObjs = {}

# ________________________________________________________________

def createObjects():

    def deleteAllBuildings():
        conn.request('DELETE', '/api/buildings/', headers={})
        conn.getresponse()

    def postAndGetBuildingId():
        conn.request('POST', '/api/buildings/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        return data['id']

    def postAndGetSensorIdOfBuilding(x):
        # create sensors for building 1
        sensorIdsOfBuildingX = []
        for i in range(NUM_SENSORS_OF_BUILDING[x]):
            conn.request('POST', '/api/buildings/' + buildingIds[x] + '/sensors/', headers={})
            data = json.loads(conn.getresponse().read().decode('utf-8'))
            time.sleep(0.1)
            sensorIdsOfBuildingX.append(data['id'])
        return sensorIdsOfBuildingX

    def putSensorForBuilding(x):
        sensorObjs[buildingIds[x]] = {}
        iter = 0
        counter = MAX_PERMUTATION - 1
        for room in range(NUM_ROOMS):
            for floor in range(NUM_FLOORS):
                for x_pos in range(NUM_XS):
                    for y_pos in range(NUM_YS):
                        counter = (counter + 1) % MAX_PERMUTATION + 1
                        sensorObjs[buildingIds[x]][(room, floor, x_pos, y_pos)] = []
                        for num in range(counter):
                            data = {
                                'room': room,
                                'floor': floor,
                                'xpos': x_pos,
                                'ypos': y_pos
                            }
                            payload = json.dumps(data)
                            conn.request('PUT', '/api/sensors/' + sensorIds[buildingIds[x]][iter],
                                         payload, {'content-type': 'application/json'})
                            print(conn.getresponse().read().decode('utf-8'))
                            time.sleep(0.1)
                            conn.request('GET', '/api/sensors/' + sensorIds[buildingIds[x]][iter], headers={})
                            sensor = json.loads(conn.getresponse().read().decode('utf-8'))
                            time.sleep(0.1)
                            sensorObjs[buildingIds[x]][(room, floor, x_pos, y_pos)].append(sensor)
                            iter = iter + 1

    print('******Creating objects for test cases******')
    for i in range(NUM_BUILDINGS):
        buildingIds.append(postAndGetBuildingId())
        print('Created building%d with id=%s' % (i, buildingIds[i]))
        sensorIds[buildingIds[i]] = postAndGetSensorIdOfBuilding(i)
        print('Created sensors for building%d, ids=%s' % (i, sensorIds[buildingIds[i]]))
        putSensorForBuilding(i)
    print('******Finished creating objects for test cases******')

# ________________________________________________________________

class TestGetSensorsAtLocation(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetSensorsAtLocation, self).__init__(*args, **kwargs)
        createObjects()

    def test(self):
        print('******Running test cases******')
        for buildingId in buildingIds:
            for room in range(NUM_ROOMS):
                for floor in range(NUM_FLOORS):
                    for x_pos in range(NUM_XS):
                        for y_pos in range(NUM_YS):
                            sensors = getSensorsAtLocation(buildingId, room, floor, x_pos, y_pos)
                            compare = sensorObjs[buildingId][(room, floor, x_pos, y_pos)]
                            self.assertEqual(len(sensors), len(compare))
                            for sensor in sensors:
                                self.assertEqual(True, sensor in compare)
                        self.assertEqual([], getSensorsAtLocation(buildingId, room, floor, x_pos, NUM_YS))
                    self.assertEqual([], getSensorsAtLocation(buildingId, room, floor, NUM_XS, 0))
                self.assertEqual([], getSensorsAtLocation(buildingId, room, NUM_FLOORS, 0, 0))
            self.assertEqual([], getSensorsAtLocation(buildingId, NUM_ROOMS, 0, 0, 0))
        print('******Finished running test cases******')

# ________________________________________________________________

if __name__ == '__main__':
    unittest.main()
# ________________________________________________________________
