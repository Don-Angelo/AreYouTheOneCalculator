from numpy.lib.twodim_base import triu_indices_from


def no_double_names_in_pair_combination(pair_combination):
    includet_men = []
    includet_women = []
    for pair in pair_combination:

        men,women = pair.split("+")
        if men not in includet_men:
            includet_men.append(men)
        else:
            return False

        if women not in includet_women:
            includet_women.append(women)
        else:
            return False
    
    return True

def print_list(list):
    for entry in list:
        print(entry,end=" ")
    print("")

def one_of_pair_is_in_pair_list(input_pair,input_pair_list):
    input_pair_men,input_pair_women = input_pair.split("+")
    return_pair_list=[]
    for pair in input_pair_list:
        pair_men,pair_women = pair.split("+")
        if (pair_men == input_pair_men) and (pair_women == input_pair_women):
            return True

    return False

def remove_each_of_pair_from_pair_list(input_pair,input_pair_list):
    input_pair_men,input_pair_women = input_pair.split("+")
    return_pair_list=[]
    for pair in input_pair_list:
        pair_men,pair_women = pair.split("+")
        if (pair_men != input_pair_men) and (pair_women != input_pair_women):
            return_pair_list.append(pair)

    return return_pair_list

def person_is_not_selected(input_pair,input_pair_list):
    input_pair_men,input_pair_women = input_pair.split("+")
    for pair in input_pair_list:
        pair_men,pair_women = pair.split("+")
        if pair_men == input_pair_men or pair_women == input_pair_women:
            return False

    return True

def alter_string(spaces_before,input_string,spaces_after):
    return spaces_before + input_string + spaces_after

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

def print_table(men_dict,women_dict,pair_dict,process_result_dict):
    pass

def percent_string(double_val):
    result = str(double_val)

    pre,after = result.split(".")
    if len(after) < 2:
        after = after + "0"
    
    result = pre+","+after+" %"
    return result

