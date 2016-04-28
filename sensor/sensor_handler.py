

def lambda_handler(event, context):
    for record in event['Records']:
        temp = record['dynamodb']

        if record['eventName'] == 'MODIFY':
            if record['eventSourceARN'].find("sensors") >= 0:
                message = (parseSensor(temp['OldImage'], temp['NewImage'], record['eventName']))
                if message:
                    if message['type'] != "ok":
                        emergencyLogic(message)