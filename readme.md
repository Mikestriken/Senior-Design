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
