"""
ECE 4574: Final Exam
File Name: inttest_server_storage.py
Author: Chang Sun
Date: May 5, 2016
Description: Integration testing for server_storage.py
"""

# _________________________________________________________________________________________________


import time
import datetime
import uuid
import json
import unittest
from StringIO import StringIO
import holder
from server_storage import *


# _________________________________________________________________________________________________


def generate_lambda_event(new_status, id, test_type, old_status='fire'):
    json_str = """{
        "Records": [
          {
            "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
            "eventVersion": "1.0",
            "dynamodb": {
              "OldImage": {
                "buildingId": {
                      "S": "5"
                    },
                    "data": {
                      "S": \"""" + old_status + """\"
                    },
                    "floor": {
                      "N": "6"
                    },
                    "id": {
                      "S": \"""" + id + """\"
                    },
                    "model": {
                      "S": "KM07"
                    },
                    "room": {
                      "N": "3"
                    },
                    "type": {
                      "S": "motion detector"
                    },
                    "xpos": {
                      "N": "7"
                    },
                    "ypos": {
                      "N": "4"
                    }
              },
              "SequenceNumber": "12820400000000002641118120",
              "Keys": {
                "robots": {
                  "S": "3"
                }
              },
              "SizeBytes": 56,
              "NewImage": {
                 "buildingId": {
                      "S": "5"
                    },
                    "data": {
                      "S": \"""" + new_status + """\"
                    },
                    "floor": {
                      "N": "6"
                    },
                    "id": {
                      "S": \"""" + id + """\"
                    },
                    "model": {
                      "S": "KM07"
                    },
                    "room": {
                      "N": "3"
                    },
                    "type": {
                      "S": "motion detector"
                    },
                    "xpos": {
                      "N": "7"
                    },
                    "ypos": {
                      "N": "4"
                    }
              },
              "StreamViewType": "NEW_AND_OLD_IMAGES"
            },
            "awsRegion": "us-east-1",
            "eventName": \"""" + test_type + """\",
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/sensors/stream/2016-03-17T17:55:28.502",
            "eventSource": "aws:dynamodb"
          }
        ]
      }"""
    return json.loads(json_str)


# _________________________________________________________________________________________________


class IntTestServerStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(IntTestServerStorage, self).__init__(*args, **kwargs)

    def setUp(self):
        print('******Running test case******')

    def tearDown(self):
        print('******Finished running test case******\n')

    def test1(self):
        print('Case 1: Check integration with MODIFY event')
        id = str(uuid.uuid4())
        history = get_last_states(id)
        self.assertEqual(0, len(history))
        event = generate_lambda_event('normal', id, 'MODIFY')
        holder.lambda_handler(event, 0)
        history = get_last_states(id)
        self.assertEqual(1, len(history))

    def test2(self):
        print('Case 2: Check multiple entries with MODIFY event')
        id = str(uuid.uuid4())
        event = generate_lambda_event('normal', id, 'MODIFY')
        history = get_last_states(id)
        self.assertEqual(0, len(history))
        count = 6
        for i in range(count):
            holder.lambda_handler(event, 0)
        history = get_last_states(id, size=count)
        self.assertEqual(count, len(history))

    def test3(self):
        print('Case 3: Check excessive entries with MODIFY event')
        id = str(uuid.uuid4())
        event = generate_lambda_event('normal', id, 'MODIFY')
        history = get_last_states(id)
        self.assertEqual(0, len(history))
        count = MAX_HISTORY_SIZE + 1
        for i in range(count):
            holder.lambda_handler(event, 0)
        history = get_last_states(id, size=count)
        self.assertEqual(MAX_HISTORY_SIZE, len(history))

    def test4(self):
        print('Case 4: Check integration with INSERT event')
        id = str(uuid.uuid4())
        event = generate_lambda_event('normal', id, 'INSERT')
        history = get_last_states(id)
        self.assertEqual(0, len(history))
        holder.lambda_handler(event, 0)
        history = get_last_states(id)
        self.assertEqual(0, len(history))


# _________________________________________________________________________________________________


if __name__ == '__main__':
    unittest.main()


# _________________________________________________________________________________________________
