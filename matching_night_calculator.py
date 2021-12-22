import copy
import logging
import time
import ayto_functions as ayto


class matching_night_calculator:
    def __init__(self,season_data,total_possible_pairs,process_number,client_logger):
        self.men_dict = season_data["men"]
        self.women_dict = season_data["women"]
        self.perfect_matches = season_data["perfect_matches"]
        self.no_matches = season_data["no_matches"]
        self.matching_nights = season_data["matching_nights"]

        self.pairs_per_matching_night = min(len(self.men_dict),len(self.women_dict))
        self.process_number = process_number

        self.total_possible_pairs = total_possible_pairs

        self.logger = client_logger

        self.calc_results = {
                                "results":{
                                    "calculations":0,
                                    "possible_combinations_cnt":0,
                                    "pairs":{}
                                }
                            }
        self.calc_cnt = 0
        
        
    def iterate_combinations(self,initial_combination,possible_men_dict,possible_women_dict):
        #self.calc_results["results"]["max_init_pairs"] = len(initial_pairs)
        selected_pairs = copy.deepcopy(initial_combination)
        possible_men = []
        possible_women = []

        for men_name in possible_men_dict:
            possible_men.append(str(men_name))

        for women_name in possible_women_dict:
            possible_women.append(str(women_name))

        for pair in initial_combination:
            men_name,women_name = str(pair).split("+")
            possible_men = ayto.remove_person_from_person_list(men_name,possible_men)
            possible_women = ayto.remove_person_from_person_list(women_name,possible_women)

        self._select_pairs(selected_pairs,possible_men,possible_women,0)
        #self.logger.debug("Process " + str(self.process_number) + " start iteraring")
        #self._select_pairs(copy.deepcopy(possible_pairs),copy.deepcopy(initial_combination),0)


    def get_results(self):
        return self.calc_results

    
    def _select_pairs(self,already_selected_pairs,possible_men_input,possible_women_input,depth):
        depth += 1
        #print_list(selected_pairs)
        #for pair in selected_pairs:
        #    men,women = pair.split("+")
        #    del men_dict[men]
        #    del women_dict[women]

        possible_men = copy.deepcopy(possible_men_input)
        possible_women = copy.deepcopy(possible_women_input)
        #print(str(depth)+" Already selected: " +str(already_selected_pairs))
        #print(str(depth)+" Possible: "+str(input_possible_pairs))
        men_name = possible_men[0]
        for women_name in possible_women:
            pair = str(men_name)+"+"+str(women_name)
            if pair in self.total_possible_pairs:
                selected_pairs = copy.deepcopy(already_selected_pairs)
                selected_pairs.append(pair)
                if len(selected_pairs) < self.pairs_per_matching_night:
                    possible_men_copy = copy.deepcopy(possible_men)
                    possible_women_copy = copy.deepcopy(possible_women)
                    possible_men_copy = ayto.remove_person_from_person_list(men_name,possible_men_copy)
                    possible_women_copy = ayto.remove_person_from_person_list(women_name,possible_women_copy)
                    selected_pairs_copy = copy.deepcopy(selected_pairs)
                    self._select_pairs(selected_pairs_copy,possible_men_copy,possible_women_copy,depth)
                else:
                    #print(selected_pairs)
                    self._check_combination(selected_pairs)


    
         
    
    def _check_combination(self,selected_pairs):
        
        self.calc_results["results"]["calculations"] += 1
        #print(str(self.calc_results["results"]["calculations"]) + " " +str(self.calc_results["callback_value"])+ " " +str(selected_pairs))
        #self.calc_results["callback_value"] -= 1
        #if self.calc_results["callback_value"] <= 0:
        #    self.calc_results["callback_value"] = 100000
        #    self.callback_queue.put(self.get_results())


        valid_matching_nights = 0

        for matching_night_id in self.matching_nights:
            matching_night = self.matching_nights[matching_night_id]
            matching_night_pairs = matching_night["pairs"]
            matching_night_spots = matching_night["spots"]
      

            hit_spots = 0
            for pair_entry in selected_pairs:
                if ayto.pair_is_in_pair_list(pair_entry,matching_night_pairs):
                    hit_spots += 1

            if hit_spots == matching_night_spots:
                valid_matching_nights += 1

        if valid_matching_nights == len(self.matching_nights):
            
            self._combination_valid(selected_pairs)
     
    
    def _combination_valid(self,selected_pairs):
        self.calc_results["results"]["possible_combinations_cnt"] += 1
        

        for pair_entry in selected_pairs:
            self._add_pair_to_result(pair_entry)
    

    def _add_pair_to_result(self,input_pair):
        output = False
        if ayto.key_is_in_dict(input_pair,self.calc_results["results"]["pairs"]):
            
            self.calc_results["results"]["pairs"][input_pair] += 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])
        else:
            
            self.calc_results["results"]["pairs"][input_pair] = 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])


