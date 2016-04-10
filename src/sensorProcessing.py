
# This import will change when we don't do dummy processing anymore
import sensorProcessingTest as db


def processWeightSensors(history, newData):
    '''
    Process Weight sensors by reading the sensor history and new incoming data 
    and determines if there's an emergency or not.
    The emergency this looks for is intruders (based on other sensors too,
    possibly)

    If a weight is < 45, it's asumed to be a child or robot.
    '''
    pass #for now

def processTempSensor(history, newData):
    '''
    Process the temperature sensor by reading history and determining if there 
    could be a fire.  A fire is determined if temp > 100.  If temp >50, temp 
    is only a fire if there's smoke.
    '''
    pass

def processSmokeSensor(history, newData):
    '''
    Process the smoke sensor by reading the temperature sensor history.
    If the smoke sensor, it could be a flaw.  Check the temperature history to
    judge as well.  Only fire if smoke is 1 and temp > 50
    '''
    pass

def processDoorSensor(history, newData):
    '''
    Process the door sensor. Used for intruder detection.  
    '''
    pass

def processGasSensor(history, newData):
    '''
    If the new data is a 1, create a gas event.  If it's 0, end an existing
    gas event.
    '''
    pass


def processNewSensorData(sensorID, sensorType, newData):
    '''
    Process new sensor data depending on the sensor type and possibly previous
    sensor data.  This "main" method acts as a switch to route sensor types
    to particular subroutines.
    If the new sensor data is the same as the last in the history, it is 
    ignored and None is returned.
    If a new emergency is detected, the emergency is created and returned.
    Otherwise, None is returned.
    '''
    history = db.getSensorHistory(sensorID)
    # check to see if the data has changed at all
    # Might want to check if status is still set and act accordingly
    # for now just return None
    if not history or history[0] == newData:
        return None 

    if sensorType == 'weight':
        processWeightSensors(history, newData)
        

    db.shiftHistory(sensorID, newData)
    return None
