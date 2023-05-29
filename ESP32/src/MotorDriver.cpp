#include "MotorDriver.h"
#include <WiFi.h>
#include "messages.h"
#include <vector>
using namespace std;

vector<double> rightSpeedVec = {1, 2, 3, 4, 5};
vector<double> leftSpeedVec = {5, 4, 3, 2, 1};

void LineFollowerForward(unsigned int time_angle);
void processCarMovement(MSG directionMSG);
void processEasyCarMovement(unsigned char direction, int speedMotorA, int speedMotorB, int timeDelay);

void processCarMovement(MSG directionMSG)
{
    switch (directionMSG.direction)
    {
    case FORWARD:
        Serial.println("FORWARD");
        LineFollowerForward(directionMSG.time_angle);
        // stop the car
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

void processEasyCarMovement(unsigned char direction, int speedMotorA, int speedMotorB, int timeDelay)
{
    switch (direction)
    {
    case FORWARD:
        // Serial.println("FORWARD");
        //  this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        analogWrite(PWMA, speedMotorA);

        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        analogWrite(PWMB, speedMotorB);

        delay(timeDelay);

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

        delay(670);
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

        delay(670);
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

void LineFollowerForward(unsigned int time_angle)
{
    // default values for speed.
    // changes if the line follower get indication to deviation.
    double speedLeft = 200;
    double speedRight = 200;
    while (time_angle > 0)
    {
        uint16_t lfor = digitalRead(LFO_R);
        uint16_t lfir = digitalRead(LFI_R);
        uint16_t lfc = digitalRead(LF_C);
        uint16_t lfil = digitalRead(LFI_L);
        uint16_t lfol = digitalRead(LFO_L);

        if ((lfol + lfil + lfc + lfir + lfor) > 2)
        {

            speedLeft = lfol * leftSpeedVec[0] + lfil * leftSpeedVec[1] + lfc * leftSpeedVec[2] + lfir * leftSpeedVec[3] + lfor * leftSpeedVec[4];
            speedRight = lfol * rightSpeedVec[0] + lfil * rightSpeedVec[1] + lfc * rightSpeedVec[2] + lfir * rightSpeedVec[3] + lfor * rightSpeedVec[4];

            speedLeft = speedLeft * 255 / 15;
            speedRight = speedRight * 255 / 15;
        }

        // Serial.println("FORWARD");
        //  this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        analogWrite(PWMA, speedRight);

        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        analogWrite(PWMB, speedLeft);

        delay(10);
        time_angle -= 10;
    }
}

void setupPinCarModes()
{
    // set the ENABLES pins to output type
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    // set the motor driver pins to output type
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    // standby
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);
}
