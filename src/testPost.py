import httplib
import json
import unittest


def generatePOST(message):
    params = json.dumps(message) #necessary to format message in string format
    #print(params)
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
    }
    conn.request("POST", "/testing", params, headers)
    response = conn.getresponse()
    data = response.read()
    print(data, "data")
    return(data.decode("utf-8"))


def get():
    params = ""
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
    }
    conn.request("GET", "/testing/mfeneley_test/messages", params, headers)
    response = conn.getresponse()
    data = response.read()
    print (data, "data")
    return response

def get_id(message):
    params = ""
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
    }
    conn.request("GET", "/testing/mfeneley_test/messages/" + message, params, headers)
    response = conn.getresponse()
    data = response.read()
    return(data.decode("utf-8"))

def delete(the_id):
    params = ""
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
    }
    conn.request("DELETE", "/testing/mfeneley_test/messages/" + the_id , params, headers)
    response = conn.getresponse()
    data = response.read()
    return(data.decode("utf-8"))



class testPost(unittest.TestCase):

    def test_Post(self):
        test_object = {
                            "id":  ["mfeneley_test"], 
                            "message": {
                                "msg_type": "alert", 
                                "body":{ "buildingId":"1", 
                                "new_id": "2",
                                "xpos": "3", 
                                "ypos": "4", 
                                "room": "5",
                                "floor": "6", 
                                "owner": "Michael"
                                 }
                             }
                          }
        test_object2 = {
                            "id":  ["mfeneley_test"], 
                            "message": {
                                "msg_type": "alert", 
                                "body":{ "buildingId":"7", 
                                "new_id": "8",
                                "xpos": "9", 
                                "ypos": "10", 
                                "room": "11",
                                "floor": "12", 
                                "owner": "Sam"
                                 }
                             }
                          }

        
        init = get()
        print(init)


        this = delete('82715529-fab8-11e5-a809-e52a6b96a970')


        """

        self.assertEqual(404, init.status)
        response = generatePOST(test_object)
        json_object = eval(response)
        msg_id1 = json_object["messageId"]
        after = get()
        self.assertEqual(200, after.status)
        obj = get_id(msg_id1)       
        json_object = eval(obj)
        message = json_object['body']
        body = message["body"]
        xpos = body["xpos"]
        ypos = body["ypos"]
        room = body["room"]
        floor = body["floor"]
        owner = body["owner"]       
        self.assertEqual(xpos, '3')
        self.assertEqual(ypos, '4')
        self.assertEqual(room, '5')
        self.assertEqual(floor, '6')
        self.assertEqual(owner, 'Michael')


        response = generatePOST(test_object2)
        json_object = eval(response)
        msg_id2 = json_object["messageId"]
        after = get()
        self.assertEqual(200, after.status)
        obj = get_id(msg_id2)       
        json_object = eval(obj)
        message = json_object['body']
        body = message["body"]
        xpos = body["xpos"]
        ypos = body["ypos"]
        room = body["room"]
        floor = body["floor"]
        owner = body["owner"]       
        self.assertEqual(xpos, '9')
        self.assertEqual(ypos, '10')
        self.assertEqual(room, '11')
        self.assertEqual(floor, '12')
        self.assertEqual(owner, 'Sam')
        
        response = delete(msg_id1)
        response = delete(msg_id2)
        """

suite = unittest.TestLoader().loadTestsFromTestCase(testPost)
unittest.TextTestRunner(verbosity=2).run(suite)
