/* Modified from:
 * ESP8266 (Adafruit HUZZAH) Mosquitto MQTT Publish Example
 * for use with team EPRI_SPOT
 */

#include <WiFi.h>
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

const int ledPin = 0; // This code uses the built-in led for visual feedback that the button has been pressed

// WiFi
/* 
SSID:	IBR900-96a-5g
Protocol:	Wi-Fi 5 (802.11ac)
Security type:	WPA2-Personal
Manufacturer:	Intel Corporation
Description:	Intel(R) Wi-Fi 6E AX211 160MHz
Driver version:	22.250.0.4
Network band:	5 GHz
Network channel:	161
Link speed (Receive/Transmit):	468/216 (Mbps)
Link-local IPv6 address:	fe80::99ef:6960:d53f:f98c%15
IPv4 address:	192.168.0.99
IPv4 DNS servers:	192.168.0.1 (Unencrypted)
Physical address (MAC):	F4-CE-23-FC-CC-09
*/

// Make sure to update this for your own WiFi network!

const char* ssid = "Joelle"; // your ssid
const char* password = "test1234";



// MQTT
// Make sure to update this for your own MQTT Broker!
char* mqtt_server = "192.168.0.142"; // IP of Raspberry Pi, default
const char* mqtt_topic = "rssi";
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "SpotCollar";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

#define MAX_DATA_LEN 128 // Maximum length of the data you expect to receive

char data[MAX_DATA_LEN]; // Array to store received data

void setup() {
  pinMode(ledPin, OUTPUT);

  // Switch the on-board LED off to start with
  digitalWrite(ledPin, HIGH);

  // Begin Serial on 115200
  // Remember to choose the correct Baudrate on the Serial monitor!
  // This is just for debugging purposes
  Serial.begin(115200);

  for(int i; i <10; i++){
    if (Serial.available()) {
        int bytesRead = Serial.readBytesUntil('\n', data, MAX_DATA_LEN - 1); // Read until newline or until buffer is full
        data[bytesRead] = '\0'; // Null-terminate the string
        Serial.print("Received: ");
        Serial.println(data);

        mqtt_server = data;
        break;
      }
  }

  Serial.print("Connecting to ");
  Serial.println(ssid);

      // Scan for available networks
  int numNetworks = WiFi.scanNetworks(false,true);
  if (numNetworks == 0) {
    Serial.println("No networks found");
  } else {
    Serial.print("Found ");
    Serial.print(numNetworks);
    Serial.println(" networks:");
    for (int i = 0; i < numNetworks; i++) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.println(WiFi.SSID(i)); // Print the SSID of the network
    }
  }

  WiFi.begin(ssid, password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.println(WiFi.status());
    //Serial.println(WiFi.status());
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(clientID)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
  
}

void loop() {

  // convert int8_t to const char*
  char buffer[12];    
  itoa(WiFi.RSSI(), buffer, 10);
  const char* rssi_string = buffer;

  if (client.publish(mqtt_topic, rssi_string)) {
    Serial.println("message sent!");
  }
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
  else {
    Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(mqtt_topic, rssi_string);
  }
  
  delay(100);
}
