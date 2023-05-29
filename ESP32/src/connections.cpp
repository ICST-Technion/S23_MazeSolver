#include "connections.h"
#include "WiFi.h"
#include "main.h"

#define SERVER_CONNECTION_ERROR 0

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
}

void connectToServer(WiFiClient &client, const char *host, const uint16_t port)
{
    int connectionTimeOut = 10000;
    while (client.connect(host, port, connectionTimeOut) == SERVER_CONNECTION_ERROR)
    {
        Serial.println("Try to connect server");
        delay(1000);
    }
}

ROBOT_STATE checkConnectivity(WiFiClient &client)
{
    // check WiFi connection
    if (WiFi.status() != WL_CONNECTED)
    {
        return CONNECT_TO_WIFI;
    }
    // check client-server connection
    if (WiFi.status() == WL_CONNECTED && client.connected() == false)
    {
        return CONNECT_TO_SERVER;
    }
    // everything is fine .. do more steps :)
    return DO_COMMANDS;
}