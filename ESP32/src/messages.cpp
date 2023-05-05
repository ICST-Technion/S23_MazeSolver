
#include "messages.h"

void buildAndSendAckMsg(WiFiClient *client, MSG direction_msg)
{
    MSG ack;
    ack.opcode = OPCODES::ESP32_ACK;
    ack.src_device = DEVICE::ESP_32;
    ack.dst_device = DEVICE::RSP;
    ack.direction = direction_msg.direction;
    ack.time_angle = direction_msg.time_angle;

    client->write((uint8_t *)&ack, sizeof(ack));
}

void requestDirection(WiFiClient *client)
{
    MSG requestMsg;
    requestMsg.opcode = (unsigned char)(OPCODES::DIRECTION_REQUEST);
    requestMsg.src_device = (unsigned char)DEVICE::ESP_32;
    requestMsg.dst_device = (unsigned char)DEVICE::RSP;
    requestMsg.direction = (unsigned char)0;
    requestMsg.time_angle = (unsigned int)0;

    client->write((uint8_t *)&requestMsg, sizeof(requestMsg));
}