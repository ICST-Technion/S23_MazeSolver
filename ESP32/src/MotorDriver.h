#ifndef __MOTOR_DRIVER_H
#define __MOTOR_DRIVER_H

#include <vector>
#include "main.h"
#include "messages.h"

// driver motor pins
#define PWMA 12
#define PWMB 32
// motor a

#define IN1 27
#define IN2 14
// motor b
#define IN3 33
#define IN4 25


#define STBY 26

void setupPinCarModes();
void processCarMovement(MSG directionMsg);
void processEasyCarMovement(unsigned char direction, int speedMotorA = 0, int speedMotorB = 0, int timeDelay = 10);

#endif