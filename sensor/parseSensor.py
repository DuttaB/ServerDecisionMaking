'''
This function parses a sensor object, and determines if something
has changed. If it has, it returns a dictionary contaning all
pertinent information to be sent in a message to whoever requires it.
'''
def parseSensor(old,new,eventName):
    if old['data']['S'] == new['data']['S']:
    #if it's the same nothing has changed
        print("0")
        return 0
    else:
    #if it has changed there must be a problem
        emergency = {
                        "type": new['type']['S'],
                        "buildingId": new['buildingId']['S'],
                        "room": new['room']['N'],
                        "from": "sensor",
                        "xpos": new['xpos']['N'],
                        "ypos": new['ypos']['N'],
                        "floor": new['floor']['N'],
			"id": new['id']['S'],
			"oldData": old['data']['S'],
			"newData": new['data']['S']
                    }
        if "robotId" in new:
            emergency['robotId'] = new['robotId']['S']

	sens = sensorProcessing()
        return sens.processNewSensorData(emergency)
