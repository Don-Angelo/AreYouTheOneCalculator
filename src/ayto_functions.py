import os
import json

def load_settings():
    f = open("settings.json")
    settings = json.load(f)
    f.close()
    return settings

def load_season_data(season_name,matching_night_data):
    filename_full = "./data/"+season_name+"/"+matching_night_data+".json"
    f = open(filename_full)
    season_data = json.load(f)
    f.close()
    return season_data

def remove_person_from_person_list(person_name_input,person_list_input):
    person_list = []
    for person_name in person_list_input:
        if person_name != person_name_input:
            person_list.append(person_name)
    return person_list    
    
def get_total_possible_pairs(season_data):
    total_possible_pairs = []
    for men in season_data["men"]:
        for women in season_data["women"]:
            pair = men + "+" + women
            if pair not in season_data["no_matches"]:
                total_possible_pairs.append(pair)
    
    for men in season_data["additional_men"]:
        for women in season_data["women"]:
            pair = men + "+" + women
            if pair not in season_data["no_matches"]:
                total_possible_pairs.append(pair)
        for women in season_data["additional_women"]:
            pair = men + "+" + women
            if pair not in season_data["no_matches"]:
                total_possible_pairs.append(pair)

    for women in season_data["additional_women"]:
        for men in season_data["men"]:
            pair = men + "+" + women
            if pair not in season_data["no_matches"]:
                total_possible_pairs.append(pair)
        for men in season_data["additional_men"]:
            pair = men + "+" + women
            if pair not in season_data["no_matches"]:
                total_possible_pairs.append(pair)

    return total_possible_pairs

def pair_is_in_pair_list(input_pair, input_pair_list):
        for pair_entry in input_pair_list:
            if pair_entry == input_pair:
                return True
        return False

def fixed_string(input_string,lenght):
    in_str = input_string
    while len(in_str) < lenght:
        in_str = " " + in_str
    return in_str

def pair_is_in_pair_list(input_pair, input_pair_list):
    for pair_entry in input_pair_list:
        if pair_entry == input_pair:
            return True
    return False

def key_is_in_dict(input_key,input_dict):
        for key in input_dict:
            if key == input_key:
                return True
        return False 

def percent_string(double_val):
    result = str(double_val)

    pre,after = result.split(".")
    if len(after) < 2:
        after = after + "0"
    
    result = pre+","+after+" %"
    return result

def clear_console():
    if os.name in ('nt', 'dos'): 
        os.system('cls')
    else:
        os.system('clear')