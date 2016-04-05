import httplib
import json
import unittest
import time


def get():
    params = ""
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
    }
    conn.request("GET", "/testing/mfeneley_test/messages/", params, headers)
    response = conn.getresponse()
#    data = response.read()
    return response

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


class TestServerMethods(unittest.TestCase):
    
    def test_new_user1(self):
        # Check that there are initially no messages
        response = get()

        self.assertEqual(404, response.status)
        
        # Post to the local db
        basePath = "localhost"
        conn = httplib.HTTPConnection(basePath, 8080)
        conn.request("POST", "/api/users/")
        res = conn.getresponse()
        data = res.read()
        print data
        time.sleep(2)
        
        # Check for the new message
        response = get()
        self.assertEqual(200, response.status)
        data = response.read()

        # Delete the new message
        obj = eval(data)
        message = obj['messages']
        print(message, "id")
        obj = message[0]
        the_id = obj['messageId']
        delete(the_id)
        
    
    def test_new_sensor1(self):
        # Check that there are initially no messages
        response = get()
        self.assertEqual(404, response.status)

        # Post to the local db
        basePath = "localhost"
        conn = httplib.HTTPConnection(basePath, 8080)
        conn.request("POST", "/api/sensors/")
        res = conn.getresponse()
        data = res.read()
        print data, "data"
        time.sleep(2)
        
        # Check for the new message
        response = get()
        self.assertEqual(200, response.status)
        data = response.read()

        # Delete the new message
        obj = eval(data)
        message = obj['messages']
        print(message, "id")
        obj = message[0]
        the_id = obj['messageId']
        delete(the_id)
    


    def test_new_robot1(self):
        # Check that there are initially no messages
        response = get()
        self.assertEqual(404, response.status)

        # Post to the local db
        basePath = "localhost"
        conn = httplib.HTTPConnection(basePath, 8080)
        conn.request("POST", "/api/buildings/44131ffa-8e1e-494b-84b0-1e9e8bedccdd/robots/")
        res = conn.getresponse()
        data = res.read()
        print data, "data"
        time.sleep(2)
        
        # Check for the new message
        response = get()
        self.assertEqual(200, response.status)
        data = response.read()

        # Delete the new message
        obj = eval(data)
        message = obj['messages']
        print(message, "id")
        obj = message[0]
        the_id = obj['messageId']
        delete(the_id)
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestServerMethods)
unittest.TextTestRunner(verbosity=2).run(suite)