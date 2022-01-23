import os
import datetime
import ayto_functions as ayto

class result_data_handler:
    def __init__(self,settings,season_data,result_data_list):
        self.settings = settings
        self.season_data = season_data
        self.result_data_list = result_data_list
        self.calculations = 0
        self.possible_combinations = 0
        self.result_data = {
            "calculations": 0,
            "possible_combinations":0,
            "pairs":{}
        }

    def calcutlating_results(self):
        for result_entry in self.result_data_list:
            result = result_entry["results"]

            self.result_data["calculations"] += result["calculations"]
            self.result_data["possible_combinations"] += result["possible_combinations"]

            for pair in result["pairs"]:
                if ayto.key_is_in_dict(pair,self.result_data["pairs"]):
                    self.result_data["pairs"][pair] += result["pairs"][pair]
                else:
                    self.result_data["pairs"][pair] = result["pairs"][pair]

    def print_results(self,write_to_file = False):
        men_list = self.season_data["men"]
        for men in self.season_data["additional_men"]:
            men_list.append(men)
        women_list = self.season_data["women"]
        for women in self.season_data["additional_women"]:
            women_list.append(women)

        result_pairs = self.result_data["pairs"]

        lines = []
        lines.append("Checked  combinations: " + str(self.result_data["calculations"]))
        lines.append("Possible combinations: " + str(self.result_data["possible_combinations"]))
        lines.append("")

        pair_list = []
        no_match_list = []
        perfect_match_list = []



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
                    calc_val = round(((result_pairs[pair]/self.result_data["possible_combinations"])*100),2)
                    value_string = ayto.percent_string(calc_val)
                    men_line = men_line + "  " + ayto.fixed_string(value_string,max_len_women)
                else:
                    men_line = men_line + "  " + ayto.fixed_string("X  ", max_len_women)

            lines.append(men_line)

        lines.append("")

        ayto.clear_console()
        for line in lines:
            print(line)

        if write_to_file:
            time = datetime.datetime.now()
            date = time.strftime("%Y-%m-%d")
            folder = time.strftime("%Y")
            result_folder = "./results/"+folder
            filename = result_folder+"/"+self.settings["season_data_name"]+"_"+"result_"+date+".txt"

            try:
                os.mkdir(result_folder)
            except OSError:
                pass
            
            f = open(filename, "w")
            for line in lines:
                f.write(line)
                f.write("\n")
        
