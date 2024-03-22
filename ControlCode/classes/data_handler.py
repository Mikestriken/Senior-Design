import copy
import threading

class DataHandler:
    def __init__(self, data_format):
        self.current_data = data_format
        self.previous_data = copy.deepcopy(self.current_data)
        self.lock = threading.Lock()
        self.update_flag = False

    def update_current_data(self, new_data):
        with self.lock:
            self.previous_data = self.current_data
            self.current_data = new_data
            self.update_flag = True
            

    def get_current_data(self):
        with self.lock:
            return self.current_data

    def unset_update_flag(self):
        with self.lock:
            self.update_flag = False

    def set_update_flag(self):
        with self.lock:
            self.update_flag = True

    def get_update_flag(self):
        with self.lock:
            return self.update_flag