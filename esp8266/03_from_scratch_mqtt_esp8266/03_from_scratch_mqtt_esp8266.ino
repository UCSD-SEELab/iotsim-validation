//Implemented from techtutorialsx.com
#include <ESP8266WiFi.h>
#include<PubSubClient.h>

/*Connecting to WiFi network*/
const char* ssid = "SEELAB_IN_LAB"; //SEELAB_IN_LAB, Samsung Galaxy J3 Prime 6909
const char* password = "seelab2148"; //seelab2148, prime6909

/*MQTT server credentials*/
const char* mqttServer = "192.168.1.57";  //192.168.1.57 - For the SEELAB setup; tailor.cloudmqtt.com - for cloudMQTT
const int mqttPort = 61613 ; //61613 - For the SEELAB setup ; 18660 - for cloudMQTT
// Optional additional authentication; Not included in present setup
// const char* mqttUser = "ngwojkpj";
// const char* mqttPassword = "4Fvo2zQ51rb7";
const char* clientID = "esp8266";
const char* topic = "esp/test";

/*Declaring WiFi client to establish connection to a specific IP and port*/
WiFiClient espClient;

/*Declaring object of class PubSubClient which receives input of the constructor the previously defined WiFiClient*/
PubSubClient client(espClient);

// put your setup code here, to run once:
void setup() 
{
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print("Connecting to WiFi..");
    }
    IPAddress ip = WiFi.localIP();
    Serial.println(ip);

    /*Using setServer(method) to specify address and port of MQTT server*/
    client.setServer(mqttServer, mqttPort);

    /*setCallback on the same object is used to specify a handling function that is executed when a MQTT message is received*/
    client.setCallback(callback);

    /*Try to establishing connection with MQTT server*/
    while(!client.connected())
    {
        connect_MQTT();
    }
    /*Subscribing to the topic to receive messages from other publishers*/
    //client.subscribe("esp/test");
}

void connect_MQTT()
{
    Serial.println("Connecting to MQTT...");
    if (client.connect(clientID))
    {
        Serial.println("Connected to MQTT server");  
    }
    else 
    {
        Serial.print("failed with state");
        Serial.print(client.state());
        delay(2000);
    }
}

/*Defining callback function which handles incoming messages for the topics subscribed*/
void callback(char* topic, byte* payload, unsigned int length)
{
    /*Print topic name to the serial port*/
    Serial.print("Message arrived in topic:");
    Serial.println(topic);

    /*Print each byte of mesaage received*/
    Serial.print("Message:");
    for (int i=0; i<length; i++)
    {
      Serial.print((char)payload[i]);
    }    
}

// put your main code here, to run repeatedly:
void loop() 
{
    /*Publishing message on a topic*/
    client.publish("esp/test","Hello from ESP8266");
    Serial.println("Published");
    /*Try to reconnect to MQTT server if not connected*/
    while(!client.connected())
    {
        connect_MQTT();
    }

  /*Calling the loop method of PubSubClient. Called continuously to process incoming messages and maintain connection to the server*/
  // client.loop();
}
