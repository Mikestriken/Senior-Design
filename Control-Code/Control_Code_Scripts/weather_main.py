import Classes.weather_class as weather_class
# import Classes.indoor_temp as indoor_temp

# * ------------------------ Weather Station --------------------
port = "ttyUSB0"
baud = 4800
weather_station = weather_class.WeatherStation(baud, port)
# indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

while True:
        print(weather_station.get_line())
        weather_station.read_and_update()
        # indoor_temp_shtc3.publish_reading()