import os
import logging
import ayto_functions as ayto
import multiprocessing as mp
from matching_night_calculator import matching_night_calculator
from result_data_handler import result_data_handler

class calculation_daemon:
    def __init__(self,settings,season_data):
        self.settings = settings
        self.season_data = season_data

        self.total_possible_pairs = ayto.get_total_possible_pairs(self.season_data)

        self.logger = logging.getLogger("calculation_daemon")

        

    def _process_function(self,process_arguments):
        process_id = os.getpid()

        seeding_pair_combination = process_arguments[0]
        combination_len = process_arguments[1]
        result_data = None
        print("Process " + str(process_id) + " calculating " + str(seeding_pair_combination))

        if combination_len == 10:
            mnc = matching_night_calculator(self.season_data,self.total_possible_pairs,process_id)
            mnc.iterate_10_pair_combinations(seeding_pair_combination)
            result_data = mnc.get_results()
        elif combination_len == 11:
            mnc = matching_night_calculator(self.season_data,self.total_possible_pairs,process_id)
            mnc.iterate_11_pair_combinations(seeding_pair_combination)
            result_data = mnc.get_results()
            

            
        return result_data


    def start_clalculation(self,seeding_pairs,combination_len):
        process_count = mp.cpu_count()
        self.logger.debug("Running with " + str(process_count) + " processes")
        
        result_list = []

        if self.settings["multiprocessing"]:
  
           
            process_arguments = []
            for pair_combination in seeding_pairs:
                process_data = (pair_combination,combination_len)
                process_arguments.append(process_data)
            
       
            pool = mp.Pool(process_count)
            result_list = pool.map(self._process_function,process_arguments)
            

      
        else:
            result_list.append(self._process_function((seeding_pairs[0],combination_len)))
        self.logger.debug(result_list)
        
        return result_list