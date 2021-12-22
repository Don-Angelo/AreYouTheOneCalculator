import logging
import time
import multiprocessing as mp


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

        self.calculation_data_url = 'http://127.0.0.1:50000/calculation_data'

        self._start_client()

    def _process_function(self,data):
        process_number = data
        self.logger.debug("Process " + str(process_number) + " started")
        comm = rc.rest_communication()

        run = True
        while run:
            # get calculation data
            calculation_data = comm.get_data(self.calculation_data_url)
            print(str(process_number) + " " + str(calculation_data))
            if calculation_data["finished"]:
                run = False
            else:
                pass

            # run calculation

            # return results

        self.logger.debug("Process " + str(process_number) + " finished")
        return True

    def _start_client(self):
        print()

        process_count = mp.cpu_count()
        process_arguments = []
        for i in range(process_count):
            process_data = (i)
            process_arguments.append(process_data)

        print(process_arguments)

        if self.settings["multiprocessing"]:
            
            pool = mp.Pool(process_count)
            result_list = pool.map_async(self._process_function,process_arguments)
            pool.close()
        
