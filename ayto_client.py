import logging
import time
import requests


import ayto_functions as ayto
import rest_communication as rc

class ayto_client:
    def __init__(self):
        self.settings = ayto.load_settings()
        # =========================================================
        # logger configuration
        logging_level = logging.INFO
        if self.settings["logging"] == "debug":
            logging_level = logging.DEBUG
        #logging_level = logging.DEBUG
        #logging_level = logging.INFO
        #logging_level = logging.ERROR
        #logging_level = logging.CRITICAL

        timecode = time.strftime("%Y-%m-%d-%H-%M")
        logging_filename = "./logs/server_"+timecode+".log"
        logging.basicConfig(filename=logging_filename,level=logging_level,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('Client')
        # =========================================================

        self.logger.debug("Client started")

        server_url = 'http://127.0.0.1:50000/'
        self.calculation_data_url = server_url + 'calculation_data'

        self._start_client()

    def _process_function(self):
        # get calculation data
        calculation_data = rc.get_data(self.calculation_data_url)
        
        # run calculation

        # return results

    def _start_client(self):
        pass
        
