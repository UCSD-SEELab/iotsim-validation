# Setup ESP8266 as Mesh Nodes

The installation steps are adapted from [painlessMesh](https://gitlab.com/painlessMesh/painlessMesh/tree/master) wiki page.

1. Install board ESP8266 to Arduino IDE, using Generic ESP8266 Module version 2.5.2.
2. Install the following packages to Arduino IDE. The first three could be installed through the Arduino Library Manager.
   * painlessMesh (1.4.3)
   * ArduinoJson (6.13.0)
   * TaskScheduler (3.0.2)
   * ESPAsyncTCP. Has to be installed manually from [its github source](https://github.com/me-no-dev/ESPAsyncTCP).
3. Compile and flash scripts in this directory to different ESP8266 nodes.
   * **mqttBridge**: this script is for the bridge node connecting ESP mesh and a MQTT broker on another network. Here, for the external network, SSID and password of the network should be given. After connecting to the desired outside network, the bridge node will find the broker and connect to it.
     In the mesh network, the bridge node acts as the root node (a.k.a gateway or AP). This bridge node is responsible for transformation between mesh protocol and MQTT protocol with the outside network.
   * **basic**: this script is for the rest normal mesh nodes. All is for maintaining a mesh network, broadcasting information to the rest nodes.