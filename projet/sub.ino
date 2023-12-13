#include <DHT.h>
#include <ArduinoMqttClient.h>
#include <WiFi.h>

const char* ip = "192.168.5.193";

const char* MQTT_USER = "toto";
const char* MQTT_PASSWD = "tata";

const char topic[20] = "humidite";
const char topic2[20] = "temperature";

float temp;
float hum;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char* ssid = "Nothing (2)";
const char* password = "12345678";

void callback(String &topic, String &payload) {
  Serial.println("Received message:");
  Serial.print("Topic: ");
  Serial.println(topic);
  Serial.print("Payload: ");
  Serial.println(payload);
  
  // Here you can add your logic to handle the received message
}

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Set up MQTT
  mqttClient.onMessage(callback);
  mqttClient.setServer(ip, 1883);
  mqttClient.setCredentials(MQTT_USER, MQTT_PASSWD);
  
  // Subscribe to topics
  mqttClient.subscribe(topic);
  mqttClient.subscribe(topic2);
}

void loop() {
  // Maintain the MQTT connection
  if (!mqttClient.connected()) {
    Serial.println("Reconnecting to MQTT...");
    if (mqttClient.connect("ClientID")) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.println("Failed to connect to MQTT. Trying again in 5 seconds...");
      delay(5000);
      return;
    }
  }
   // Keep the MQTT client connected
  mqttClient.loop();
  
  // Add any other code you want to run in the loop here
}
