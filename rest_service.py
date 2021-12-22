from flask import Flask, request 
from flask_restful import Resource, Api
import json

import ayto_functions as ayto

app = Flask(__name__)

api = Api(app)

class rest_service:
    def __init__(self):
        
        self.port = 50000
        self.url = 'http://127.0.0.1:50000/'

       

        #=============================================
        #calculation
        #=============================================
        class calculation_data(Resource):
            def get(self):
                request_data = ayto.get_calculation_data()
                return request_data


        #=============================================
        #result
        #=============================================
        class result(Resource):
            def post(self):
                jsonMessage = request.get_json()
                print('Incomming message:')
                print(jsonMessage)


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
