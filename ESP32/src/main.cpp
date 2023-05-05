

#include <WiFi.h>
#include "MotorDriver.h"
#include <vector>
#include "main.h"
#include <string>
#include "messages.h"

using namespace std;
// Wifi info
const char *ssid = "GIVE_ME_PI";
const char *password = "";
const uint16_t port = 8080;
const char *host = "192.168.5.1"; // raspberry pi ip
int connectionTimeOut = 10000;    // 10 ms
WiFiClient client;
bool connectedToServer = false;

std::vector<int> logVec;

int connectToWiFi(const char *ssid, const char *password)
{
  int loopCounter = 0;
  int maxLoops = 10;
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Connecting to WiFi...");
    delay(1000);
    loopCounter++;
    if (loopCounter > maxLoops)
    {
      return WIFI_CONNECTION_ERROR;
    }
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
  return 0;
}

ROBOT_STATE state;

void setup()
{
  setUpPinModes();
  Serial.begin(9600);
  state = CONNECT_TO_WIFI;
  // Connect to Wi-Fi network

  WiFi.mode(WIFI_STA);
}

void loop()
{
  switch (state)
  {
  case CONNECT_TO_WIFI:
    while (connectToWiFi(ssid, password) == WIFI_CONNECTION_ERROR)
    {
      Serial.println("Try to connect Wi-Fi network");
      delay(1000);
    }
    // wifi connection succeed
    state = CONNECT_TO_SERVER;
    break;
  case CONNECT_TO_SERVER:
    if (WiFi.status() == WL_CONNECTED)
    {
      while (client.connect(host, port, connectionTimeOut) == SERVER_CONNECTION_ERROR)
      {
        Serial.println("Try to connect server");
        delay(1000);
      }
      // wifi and server connection succeed
      state = DO_COMMANDS;
    }
    else
    {
      // returning to the initial state
      state = CONNECT_TO_WIFI;
    }
    break;
  case DO_COMMANDS:

    delay(100);

    requestDirection(&client);

    uint8_t rxBuffer;
    int check_connection_counter = 0;
    while (client.available() <= 0)
    {
      delay(200);
      check_connection_counter++;
      if (check_connection_counter > MAX_TEMPS_BEFORE_BREAK)
      {
        break;
      }
    }

    MSG directionMsg;
    int directionMsgCounter = 0;
    int bytesRemain = sizeof(directionMsg);
    bool timeout = false;
    while (bytesRemain > 0)
    {
      bytesRemain -= client.read((uint8_t *)&directionMsg, bytesRemain);
      if (bytesRemain > 0 && directionMsgCounter > MAX_TEMPS_BEFORE_BREAK)
      {
        timeout = true;
        break;
      }
      if (bytesRemain > 0)
      {
        directionMsgCounter++;
        delay(500);
      }
    }

    if (timeout)
    {
      break;
    }

    if ((directionMsg.opcode != OPCODES::DIRECTION_MSG) ||
        (directionMsg.dst_device != DEVICE::ESP_32) ||
        (directionMsg.src_device != DEVICE::RSP))
    {
      // wrong message
      break;
    }

    buildAndSendAckMsg(&client, directionMsg);

    processCarMovement(directionMsg);

    break;
  }

  // check WiFi connection
  if (WiFi.status() != WL_CONNECTED)
  {
    state = CONNECT_TO_WIFI;
  }

  if (WiFi.status() == WL_CONNECTED && client.connected() == false)
  {
    state = CONNECT_TO_SERVER;
  }

  delay(2000);
}
