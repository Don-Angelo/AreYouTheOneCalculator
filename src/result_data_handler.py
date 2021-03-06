import os
import datetime
import ayto_functions as ayto

class result_data_handler:
    def __init__(self,settings):
        self.settings = settings
        self.season_data = ayto.load_season_data(self.settings["season_name"],self.settings["matching_night_data"])
        self.calculations = 0
        self.possible_combinations = 0
        self.result_data = {
            "calculations": 0,
            "possible_combinations":0,
            "pairs":{}
        }

    def calcutlating_results(self,result_data_list):
        result_data = {
            "calculations": 0,
            "possible_combinations":0,
            "pairs":{}
        }
        for result_entry in result_data_list:
            result = result_entry["results"]

            result_data["calculations"] += result["calculations"]
            result_data["possible_combinations"] += result["possible_combinations"]

            for pair in result["pairs"]:
                if ayto.key_is_in_dict(pair,result_data["pairs"]):
                    result_data["pairs"][pair] += result["pairs"][pair]
                else:
                    result_data["pairs"][pair] = result["pairs"][pair]

        return result_data

    def build_results(self,result_data,pre_lines=[""],after_lines=[""]):
        men_list = self.season_data["men"]
        for men in self.season_data["additional_men"]:
            if men not in men_list:
                men_list.append(men)
        women_list = self.season_data["women"]
        for women in self.season_data["additional_women"]:
            if women not in women_list:
                women_list.append(women)

        result_pairs = result_data["pairs"]

        lines = []
        for line in pre_lines:
            lines.append(line)
        
        lines.append("Checked  combinations: " + str(result_data["calculations"]))
        lines.append("Possible combinations: " + str(result_data["possible_combinations"]))
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
                    calc_val = round(((result_pairs[pair]/result_data["possible_combinations"])*100),2)
                    value_string = ayto.percent_string(calc_val)
                    men_line = men_line + "  " + ayto.fixed_string(value_string,max_len_women)
                else:
                    men_line = men_line + "  " + ayto.fixed_string("X  ", max_len_women)

            lines.append(men_line)
        for line in after_lines:
            lines.append(line)
        lines.append("")

        return lines

        
        
    def print_results(self,result_lines):
        for line in result_lines:
            print(line)

    def write_results(self,result_lines):
        time = datetime.datetime.now()
        date = time.strftime("%Y-%m-%d")
        folder = time.strftime("%Y")
        result_folder = "./results/"+self.settings["season_name"]
        filename = result_folder+"/"+self.settings["season_name"]+"_"+"result_"+self.settings["matching_night_data"]+".txt"

        try:
            os.mkdir(result_folder)
        except OSError:
            pass
        
        f = open(filename, "a")
        for line in result_lines:
            f.write(line)
            f.write("\n")