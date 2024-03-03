import copy
import threading

class DataHandler:
    def __init__(self):
        self.current_data = {
            'weather_data': {
                'wind': {
                    'speed': "TBD",
                    'direction': "TBD",
                    'status': "TBD"
                },
                'heading': "TBD",
                'meteorological': {
                    'pressureMercury': "TBD",
                    'pressureBars': "TBD",
                    'temperature': "TBD",
                    'humidity' : "TBD",
                    'dewPoint': "TBD"
                }
            },
            'indoor_weather': {
                'temperature' : "TBD",
                'relative_humidity' : "TBD"
            }
        }
        self.previous_data = copy.deepcopy(self.current_data)
        self.lock = threading.Lock()

    def update_current_data(self, new_data):
        with self.lock:
            self.previous_data = self.current_data
            self.current_data = new_data

    def get_current_data(self):
        with self.lock:
            return self.current_data