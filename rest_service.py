from flask import Flask, request 
from flask_restful import Resource, Api
import json
from multiprocessing import Queue


import ayto_functions as ayto

app = Flask(__name__)

api = Api(app)

class calculation_data_handler:
    def __init__(self):
        self.calculation_data = Queue()
        f = open("./cache/server_data.txt", "r")
        data_str = f.read()
        json_data = json.loads(data_str)
        f.close()


        for entry in json_data["seeding_pairs"]:
            self.calculation_data.put(entry)

    def get_calculation_data(self):
        return_data = {}
        if self.calculation_data.empty():
            return_data["finished"] = True
        else:
            return_data["finished"] = False
            return_data["seeding_combination"] = self.calculation_data.get()
        return return_data

    def insert_result_data(self):
        pass

class rest_service:
    def __init__(self):
        
        self.port = 50000
        self.url = 'http://127.0.0.1:50000/'

        cdh = calculation_data_handler()       

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
