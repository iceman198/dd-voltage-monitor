#include <Arduino.h>

int ledPin = 16; //0 is the built in RED LED on the NodeMCU...but when we use the arduino libraries, the pin numbers are different so it is 16 in this case
bool ledOn = false;
int mycounter = 0;

int v1Pin = A0;
int v2Pin = A1;
int v3Pin = A2;
int v4Pin = A3;

int delaySpeed = 1000;

void toggleLED() {
  if (ledOn) {
    digitalWrite(ledPin, HIGH);
    ledOn = false;
  } else {
    digitalWrite(ledPin, LOW);
    ledOn = true;
  }
}

void ledOff() {
  digitalWrite(ledPin, HIGH);
  ledOn = false;
}

String getVoltageOne() {
  int v = analogRead(v1Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V1:";
  String msg = s + v3;
  String s3 = "|analogVal:";
  s3 = s3 + v;
  msg = msg + s3;
  //Serial.print(msg);
  return msg;
}

String getVoltageTwo() {
  int v = analogRead(v2Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V2:";
  String msg = s + v3;
  String s3 = "|analogVal:";
  s3 = s3 + v;
  msg = msg + s3;
  //Serial.print(msg);
  return msg;
}

String getVoltageThree() {
  int v = analogRead(v3Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V3:";
  String msg = s + v3;
  String s3 = "|analogVal:";
  s3 = s3 + v;
  msg = msg + s3;
  //Serial.print(msg);
  return msg;
}

String getVoltageFour() {
  int v = analogRead(v4Pin);
  float v2 = v / 6.56;
  float v3 = v2 / 10;

  String s = "V4:";
  String msg = s + v3;
  String s3 = "|analogVal:";
  s3 = s3 + v;
  msg = msg + s3;
  //Serial.print(msg);
  return msg;
}

void setup() {
  delay(1000);
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  ledOff();

  //Setup voltage read
  pinMode(v1Pin, INPUT);
  pinMode(v2Pin, INPUT);
  pinMode(v3Pin, INPUT);
  pinMode(v4Pin, INPUT);
}

void loop() {
  String myMsg = getVoltageOne() + "," + getVoltageTwo() + "," + getVoltageThree() + "," + getVoltageFour();
  Serial.println(myMsg);
  delay(delaySpeed);
}
