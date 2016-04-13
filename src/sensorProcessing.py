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
            self.storage.getSensorHistory('smoke')
            smokeSensors = self.storage.getSensorData('smoke',\
                    sensor['buildingId'], sensor['room'])
            for val in smokeSensors.values():
                if val == '1':
                    emergency = 'fire'

        if emergency is not None:
            trueEmergency = self.checkEmergency.confirmEmergency('fire', sensor)
            return 'fire' if trueEmergency else None
        return None

    def processSmokeSensor(self, newData):
        '''
        Process the smoke sensor by reading the temperature sensor history.
        If the smoke sensor, it could be a flaw.  Check the temperature history to
        judge as well.  Only fire if smoke is 1 and temp > 50
        '''
        pass

    def processDoorSensor(self, newData):
        '''
        Process the door sensor. Used for intruder detection.  
        '''
        pass

    def processGasSensor(self, newData):
        '''
        If the new data is a 1, create a gas event.  If it's 0, end an existing
        gas event.
        '''
        pass


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
        

        self.db.shiftHistory(sensorID, newData)
        return emergency
