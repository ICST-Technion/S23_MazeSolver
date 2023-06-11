#ifndef __MOTOR_DRIVER_H
#define __MOTOR_DRIVER_H

#include <vector>
#include "main.h"
#include "messages.h"

// driver motor pins
#define PWMA 32 // 12
#define PWMB 12 // 32
// motor a

#define IN1 25 // 27
#define IN2 33 // 14
// motor b
#define IN3 14 // 33
#define IN4 27 // 25

#define STBY 26

void setupPinCarModes();
void processCarMovement(MSG directionMsg);
void processEasyCarMovement(unsigned char direction, int speedMotorA = 0, int speedMotorB = 0, int timeDelay = 10);

#endif