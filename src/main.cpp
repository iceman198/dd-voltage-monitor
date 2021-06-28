#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WebSocketsServer.h>

#include "index.h"

//Hotspot Name and Password
const char *ssid = "dd-voltage";
const char *password = "1234567890";

WebSocketsServer webSocket = WebSocketsServer(8181);
ESP8266WebServer server(80);

int ledPin = 16; //0 is the built in RED LED on the NodeMCU...but when we use the arduino libraries, the pin numbers are different so it is 16 in this case
bool ledOn = false;
int mycounter = 0;
int webSendDelay = 5000;
bool clientConnected = false;
bool voltageGood = true;
int voltageCount = 0;
bool serialMsgSent = true;

float goodVoltage = 12.00;
int v1Pin = 0;
int v2Pin = 1;

int delaySpeed = 1;
//int delaySpeed = 1000;

void handleRoot()
{
  Serial.println("handleRoot() ~ start");
  //String html[] = MAIN_page;
  Serial.println("handleRoot() ~ sending html");
  server.send(200, "text/html", MAIN_page);
  //server.send(200, "text/html", "This is a test");
  Serial.println("handleRoot() ~ done");
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, int length)
{
  if (type == WStype_TEXT)
  {
    Serial.println("webSocketEvent() ~ incoming payload");
    Serial.print("webSocketEvent() ~ num = ");
    Serial.println(num);
    String fullpayload = "";
    for (int i = 0; i < length; i++)
    {
      //Serial.print((char)payload[i]);
      fullpayload += (char)payload[i];
    }
    Serial.print("webSocketEvent() ~ fullpayload = ");
    Serial.println(fullpayload);
    Serial.println("webSocketEvent() ~ payload complete");
    Serial.println("");
  }

  if (type == WStype_CONNECTED)
  {
    clientConnected = true;
    Serial.println("webSocketEvent() ~ Client connected");
  }
  if (type == WStype_DISCONNECTED)
  {
    clientConnected = false;
    Serial.println("webSocketEvent() ~ Client disconnected");
  }
  if (type == WStype_ERROR)
  {
    Serial.println("webSocketEvent() ~ Client ERROR");
  }
  if (type == WStype_BIN)
  {
    Serial.println("webSocketEvent() ~ Client WStype_BIN");
  }
  if (type == WStype_FRAGMENT_TEXT_START)
  {
    Serial.println("webSocketEvent() ~ Client WStype_FRAGMENT_TEXT_START");
  }
  if (type == WStype_FRAGMENT_BIN_START)
  {
    Serial.println("webSocketEvent() ~ Client WStype_FRAGMENT_BIN_START");
  }
  if (type == WStype_FRAGMENT)
  {
    Serial.println("webSocketEvent() ~ Client WStype_FRAGMENT");
  }
  if (type == WStype_FRAGMENT_FIN)
  {
    Serial.println("webSocketEvent() ~ Client WStype_FRAGMENT_FIN");
  }
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
  Serial.println(msg);

  if (v3 > goodVoltage) {
    voltageGood = true;
    voltageCount = 0;
    Serial.println("V1 is good");
  } else {
    voltageCount++;
    if (voltageCount > 3) {
      voltageGood = false;
      //Serial.println("V1 is BAAAD");
    }
    Serial.println("V1 is BAAAD");
  }

  if (clientConnected) {
    // 800 = 12.36v
    // 74 = 1.167v
    webSocket.sendTXT(0, msg);
  }
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
  Serial.println(msg);

  if (v3 > goodVoltage) {
    voltageGood = true;
    voltageCount = 0;
    Serial.println("V2 is good");
  } else {
    voltageCount++;
    if (voltageCount > 3) {
      voltageGood = false;
      //Serial.println("V2 is BAAAD");
    }
    Serial.println("V2 is BAAAD");
  }

  if (clientConnected) {
    // 800 = 12.36v
    // 74 = 1.167v
    webSocket.sendTXT(0, msg);
  }
}

void setup()
{
  delay(1000);
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  //Setup voltage read
  pinMode(A0, INPUT);
  
  //Setup WIFI
  Serial.println("setup() ~ Configuring access point...");
  //WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  IPAddress myIP = WiFi.softAPIP();
  if (MDNS.begin("esp8266"))
  {
    Serial.println("setup() ~ MDNS responder started");
  }
  server.on("/", handleRoot);
  server.begin();
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  Serial.println("setup() ~ HTTP server started");
  Serial.print("setup() ~ HotSpot IP:");
  Serial.println(myIP);
}

void loop()
{
  server.handleClient();
  webSocket.loop();

  if (mycounter > webSendDelay) {
    readVoltageOne();
    readVoltageTwo();
    mycounter = 0;
  }
  mycounter++;

  if (!clientConnected) {

  }

  if (!voltageGood) {

  }

  yield();
  delay(delaySpeed);
}
