import json
#This method will return sensor ids and data of the sensors of specific type present in the given building and room
#currently some dummy code
def getSensors(buildingID, room, sensorType):
    if(buildingID==1 and room==2):
        return ["a123","b123"]
    else:
        return ["d123"]
#These methods will check if the data of a particular sensor indicates that there is Fire.
#For example, the method will return true if temperature of temperature sensor is greater than 50. currently dummy code
def ifFireTemperature(tempSensor):
    if(tempSensor=="a123" or tempSensor=="b123"):
        return True
    else:
        return False

def ifFireSmoke(smokeSensor):
    return True

#If weight>50 then there is an intruder. right now, always False.
def isIntruder(weightSensor):
    return False
#This method will receive the emergency object as the input and confirm if the emergency is real by checking other sensors in the same location
def confirmEmergency(emergency):
#Get the type of emergency and the details such as room number
    msgType=emergency['msg_type']
    buildingID=emergency['body']['buildingID']
    room=emergency['body']['room']


#Based upon the type of emergency, get the respective sensors in that room
    if(msgType=="Fire"):
        smokeSensorsArray=getSensors(buildingID, room,"Smoke")
        tempSensorsArray=getSensors(buildingID, room,"Temperature")
        smokeCount=0
        tempCount=0
        for smokeSensor in smokeSensorsArray:
            if(ifFireSmoke(smokeSensor)):
                smokeCount=smokeCount+1

        for tempSensor in tempSensorsArray:
            if(ifFireTemperature(tempSensor)):
                tempCount=tempCount+1
#If more than half of the smoke and temperature sensors detect that there is fire then fire emergency is confirmed
        if((smokeCount>len(smokeSensorsArray)/2) & (tempCount>len(tempSensorsArray)/2)):
            return True
        else:
            return False



    elif(msgType=="Intruder"):
        weightSensorsArray=getSensors(buildingID,room,"Weight")
        weightSensorsCount=0
        for weightSensor in weightSensorsArray:
            if(isIntruder(weightSensor)):
                weightSensorsCount=weightSensorsCount+1
#If more than half of the weight sensors detect that there is an intruder then intruder emergency is confirmed
        if(weightSensorsCount>len(weightSensorsArray)/2):
            return True
        else:
            return False




'''if __name__ == '__main__':
    string='{"msg_type": "Intruder","body":{"buildingID":2,"room": 2, "floor": 2, "severity": 1}}'

    emergency= json.loads(string)
    this = confirmEmergency(emergency)
    print(this)
    '''
