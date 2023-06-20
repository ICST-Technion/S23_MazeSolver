
#include "main.h"
#include <WiFi.h>
#include "MotorDriver.h"
#include <vector>

#include <string>
#include "messages.h"
#include "connections.h"

using namespace std;

// testing functions.
static void testWheels();
static void testPWMWheels();

// Wifi info
const char *ssid = "GIVE_ME_PI";
const char *password = "";
const uint16_t port = 8080;
const char *host = "192.168.5.1"; // raspberry pi ip
int connectionTimeOut = 10000;    // 10 ms
WiFiClient client;

/**
 * ROBOT states:
 * 1. CONNECT_TO_WIFI.
 * 2. CONNECT_TO_SERVER.
 * 3. DO_COMMANDS.
 */
ROBOT_STATE state;

/**
 * Setup function starts car pins (motors) and set up two leds.
 * configure the wifi to station mode.
 */
void setup()
{
  Serial.begin(9600);

  // car motor drivers pins
  setupPinCarModes();

  // leds
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  // Connect to Wi-Fi network
  state = CONNECT_TO_WIFI;
  WiFi.mode(WIFI_STA);
}

/**
 * This is the main loop:
 * There are three states.
 * The main state is the DO_COMMANDS state.
 * The flow is:
 * 1. Request direction from the RPI.
 * 2. Send ack back to RPI.
 * 3. Move to msg direction.
 * 4. Check connectivity before starting new cycle.
 */
void loop()
{
  // testWheels();
  switch (state)
  {
  case CONNECT_TO_WIFI:
    // blocking
    connectToWiFi(ssid, password);
    //  wifi connected
    state = CONNECT_TO_SERVER;
    break;
  case CONNECT_TO_SERVER:
    if (WiFi.status() == WL_CONNECTED)
    {
      if (connectToServer(client, host, port) == SUCCESS)
      {
        //  wifi and server connection succeed
        state = DO_COMMANDS;
      }
      else
      {
        state = CONNECT_TO_SERVER;
      }
    }
    else
    {
      // returning to the initial state
      state = CONNECT_TO_WIFI;
    }
    break;
  case DO_COMMANDS:
    // waiting 100 ms before requesting new commands. (we dont want to overflow the RPI with the uart)
    // delay(20);
    // asking for new directions.
    requestDirection(&client);
    uint8_t rxBuffer;
    // check if client is available.
    if (waitForClient(&client) != SUCCESS)
    {
      // if the buffer is empty.
      break;
    }

    MSG directionMsg;
    // check if client send new direction in rx buffer.
    if (readMessage(&directionMsg, &client) != SUCCESS)
    {
      break;
    }
    // check correctness of message.
    if ((directionMsg.opcode != OPCODES::DIRECTION_MSG) ||
        (directionMsg.dst_device != DEVICE::ESP_32) ||
        (directionMsg.src_device != DEVICE::RSP))
    {
      // wrong message
      break;
    }
    // send ack back BEFORE moving the car in order to optimized the time between to commands.
    // now the RPI can be ready while the car is moving.
    buildAndSendAckMsg(&client, directionMsg);
    // move the robot.
    processCarMovement(directionMsg);
    break;
  }
  // before moving to the next direction - check that everything is fine. (client and Wifi connectivity)
  if (state == DO_COMMANDS){
    state = checkConnectivity(client);
  }
}

// check wheels performence
static void testWheels()
{
  MSG direction;
  direction.speed_left_wheel = 255;
  direction.speed_right_wheel = 255;

  while (1)
  {

    Serial.println(direction.speed_left_wheel);

    direction.direction = FORWARD;

    direction.time_angle = 3000;
    int delay_time = 1000;
    processCarMovement(direction);
    continue;
    delay(delay_time);
    direction.direction = BACKWARD;
    processCarMovement(direction);
    delay(delay_time);
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

// check wheels with diffrent speed performence
static void testPWMWheels()
{
  MSG direction;
  direction.speed_left_wheel = 200;
  direction.speed_right_wheel = 255;
  while (direction.speed_left_wheel > 0)
  {
    direction.direction = FORWARD;

    direction.time_angle = 1000;
    int delay_time = 200;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = BACKWARD;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = LEFT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = RIGHT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = STOP;
    processCarMovement(direction);
    delay(delay_time * 5);

    direction.speed_left_wheel -= 40;
    direction.speed_right_wheel -= 40;
  }

  direction.speed_left_wheel = 255;
  direction.speed_right_wheel = 255;

  while (direction.speed_left_wheel > 0)
  {
    direction.direction = FORWARD;

    direction.time_angle = 1000;
    int delay_time = 200;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = BACKWARD;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = LEFT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = RIGHT;
    processCarMovement(direction);
    delay(delay_time);
    direction.direction = STOP;
    processCarMovement(direction);
    delay(delay_time * 5);

    direction.speed_left_wheel -= 25;
    direction.speed_right_wheel -= 25;
  }
}
