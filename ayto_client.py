import logging
import time
import multiprocessing as mp
import rest_communication
import matching_night_calculator

import ayto_functions as ayto


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

        timecode = time.strftime("%Y-%m-%d_%H:%M")
        logging_filename = "./logs/client_"+timecode+".log"
        logging.basicConfig(filename=logging_filename,level=logging_level,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('Client')
        # =========================================================

        self.logger.debug("Client started")

        self.calculation_data_url = 'http://127.0.0.1:50000/calculation_data'

        self.season_data = ayto.load_season_data(self.settings["season_data_name"])
        self.total_possible_pairs = ayto.get_total_possible_pairs(self.season_data)


        self._start_client()

    def _process_function(self,data):
        process_number = data
        self.logger.debug("Process " + str(process_number) + " started")

        comm = rest_communication.rest_communication()

        mnc = matching_night_calculator.matching_night_calculator(self.season_data,self.total_possible_pairs,process_number,self.logger)
        
        while True:
            # get calculation data
            try:
                calculation_data = comm.get_data(self.calculation_data_url)
            except:
                self.logger.warning("Process " +str(process_number) + " connection to server failed")
                break

            self.logger.debug("Process " + str(process_number) + " calculating " + str(calculation_data))
            print("Process " + str(process_number) + " calculating " + str(calculation_data))
            if calculation_data["finished"]:
                break
           
            mnc.iterate_combinations(calculation_data["seeding_combination"],self.season_data["men"],self.season_data["women"])
            # run calculation
            self.logger.debug("Process "+str(process_number) + " calculation finished")
            print("Process "+str(process_number) + " calculation finished")

            # return results
            results = mnc.get_results()

            comm.post_data(results)

            

        self.logger.debug("Process " + str(process_number) + " finished")
        return True

    def _start_client(self):

        process_count = mp.cpu_count()
        process_arguments = []
        for i in range(process_count):
            process_data = (i)
            process_arguments.append(process_data)


        if self.settings["multiprocessing"]:
            
            pool = mp.Pool(process_count)
            result_list = pool.map_async(self._process_function,process_arguments)
            pool.close()
            pool.join()
        else:
            self._process_function(0)

        
