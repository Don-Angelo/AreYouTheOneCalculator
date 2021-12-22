from flask import Flask, request 
from flask_restful import Resource, Api
import json
from multiprocessing import Queue


import ayto_functions as ayto

app = Flask(__name__)

api = Api(app)



class rest_service:
    def __init__(self,data_handler):
        
        self.port = 50000
        self.url = 'http://127.0.0.1:50000/'

        cdh = data_handler     

        #=============================================
        #calculation
        #=============================================
        class calculation_data(Resource):
            def get(self):
                print("get request")
                request_data = cdh.get_calculation_data()
                return request_data


        #=============================================
        #result
        #=============================================
        class result(Resource):
            def post(self):
                json_data = request.get_json()
                print('Incomming message:')
                print(json_data)

                cdh.insert_result_data(json_data)

                response = {}
                response['received'] = True
                jsonResponse = json.dumps(response)
                responseMessage = app.response_class(
                    response = jsonResponse, 
                    status = 201, 
                    mimetype = 'application/json')
                return responseMessage

        #Binds the classes to the api
        api.add_resource(calculation_data, '/calculation_data')
        api.add_resource(result, '/result')

    #Stars the service
    def start_service(self):
        app.run(port=self.port)
