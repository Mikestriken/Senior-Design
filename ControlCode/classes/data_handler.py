##############################################################################
#                      Data Handler Class Python Script
# This python script defines a data structure with thread locking.
# 
# Its main purpose is to be used as a wrapper for data when multiple threads
# need to access the same data in parallel.
# 
# In addition it also has update flags that can be used to tell processes that
# use the data if old data has been replaced with new data.
# 
# This class is mainly tied to the flask webserver control code found in the
# /ControlCode/flask_webserver/flask_webserver.py python script.
#
# Created by Michael Marais and Joelle Bailey, Spring 2024
##############################################################################

import copy
import threading

class DataHandler:
    def __init__(self, data_format):
        self.current_data = data_format
        self.previous_data = copy.deepcopy(self.current_data)
        self.lock = threading.Lock()
        
        self.update_flags = copy.deepcopy(self.current_data)
        
        for key in self.update_flags.keys():
            self.update_flags[key] = False

    def update_current_data(self, topic, new_data):
        with self.lock:
            self.previous_data[topic] = self.current_data[topic]
            self.current_data[topic] = new_data
            self.update_flags[topic] = True
            

    def get_current_data(self):
        with self.lock:
            return self.current_data

    def unset_update_flag(self, topic):
        with self.lock:
            self.update_flags[topic] = False

    def set_update_flag(self, topic):
        with self.lock:
            self.update_flags[topic] = True

    def set_all_update_flags(self):
        with self.lock:
            for key in self.update_flags.keys():
                self.update_flags[key] = True

    def get_update_flag(self, topic):
        with self.lock:
            return self.update_flags[topic]