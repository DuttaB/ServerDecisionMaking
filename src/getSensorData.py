"""
Implements the function getSensorData(sensor_type, building, room)
Chang Sun, 4/12/2016
"""

import http.client
import json

def getSensorData(sensor_type, buildingId, room):
    try:
        conn = http.client.HTTPConnection('localhost:8080')
        conn.request('GET', '/api/buildings/' + buildingId + '/sensors/', headers={})
        sensors = json.loads(conn.getresponse().read().decode('utf-8'))
        sensorData = {}
        for sensor in sensors:
            if sensor['type'] == sensor_type and sensor['room'] == room:
                sensorData[sensor['id']] = sensor['data']
        return sensorData
    except Exception as e:
        print('Error: ', e)
    return None
