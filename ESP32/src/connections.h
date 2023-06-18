#ifndef __CONNECTIONS__H
#define __CONNECTIONS__H

#define SERVER_CONNECTION_ERROR 0
/**
 * @brief connect to WiFi
 *  @param ssid - the name of the WiFi network
 * @param password - the password of the WiFi network
 *  @return void
 * what the function does is :
 * 1. try to connect to WiFi
 * 2. if connection failed, try again
 * 3. if connection failed again, try again
 * 4. if connection failed again, try again
 * 5. if connection failed again, try again
 *  6. if connection failed again, try again
*/
void connectToWiFi(const char *ssid, const char *password);
//connectToServer function does :
// 1. try to connect to server
// 2. if connection failed, try again

void connectToServer(WiFiClient &client, const char *host, const uint16_t port);
ROBOT_STATE checkConnectivity(WiFiClient &client);

#endif