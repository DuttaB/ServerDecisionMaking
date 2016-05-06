"""
Implements the function getSensorData(sensor_type, building, room)
Chang Sun, 4/12/2016
Bishwajit Dutta 5/2/2016 - Modified and Enhanced
"""

import httplib
import json
from connectTOnetwork import *

INVALID_SENSOR_INPUTS_ERROR_CODE = 99999

# ________________________________________________________________
      

def getSensorData(sensor_type, buildingId, room):
    """
    Queries the database for sensor data.
    Parameters:
        sensor_type -- /string/, 'type' field of sensor object
        buildingId -- /string/, uuid of the building for the sensor
        room -- /int/, room number of the sensor
    Returns:
        dict() of (key, value) pair where key=sensorId, value=data
        e.g.
            {
                '3d33d19e-2956-4520-bce6-2bcaba48b293' : '0xFF00',
                '243f7e81-6c21-4068-9c7d-b89963e3e38c' : '0x029A'
            }
        999 on input error
    """
    try:
        #input parameer check
        if sensor_type < 0 or buildingId < 0 or room < 0:
            return INVALID_SENSOR_INPUTS_ERROR_CODE
        conn = connectTOnetwork()
        conn.request('GET', '/api/buildings/' + buildingId + '/sensors/', headers={})
        sensors = json.loads(conn.getresponse().read().decode('utf-8'))
        sensorData = {}
        for sensor in sensors:
            if sensor['type'] == sensor_type and sensor['room'] == room:
                sensorData[sensor['id']] = sensor['data']
        return sensorData      
    except Exception as e:
        return e
    return None

# ________________________________________________________________
