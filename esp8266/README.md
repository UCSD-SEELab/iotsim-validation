# ESP8266 as MQTT Client

The script in this folder works on ESP8266 with Arduino IDE. It has the following functionailities:

* Connect to local gateway with specified IP and port.
* Connect and send data to specified MQTT broker.
* Run local Linear Regression of specified input and output data size.

### Dependencies

Arduino library `PubSubClient` and `Adafruit_INA219.h` are required. You can install them from the Package Manager in Arduino IDE.

### Run Instructions

To run it, simply compile and flash the program to ESP8266. Remember to change the `client_ID` for different ESP's to distinguish between them.