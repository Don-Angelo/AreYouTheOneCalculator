import json
import logging
import time
import ayto_functions as ayto

class ayto_server:
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

        timecode = time.strftime("%Y-%m-%d-%H-%M")
        logging_filename = "./logs/server_"+timecode+".log"
        logging.basicConfig(filename=logging_filename,level=logging_level,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('Server')
        # =========================================================

        self.logger.debug("Server started")

        # loading the season data
        try:
            self.season_data = ayto.load_season_data(self.settings["season_data_name"])
            self.logger.debug("Season data loaded")
        except:
            self.logger.critical("Loading season data failed - exit")
            exit()
        
        for perfect_match in self.season_data["perfect_matches"]:
            men_name,women_name = perfect_match.split("+")

            self.season_data["men"][men_name]["possible_matches"] -= 1
            if self.season_data["men"][men_name]["possible_matches"] == 0:
                self.season_data["men"][men_name]["all_matches_found"] = True
            
            self.season_data["women"][women_name]["possible_matches"] -= 1
            if self.season_data["women"][women_name]["possible_matches"] == 0:
                self.season_data["women"][women_name]["all_matches_found"] = True

        try:
            self.seeding_pairs = self._load_seeding_pairs()
            self.logger.debug("Seeding pairs loaded")
        except:
            self.seeding_pairs = self._create_seeding_information()
            self._write_seeding_pairs()
            self.logger.debug("Seeding pairs created and wrote")

        self.seeding_pairs_cnt = len(self.seeding_pairs)
        self.logger.debug("Seeding pairs cnt: " + str(self.seeding_pairs_cnt))

        
        

        for entry in self.seeding_pairs:
            print(entry)


    def _create_seeding_information(self):
        primary_gender = None
        secondary_gender = None

        if len(self.season_data["men"]) <= len(self.season_data["women"]):
            primary_gender = "men"
            secondary_gender = "women"
        else:
            primary_gender = "women"
            secondary_gender = "men"

        self.logger.debug("Primary gender: " + primary_gender)

        secondary_gender_person_cnt = len(self.season_data[secondary_gender])

        primary_dict = {}
        for person in self.season_data[primary_gender]:
            primary_dict[person] = self.season_data[primary_gender][person]
            primary_dict[person]["possible_pairs"] = secondary_gender_person_cnt   



        for pair in self.season_data["perfect_matches"]:
            men_name,women_name = str(pair).split("+")
            if primary_gender == "men":
                primary_dict[men_name]["possible_pairs"] -= 1
            else:
                primary_dict[women_name]["possible_pairs"] -= 1

        for pair in self.season_data["no_matches"]:
            men_name,women_name = str(pair).split("+")
            if primary_gender == "men":
                primary_dict[men_name]["possible_pairs"] -= 1
            else:
                primary_dict[women_name]["possible_pairs"] -= 1


        first_person = None
        first_person_possible_pairs = 0
        second_person = None
        second_person_possible_pairs = 0
        third_person = None
        third_person_possible_pairs = 0

        for person in primary_dict:
            possible_pairs_of_person = primary_dict[person]["possible_pairs"]
            if possible_pairs_of_person > first_person_possible_pairs:
                third_person = second_person
                third_person_possible_pairs = second_person_possible_pairs

                second_person = first_person
                second_person_possible_pairs = first_person_possible_pairs

                first_person = str(person)
                first_person_possible_pairs = possible_pairs_of_person

            elif possible_pairs_of_person > second_person_possible_pairs:
                third_person = second_person
                third_person_possible_pairs = second_person_possible_pairs

                second_person = str(person)
                second_person_possible_pairs = possible_pairs_of_person
            
            elif possible_pairs_of_person > third_person_possible_pairs:
                third_person = str(person)
                third_person_possible_pairs = possible_pairs_of_person

        self.logger.debug("First person: " + first_person)
        self.logger.debug("Second person: " + second_person)
        self.logger.debug("Third person: " + third_person)

        seeding_pairs = []
        for person_1 in self.season_data[secondary_gender]:
            first_pair = ""
            if primary_gender == "men":
                first_pair = first_person+"+"+str(person_1)
            else:
                first_pair = str(person_1)+"+"+first_person
            if not ayto.pair_is_in_pair_list(first_pair,self.season_data["perfect_matches"]):
                for person_2 in self.season_data[secondary_gender]:
                    second_pair = ""
                    if primary_gender == "men":
                        second_pair = second_person+"+"+str(person_2)
                    else:
                        second_pair = str(person_2)+"+"+second_person
                    
                    if (person_2 != person_1) and (not ayto.pair_is_in_pair_list(second_pair,self.season_data["perfect_matches"])):

                        for person_3 in self.season_data[secondary_gender]:
                            third_pair = ""
                            if primary_gender == "men":
                                third_pair = third_person+"+"+str(person_3)
                            else:
                                third_pair = str(person_3)+"+"+third_person

                            if (person_3 != person_2) and (person_3 != person_1) and (not ayto.pair_is_in_pair_list(second_pair,self.season_data["perfect_matches"])):
                                seeding_pairs.append([first_pair,second_pair,third_pair])

        return seeding_pairs

    def _write_seeding_pairs(self):
        f = open("./cache/seeding_pairs.txt", "w")
        json_file = json.dumps(self.seeding_pairs)
        f.write(json_file)
        f.close()

    def _load_seeding_pairs(self):
        f = open("./cache/seeding_pairs.txt", "r")
        data_str = f.read()
        json_data = json.loads(data_str)
        f.close()
        return json_data
