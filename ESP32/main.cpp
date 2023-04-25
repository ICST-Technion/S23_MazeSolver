

#include <WiFi.h>
#include "MotorDriver.h"
#include <vector>

// Wifi info
const char *ssid = "GIVE_ME_PI";
const char *password = "";
const uint16_t port = 8080;
const char *host = "192.168.5.1"; // raspberry pi ip
int connectionTimeOut = 10000;    // 10 ms
WiFiClient client;
bool connectedToServer = false;

std::vector<int> logVec;
#define WIFI_CONNECTION_ERROR -1
#define ONE_STEP 1

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

void sendAStepRequest()
{
  client.print("dir: ");
}

void flushLogger()
{
  client.print("log: ");
  for (const auto &direction : logVec)
  {
    client.print(direction);
  }
  // clear the log vector
  logVec.clear();
}

void setup1()
{
  setUpPinModes();
  Serial.begin(9600);
  Serial.println("hey...");
  // Connect to Wi-Fi network

  WiFi.mode(WIFI_STA);
  if (connectToWiFi(ssid, password) == WIFI_CONNECTION_ERROR)
  {
    Serial.println("connection error occurred...");
    exit(0);
  };
}

void setup()
{
  setUpPinModes();

  Serial.begin(9600);
  Serial.println("hey...");
}

void loop()
{

  processCarMovement(FORWARD);
  delay(2000);
  processCarMovement(BACKWARD);
  delay(2000);
  processCarMovement(STOP);
  delay(2000);
  processCarMovement(RIGHT);
  delay(800);
  processCarMovement(STOP);
  delay(2000);
  processCarMovement(LEFT);
  delay(800);
  processCarMovement(STOP);
  delay(2000);
}

void loop1()
{
  // check WiFi connection
  if (WiFi.status() != WL_CONNECTED)
  {
    while (connectToWiFi(ssid, password) == WIFI_CONNECTION_ERROR)
    {
      Serial.println("Lost connection to Wi-Fi network, reconnecting...");
      delay(1000);
    };
    Serial.println("Reconnecting to the wifi has succeeded.");

    // if reconneting to Wifi, we need to connect the server again.
    connectedToServer = false;
  }

  if (connectedToServer == false || client.connected() == false)
  {
    // create a connection with the server.
    if (!client.connect(host, port, connectionTimeOut))
    {
      return;
    }
    connectedToServer = true;
    Serial.println("connected to the server");
  }

  sendAStepRequest();

  // wait for the server's reply to become available
  while (!client.available())
  {
    // wait until the rxBuffer received a step direction.
  }

  uint8_t rxBuffer = UNDEFINED;
  if (client.available() > 0)
  {
    Serial.println("server is available");
    // read back one line from the server

    int bytesReceived = client.read(&rxBuffer, ONE_STEP);
    if (bytesReceived == ONE_STEP)
    {
      Serial.println(rxBuffer);
      logVec.push_back(rxBuffer);
      if (logVec.size() > 10)
      {
        flushLogger();
      }
      switch (rxBuffer)
      {
      case FORWARD:
        Serial.println("got a forward step");
        break;
      case BACKWARD:
        Serial.println("got a backward step");
        break;
      case RIGHT:
        Serial.println("got a right step");
        break;
      case LEFT:
        Serial.println("got a left step");
        break;
      case STOP:
        Serial.println("got a halted request");
        break;
      default:
        Serial.println("something went wrong ?");
      }
      processCarMovement(FORWARD);
      delay(500);
    }
  }
}
