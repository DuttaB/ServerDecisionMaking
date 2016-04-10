#!/usr/bin/python
#Bug Fixes for version 1.0


'''
	Input json_object:
	{
		'from' : 'sensor'
		'building' : 
		'type' :
		'room' :
		'xpos':
		'ypos':
		'floor' : 
		
	}	
	
	
	{
		'from': 'robot_sensor',
		'building': 
		'room': 
		'emergency':
		'floor':  
		'offensive':
		'xpos':
		'ypos':
		'type': 
		'movement': 
		'robot':
		'capabilities' : ?
	}
	{
		'from': 'robot',
		'offensive': 
		'movement': 
		'emergency': 
		'floor':
		'building' : 
		'robot'
		'capabilities' : ?
		'room' : 
		'xpos':
		'ypos':
	}	
	
	Output json_message:
	{
	"id":  {
			"type": string
			"ids": string[]
			}
	
	"message": {
				'msg_type': string,
				'body':{
					'floor': int,
					'room': int,
					'xpos': int,
					'ypos': int,
					'severity': int,
					'action': string,
					'message': string,
					'building': int,
				}
	}
'''

# Finds a robot that can fix the given emergency event within the given building and returns the Robot ID
def findRobot(event_type, building):
	if(event_type == 'fire'):
		robot  = ['0']
	elif(event_type == 'flood'):
		robot  = ['0']
	elif(event_type == 'gas_leak'):
		robot  = ['0']
	elif(event_type == 'intruder'):
		robot  = ['0']
		
	return robot #returns list of robot ids
	
# Finds app users linked to the given building
def findBuildingOccupants(building):

	return ['0']

# Generate HTTP POST request to Push Notification's API	
def generatePOST(message):
	return

# Server logic to process emergency	
def server_logic(json_object):
	
	# Severity Levels
	FIRE = 5
	WATER_LEAK = 2
	INTRUDER = 3
	GAS_LEAK = 4

	# Message Formats				
	user_message = {
						'id':  {
								'type': 'users',
								'ids': []
								}
						
						'message': {
									'msg_type': json_object['type'],
									'body':{
										'building':json_object['building']
										'xpos': json_object['xpos'],
										'ypos': json_object['ypos'],
										'room': json_object['room'],
										'floor': json_object['floor'],
										'message': ''
									}
						}
					}
	robot_command = {
						'id':  {
								'type': 'robots',
								'ids': []
								}
						
						'message': {
									'msg_type': json_object['type'],
									'body':{
										'building':json_object['building']
										'xpos': json_object['xpos'],
										'ypos': json_object['ypos'],
										'room': json_object['room'],
										'floor': json_object['floor'],
										'action': '', 
										'severity': 0
									}
						}
					}
	
	# Handle Emergency from Robot
	if(json_object['from'] == 'robot'):
		return # Need more information to generate response
	
	# Handle Emergency from Sensor
	elif(json_object['from'] == 'sensor'):
		robot_command['id']['ids'] = findRobot(json_object['type'], json_object['building'])				
		
	# Handle Emergency from Sensor on Robot
	elif(json_object['from'] == 'robot_sensor'):
		# Check if this robot can handle the emergency
		if(json_object['offensive']):
			robot_command['id']['ids'] = [json_object['robot']]
		else:
			robot_command['id']['ids'] = findRobot(json_object['type'], json_object['building'])
	

	# Generate Command/Message Content
	if len(robot_command['id']['ids']) == 0:
		return # What do we do if no robots can solve problem
	elif json_object['type'] == 'fire'	
		robot_command['message']['body']['action'] = 'Extinguish':
		robot_command['message']['body']['severity'] = FIRE
		
	elif json_object['type'] == 'intruder':
		robot_command['message']['body']['action'] = 'Scare'
		robot_command['message']['body']['severity'] = INTRUDER
		
	elif json_object['type'] == 'water_leak':
		robot_command['message']['body']['action'] = 'Pump'
		robot_command['message']['body']['severity'] = WATER_LEAK
		
	elif json_object['type'] == 'gas_leak':
		robot_command['message']['body']['action'] = 'Vent'
		robot_command['message']['body']['severity'] = GAS_LEAK
	else:
		return # Unhandled Event		
		
	# Send Robot Command
	generatePOST(robot_command)

	user_message['id']['ids'] = findBuildingOccupants(json_object['building'])
	
	if len(user_message['id']['ids']) == 0:
		if len(robot_command['id']['ids']) == 0:
			return # No users and No robots what do we do?
		return # No users what do we do?
		
	user_message['message']['body']['message'] = 'Emergency: ' + json_object['type']
	
	# Send User Message
	generatePOST(user_message)
	
	return		
			
			