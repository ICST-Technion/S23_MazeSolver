#include "MotorDriver.h"
#include <WiFi.h>
#include "messages.h"

void processCarMovement(MSG directionMSG)
{
    switch (directionMSG.direction)
    {
    case FORWARD:
        Serial.println("FORWARD");
        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        delay(directionMSG.time_angle * 10);

        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(directionMSG.time_angle * 10);
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;

    case LEFT:
        Serial.println("LEFT");

        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(680);
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);

        break;

    case RIGHT:
        Serial.println("RIGHT");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        delay(680);
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
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
        delay(700);

        break;
    }
}

void processEasyCarMovement(unsigned char direction)
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

        delay(700);
        processEasyCarMovement(STOP);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(700);
        processEasyCarMovement(STOP);
        break;

    case LEFT:
        Serial.println("LEFT");

        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(700);
        processEasyCarMovement(STOP);

        break;

    case RIGHT:
        Serial.println("RIGHT");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        delay(700);
        processEasyCarMovement(STOP);
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
        delay(700);

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

    // standby
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);

    // set the motors enable to HIGH
    digitalWrite(EN1, HIGH);
    digitalWrite(EN2, HIGH);
}
