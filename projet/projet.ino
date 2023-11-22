#include "DHT.h"

const int buttonPin = 27;  // the number of the pushbutton pin
const int whiteLedPin = 33;    // the number of the LED pin
const int redLedPin = 32;    // the number of the LED pin
int buttonState = 0;  // variable for reading the pushbutton status

const int dhtPin = 26;  // the number of the DHT11 pin
const int dhtType = 11;  // the number of the DHT type
DHT dht11(dhtPin, dhtType);

float temp;
float hum;

void setup() {
  
  // Code for Button
  pinMode(whiteLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(buttonPin, INPUT);

  // Code for DHT11 Sensor
  Serial.begin(9600);
  dht11.begin();

}

void loop() {

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
  Serial.print("Humidity (%): ");
  Serial.println(hum);

  Serial.print("Temperature  (C): ");
  Serial.println(temp);

}
