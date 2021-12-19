import numpy
import copy

from itertools import combinations

from numpy.core.numeric import outer
from ayto_functions import no_double_names_in_pair_combination, print_list,person_is_not_selected

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
                                "results":{
                                    "calculations":0,
                                    "possible_combinations_cnt":0,
                                    "pairs":{}
                                }
                            }
        self.calc_cnt = 0
        
        
    def iterate_combinations(self,initial_pair,total_possible_pairs):

        selected_pairs = [initial_pair]
        
        self._select_pairs(total_possible_pairs,selected_pairs)

    def test_callback(self):
        self.callback_queue.put(self.get_results())

    def run_callback(self):
        ret_list = []
        ret_list.append(self.get_results())  

        #print(self.callback_queue.qsize())

        self.callback_queue.put(self.get_results())
        self.process_callback()
        del ret_list

    def get_results(self):
        return self.calc_results

    def _select_pairs(self,total_possible_pairs,already_selected_pairs):
        
        
        #print_list(selected_pairs)
        #for pair in selected_pairs:
        #    men,women = pair.split("+")
        #    del men_dict[men]
        #    del women_dict[women]
        

        
        for men in self.men_dict:
            for women in self.women_dict:
                pair = men+"+"+women
                selected_pairs = copy.deepcopy(already_selected_pairs)
               
                    
                if (not self._one_of_pair_is_in_pair_list(pair,selected_pairs)) and self._pair_is_in_pair_list(pair,total_possible_pairs):
                    
                    
                    
                    selected_pairs.append(pair)
                    #if self.output:     
                    #    print("")
                    #    print(pair,end=" ")
                    #    print("possible")
                    #    print_list(selected_pairs)
                        
                        
                    if len(selected_pairs) < self.pairs_per_matching_night:
                        #if self.output:
                        #    #print_list(selected_pairs)
                        #    pass
                        self._select_pairs(total_possible_pairs,selected_pairs)
                        
                        
                    else:
                       
                        self._check_combination(selected_pairs)
                        #if self.output:
                        #    print_list(selected_pairs)
                        #    pass
                #else:
                #    if self.output:
                        
                            
                        #print(pair,end=" ")
                        #print("not possible")
               
    
    def _check_combination(self,selected_pairs):
        self.calc_results["results"]["calculations"] += 1


        if self.calc_results["results"]["calculations"] > 10000:
            cntstr = str(self.calc_results["results"]["calculations"])
            cntstr_len = len(cntstr)
            str2 = cntstr
            last_int = 0
            second_last_int = 0
            third_last_int = 0
            fourth_last_int = 0
            for char in cntstr:
                fourth_last_int = third_last_int
                third_last_int = second_last_int
                second_last_int = last_int
                last_int = int(char)
    
            #print(cntstr + " "+ str(second_last_int) + " " + str(last_int))
            
            if second_last_int == 0 and last_int == 0 and third_last_int == 0 and fourth_last_int == 0:
                #print("Process: " + str(self.process_number) + " Calculations: " + str(self.calc_results["results"]["calculations"]) + " Possible combinations: " + str(self.calc_results["results"]["possible_combinations_cnt"]))
                # run callback
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
                if self._pair_is_in_pair_list(pair_entry,matching_night_pairs):
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
        if self._key_is_in_dict(input_pair,self.calc_results["results"]["pairs"]):
            
            self.calc_results["results"]["pairs"][input_pair] += 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])
        else:
            
            self.calc_results["results"]["pairs"][input_pair] = 1
            if output:
                print(self.calc_results["results"]["pairs"][input_pair])


    def _pair_is_in_pair_list(self,input_pair, input_pair_list):
        for pair_entry in input_pair_list:
            if pair_entry == input_pair:
                return True
        return False

    def _one_of_pair_is_in_pair_list(self,input_pair,input_pair_list):
        input_pair_men,input_pair_women = input_pair.split("+")
        for pair in input_pair_list:
            pair_men,pair_women = pair.split("+")
            if pair_men == input_pair_men or pair_women == input_pair_women:
                return True
        return False

    
        

       
     

    def _key_is_in_dict(self,input_key, input_dict):
        for key in input_dict:
            if key == input_key:
                return True
        return False
