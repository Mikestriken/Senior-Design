### Language Versions:
Python 3.12.2

### Microcontroller
Raspberry Pi 4B

### Documentation
The latest documentation can be found in *Dock House Documentation.pdf* in the `/documentation/` directory.  
A comprehensive list of all the items bought along with a link to the vendor's page, can be found in the *Bill of Materials.xlsx* also in the `/documentation/` directory.

### Quick Installation
*Note: if this fails, try the Manual Installation Steps*  
1. clone this repository.
2. Run `install/install.sh`

### Manual Installation Steps
1. clone this repository.
2. Run `install/repairScripts.sh`
3. Run `install/installAndRepairAPTInstalls.sh`
4. Run `install/installAndRepairVEnv.sh`
5. Run `install/installAndRepairServices.sh` without sudo (user must have sudo permissions still though)

### Python Virtual Environment
After the install scripts have been ran, a python virtual environment will be created in the git repository. The user can access the virtual environment by running the below commands:  
**Linux:**  
`source venv/bin/activate`  

**Windows:**  
`venv\Scripts\activate`  

### MQTT Topics
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

4. fan_HOA
    - off -- Turn off the fan, regardless of fan speed slider.
    - hand -- Enable the fan speed slider.
    - auto -- Set fan to ignore speed slider and temp sensor control code instead.
    - query_state -- Returns 'is_off'/'is_hand'/'is_auto' on mqtt topic.

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

10. mode
    - Sets the HOA 'manual' or 'automatic' for fan, door


