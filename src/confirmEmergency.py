#from checkIntruder import checkIntruder
from getSensorData import getSensorData

# dummy function for checkIntruder. this will be replaced by actual checkIntruder once it is imported
def checkIntruder(building_id, floor_id, room_id, xpos_id, ypos_id):
    return True
def confirmFireEmergency(sensor):
    #get all temperature sensors in the same building,room as the given sensor
    tempSensors=getSensorData(sensor['type'],sensor['buildingId'],int(sensor['room']))
    tempCount=0
    #if more than 2 temperature sensors then atleast 2 should be greater than 50
    if(len(tempSensors)>2):
        for key,value in tempSensors.items():
            if(int(value)>50):
                tempCount=tempCount+1
        if(tempCount<2):
            return False
    #get all smoke sensors in that building,room
    #if more than 2 smoke sensors then atleast 2 should be 1
    smokeSensors=getSensorData('smoke',sensor['buildingId'],sensor['room'])
    smokeCount=0
    if(len(smokeSensors)>2):
        for key,value in smokeSensors.items():
            if(int(value)==1):
                smokeCount=smokeCount+1
        if(smokeCount<2):
            return False
    return True
    
def confirmIntruderEmergency(sensor):
    #get all weight sensors in the same building,room as the given sensor
    return checkIntruder(sensor['buildingId'],sensor['floor'],sensor['room'],sensor['xpos'],sensor['ypos'])
    
def confirmGasLeakEmergency (sensor): 
    #get all gas sensors in the same building,room as the given sensor
    gasSensors=getSensorData(sensor['type'],sensor['buildingId'],int(sensor['room'])) 
    #if more than 2 gas sensors then return true if atleast 2 of them are 1
    if(len(gasSensors)<=2):
        return True
    else:
        gasCount=0
        for key,value in gasSensors.items():
            if(int(value)==1):
                gasCount=gasCount+1
        if(gasCount>=2):
            return True
        else:
            return False 
        
def confirmWaterLeakEmergency (sensor): 
    #get all water pressure sensors in the same building,room as the given sensor
    waterSensors=getSensorData(sensor['type'],sensor['buildingId'],int(sensor['room'])) 
    #if more than 2 water pressure sensors then return true if atleast 2 of them satisfy the water leak criteria
    if(len(waterSensors)<=2):
        return True
    else:
        waterCount=0
        for key,value in waterSensors.items():
            if(int(value) <40 or int(value) >60):
                waterCount=waterCount+1
        if(waterCount>=2):
            return True
        else:
            return False           
        
    
def confirmEmergency(emergency, sensor):
    #calling respective method based on type of emergency
    if(emergency=='fire'):
        return confirmFireEmergency(sensor)
    elif(emergency=='intruder'):
        return confirmIntruderEmergency(sensor)
    elif(emergency=='gas leak'):
        return confirmGasLeakEmergency(sensor)
    elif(emergency=='water leak'):
        return confirmWaterLeakEmergency(sensor)
    else:
        return False
