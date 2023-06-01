#include "MotorDriver.h"
#include <WiFi.h>
#include "messages.h"
#include <vector>
using namespace std;
#define LED1 35
#define MAX_SPEED 255

// #define LED2 34
vector<double> rightSpeedVec = {1, 2, 3, 4, 5};
vector<double> leftSpeedVec = {5, 4, 3, 2, 1};

void LineFollowerForward(int time_angle);
void processCarMovement(MSG directionMSG);
void processEasyCarMovement(unsigned char direction, int speedMotorA, int speedMotorB, int timeDelay);
void newForward(MSG forward_msg);

void newForward(MSG forward_msg)
{
    if (forward_msg.direction != FORWARD || forward_msg.speed_left_wheel > MAX_SPEED || forward_msg.speed_left_wheel < 0 || forward_msg.speed_right_wheel > MAX_SPEED || forward_msg.speed_right_wheel < 0)
    {
        return;
    }

    Serial.println("FORWARD");
    digitalWrite(LED1, HIGH);

    //  this is the motor - A
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(PWMA, forward_msg.speed_right_wheel);

    // // this is the motor - B
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(PWMB, forward_msg.speed_left_wheel);
    Serial.println(forward_msg.speed_right_wheel);
    Serial.println(forward_msg.speed_right_wheel);
}

void processCarMovement(MSG directionMSG)
{
    switch (directionMSG.direction)
    {
    case FORWARD:
        Serial.println("FORWARD");
        digitalWrite(LED1, HIGH);
        LineFollowerForward(directionMSG.time_angle);
        newForward(directionMSG);
        // digitalWrite(LED1, HIGH);
        //  stop the car
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        //
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
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        analogWrite(PWMB, 255);
        analogWrite(PWMA, 255);
        delay(680);
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);

        break;

    case RIGHT:
        Serial.println("RIGHT");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        analogWrite(PWMB, 255);
        analogWrite(PWMA, 255);
        // analogWrite(PWMA, 255);
        // analogWrite(PWMB, 0);
        delay(680);
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;

    case STOP:
        Serial.println("STOP");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        analogWrite(PWMB, 0);
        analogWrite(PWMA, 0);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
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
        // digitalWrite(LED1, HIGH);

        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        analogWrite(PWMB, speedMotorB);

        delay(timeDelay);

        processEasyCarMovement(STOP, 0, 0, 0);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(700);
        processEasyCarMovement(STOP, 0, 0, 0);
        break;

    case LEFT:
        Serial.println("LEFT");

        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(670);
        processEasyCarMovement(STOP, 0, 0, 0);

        break;

    case RIGHT:
        Serial.println("RIGHT");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        delay(670);
        processEasyCarMovement(STOP, 0, 0, 0);
        break;

    case STOP:
        Serial.println("STOP");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);

        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;

    default:
        delay(700);

        break;
    }
}

void LineFollowerForward(int time_angle)
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
        Serial.println(speedLeft);
        Serial.println(speedRight);
        delay(35);
        time_angle -= 10;
    }
}

void setupPinCarModes()
{
    pinMode(LED1, OUTPUT);
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
