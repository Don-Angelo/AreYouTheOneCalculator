import json
import requests

class rest_communication:
    def __init__(self):
        server_url = 'http://127.0.0.1:50000/'
        self.result_url = server_url + 'result'

    #HTTP post methode
    def post_data(self,input_data):
        json_data = json.dumps(input_data)
        response = requests.post(self.result_url,json=json_data)
        responseStatus = response.status_code
        responseMessage = response.text
        #print('Post:', responseStatus, responseMessage)

    def get_data(self,data_url):
        response = requests.get(data_url)
        json_response = response.json()
        return json_response
    