#include "connections.h"
#include "WiFi.h"
#include "main.h"

/**
 * connect to the Wifi (RPI's wifi)/
 */
void connectToWiFi(const char *ssid, const char *password)
{
    int loopCounter = 0;
    int maxLoops = 10;
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Connecting to WiFi...");
        delay(1000);
    }
    Serial.println("Connected to WiFi");
    digitalWrite(LED1, LOW);
}

/**
 * connect to the server (RPI)/
 */
int connectToServer(WiFiClient &client, const char *host, const uint16_t port)
{
    int connectionTimeOut = 200;
    if (client.connect(host, port, connectionTimeOut) != SERVER_CONNECTION_ERROR)
    {
        digitalWrite(LED2, LOW);
        return 0;
    }
    return -1;
    
}

/**
 * Checks if there is a connection to the wifi.
 * Checks if there is a connection to the server.
 * Sets the robot state to the relevent state.
 */
ROBOT_STATE checkConnectivity(WiFiClient &client)
{
    // check WiFi connection
    if (WiFi.status() != WL_CONNECTED)
    {
        digitalWrite(LED2, HIGH);
        digitalWrite(LED1, HIGH);
        return CONNECT_TO_WIFI;
    }
    // check client-server connection
    if (WiFi.status() == WL_CONNECTED && client.connected() == false)
    {
        digitalWrite(LED2, HIGH);
        return CONNECT_TO_SERVER;
    }
    // everything is fine .. do more steps :)
    return DO_COMMANDS;
}