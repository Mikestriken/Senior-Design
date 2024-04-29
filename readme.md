### Language Versions:
Python 3.12.2

### Microcontroller
Raspberry Pi 4B

### Documentation
The latest documentation can be found in *Dock House Software and Electronics Documentation.pdf* in the `/documentation/` directory.  
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
For information on MQTT topics find the relevant section in the *Dock House Software and Electronics Documentation.pdf*.