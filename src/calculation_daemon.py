from datetime import date, datetime
import os
import logging
import ayto_functions as ayto
import multiprocessing as mp
from matching_night_calculator import matching_night_calculator
from result_data_handler import result_data_handler

class calculation_daemon:
    def __init__(self,settings,season_data,seeding_pairs):
        self.settings = settings
        self.season_data = season_data
        self.seeding_pairs = seeding_pairs
        self.total_possible_pairs = ayto.get_total_possible_pairs(self.season_data)

        self.logger = logging.getLogger("calculation_daemon")

        self.start_time = None
        self.finishing_time = None

    def _process_function(self,process_arguments):
        process_id = os.getpid()

        seeding_pair_combination = process_arguments
        mnc = matching_night_calculator(self.season_data,self.total_possible_pairs,process_id)

        self.logger.debug("Process " + str(process_id) + " calculating " + str(seeding_pair_combination))
        print("Process " + str(process_id) + " calculating " + str(seeding_pair_combination))
        mnc.iterate_combinations(seeding_pair_combination)
        result_data = mnc.get_results()
        #self.result_data_queue.put(result_data)
        #self.data_handler.update_results()
        #mnc.reset_results()

        #self.logger.debug("Process " + str(process_number) + " finished")
        return result_data


    def start_clalculation(self):
        self.start_time = datetime.now()
        process_count = mp.cpu_count()
        self.logger.debug("Running with " + str(process_count) + " processes")
        
        result_list = []

        if self.settings["multiprocessing"]:
  
           
            process_arguments = []
            for pair_combination in self.seeding_pairs:
                process_data = (pair_combination)
                process_arguments.append(process_data)
            
       
            pool = mp.Pool(process_count)
            result_list = pool.map(self._process_function,process_arguments)
            

      
        else:
            result_list.append(self._process_function(self.seeding_pairs[0]))
        self.logger.debug(result_list)
        self.finishing_time = datetime.now()
        calculation_time = self.finishing_time - self.start_time
        rdh = result_data_handler(self.settings,self.season_data,result_list,calculation_time)
        rdh.calcutlating_results()
        rdh.print_results(write_to_file=True)