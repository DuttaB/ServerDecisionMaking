"""
Implements the function getSensorsAtLocation(buildingId, room, floor, x, y)
Chang Sun, 4/18/2016
"""

import httplib
import json

# ________________________________________________________________

def getSensorsAtLocation(buildingId, room, floor, x, y):
    """
    Queries the database for sensor objects.
    Parameters:
        buildingId -- /string/, uuid of the building for the sensor
        room -- /int/, room number of the sensor
        floor -- /int/, floor of the sensor
        x -- /int/, x position value
        y -- /int/, y position value
    Returns:
        List of sensor objects where each object is a dict of the form:
        {
            "id": string,
            "buildingId": string,
            "robotId": string, (optional)
            "floor": int,
            "room": int,
            "xpos": int,"ypos": int,
            "data": string,
            "newData": string,
            "oldData", string
            "model": string,
            "type": string
        }
        Returns an empty list if no sensors exist in that location.
        Returns None if any error occurs.
    """
    try:
        conn = httplib.HTTPConnection('localhost:8080')
        conn.request('GET', '/api/buildings/' + buildingId + '/sensors/', headers={})
        allSensors = json.loads(conn.getresponse().read().decode('utf-8'))
        sensors = []
        for sensor in allSensors:
            if sensor['room'] == room and sensor['floor'] == floor \
                    and sensor['x'] == x and sensor['y'] == y:
                sensors.append(sensor)
        return sensors
    except Exception as e:
        print('Error: ', e)
    return None

# ________________________________________________________________
