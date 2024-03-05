import Classes.weather as weather
# import Classes.indoor_temp as indoor_temp

# * ------------------------Weather Station & SHTC3--------------------
weather_station = weather.WeatherStation()
# indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

while True:
        # print(weather_station.get_line())
        weather_station.read_and_update()
        # indoor_temp_shtc3.publish_reading()