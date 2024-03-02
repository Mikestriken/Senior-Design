### Language Versions:
Python 3.12.2

### PIP Dependencies
`pip install pyserial` -- For weather station communication  
`pip install Flask` -- For Flask web server  
`pip install RPi.GPIO` -- Raspberry Pi GPIO Access  
`pip install picamera` -- Raspberry Pi Camera Access  
`pip install greenlet` -- Multi-Threading to Stream the Pi Camera  
`pip install paho-mqtt` -- MQTT communication between different applications running on the Pi
`pip install typing_extensions` -- paho-mqtt dependency

All in 1:
Windows:  
`pip3 install pyserial Flask greenlet paho-mqtt typing_extensions`

Raspberry Pi:  
`pip3 install pyserial Flask greenlet paho-mqtt typing_extensions RPi.GPIO picamera`

### Hardware
Raspberry Pi 4B
Airmar 150WX WeatherStation → NMEA 0183 → USB Serial

### Apt Installs
`sudo apt install mosquitto` -- Broker used to allow use of paho-mqtt  
`sudo apt install mosquitto-clients` -- Broker used to help debug MQTT clients 
