### Language Versions:
Python 3.12.2

### PIP Dependencies
`pip3 install pyserial` -- For weather station communication  
`pip3 install Flask` -- For Flask web server  
`pip3 install RPi.GPIO` -- Raspberry Pi GPIO Access  
`pip3 install picamera` -- Raspberry Pi Camera Access  
`pip3 install greenlet` -- Multi-Threading to Stream the Pi Camera  
`pip3 install paho-mqtt` -- MQTT communication between different applications running on the Pi
        `pip3 install paho-mqtt==1.6.1` -- Older version
`pip3 install typing_extensions` -- paho-mqtt dependency

All in 1:
Windows:  
`pip3 install pyserial Flask greenlet paho-mqtt typing_extensions`

Raspberry Pi:  
`pip3 install pyserial Flask greenlet paho-mqtt typing_extensions RPi.GPIO picamera`