
class sensorProcessing(object):
    getUsers = None
    getSensors = None
    getSensorData = None
    checkEmergency = None
    get_last_states = None
    db = None

    def __init__(self, module=None):
        if not module:
            import getUsersAtLocation as getUsers
            import getSensorsAtLocation as getSensors
            import getSensorData as getSensorData
            import confirmEmergency as checkEmergency
            import get_last_states as get_last_states
            db = None
        else:
            getUsers = module
            getSensors = module
            getSensorData = module
            checkEmergency = module
            get_last_states = module
            db = module
        if not self.getUsers:
            self.getUsers = getUsers
        if not self.getSensors:
            self.getSensors = getSensors
        if not self.getSensorData:
            self.getSensorData = getSensorData
        if not self.checkEmergency:
            self.checkEmergency = checkEmergency
        if not self.get_last_states:
            self.get_last_states = get_last_states
        if not self.db:
            self.db = db
        
    def processWeightSensor(self, sensor):
        '''
        Process Weight sensors by reading the sensor history and new incoming data
        and determines if there's an emergency or not.
        The emergency this looks for is intruders (based on other sensors too,
        possibly)

        If a weight is < 45, it's asumed to be a child or robot.

        weight sensor changes will never cause an emergency.
        The weight sensor will only be read when door sensors change.
        '''
        pass #for now

    def processTempSensor(self, sensor):
        '''
        Process the temperature sensor by reading history and determining if there 
        could be a fire.  A fire is determined if temp > 100.  If temp >50, temp 
        is only a fire if there's smoke.
        check if there was a fire based on the historical temperature, 
        smoke data. if thats the case, don't raise another fire emergency and set
        emergency=None
        '''
        emergency = None
        if int(self.get_last_states.get_last_states(sensor['id'])[0][1]) > 100:
            return emergency
        elif int(self.get_last_states.get_last_states(sensor['id'])[0][1]) > 50:
            sensors = self.getSensors.getSensorsAtLocation(sensor['buildingId'],\
                    sensor['room'], sensor['floor'], sensor['xpos'],\
                    sensor['ypos'])
            for sensor in sensors:
                if sensor['type'] == 'smoke' and int(self.get_last_states.get_last_states(sensor['id'])[0][1]) == 1:
                    return emergency
        else:
            if int(sensor['newData']) > 100:
                emergency = 'fire'
            elif int(sensor['newData']) > 50:
                smokeSensors = self.getSensorData.getSensorData('smoke',\
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
            tempSensors = self.getSensorData.getSensorData('temperature',\
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
        If door sensor is 1, one of the proximity sensors in the room is 1 and sum of all
        the weight sensors in that room has changed by 80 as compared to previous sum, raise intruder emergency.
        The confirmEmergency function will invalidate the emergency in case the person entering the room is a user and not an intruder
        '''
        emergency = None
        proximitySensorOn = False
        newWeight = 0
        oldWeight = 0
        if sensor['newData'] == '1':
            #door sensor went off
            sensors = self.getSensors.getSensorsAtLocation(sensor['buildingId'],\
                    sensor['room'], sensor['floor'], sensor['xpos'],\
                    sensor['ypos'])
            assert sensors is not None, "sensors has to at least have a door sensor!"
            users = self.getUsers.getUsersAtLocation(sensor['buildingId'], sensor['room'],\
                    sensor['floor'], sensor['xpos'], sensor['ypos'])
            if not not users :
                return emergency
            for sensor in sensors:
                if sensor['type'] == 'proximity' and int(sensor['data']) == 1:
                    proximitySensorOn = True
                if sensor['type'] == 'weight':
                    newWeight = newWeight + int(sensor['data'])
                    oldWeight = oldWeight + int(self.get_last_states.get_last_states(sensor['id'])[0][1])

            if proximitySensorOn and (newWeight - oldWeight) >= 80:
                emergency = 'intruder'
        return emergency

    def processGasSensor(self, sensor):
        '''
        If the new data is a 1 and old data was 0, create a gas event.  
        '''
        return 'gas leak' if sensor['newData'] == '1' and self.get_last_states.get_last_states(sensor['id'])[0][1] =='0' else None

    def processWaterSensor(self, sensor):
        '''
        If < 40 or > 65 and old data was between 40 and 65, return emergency
        '''
        newData = int(sensor['newData'])
        lastData=int(self.get_last_states.get_last_states(sensor['id'])[0][1])
        if (newData < 40 or newData > 65):
            if(lastData <= 65 and lastData >= 40):
                return 'water leak'
        else:
            return None
        #return 'water leak' if (newData < 40 or newData > 65) and (lastData <= 65 and lastData >= 45) else None


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
        try:
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
        

            if self.db is not None:
                self.db.shiftHistory(sensorID, newData)

            if emergency is not None:
                trueEmergency = self.checkEmergency.confirmEmergency(emergency, sensor)
                return emergency if trueEmergency else None
            return None
        except Exception as e:
            print ('')
        return None
