const int buttonPin = 27;  // the number of the pushbutton pin
const int whiteLedPin = 33;    // the number of the LED pin

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  
  // Code for Button
  pinMode(whiteLedPin, OUTPUT);
  pinMode(buttonPin, INPUT);

}

void loop() {

  // Code for Button
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    digitalWrite(whiteLedPin, HIGH);
  } else {
    digitalWrite(whiteLedPin, LOW);
  }

}
