# This import will change when we don't do dummy processing anymore
#import sensorProcessingTest as db
#import sensorProcessingTest as storage
#import sensorProcessingTest as checkEmergency


class sensorProcessing(object):
    def __init__(self, module=None):
        if not module:
            pass #will import other modules here to call functions
            #import getSensorData as storage 
        else:
            storage = module
            db = module
            checkEmergency = module
        self.storage = storage
        self.db = db
        self.checkEmergency = checkEmergency
        
    def processWeightSensor(self, sensor):
        '''
        Process Weight sensors by reading the sensor history and new incoming data 
        and determines if there's an emergency or not.
        The emergency this looks for is intruders (based on other sensors too,
        possibly)

        If a weight is < 45, it's asumed to be a child or robot.

        As of right now, weight sensor changes will never cause an emergency.
        The weight sensor will only be read when door sensors change.
        '''
        pass #for now

    def processTempSensor(self, sensor):
        '''
        Process the temperature sensor by reading history and determining if there 
        could be a fire.  A fire is determined if temp > 100.  If temp >50, temp 
        is only a fire if there's smoke.
        '''
        emergency = None
        if int(sensor['newData']) > 100:
            emergency = 'fire'
        elif int(sensor['newData']) > 50:
            smokeSensors = self.storage.getSensorData('smoke',\
                    sensor['buildingId'], sensor['room'])
            if smokeSensors is None:
                return None
            for val in smokeSensors.values():
                if val == '1':
                    emergency = 'fire'

        return emergency

    def processSmokeSensor(self, sensor):
        '''
        Process the smoke sensor by reading the temperature sensor history.
        If the smoke sensor, it could be a flaw.  Check the temperature history to
        judge as well.  Only fire if smoke is 1 and temp > 50
        '''
        emergency = None
        if sensor['newData'] == '1':
            tempSensors = self.storage.getSensorData('temperature',\
                    sensor['buildingId'], sensor['room'])
            if tempSensors is None:
                return None
            for val in tempSensors.values():
                if int(val) > 50:
                    emergency = 'fire'
        return emergency


    def processDoorSensor(self, sensor):
        '''
        Process the door sensor. Used for intruder detection.  
        '''
        emergency = None
        if sensor['newData'] == '1':
            #door sensor went off
            sensors = self.storage.getSensorsAtLocation(sensor['buildingId'],\
                    sensor['room'], sensor['floor'], sensor['xpos'],\
                    sensor['ypos'])
            assert sensors is not None, "sensors has to at least have a door sensor!"
            for sensor in sensors:
                if sensor['type'] == 'weight' and int(sensor['data']) > 80:
                    #weight sensor heavy
                    users = self.storage.getUsersInRoom(sensor['room'])
                    if users is None or not users:
                        emergency = 'intruder'
        return emergency

    def processGasSensor(self, sensor):
        '''
        If the new data is a 1, create a gas event.  If it's 0, end an existing
        gas event.
        '''
        return 'gas leak' if sensor['newData'] == '1' else None

    def processWaterSensor(self, sensor):
        '''
        If < 40 or > 65, return emergency
        '''
        newData = int(sensor['newData'])
        return 'water leak' if newData < 40 or newData > 65 else None


    #update to us passing a sensor dict object with oldData and newData already 
    #filled in.  We'll return a string 'emergency' if there is one.  'emergency'
    #can be something like 'fire' or 'gas'
    def processNewSensorData(self, sensor):
        '''
        Process new sensor data depending on the sensor type and possibly previous
        sensor data.  This "main" method acts as a switch to route sensor types
        to particular subroutines.
        If the new sensor data is the same as the last in the history, it is 
        ignored and None is returned.
        If a new emergency is detected, the emergency is created and returned.
        Otherwise, None is returned.
        '''
        sensorType = sensor['type']
        sensorID = sensor['id']
        newData = sensor['newData']
        if 'oldData' in sensor:
            oldData = sensor['oldData']
        else:
            oldData = None
        #history = db.getSensorHistory(sensorID)

        # check to see if the data has changed at all
        # Might want to check if status is still set and act accordingly
        # for now just return None
        # This should never happen so this is just a sanity check
        if oldData and oldData == newData:
            return None 

        emergency = None
        if sensorType == 'temperature':
            emergency = self.processTempSensor(sensor)
        elif sensorType == 'smoke':
            emergency = self.processSmokeSensor(sensor)
        elif sensorType == 'weight':
            emergency = self.processWeightSensor(sensor)
        elif sensorType == 'gas':
            emergency = self.processGasSensor(sensor)
        elif sensorType == 'door':
            emergency = self.processDoorSensor(sensor)
        elif sensorType == 'water pressure':
            emergency = self.processWaterSensor(sensor)
        

        self.db.shiftHistory(sensorID, newData)
        if emergency is not None:
            trueEmergency = self.checkEmergency.confirmEmergency(emergency, sensor)
            return emergency if trueEmergency else None
        return None
