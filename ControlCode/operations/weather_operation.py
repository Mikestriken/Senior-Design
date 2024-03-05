import weather, indoor_temp

# * ------------------------Weather Station & SHTC3--------------------
weather_station = weather.WeatherStation()
indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

while True:
        weather_station.read_and_update()
        indoor_temp_shtc3.publish_reading()