"""
This is the automatic test for function getUsersInRoom(buildingId, room).
Chang Sun, 4/18/2016
"""

import httplib
import json
import unittest
from getUsersInRoom import *

# ________________________________________________________________

NUM_USERS_OF_BUILDING = [6, 2]
NUM_BUILDINGS = len(NUM_USERS_OF_BUILDING)

NUM_ROOMS_OF_BUILDING = [2, 2]

# ________________________________________________________________

conn = httplib.HTTPConnection('localhost:8080')
buildingIds = []
userIds = {}
usersInBuilding = {}

# ________________________________________________________________

def createObjects():

    def deleteAllBuildings():
        conn.request('DELETE', '/api/buildings/', headers={})
        conn.getresponse()

    def postAndGetBuildingId():
        conn.request('POST', '/api/buildings/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        return data['id']

    def getUserPrototype():
        conn.request('POST', '/api/users/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        conn.request('DELETE', '/api/users/' + data['id'], headers={})
        conn.getresponse()
        return data

    def postAndGetUserIdsOfBuilding(x):
        # create users for building x
        userIdsOfBuildingX = []
        for i in range(NUM_USERS_OF_BUILDING[x]):
            conn.request('POST', '/api/users/', headers={})
            data = json.loads(conn.getresponse().read().decode('utf-8'))
            userIdsOfBuildingX.append(data['id'])
        return userIdsOfBuildingX

    def putUsersForBuilding(x):
        usersInBuilding[x] = {}
        for i in range(NUM_ROOMS_OF_BUILDING[x]):
            usersInBuilding[x][i] = []
        for i in range(NUM_USERS_OF_BUILDING[x]):
            room = i % NUM_ROOMS_OF_BUILDING[x]
            data = {
                'buildingId': buildingIds[x],
                'room': room
            }
            payload = json.dumps(data)
            conn.request('PUT', '/api/users/' + userIds[buildingIds[x]][i],
                         payload, {'content-type': 'application/json'})
            print(conn.getresponse().read().decode('utf-8'))
            conn.request('GET', '/api/users/' + userIds[buildingIds[x]][i], headers={})
            user = json.loads(conn.getresponse().read().decode('utf-8'))
            usersInBuilding[x][room].append(user)

    print('******Creating objects for test cases******')
    for i in range(NUM_BUILDINGS):
        buildingIds.append(postAndGetBuildingId())
        print('Created building%d with id=%s' % (i, buildingIds[i]))
        userIds[buildingIds[i]] = postAndGetUserIdsOfBuilding(i)
        print('Created users for building%d, ids=%s' % (i, userIds[buildingIds[i]]))
        putUsersForBuilding(i)
    print('******Finished creating objects for test cases******')

# ________________________________________________________________

class TestGetUsersInRoom(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetUsersInRoom, self).__init__(*args, **kwargs)
        createObjects()

    def test(self):
        print('******Running test cases******')
        for x in range(NUM_BUILDINGS):
            for room in range(NUM_ROOMS_OF_BUILDING[x]):
                users = getUsersInRoom(buildingIds[x], room)
                self.assertEqual(len(users), len(usersInBuilding[x][room]))
                for user in users:
                    self.assertEqual(True, user in usersInBuilding[x][room])
        print('******Finished running test cases******')

# ________________________________________________________________

if __name__ == '__main__':
    unittest.main()
# ________________________________________________________________
