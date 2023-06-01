#ifndef __MAIN_H
#define __MAIN_H

// line follwer pins
#define LFO_R 19
#define LFI_R 18
#define LF_C 5
#define LFI_L 17
#define LFO_L 16

typedef enum
{
    CONNECT_TO_WIFI,
    CONNECT_TO_SERVER,
    DO_COMMANDS,

} ROBOT_STATE;

#endif