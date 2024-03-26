### Language Versions: {#language-versions}
Python 3.12.2

### Python Virtual Environment {#python-virtual-environment}
**Linux:**  
`source .venv/bin/activate`  

**Windows:**  
`.venv\Scripts\Activate.ps1`

### PIP Dependencies {#pip-dependencies}
`pip install pyserial` -- For weather station communication  
`pip install Flask` -- For Flask web server  
`pip install RPi.GPIO` -- Raspberry Pi GPIO Access  
`pip install picamera` -- Raspberry Pi Camera Access  
`pip install greenlet` -- Multi-Threading to Stream the Pi Camera  
`pip install paho-mqtt` -- MQTT communication between different applications running on the Pi

### Hardware {#hardware}
Raspberry Pi 4B
Airmar 150WX WeatherStation → NMEA 0183 → USB Serial

### Apt Installs {#apt-installs}
`sudo apt install mosquitto` -- Broker used to allow use of paho-mqtt  
`sudo apt install mosquitto-clients` -- Broker used to help debug MQTT clients

### quick Installation {#quick-installation}
*Note: if this fails, try [Manual Installation Steps](#manual-installation-steps)*  
1. clone this repository.
2. Run `install/install.sh`

### Manual Installation Steps {#manual-installation-steps}
1. clone this repository.
2. Run `install/repairScripts.sh`
3. Run `install/installAndRepairAPTInstalls.sh`
4. Run `install/installAndRepairVEnv.sh`
5. Run `install/installAndRepairServices.sh` without sudo (user must have sudo permissions still though)


### Mosquitto Configuration Changes


### MQTT Topics {#mqtt-topics}

1. alerts 
    - publishes various messages from GPIO to Webserver

2. battery_state
    - publishes charge percentage when Spot is connected

3. door
    - open
    - close
    - stop
    - query_state - returns percent open on mqtt topic

4. outdoor_light
    - power_on
    - power_off
    - toggle
    - query_state - returns 'is_on'/'is_off' on mqtt topic

5. indoor_light
    - power_on
    - power_off
    - toggle
    - query_state - returns 'is_on'/'is_off' on mqtt topic

6. fan
    - fast
    - slow
    - stop
    - query_state - returns 'is_on'/'is_slow/is_fast' on mqtt topic

7. indoor_weather
    - SHTC3 publishes on a JSON template of {'temperature': temp, 'relative_humidity': humid}




