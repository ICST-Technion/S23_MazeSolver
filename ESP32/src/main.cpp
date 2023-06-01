

#include <WiFi.h>
#include "MotorDriver.h"
#include <vector>
#include "main.h"
#include <string>
#include "messages.h"
#include "connections.h"

using namespace std;

#define LED1 (35)
#define LED2 (34)
#define ERROR (-1)
#define SUCCESS (0)

// Wifi info
const char *ssid = "GIVE_ME_PI";
const char *password = "";
const uint16_t port = 8080;
const char *host = "192.168.5.1"; // raspberry pi ip
int connectionTimeOut = 10000;    // 10 ms

WiFiClient client;

ROBOT_STATE state;

void setup()
{
  Serial.begin(9600);

  // car motor drivers pins
  setupPinCarModes();

  // leds
  // pinMode(LED1, OUTPUT);
  // pinMode(LED2, OUTPUT);

  // line follower pins
  pinMode(LFO_R, INPUT);
  pinMode(LFI_R, INPUT);
  pinMode(LF_C, INPUT);
  pinMode(LFI_L, INPUT);
  pinMode(LFO_L, INPUT);

  // Connect to Wi-Fi network
  state = CONNECT_TO_WIFI;
  WiFi.mode(WIFI_STA);
}

void loop()
{
  switch (state)
  {
  case CONNECT_TO_WIFI:
    // blocking
    connectToWiFi(ssid, password);
    // digitalWrite(LED1, HIGH);
    //  wifi connected
    state = CONNECT_TO_SERVER;
    break;
  case CONNECT_TO_SERVER:
    if (WiFi.status() == WL_CONNECTED)
    {
      connectToServer(client, host, port);
      // digitalWrite(LED2, HIGH);
      //  wifi and server connection succeed
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
    if (readMessage(&directionMsg, &client) != SUCCESS)
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

  state = checkConnectivity(client);

  delay(1000);
}
