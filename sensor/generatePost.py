'''
Generates a POST request to the push notification team that sends a message
to them for them to store
'''
def generatePOST(message):
    params = json.dumps(message) #necessary to format message in string format
    print(params)
    return
    conn = httplib.HTTPSConnection("2bj29vv7f3.execute-api.us-east-1.amazonaws.com")
    headers = {
        'x-api-key': "F2yxLdt3dNfvsncGwl0g8eCik3OxNej3LO9M2iHj",
        'cache-control': "no-cache",
        }
    conn.request("POST", "/testing", params, headers)
    response = conn.getresponse()
    data = response.read()
    print(data.decode("utf-8"))
