#include <Arduino.h>

int ledPin = 16; //0 is the built in RED LED on the NodeMCU...but when we use the arduino libraries, the pin numbers are different so it is 16 in this case
bool ledOn = false;
int mycounter = 0;

int v1Pin = A0;
int v2Pin = D1;

int delaySpeed = 1;

void toggleLED() {
  if (ledOn) {
    digitalWrite(ledPin, HIGH);
    //Serial.println("toggleLED() ~ led off");
    ledOn = false;
  } else {
    digitalWrite(ledPin, LOW);
    //Serial.println("toggleLED() ~ led on");
    ledOn = true;
  }
}

void ledOff() {
  digitalWrite(ledPin, HIGH);
  //Serial.println("ledOff() ~ led off");
  ledOn = false;
}

void readVoltageOne() {
  int v = analogRead(v1Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V1=";
  String msg = s + v3;
  String s3 = " | analogVal=";
  s3 = s3 + v;
  msg = msg + s3;
  Serial.print(msg);
}

void readVoltageTwo() {
  int v = analogRead(v2Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V2=";
  String msg = s + v3;
  String s3 = " | analogVal=";
  s3 = s3 + v;
  msg = msg + s3;
  Serial.print(msg);
}

void setup() {
  delay(1000);
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  ledOff();

  //Setup voltage read
  pinMode(v1Pin, INPUT);
  pinMode(v2Pin, INPUT);
}

void loop() {
  readVoltageOne();
  readVoltageTwo();
  delay(delaySpeed);
}
