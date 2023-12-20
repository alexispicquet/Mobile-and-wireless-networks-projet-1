#include <DHT.h>
#include <ArduinoMqttClient.h>
#include <WiFi.h>
#include "AESLib.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// import base64 conversion library
#include "arduino_base64.hpp"

// declare a global AESLib object
AESLib aesLib;

const int buttonPin = 27;  // the number of the pushbutton pin
const int whiteLedPin = 33;    // the number of the LED pin
const int redLedPin = 32;    // the number of the LED pin
int buttonState = 0;  // variable for reading the pushbutton status

const int dhtPin = 26;  // the number of the DHT11 pin
const int dhtType = 11;  // the number of the DHT type
DHT dht11(dhtPin, dhtType);

const char* ip = "192.168.21.193";

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

String addPadding(String inputText) {
    // Determine the block size of your encryption algorithm
    int blockSize = 16 ;

    // Calculate the number of bytes needed to fill a complete block
    int paddingSize = blockSize - (inputText.length() % blockSize);

    // Create a string with the necessary padding
    for (int i = 0; i < paddingSize; i++) {
        inputText += char(paddingSize);
    }

    return inputText;
}

String encrypt(String inputText) {

    inputText = addPadding(inputText) ;
   
    int bytesInputLength = inputText.length() + 1;

    byte bytesInput[bytesInputLength];

    inputText.getBytes(bytesInput, bytesInputLength);

    int outputLength = aesLib.get_cipher_length(bytesInputLength);

    byte bytesEncrypted[outputLength];

    // KEY and IV
    byte aesKey[] = { 23, 45, 56, 67, 67, 87, 98, 12, 32, 34, 45, 56, 67, 87, 65, 5 };
    //Completely random Iv 

    int listByte[16] = { rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256, rand()%256 };

    //int listByte[16] = { 123, 43, 46, 89, 29, 187, 58, 213, 78, 50, 19, 106, 205, 1, 5, 7 };

    byte aesIv[] = { listByte[0], listByte[1], listByte[2], listByte[3], listByte[4], listByte[5], listByte[6], listByte[7], listByte[8], listByte[9], listByte[10], listByte[11], listByte[12], listByte[13], listByte[14], listByte[15] };

    aesLib.encrypt(bytesInput, bytesInputLength, bytesEncrypted, aesKey, 16, aesIv);

    char base64EncodedOutput[base64::encodeLength(outputLength)];

    // convert the encrypted bytes into base64 string "base64EncodedOutput"
    base64::encode(bytesEncrypted, outputLength, base64EncodedOutput);
  
    //String for the concat of Iv and encryptedMassage
    String encryptToSend ;
    for(int loop = 0; loop < 15; loop++){
      Serial.println(listByte[loop]);
      encryptToSend += listByte[loop] ;
      encryptToSend += "," ;
    }
    
    //Concat the last byte and the message with ";" as a separator
    encryptToSend += listByte[15] ;
    encryptToSend += ";" ;
    encryptToSend += String(base64EncodedOutput) ;

    // convert the encoded base64 char array into string
    return encryptToSend;
    

    //return String(base64EncodedOutput);
}


String floatToString(float num) {

  char output[50];
  snprintf(output, 50, "%f", num);
  return output ;
}


void setup(){
  srand (time(NULL));
  
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

  mqttClient.setUsernamePassword(MQTT_USER, MQTT_PASSWD);

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

  char stringHum[12];
  sprintf(stringHum, "%d", (int)hum);

  mqttClient.beginMessage(topic);
  mqttClient.print(encrypt(stringHum));
  //Serial.println(hum);
  mqttClient.endMessage();

  float temp_rounded_down = floorf(temp * 100) / 100;

  mqttClient.beginMessage(topic2);
  mqttClient.print(encrypt(floatToString(temp_rounded_down)));
  mqttClient.endMessage();

}