from datetime import datetime
import os
import logging
import time
import ayto_functions as ayto
from calculation_daemon import calculation_daemon

class ayto_calculator:
    def __init__(self):
        self.settings = ayto.load_settings()

        # =========================================================
        # logger configuration
        logging_level = logging.INFO
        if self.settings["logging"] == "debug":
            logging_level = logging.DEBUG
        #logging_level = logging.DEBUG
        #logging_level = logging.INFO
        #logging_level = logging.ERROR
        #logging_level = logging.CRITICAL

        timecode = time.strftime("%Y-%m-%d_%H:%M")
        logging_filename = "./logs/"+timecode+".log"
        logging.basicConfig(filename=logging_filename,level=logging_level,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('ayto_calculator')
        # =========================================================
        # loading the season data
        try:
            self.season_data = ayto.load_season_data(self.settings["season_name"],self.settings["matching_night_data"])
            self.logger.debug("Season data loaded")
        except:
            self.logger.critical("Loading season data failed - exit")
            exit()

        
        
        
        self.seeding_pairs = self._create_seeding_information()
        self.seeding_pairs = self._add_PM_to_seeding_information(self.seeding_pairs)
        

        
        daemon = calculation_daemon(self.settings,self.season_data,self.seeding_pairs)
        self.logger.info("Starting calculation")
        daemon.start_clalculation()
        self.logger.info("Calculation finished")

        #data_handler.print_results(write_to_file=True)

   

    def _create_seeding_information(self):
        primary_gender = None
        secondary_gender = None

        if len(self.season_data["additional_men"]) <= len(self.season_data["additional_women"]):
            primary_gender = "men"
            secondary_gender = "women"
        else:
            primary_gender = "women"
            secondary_gender = "men"

        self.logger.debug("Primary gender: " + primary_gender)

        secondary_gender_person_cnt = len(self.season_data[secondary_gender]) + len(self.season_data["additional_"+secondary_gender])

        possible_primary_pairs = {}
        for person in self.season_data[primary_gender]:
            possible_primary_pairs[person] = secondary_gender_person_cnt   



        for pair in self.season_data["perfect_matches"]:
            men_name,women_name = str(pair).split("+")
            if primary_gender == "men":
                possible_primary_pairs[men_name] -= 1
            else:
                possible_primary_pairs[women_name] -= 1

        for pair in self.season_data["no_matches"]:
            men_name,women_name = str(pair).split("+")
            if primary_gender == "men":
                possible_primary_pairs[men_name] -= 1
            else:
                possible_primary_pairs[women_name] -= 1


        first_person = None
        first_person_possible_pairs = 0
        second_person = None
        second_person_possible_pairs = 0


        for person in possible_primary_pairs:
            possible_pairs_of_person = possible_primary_pairs[person]
            if possible_pairs_of_person > first_person_possible_pairs:

                second_person = first_person
                second_person_possible_pairs = first_person_possible_pairs

                first_person = str(person)
                first_person_possible_pairs = possible_pairs_of_person

            elif possible_pairs_of_person > second_person_possible_pairs:

                second_person = str(person)
                second_person_possible_pairs = possible_pairs_of_person
            

        self.logger.debug("First person: " + first_person)
        self.logger.debug("Second person: " + second_person)

        seeding_pairs = []
        for person_1 in self.season_data[secondary_gender]:
            first_pair = ""
            if primary_gender == "men":
                first_pair = first_person+"+"+str(person_1)
            else:
                first_pair = str(person_1)+"+"+first_person
            if (not ayto.pair_is_in_pair_list(first_pair,self.season_data["perfect_matches"])) and (not ayto.pair_is_in_pair_list(first_pair,self.season_data["no_matches"])):
                for person_2 in self.season_data[secondary_gender]:
                    second_pair = ""
                    if primary_gender == "men":
                        second_pair = second_person+"+"+str(person_2)
                    else:
                        second_pair = str(person_2)+"+"+second_person
                    
                    if (person_2 != person_1) and (not ayto.pair_is_in_pair_list(second_pair,self.season_data["perfect_matches"])) and (not ayto.pair_is_in_pair_list(second_pair,self.season_data["no_matches"])):

                        seeding_pairs.append([first_pair,second_pair])

        return seeding_pairs

    def _add_PM_to_seeding_information(self,seeding_pairs):
        seeding_pair_list = []
        for pair_combination in seeding_pairs:
            for pair in self.season_data["perfect_matches"]:
                pair_combination.append(pair)
            seeding_pair_list.append(pair_combination)
        return seeding_pair_list



if __name__ == "__main__":
    logs_folder = "./logs"
        
    try:
        os.mkdir(logs_folder)
    except OSError:
        pass

    ayto_c = ayto_calculator()
            


            