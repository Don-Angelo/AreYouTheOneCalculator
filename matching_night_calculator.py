import copy
from ayto_functions import remove_each_of_pair_from_pair_list,key_is_in_dict,pair_is_in_pair_list

class matching_night_calculator:
    def __init__(self,men_dict,women_dict,perfect_matches,no_matches,matching_nights,process_number,callback_queue):
        self.men_dict = men_dict
        self.women_dict = women_dict
        self.perfect_matches = perfect_matches
        self.no_matches = no_matches
        self.matching_nights = matching_nights
        self.pairs_per_matching_night = min(len(self.men_dict),len(self.women_dict))
        self.process_number = process_number
        self.callback_queue = callback_queue

        self.calc_results = {   "process_number":self.process_number,
                                
                                "callback_value":10000,
                                "results":{
                                    "init_pair_cnt":0,
                                    "max_init_pairs":0,
                                    "calculations":0,
                                    "possible_combinations_cnt":0,
                                    "pairs":{}
                                }
                            }
        self.calc_cnt = 0
        
        
    def iterate_combinations(self,initial_pairs,total_possible_pairs):
        self.calc_results["results"]["max_init_pairs"] = len(initial_pairs)
        
        for pair in initial_pairs:
            self.calc_results["results"]["init_pair_cnt"] += 1
            
            possible_pairs = copy.deepcopy(total_possible_pairs)
            possible_pairs = remove_each_of_pair_from_pair_list(pair,possible_pairs)
            self._select_pairs(copy.deepcopy(possible_pairs),copy.deepcopy([pair]),0)

    def get_results(self):
        return self.calc_results

    
    def _select_pairs(self,input_possible_pairs,already_selected_pairs,depth):
        depth += 1
        #print_list(selected_pairs)
        #for pair in selected_pairs:
        #    men,women = pair.split("+")
        #    del men_dict[men]
        #    del women_dict[women]

        possible_pairs = copy.deepcopy(input_possible_pairs)
        #print(str(depth)+" Already selected: " +str(already_selected_pairs))
        #print(str(depth)+" Possible: "+str(input_possible_pairs))

        for pair in possible_pairs:
            selected_pairs = copy.deepcopy(already_selected_pairs)
            selected_pairs.append(pair)
            #print(str(depth)+ " Appending " + pair)
            if len(selected_pairs) < self.pairs_per_matching_night:
                possible_pairs_copy = copy.deepcopy(possible_pairs)

                possible_pairs_copy = remove_each_of_pair_from_pair_list(pair,possible_pairs_copy)
                
                selected_pairs_copy = copy.deepcopy(selected_pairs)
            

                self._select_pairs(possible_pairs_copy,selected_pairs_copy,depth)
            else:
                self._check_combination(selected_pairs)
    
         
    
    def _check_combination(self,selected_pairs):
        
        self.calc_results["results"]["calculations"] += 1
        #print(str(self.calc_results["results"]["calculations"]) + " " +str(self.calc_results["callback_value"])+ " " +str(selected_pairs))
        self.calc_results["callback_value"] -= 1
        if self.calc_results["callback_value"] <= 0:
            self.calc_results["callback_value"] = 10000
            self.callback_queue.put(self.get_results())



        #if self.possible_output:
        #    print("Calculations: " + str(self.calc_results["calculations"]),end="\r")

        #if self.possible_output:
        #    print("Start check")
    #    for entry in selected_pairs:
        #        print(entry,end=" ")
        #    pass   
        #    print("")


        valid_matching_nights = 0

        for matching_night_id in self.matching_nights:
            matching_night = self.matching_nights[matching_night_id]
            matching_night_pairs = matching_night["pairs"]
            matching_night_spots = matching_night["spots"]
      

            hit_spots = 0
            for pair_entry in selected_pairs:
                if pair_is_in_pair_list(pair_entry,matching_night_pairs):
                    hit_spots += 1

            #if self.possible_output:
                #print("Hit Spots: " + str(hit_spots),end="    ")
                #for pair in selected_pairs:
                #    print(pair,end=" ")
                #print("")

            if hit_spots == matching_night_spots:
                valid_matching_nights += 1

            #if self.possible_output and valid_matching_nights >0:
            #    line = "Matching night: " +str(matching_night_id)
            #    line = line + " Hit Spots: " + str(hit_spots) +"/"+str(matching_night_spots)+ " Valid matching night: " + str(valid_matching_nights) + "/1   "
            
           ##     for pair in selected_pairs:
            #        line = line + pair + " "
            #    print(line)
               
          

            #if self.possible_output:

                #line = "Hit Spots: " + str(hit_spots) +"/"+str(matching_night_spots)+ " Valid matching night: " + str(valid_matching_nights) + "/1   "
                
                #for pair in selected_pairs:
                #    line = line + pair + " "
                #print(line,end="\r")
        #if self.possible_output:
        #    print(" test")
        if valid_matching_nights == len(self.matching_nights):
            
            self._combination_valid(selected_pairs)
     
    
    def _combination_valid(self,selected_pairs):
        self.calc_results["results"]["possible_combinations_cnt"] += 1
        

        #line = "Process: "+str(self.process_number)+ " Valid combinations: "
        #for pair in selected_pairs:
        #        line = line + pair + " "
        #print(line)
            
            
        #if self.possible_output:
        #    print("Possible: ",end="")
        #    for pair_entry in selected_pairs:
        #            print(pair_entry, end="  ")
        #    print("")

        

        for pair_entry in selected_pairs:
            self._add_pair_to_result(pair_entry)
    

    def _add_pair_to_result(self,input_pair):
        output = False
        if key_is_in_dict(input_pair,self.calc_results["results"]["pairs"]):
            
            self.calc_results["results"]["pairs"][input_pair] += 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])
        else:
            
            self.calc_results["results"]["pairs"][input_pair] = 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])


