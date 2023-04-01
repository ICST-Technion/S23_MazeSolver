#include <WiFi.h>

// Wifi info
const char *ssid = "GIVE_ME_PI";
const char *password = "";
const uint16_t port = 8888;
const char *host = "10.42.0.1"; // raspberry pi ip
int connectionTimeOut = 10000;  // 10 ms
WiFiClient client;
bool connectedToServer = false;

#define WIFI_CONNECTION_ERROR -1
#define ONE_STEP 1

typedef enum
{
  RIGHT = 1,
  LEFT = 2,
  FORWARD = 3,
  BACKWARD = 4,
  HALTED = 5,
  UNDEFINED = 6
} DIRECTION;

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
  client.print("please send me the next step\r");
}

void setup()
{

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

void loop()
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

  if (connectedToServer == false)
  {
    // create a connection with the server.
    if (!client.connect(host, port, connectionTimeOut))
    {
      return;
    }
    connectedToServer = true;
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
      Serial.print(rxBuffer);
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
      case HALTED:
        Serial.println("got a halted request");
        break;
      default:
        Serial.println("something went wrong ?");
      }
    }
  }
}
