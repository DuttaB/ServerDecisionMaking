'''
This function is called when a sensor determines an emergency has occurred. This
determines what robot(s) to send to handle the emergency as well as sends a
message to all affected users about the emergency.
'''
def emergencyLogic(json_object):

    # Severity Levels
    FIRE = 5
    WATER_LEAK = 2
    INTRUDER = 3
    GAS_LEAK = 4

    # Message Formats
    user_message = {
                        'id':  [],
                        'message': {
                                    'msg_type': 'notification',
                                    'body':{
                                        'buildingId':json_object['buildingId'],
                                        'xpos': json_object['xpos'],
                                        'ypos': json_object['ypos'],
                                        'room': json_object['room'],
                                        'floor': json_object['floor'],
                                        'message': ''
                                    }
                        }
                    }
    robot_command = {
                        'id':  [],
                        'message': {
                                    'msg_type': json_object['type'],
                                    'body':{
                                        'buildingId':json_object['buildingId'],
                                        'xpos': json_object['xpos'],
                                        'ypos': json_object['ypos'],
                                        'room': json_object['room'],
                                        'floor': json_object['floor'],
                                        'action': '',
                                        'severity': 0
                                    }
                        }
                    }

    building_status = {
                        'id':  [json_object['buildingId']],
                        'message': {
                                    'msg_type': 'update status',
                                    'body':{
                                        'xpos': json_object['xpos'],
                                        'ypos': json_object['ypos'],
                                        'room': json_object['room'],
                                        'floor': json_object['floor'],
                                        'status': json_object['type']
                                    }
                        }
                    }

    # Send new building status if the building is not up to date
    if(~checkBuildingStatus(json_object['type'], json_object['buildingId'])):
        generatePOST(building_status)

    # Get list of robots that can respond to the event
    robot_command['id'] = findRobot(json_object['type'], json_object['buildingId'])

    # Generate Command/Message Content
    if len(robot_command['id']) == 0:
        return # What do we do if no robots can solve problem
    elif json_object['type'] == 'fire':
        robot_command['message']['body']['action'] = 'Extinguish'
        robot_command['message']['body']['severity'] = FIRE

    elif json_object['type'] == 'intruder':
        robot_command['message']['body']['action'] = 'Attack'
        robot_command['message']['body']['severity'] = INTRUDER

    elif json_object['type'] == 'water leak':
        robot_command['message']['body']['action'] = 'Pump'
        robot_command['message']['body']['severity'] = WATER_LEAK

    elif json_object['type'] == 'gas leak':
        robot_command['message']['body']['action'] = 'Vent'
        robot_command['message']['body']['severity'] = GAS_LEAK
    else:
        return # Unhandled Event

    # Send Robot Command
    generatePOST(robot_command)

    # Get list of users linked to the buildingId
    user_message['id'] = findBuildingOccupants(json_object['buildingId'])

    if len(user_message['id']) == 0:
        if len(robot_command['id']) == 0:
            return # No users and No robots what do we do?
        return # No users what do we do?

    # Generate user message
    user_message['message']['body']['message'] = 'Emergency: ' + json_object['type'].upper() + ' of Severity: ' + str(robot_command['message']['body']['severity'])

    # Send User Message
    generatePOST(user_message)
