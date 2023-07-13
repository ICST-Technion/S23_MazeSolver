#ifndef __MAIN_H
#define __MAIN_H


#define LED1 (23)
#define LED2 (13)

#define ERROR (-1)
#define SUCCESS (0)

typedef enum ROBOT_STATE
{
    CONNECT_TO_WIFI,
    CONNECT_TO_SERVER,
    DO_COMMANDS,

} ROBOT_STATE;

#endif