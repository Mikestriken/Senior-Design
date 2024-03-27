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

### Quick Installation {#quick-installation}
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
    - Publishes various messages from GPIO to Webserver.

2. battery_state
    - Publishes charge percentage when Spot is connected.

2. wall_power
    - Publishes "Wall Power Disconnected!" and "Wall Power Reconnected!" to alert and wall_power MQTT Topics if wall power state has been changed a set period of time.
    - query_state -- publishes wall power state ("Wall Power Disconnected!" / "Wall Power Reconnected!") immediately without waiting for set period of time.

3. door
    - open -- Start opening the door (until fully open).
    - close -- Start closing the door (until fully closed).
    - stop -- Stop the door.
    - query_state -- Returns percent open on mqtt topic.

4. outdoor_light
    - power_on -- Turn the light on.
    - power_off -- Turn the light off.
    - toggle -- Toggle the light on/off.
    - query_state -- Returns 'is_on'/'is_off' on mqtt topic.

5. indoor_light
    - power_on -- Turn the light on.
    - power_off -- Turn the light off.
    - toggle -- Toggle the light on/off.
    - query_state -- Returns 'is_on'/'is_off' on mqtt topic.

6. fan
    - fast -- Set fan to fast speed setting.
    - slow -- Set fan to slow speed setting.
    - stop -- Set fan to off speed setting.
    - query_state -- Returns 'is_on'/'is_slow/is_fast' on mqtt topic.

7. indoor_weather
    - SHTC3 publishes data in the JSON format below:  
    ```json
        {
            "temperature": "value",
            "relative_humidity": "value"
        }
    ```

8. weather
    - publishes data in the JSON format below:  
    ```json
        {
            "wind": {
                "speed": "value",
                "rawDirection": "value",
                "trueDirection":"value",
                "status": "value"
            },
            "heading": "value",
            "meteorological": {
                "pressureMercury": "value",
                "pressureBars": "value",
                "temperature": "value",
                "humidity" : "value",
                "dewPoint": "value"
            }
        }
    ```

9. rssi
    - Sent from the Spot Collar ESP32, negative integer representing wifi rssi




