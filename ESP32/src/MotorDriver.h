#ifndef __MOTOR_DRIVER_H
#define __MOTOR_DRIVER_H

#include <vector>
#include "main.h"
#include "messages.h"

// driver motor pins
#define EN1 12 // V
#define EN2 32 // V
// motor a
#define IN1 27 // V
#define IN2 14 // V
// motor b
#define IN3 33 // V
#define IN4 25 // V

#define STBY 26 // V

// // driver motor pins
// #define EN1 14
// #define EN2 12
// // motor a
// #define IN1 25
// #define IN2 33
// // motor b
// #define IN3 27
// #define IN4 26

void setUpPinModes();
void processCarMovement(MSG directionMsg);
void processEasyCarMovement(unsigned char direction);

#endif