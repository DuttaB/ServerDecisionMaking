"""
Implements the function getUsersInRoom(buildingId, room)
Chang Sun, 4/18/2016
"""

import httplib
import json

# ________________________________________________________________

def getUsersInRoom(buildingId, room):
    """
    Queries the database for user objects.
    Parameters:
        buildingId -- /string/, uuid of the building for the sensor
        room -- /int/, room number of the user
    Returns:
        List of all of the users in a particular building's room
        where each user object is a doct of the form:
        {
            "id": string,
            "buildingId": string,
            "floor": int,
            "room": int,
            "xpos": int,
            "ypos": int,
            "message": string,
            "owner": bool
        }
        Returns an empty list if no users exist in that room.
        Returns None if any error occurs.
    """
    try:
        conn = httplib.HTTPConnection('localhost:8080')
        conn.request('GET', '/api/users/', headers={})
        allUsers = json.loads(conn.getresponse().read().decode('utf-8'))
        users = []
        for user in allUsers:
            if user['buildingId'] == buildingId and user['room'] == room:
                users.append(user)
        return users
    except Exception as e:
        print('Error: ', e)
    return None

# ________________________________________________________________
