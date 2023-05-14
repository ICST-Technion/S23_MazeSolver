#ifndef __MESSAGES_H
#define __MESSAGES_H

#include "WiFi.h"

typedef enum
{
    DIRECTION_REQUEST = 1,
    DIRECTION_MSG = 2,
    ESP32_ACK = 3,
} OPCODES;

typedef enum
{
    RSP = 31,
    ESP_32 = 32
} DEVICE;

typedef enum
{
    RIGHT = 1,
    LEFT = 2,
    FORWARD = 3,
    BACKWARD = 4,
    STOP = 5,
} DIRECTION;

typedef struct msg
{
    unsigned char opcode;
    unsigned char src_device;
    unsigned char dst_device;
    unsigned char direction;
    unsigned int time_angle;
} MSG;

void requestDirection(WiFiClient *client);

void buildAndSendAckMsg(WiFiClient *client, MSG direction_msg);

#endif