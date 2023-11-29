#include <DHT.h>
#include <ArduinoMqttClient.h>
#include <WiFi.h>

const int buttonPin = 27;  // the number of the pushbutton pin
const int whiteLedPin = 33;    // the number of the LED pin
const int redLedPin = 32;    // the number of the LED pin
int buttonState = 0;  // variable for reading the pushbutton status

const int dhtPin = 26;  // the number of the DHT11 pin
const int dhtType = 11;  // the number of the DHT type
DHT dht11(dhtPin, dhtType);

const char* ip = "192.168.5.193";

const char topic[20] = "humidite";
const char topic2[20] = "temperature";

float temp;
float hum;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char* ssid = "Nothing (2)";
const char* password = "12345678";

void setup(){
    
  // Code for Button
  pinMode(whiteLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  dht11.begin();

  Serial.begin(9600);
  delay(1000);

  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
      Serial.print(".");
      delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());

  // Connect to broker
  if (!mqttClient.connect(ip, 1883)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void loop(){
  mqttClient.poll();

// Code for Button
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    digitalWrite(whiteLedPin, HIGH);
  } else {
    digitalWrite(whiteLedPin, LOW);
  }

  // Code for DHT11 Sensor
  hum = dht11.readHumidity();
  temp = dht11.readTemperature();
  if (hum > 80) {
    digitalWrite(redLedPin, HIGH);
  } else {
    digitalWrite(redLedPin, LOW);
  }
  /*
  
  Serial.print("Humidity (%): ");
  Serial.println(hum);

  Serial.print("Temperature  (C): ");
  Serial.println(temp);
  */

  
  mqttClient.beginMessage(topic);
  mqttClient.print(hum);
  Serial.println(hum);
  mqttClient.endMessage();

  mqttClient.beginMessage(topic2);
  mqttClient.print(temp);
  Serial.println(temp);
  mqttClient.endMessage();

}