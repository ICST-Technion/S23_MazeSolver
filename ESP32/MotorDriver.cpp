#include "MotorDriver.h"
#include <WiFi.h>

void processCarMovement(DIRECTION direction)
{
    switch (direction)
    {
    case FORWARD:
        Serial.println("FORWARD");
        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;

    case LEFT:
        Serial.println("RIGHT");
        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;

    case RIGHT:
        Serial.println("LEFT");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;

    case STOP:
        Serial.println("STOP");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;

    default:
        break;
    }
}

void setUpPinModes()
{
    // set the ENABLES pins to output type
    pinMode(EN1, OUTPUT);
    pinMode(EN2, OUTPUT);
    // set the motor driver pins to output type
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    // set the motors enable to HIGH
    digitalWrite(EN1, HIGH);
    digitalWrite(EN2, HIGH);
}
