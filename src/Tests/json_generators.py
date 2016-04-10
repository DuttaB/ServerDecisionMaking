import json

def generate_sensor_json(event_type, new_status, old_status="fire"):
    string = """ {
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
                "S": "9"
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
                "S": "9"
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
      "eventName": \"""" + event_type + """\",
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/sensors/stream/2016-03-17T17:55:28.502",
      "eventSource": "aws:dynamodb"
    }
  ]
}"""

    json_obj = json.loads(string)
    for record in json_obj['Records']:
        temp = record['dynamodb']
        old = temp['OldImage']
        new = temp['NewImage']
    return old, new, event_type

def generate_robot_json(change):

    if change is True:
        json_str ="""

{
  "Records": [
    {
      "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
      "eventVersion": "1.0",
      "dynamodb": {
        "SequenceNumber": "12820400000000002641118120",
        "Keys": {
          "sensors": {
            "S": "3"
          }
        },
        "SizeBytes": 56,
        "NewImage": {
            "buildingId": {
                "S": "5"
              },
              "capabilities": {
                "L": [
                  {
                    "S": "attack"
                  },
                  {
                    "S": "vent"
                  }
                ]
              },
              "floor": {
                "N": "1"
              },
              "id": {
                "S": "9"
              },
              "movement": {
                "S": "air"
              },
              "room": {
                "N": "3"
              },
              "sensorId": {
                "L": [
                  {
                    "S": "0"
                  },
                  {
                    "S": "56"
                  }
                ]
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
      "eventName": "INSERT",
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/robots/2016-03-17T17:55:28.502",
      "eventSource": "aws:dynamodb"
    }
  ]
}

"""

    else:
        json_str = """

{
  "Records": [
    {
      "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
      "eventVersion": "1.0",
      "dynamodb": {
        "SequenceNumber": "12820400000000002641118120",
        "Keys": {
          "sensors": {
            "S": "3"
          }
        },
        "SizeBytes": 56,
        "NewImage": {
            "buildingId": {
                "S": "5"
              },
              "capabilities": {
                "L": [
                  {
                    "S": "attack"
                  },
                  {
                    "S": "vent"
                  }
                ]
              },
              "floor": {
                "N": "1"
              },
              "id": {
                "S": "9"
              },
              "movement": {
                "S": "air"
              },
              "room": {
                "N": "3"
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
      "eventName": "INSERT",
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/robots/2016-03-17T17:55:28.502",
      "eventSource": "aws:dynamodb"
    }
  ]
}

"""

    json_obj = json.loads(json_str)
    for record in json_obj['Records']:
        temp = record['dynamodb']
        new = temp['NewImage']
    return new

def generate_find_items_json():
    event = generate_robot_json(False)
    arr = event['capabilities']['L']
    return arr

#this will transmit a lot of extra data when testing lambda, but unneeded fields will be ignored
def generate_lambda(new_status, test_source,test_type, old_status="fire"):
    json_str = ""
    if test_source == "robots":
       json_str =  """{
          "Records": [
            {
              "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
              "eventVersion": "1.0",
              "dynamodb": {
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
                      "capabilities": {
                        "L": [
                          {
                            "S": "attack"
                          },
                          {
                            "S": "vent"
                          }
                        ]
                      },
                      "floor": {
                        "N": "1"
                      },
                      "id": {
                        "S": "9"
                      },
                      "movement": {
                        "S": "air"
                      },
                      "room": {
                        "N": "3"
                      },
                      "sensorId": {
                        "L": [
                          {
                            "S": "0"
                          },
                          {
                            "S": "56"
                          }
                        ]
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
              "eventName": "INSERT",
              "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/robots/2016-03-17T17:55:28.502",
              "eventSource": "aws:dynamodb"
            }
          ]
        }"""

    elif test_source == "users":
        json_str = """{
                      "Records": [
                        {
                          "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
                          "eventVersion": "1.0",
                          "dynamodb": {
                            "SequenceNumber": "12820400000000002641118120",
                            "Keys": {
                              "users": {
                                "S": "3"
                              }
                            },
                            "SizeBytes": 56,
                            "NewImage": {
                               "buildingId": {
                                    "S": "7"
                                  },
                                  "floor": {
                                    "N": "2"
                                  },
                                  "id": {
                                    "S": "8"
                                  },
                                  "message": {
                                    "S": "ok"
                                  },
                                  "owner": {
                                    "BOOL": false
                                  },
                                  "room": {
                                    "N": "3"
                                  },
                                  "xpos": {
                                    "N": "5"
                                  },
                                  "ypos": {
                                    "N": "4"
                                  }
                            },
                            "StreamViewType": "NEW_AND_OLD_IMAGES"
                          },
                          "awsRegion": "us-east-1",
                          "eventName": "INSERT",
                          "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/users/stream/2016-03-17T17:55:28.502",
                          "eventSource": "aws:dynamodb"
                        }
                      ]
                    }"""

    elif test_source == "sensors":
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
                            "S": "9"
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
                            "S": "9"
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

def generate_user_json(event_type, new_status, old_status="fire"):
    user_str = """
    {
  "Records": [
    {
      "eventID": "dbdbb76dd0aa5aa87976e4f749353257",
      "eventVersion": "1.0",
      "dynamodb": {
        "OldImage": {
          "buildingId": {
            "S": "7"
          },
          "floor": {
            "N": "2"
          },
          "id": {
            "S": "8"
          },
          "message": {
            "S": \"""" + old_status + """\"
          },
          "owner": {
            "BOOL": false
          },
          "room": {
            "N": "3"
          },
          "xpos": {
            "N": "5"
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
            "S": "7"
          },
          "floor": {
            "N": "2"
          },
          "id": {
            "S": "8"
          },
          "message": {
            "S": \"""" + new_status + """\"
          },
          "owner": {
            "BOOL": false
          },
          "room": {
            "N": "3"
          },
          "xpos": {
            "N": "5"
          },
          "ypos": {
            "N": "4"
          }
        },
        "StreamViewType": "NEW_AND_OLD_IMAGES"
      },
      "awsRegion": "us-east-1",
      "eventName": \"""" + event_type + """\",
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:810004246756:table/4574test/sensors/stream/2016-03-17T17:55:28.502",
      "eventSource": "aws:dynamodb"
    }
  ]
}
"""
    json_obj = json.loads(user_str)
    for record in json_obj['Records']:
        temp = record['dynamodb']
        old = temp['OldImage']
        new = temp['NewImage']
    return old, new, event_type

#structure expected from server_logic
def generate_server_json(test_action, test_type, action_flag):
    json_action = """
    {
  "action": \"""" + test_action + """\",
  "building": 0,
  "emergency": "true",
  "floor": 0,
  "room": 0,
  "location": 0,
  "robots": [0],
  "location": "0",
  "type":  \"""" + test_type + """\"
}
"""

    json_noaction = """
    {
  "building": 0,
  "emergency": "true",
  "floor": 0,
  "room": 0,
  "location": 0,
  "robots": [0],
  "location": "0",
  "type":  \"""" + test_type + """\"
  }
"""
    if(action_flag == True):
        struct = json.loads(json_action)
    else:
        struct = json.loads(json_noaction)
    return struct

def generate_emergency_json(test_type):
    emergency = """{
                        "type": \"""" + test_type + """\",
                        "buildingId": 0,
                        "room": 0,
                        "from": "user",
                        "xpos": 1,
                        "ypos": 1,
                        "floor": 2,
                        "owner": "False"
                    } """
    struct = json.loads(emergency)
    return struct