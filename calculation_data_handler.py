import json
import time
from multiprocessing import Queue

class calculation_data_handler:
    def __init__(self):
        self.calculation_data_queue = Queue()
        self.result_data_queue = Queue()

        f = open("./cache/server_data.txt", "r")
        data_str = f.read()
        self.server_data = json.loads(data_str)
        f.close()


        for entry in self.server_data["seeding_pairs"]:
            if entry not in self.server_data["finished_pairs"]:
                self.calculation_data_queue.put(entry)

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

    def _update_files(self):
        pass

    def check_queues(self):
        while True:
            if self.calculation_data_queue.empty():
                break
            time.sleep(1)

            if not self.result_data_queue.empty():
                self._update_files()
