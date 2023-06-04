

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

void testWheels();

void loop()
{
  // testWheels();
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

    if (waitForClient(&client) != SUCCESS)
    {
      break;
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
}

void testWheels()
{
  MSG direction;

  while (1)
  {

    direction.direction = FORWARD;
    direction.speed_left_wheel = 207;
    direction.speed_right_wheel = 200;
    direction.time_angle = 182;
    int delay_time = 1000;
    processCarMovement(direction);
    delay(delay_time);
    // direction.direction = BACKWARD;
    // processCarMovement(direction);
    // delay(delay_time);
    direction.direction = LEFT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = RIGHT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = STOP;
    processCarMovement(direction);
    delay(delay_time * 5);
  }
}
