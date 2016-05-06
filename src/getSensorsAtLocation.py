"""
Implements the function getSensorsAtLocation(buildingId, room, floor, x, y)
Chang Sun, 4/18/2016
Bishwajit Dutta 5/2/2016 - Modified and Enhanced
"""

import httplib
import json
from connectTOnetwork import *

INVALID_SENSOR_LOC_INPUTS_ERROR_CODE = 99998

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
        Returns Error Code if any error occurs.
    """
    try:
        #input parameer check
        if buildingId < 0 or room < 0 or floor < 0 or x < 0 or y < 0:
            return INVALID_SENSOR_LOC_INPUTS_ERROR_CODE
        conn = connectTOnetwork()
        conn.request('GET', '/api/buildings/' + buildingId + '/sensors/', headers={})
        allSensors = json.loads(conn.getresponse().read().decode('utf-8'))
        sensors = []
        for sensor in allSensors:
            if sensor['room'] == room and sensor['floor'] == floor \
                    and sensor['xpos'] == x and sensor['ypos'] == y:
                sensors.append(sensor)
        return sensors
    except Exception as e:
        return e
    return None

# ________________________________________________________________
