#ifndef __CONNECTIONS__H
#define __CONNECTIONS__H

#include "WiFi.h"
#include "main.h"

void connectToWiFi(const char *ssid, const char *password);
void connectToServer(WiFiClient &client, const char *host, const uint16_t port);
ROBOT_STATE checkConnectivity(WiFiClient &client);

#endif