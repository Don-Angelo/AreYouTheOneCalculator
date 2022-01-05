import json
import os
import datetime
import ayto_functions as ayto
from multiprocessing import Queue


class calculation_data_handler:
    def __init__(self):
        self.settings = ayto.load_settings()
        self.season_data = ayto.load_season_data(self.settings["season_data_name"])

        self.calculation_data_queue = Queue()
        self.result_data_queue = Queue()

        self.server_data = ayto.load_server_data()


        for entry in self.server_data["seeding_pairs"]:
            if entry not in self.server_data["finished_pairs"]:
                self.calculation_data_queue.put(entry)

        self.calculation_running = True
        if len(self.server_data["seeding_pairs"])==0:
            self.calculation_running = False


        try:
            self.result_data = ayto.load_result_data()
        except:
            self.result_data = {
                "calculations": 0,
                "possible_combinations_cnt":0,
                "pairs":{}
            }
            ayto.write_result_data(self.result_data)


    def get_calculation_data(self):
        return_data = {}
        if self.calculation_data_queue.empty():
            return_data["finished"] = True
        else:
            return_data["finished"] = False
            return_data["seeding_combination"] = self.calculation_data_queue.get()
        return return_data

    def insert_result_data(self,data):
        self.result_data_queue.put(data)
        self._update_results()

    def _update_results(self):
        client_response = self.result_data_queue.get()
        #print(client_response)
        client_result = client_response["results"]
        self.result_data["calculations"] += client_result["calculations"]
        self.result_data["possible_combinations_cnt"] += client_result["possible_combinations_cnt"]
        for pair in client_result["pairs"]:
            if ayto.key_is_in_dict(pair,self.result_data["pairs"]):
                self.result_data["pairs"][pair] += client_result["pairs"][pair]
            else:
                self.result_data["pairs"][pair] = client_result["pairs"][pair]

        self.server_data["finished_pairs"].append(client_response["init_combination"])
        self.server_data["seeding_pairs"].remove(client_response["init_combination"])
        

        ayto.write_server_data(self.server_data)
        ayto.write_result_data(self.result_data)

        if len(self.server_data["seeding_pairs"]) == 0:
            self.calculation_running = False
            print("Calculation finished \n")
        self.print_results()

        if not self.result_data_queue.empty():
            self._update_results()

        if self.calculation_running == False:
            os.remove("./cache/result_data.cache")
            os.remove("./cache/server_data.cache")
            
    def print_results(self):
        men_dict = self.season_data["men"]
        women_dict = self.season_data["women"]
        result_pairs = self.result_data["pairs"]

        lines = []
        lines.append("Seeding pairs cnt: " + str(len(self.server_data["seeding_pairs"]))+"/"+str(len(self.server_data["seeding_pairs"])+len(self.server_data["finished_pairs"])))
        lines.append("Checked  combinations: " + str(self.result_data["calculations"]))
        lines.append("Possible combinations: " + str(self.result_data["possible_combinations_cnt"]))
        lines.append("")

        men_list = []
        women_list = []
        pair_list = []
        no_match_list = []
        perfect_match_list = []

        for men in men_dict:
            men_name = str(men)
            men_list.append(men_name)
        
        for women in women_dict:
            women_name = str(women)
            women_list.append(women_name)

        for pair in result_pairs:
            pair_name = str(pair)
            pair_list.append(pair_name)

        for pair in self.season_data["no_matches"]:
            pair_name = str(pair)
            no_match_list.append(pair_name)

        for pair in self.season_data["perfect_matches"]:
            pair_name = str(pair)
            perfect_match_list.append(pair_name)


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


        women_line = ayto.fixed_string("  ",max_len_men)
        for women in women_list:
            women_line = women_line + "  " + ayto.fixed_string(women,max_len_women)

        lines.append(women_line)



        for men in men_list:
            men_line = ayto.fixed_string(men,max_len_men)

            for women in women_list:

                pair = men+"+"+women
                if pair in perfect_match_list:
                    men_line = men_line + "  " + ayto.fixed_string("PM  ",max_len_women)
                elif pair in no_match_list:
                    men_line = men_line + "  " + ayto.fixed_string("NM  ",max_len_women)
                elif pair in pair_list:
                    calc_val = round(((result_pairs[pair]/self.result_data["possible_combinations_cnt"])*100),2)
                    value_string = ayto.percent_string(calc_val)
                    men_line = men_line + "  " + ayto.fixed_string(value_string,max_len_women)
                else:
                    men_line = men_line + "  " + ayto.fixed_string("X  ", max_len_women)

            lines.append(men_line)

        lines.append("")

        ayto.clear_console()
        for line in lines:
            print(line)

        if not self.calculation_running:
            time = datetime.datetime.now()
            date = time.strftime("%Y-%m-%d")
            folder = time.strftime("%Y")
            result_folder = "./results/"+folder
            filename = result_folder+"/"+self.settings["season_data_name"]+"_"+"result_"+date+".txt"

            try:
                os.mkdir(result_folder)
            except OSError:
                print ("Creation of the directory %s failed" % result_folder)

            f = open(filename, "w")
            for line in lines:
                f.write(line)
                f.write("\n")

  
        
