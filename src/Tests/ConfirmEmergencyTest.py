import http.client
import json
import unittest
import sys
sys.path.append('..')
from confirmEmergency import confirmEmergency
from getSensorData import *



conn=http.client.HTTPConnection('localhost:8080')

class testConfirmEmergency(unittest.TestCase):
    sensor={}
    sensorIds = []
    building_id='0'
    def setUp(self):
        global building_id
        global sensorIds
        sensorIds=[]
        #Delete all buildings
        conn.request('DELETE', '/api/buildings/', headers={})
        conn.getresponse()
        #delete all sensors
        conn.request('DELETE', '/api/sensors/', headers={})
        conn.getresponse()
        #create one building and get its id
        conn.request('POST', '/api/buildings/', headers={})
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        building_id=data['id']
        print('building id created=%s' %building_id)

        
        #create 12 sensors in the given building
        for i in range(1,13):
            conn.request('POST', '/api/buildings/' + building_id + '/sensors/', headers={})
            data = json.loads(conn.getresponse().read().decode('utf-8'))
            sensorIds.append(data['id'])
         
        #3 temperature, 3 smoke, 2 gas and 2 water pressure sensors   
        for i in range(1,13):
            if i>=1 and i<4:
                data = {
                #'type' : 'temperature',
                'type' : 'temperature',
                'room' : 1,
                'data' : '60'
                }
            elif i>=4 and i<7:
                 data = {
                'type' : 'smoke',
                'room' : 1,
                'data' : '1'
                }
            elif i>=7 and i<10:
                data = {
                'type' : 'gas',
                'room' : 1,
                'data' : '1'
                }
            else:
                data = {
                'type' : 'water pressure',
                'room' : 1,
                'data' : '70'
                }
            payload = json.dumps(data)
            conn.request('PUT', '/api/sensors/' + sensorIds[i-1],
                         payload, {'content-type': 'application/json'})

            conn.getresponse()
            #print(conn.getresponse().read().decode('utf-8'))
            self.sensor['id'] = 'id'
            self.sensor['buildingId'] = 'bid'
            self.sensor['room'] = 1
            self.sensor['data'] = 'data'
            self.sensor['type'] = 'type'
            
	   
	#first, all 3 temperature sensors have temperature 60 and smoke sensors are true so should return true
    #after than, 2 temperature sensors are changed to temperature 45, so, should return false       
    def test_confirmFireEvent(self):
        global sensorIds
        self.sensor['id'] = sensorIds[0]
        self.sensor['buildingId']=building_id
        self.sensor['room']='1'
        self.sensor['type'] = 'temperature'
        self.assertEqual(True,confirmEmergency('fire',self.sensor), "False Fire Emergency")
	    
        for i in range(2,4):
            data = {
            'type' : 'temperature',
            'room' : 1,
            'data' : '45'
            }
            payload = json.dumps(data)
            conn.request('PUT', '/api/sensors/' + sensorIds[i-1],
                         payload, {'content-type': 'application/json'})
            
            conn.getresponse()
            #print(conn.getresponse().read().decode('utf-8')) 
	        
        self.assertEqual(False,confirmEmergency('fire',self.sensor), "False Fire Emergency")
        sensorIds=[]
    #print('finished running test cases')'''

    #first, all 3 gas sensors are 1, so returns true
    #later, 2 gas sensors are changed to 0, so returns false
    def test_gasLeakEvent(self):
        global sensorIds
        self.sensor['id'] = sensorIds[6]
        self.sensor['buildingId']=building_id
        self.sensor['room']='1'
        self.sensor['type'] = 'gas'
        self.assertEqual(True,confirmEmergency('gas leak',self.sensor), "False Gas Leak Emergency")
        data = {
        'type' : 'gas',
        'room' : 1,
        'data' : '0'
        }
        payload = json.dumps(data)
        conn.request('PUT', '/api/sensors/' + sensorIds[8],
                      payload, {'content-type': 'application/json'})
         
        conn.getresponse()   
        #print(conn.getresponse().read().decode('utf-8')) 
        self.assertEqual(True,confirmEmergency('gas leak',self.sensor), "False Gas Leak Emergency")

        conn.request('PUT', '/api/sensors/' + sensorIds[7],
                      payload, {'content-type': 'application/json'})

        conn.getresponse()
        #print(conn.getresponse().read().decode('utf-8')) 
        self.assertEqual(False,confirmEmergency('gas leak',self.sensor), "False Gas Leak Emergency")
        sensorIds=[]

    #first, all 3 water pressure sensors are 70, so return true
    #later, 2 are changed to 45, so returns false
    def test_waterLeakEvent(self):
        global sensorIds
        self.sensor['id'] = sensorIds[9]
        self.sensor['buildingId']=building_id
        self.sensor['room']='1'
        self.sensor['type'] = 'water pressure'
        self.assertEqual(True,confirmEmergency('water leak',self.sensor), "False Water Leak Emergency")
        data = {
        'type' : 'water pressure',
        'room' : 1,
        'data' : '45'
        }
        payload = json.dumps(data)
        conn.request('PUT', '/api/sensors/' + sensorIds[11],
                      payload, {'content-type': 'application/json'})
         
        conn.getresponse()   
        #print(conn.getresponse().read().decode('utf-8')) 
        self.assertEqual(True,confirmEmergency('water leak',self.sensor), "False Water Leak Emergency")

        conn.request('PUT', '/api/sensors/' + sensorIds[10],
                      payload, {'content-type': 'application/json'})

        conn.getresponse()
        #print(conn.getresponse().read().decode('utf-8')) 
        self.assertEqual(False,confirmEmergency('water leak',self.sensor), "False water Leak Emergency")
        sensorIds=[]

    def test_intruderEvent(self):
        global sensorIds
        self.sensor['buildingId']=building_id
        self.sensor['room']='1'
        self.sensor['floor']='2'
        self.sensor['xpos']=2
        self.sensor['ypos']=3
        self.assertEqual(True,confirmEmergency('intruder',self.sensor), "False Intruder Emergency")


if __name__ == '__main__':
    unittest.main()	

