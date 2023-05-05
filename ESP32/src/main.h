#ifndef __MAIN_H
#define __MAIN_H

#define WIFI_CONNECTION_ERROR -1
#define ONE_STEP 1
#define SERVER_CONNECTION_ERROR 0
#define MAX_BYTE_BEFORE_FLUSH 10
#define MAX_TEMPS_BEFORE_BREAK 10

#define ACK_OPCODE 10

typedef enum
{
    CONNECT_TO_WIFI,
    CONNECT_TO_SERVER,
    DO_COMMANDS,

} ROBOT_STATE;

typedef struct step_t
{
    unsigned char direction;
    unsigned int angle_time_element;
} Step;

#endif