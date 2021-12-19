import itertools
import json
import copy
import math
import datetime
import multiprocessing as mp
from multiprocessing import Queue
from itertools import combinations
import numpy
import time


from ayto_functions import no_double_names_in_pair_combination,remove_each_of_pair_from_pair_list,fixed_string,key_is_in_dict,percent_string


import matching_night_calculator


# copy that shit
# data = {}
# data["men_dict"] = copy.deepcopy(season_data["men"])

# Function to create combinations
# without itertools

original_data = None
process_result_dict = {}
system_info_dict = {}
callback_queue = Queue()
start_time = None

def print_results():
    actual_time = datetime.datetime.now()
    delta_time = actual_time - start_time
    men_dict = original_data["men"]
    women_dict = original_data["women"]

    total_calculations_cnt = 0
    possible_combinations_cnt = 0
    result_pairs = {}


    for process_result in process_result_dict:
        
        process_number = int(process_result)

        result_dict = process_result_dict[process_number]
        if len(result_dict) > 0:
            total_calculations_cnt += result_dict["calculations"]
            possible_combinations_cnt += result_dict["possible_combinations_cnt"]

            for pair in result_dict["pairs"]:
                if _key_is_in_dict(pair,result_pairs):
                    result_pairs[pair] += result_dict["pairs"][pair]
                else:
                    result_pairs[pair] = result_dict["pairs"][pair]
    lines = []
    lines.append("")
    lines.append("")
    lines.append("Checked  combinations: " + str(total_calculations_cnt))
    lines.append("Possible combinations: " + str(possible_combinations_cnt))
    lines.append("Calculation duration: "  + str(delta_time))
    lines.append("")
    for i in range(len(process_result_dict)):
        if len(process_result_dict[i])>0:
            lines.append("Process: " + str(i) + "  Calculations: " +str(process_result_dict[i]["calculations"])+ "  Possible combinations found: " + str(process_result_dict[i]["possible_combinations_cnt"]))
    lines.append("")

    men_list = []
    women_list = []
    pair_list = []

    for men in men_dict:
        men_name = str(men)
        men_list.append(men_name)
    
    for women in women_dict:
        women_name = str(women)
        women_list.append(women_name)

    for pair in result_pairs:
        pair_name = str(pair)
        pair_list.append(pair_name)


    max_table_entry = "100.00%"
    max_len_table_entry = len(max_table_entry)
    max_len_men = 0
    max_len_women = 0

    for men in men_list:
        men_len = len(men)

        if men_len > max_len_men:
            max_len_men = men_len
    
    if max_len_men < max_len_table_entry:
        max_len_men = max_len_table_entry
    
    

    for women in women_list:
        women_len = len(women)
        if women_len > max_len_women:
            max_len_women = women_len

    if max_len_women < max_len_table_entry:
        max_len_women = max_len_table_entry


    women_line = fixed_string("  ",max_len_men)
    for women in women_list:
        women_line = women_line + "  " + fixed_string(women,max_len_women)

    lines.append(women_line)



    for men in men_list:
        men_line = fixed_string(men,max_len_men)

        for women in women_list:

            pair = men+"+"+women
            
            if pair in pair_list:
                calc_val = round(((result_pairs[pair]/possible_combinations_cnt)*100),2)
                value_string = percent_string(calc_val)
                men_line = men_line + "  " + fixed_string(value_string,max_len_women)
            else:
                men_line = men_line + "  " + fixed_string(" ", max_len_women)

        lines.append(men_line)

    


    for line in lines:
        print(line)
    
    time = datetime.datetime.now()
    date = time.strftime("%Y-%m-%d")
    folder = time.strftime("%Y")
    filename = "./results/"+folder+"/"+season_info+"_"+"result_"+date+".txt"

    f = open(filename, "w")
    for line in lines:
        f.write(line)
        f.write("\n")
    

    


    #for i in range(len(process_result_dict)):
    #    if len(process_result_dict[i])>0:
    #        print("Process: " + str(i) + "  Calculations: " +str(process_result_dict[i]["calculations"])+ "  Possible combinations: " + str(process_result_dict[i]["possible_combinations_cnt"]))
    #print("")
    #for men in original_data["men"]:
    #    for pair in result_pairs:
    #        men_name,women_name = pair.split("+")
    #        if men == men_name:
    #            calc_val = round(((result_pairs[pair]/possible_combinations_cnt)*100),2)
    #            print(pair + " (" + str(calc_val) + "%)")

def update_values():
    #print("proc num")
    try: 
        callback_dict = callback_queue.get()
        process_number = callback_dict["process_number"]
        process_results = callback_dict["results"]
        process_result_dict[process_number] = process_results
        #print(process_result_dict)
        if callback_queue.empty():
            print_results()
            pass
        else:
            update_values()
    except:
        pass
    
    


def process_function(data):
    process_number = copy.deepcopy(data[0])
    original_data = copy.deepcopy(data[1])
    initial_pairs = copy.deepcopy(data[2])
    total_possible_pairs = copy.deepcopy(data[3])
    


    mn = matching_night_calculator.matching_night_calculator(original_data["men"],original_data["women"],original_data["perfect_matches"],original_data["no_matches"],original_data["matching_nights"],process_number,callback_queue)
    
    for i in range(len(initial_pairs)):
        pair = initial_pairs[i]
    
        possible_pairs = remove_each_of_pair_from_pair_list(pair,total_possible_pairs)
        
        mn.iterate_combinations(pair,copy.deepcopy(possible_pairs))
        
        print("Process: " + process_number + " init combinations finished: " + str(i) + "/" + str(len(initial_pairs)))

    process_results = mn.get_results()
    callback_queue.put(process_results)
    return process_results



    



     




def _key_is_in_dict(input_key,input_dict):
        for key in input_dict:
            if key == input_key:
                return True
        return False  

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    

    f = open("settings.json")
    settings = json.load(f)
    season_info = settings["datafile"]
    f.close()
    data_filename = "./data/"+season_info+".json"

    f = open(data_filename)
    season_data = json.load(f)

    original_data = copy.deepcopy(season_data)
    for perfect_match in original_data["perfect_matches"]:
        men_name,women_name = perfect_match.split("+")

        original_data["men"][men_name]["possible_matches"] -= 1
        if original_data["men"][men_name]["possible_matches"] == 0:
            original_data["men"][men_name]["all_matches_found"] = True
        
        original_data["women"][women_name]["possible_matches"] -= 1
        if original_data["women"][women_name]["possible_matches"] == 0:
            original_data["women"][women_name]["all_matches_found"] = True


    total_possible_pairs = []
    for men in original_data["men"]:
        for women in original_data["women"]:
            pair = men + "+" + women
            if pair not in original_data["no_matches"]:

                total_possible_pairs.append(pair)

    total_possible_pairs_cnt = len(total_possible_pairs)
    print("Total possible pairs: "+str(total_possible_pairs_cnt))
    system_info_dict["total_possible_pairs_cnt"] = total_possible_pairs_cnt

    total_possible_perfect_matches_cnt = max(len(original_data["men"]),len(original_data["women"]))
    print("Total possible perfect matches: "+ str(total_possible_perfect_matches_cnt))
    system_info_dict["total_possible_perfect_matches_cnt"] = total_possible_perfect_matches_cnt

    found_perfect_matches_cnt = len(original_data["perfect_matches"])
    print("Already found perfect matches: " + str(found_perfect_matches_cnt))
    system_info_dict["found_perfect_matches_cnt"] = found_perfect_matches_cnt

    missing_matches_cnt = total_possible_perfect_matches_cnt-found_perfect_matches_cnt
    print("Missing perfect matches: " +str(missing_matches_cnt))
    system_info_dict["missing_matches_cnt"] = missing_matches_cnt

    process_count = mp.cpu_count()
    print("Paralel processes: " +str(process_count))
    system_info_dict["process_count"] = process_count

    initial_pairs_per_process = int(round((total_possible_pairs_cnt/process_count),0))

    process_arguments = []
    combination_offset = 0
    for i in range(process_count):
        

        combination_start = combination_offset
        combination_end = combination_start + initial_pairs_per_process 
        if i == process_count-1:
            combination_end = total_possible_pairs_cnt

        #print("Process " + str(i),end=" ")
        #print("Start =" + str(combination_offset),end=" ")
        #print("End = " + str(combination_end))
        combination_offset = combination_end 
        initial_pairs = total_possible_pairs[combination_start:combination_end]
        #print(len(initial_pairs))

        process_data = (i,original_data,initial_pairs,total_possible_pairs)
        process_arguments.append(process_data)

        
    

    pool = mp.Pool(process_count)
    result_list = pool.map_async(process_function,process_arguments)
    pool.close()

    #pool.join()

    while True:
        #
        time.sleep(5)
        if not callback_queue.empty():
            update_values()
        if result_list.ready():
            update_values()
            break

    print("")
    print("Calculation done")
    print("")
    print_results()
    

    #for pair in total_possible_pairs:
    #    print(pair)
    #pair_combination_calculator(total_possible_pairs,min(len(original_data["men"]),len(original_data["women"])))

    #result = n_length_combo(["a","b","c","d","e","f","g","h"],3)
    #for r in result:
    #    print(r)
    #comb = combinations(total_possible_pairs, missing_matches_cnt)
    #possible_combination_list = list(comb)

    #print(len(possible_combination_list))



 


    """

    mnc = matching_night_calculator.matching_night_calculator(original_data["men"],original_data["women"],original_data["perfect_matches"],original_data["no_matches"],original_data["matching_nights"])
    init_combinations, init_results = mnc.search_init_combinations()
    print(str(len(init_combinations))+ " init combinations")

    process_count = mp.cpu_count()
    combinations_per_process = math.floor(len(init_combinations)/process_count)
    print(str(combinations_per_process) + " combinations per process")


    

    #print(str(results["calculations"]) + " calculations")

    process_arguments = []
    if False:
        for combination in init_combinations:
            process_data = (original_data,combination)
            process_arguments.append(process_data)


    if True:
        # creating all the data packages for all processes
        combination_offset = 0
        for i in range(process_count):
            

            combination_start = combination_offset
            combination_end = combination_start + combinations_per_process 
            if len(init_combinations) - (combination_end) < combinations_per_process:
                combination_end = len(init_combinations) 

            #print("Trhead " + str(i))
            #print("Start =" + str(combination_offset))
            #print("End = " + str(combination_end))
            combination_offset = combination_end 
            process_combinations = init_combinations[combination_start:combination_end]
            #print(len(process_combinations))
            
            process_data = (original_data,process_combinations)

            process_arguments.append(process_data)
    #print(len(process_arguments))

    pool = mp.Pool(process_count)
    a = ("b","d")
    result_list = pool.map(process_function, process_arguments)

    
  
    calculations = init_results["calculations"]
    for result in result_list:
        calculations += result["calculations"]
        
    possible_combinations = init_results["possible_combinations"]
    for result in result_list:
        possible_combinations += result["possible_combinations"]


    result_pairs = {}
    for pair in init_results["pairs"]:
        if _key_is_in_dict(result_pairs,pair):
            result_pairs[pair] += 1
        else:
            result_pairs[pair] = init_results["pairs"][pair]


    i = 0
    for result in result_list:
        i += 1
        for pair in result["pairs"]:
            
            if _key_is_in_dict(result_pairs,pair):
                result_pairs[pair] += result["pairs"][pair]
            else:
                result_pairs[pair] = result["pairs"][pair]


    print("")
    print("Calculation complete")
    print("Number of calculations:" + str(calculations))
    print("Possible combinations:" + str(possible_combinations))
    print("")
    for men in original_data["men"]:
        for pair in result_pairs:
            men_name,women_name = pair.split("+")
            if men == men_name:
                calc_val = round(((result_pairs[pair]/possible_combinations)*100),2)
                print(pair + " (" + str(calc_val) + "%)")

        
    time = datetime.datetime.now()
    date = time.strftime("%Y-%m-%d")
    folder = time.strftime("%Y")
    filename = "./results/"+folder+"/"+season_info+"_"+"result_"+date+".txt"

    f = open(filename, "w")
    f.write("Calculation complete\n")
    f.write("Number of calculations:" + str(calculations)+"\n")
    f.write("Possible combinations:" + str(possible_combinations)+"\n\n")
    for men in original_data["men"]:
        for pair in result_pairs:
            men_name,women_name = pair.split("+")
            if men == men_name:
                calc_val = round(((result_pairs[pair]/possible_combinations)*100),2)
                f.write(pair + " (" + str(calc_val) + "%)\n")

    
    """

    