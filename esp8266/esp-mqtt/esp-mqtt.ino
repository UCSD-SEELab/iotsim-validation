/***************************************************************
* MQTT Client running on ESP8266s. Publish power data to broker.
* Remember to change clientID for different ESP8266 device.
* Remember to set pt_interval for power sampling rate.
*
* Author: Xiaofan Yu
* Date: 11/11/2019
***************************************************************/
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

/*Connecting to WiFi network*/
const char* ssid = "SEELAB_IN_LAB";
const char* password = "seelab2148";

/*MQTT server credentials*/
const char* mqttBroker = "192.168.1.46";
const int mqttPort = 61613;
const char* clientID = "esp4"; // change this for different device
const int pt_interval = 200; // sampling power how many ms
bool sampling = false; // power sampling status flag
bool runlr = false; // run lr or not
unsigned long st_time, cur_time;
long delta;

/*Declaring WiFi and mqtt client*/
WiFiClient wifiClient;
void mqttCallback(char* topic, uint8_t* payload, unsigned int length);
PubSubClient mqttClient(mqttBroker, mqttPort, mqttCallback, wifiClient);

/*For linear regression*/
#define lr_in_size 256
#define lr_out_size 32
float lr_in[lr_in_size], lr_out[lr_out_size];
float weights[lr_in_size][lr_out_size];

void setup() 
{
    Serial.begin(115200);

    ina219.begin();
    ina219.setCalibration_32V_1A();

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print("Connecting to WiFi..");
    }
    Serial.println("WiFi connected.");

    if (mqttClient.connect(clientID)) {
        mqttClient.subscribe("cmd");
        Serial.println("Connected to broker and subscribe cmd topic.");
        delay(2000); // give some time for bridge to setup
        char topic[20];
        sprintf(topic, "status/%s", clientID);
        mqttClient.publish(topic, "ready");
        Serial.println("Publish ready message.");
    } 
}

void mqttCallback(char* topic, uint8_t* payload, unsigned int length)
{
    char* cleanPayload = (char*)malloc(length+1);
    payload[length] = '\0';
    memcpy(cleanPayload, payload, length+1);
    String msg = String(cleanPayload);
    free(cleanPayload);
    if (msg == "start") {
        sampling = true;
    }
    else if (msg == "lr") {
        runlr = true;
    }
}

void lr()
{
    memset(lr_out, 0, sizeof(lr_out));
    Serial.println("Run lr!");
    for (int i = 0; i < lr_in_size; ++i)
        for (int j = 0; j < lr_out_size; ++j)
            lr_out[j] += lr_in[i] * weights[i][j];
}

void loop() 
{
    st_time = millis();
    if (mqttClient.connected()) {
        if (sampling) {
            float power_mW = ina219.getPower_mW();
            Serial.println(power_mW);
        
            char topic[20];
            sprintf(topic, "data/%s", clientID);
            char msg[20];
            sprintf(msg, "%f", power_mW);
            mqttClient.publish(topic, msg);
        }
        if (runlr) {
            // run lr for 10 times!
            for (int i = 0; i < 10; ++i)
              lr();
            char topic[10] = "fake";
            int res = mqttClient.publish(topic, (byte *)lr_out, lr_out_size << 2);
            // Serial.print("pub result: ");
            // Serial.println(res);
        }
    }
    else {
        Serial.println("Disconnected");
        sampling = false;
        runlr = false;
        if (mqttClient.connect(clientID)) {
            mqttClient.subscribe("cmd");
            Serial.println("Connected to broker and subscribe cmd topic.");
            delay(2000); // give some time for bridge to setup
            char topic[20];
            sprintf(topic, "status/%s", clientID);
            mqttClient.publish(topic, "ready");
            Serial.println("Publish ready message.");
        }
    }
    mqttClient.loop();
    cur_time = millis();
    delta = pt_interval - (cur_time - st_time);
    if (delta > 0) {
        Serial.print("Remain time in ms: ");
        Serial.println(delta);
        delay(delta);
    }
    else {
        Serial.print("Delta is less then zero:");
        Serial.println(delta);
    }
}
