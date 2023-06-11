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

void LineFollowerForward(MSG msg);
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
    // digitalWrite(LED1, HIGH);

    //  this is the motor - A
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(PWMA, forward_msg.speed_right_wheel);

    // // this is the motor - B
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(PWMB, forward_msg.speed_left_wheel);

    delay(forward_msg.time_angle);
    Serial.println(forward_msg.speed_right_wheel);
    Serial.println(forward_msg.speed_right_wheel);
}

void processCarMovement(MSG directionMSG)
{
    uint16_t lfc;
    int64_t endTime;
    switch (directionMSG.direction)
    {
    case FORWARD:
        Serial.println("FORWARD");
        // digitalWrite(LED1, HIGH);
        LineFollowerForward(directionMSG);
        // newForward(directionMSG);
        //   digitalWrite(LED1, HIGH);
        //    stop the car
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;
    case BACKWARD:
        Serial.println("BACKWARD");

        analogWrite(PWMA, directionMSG.speed_right_wheel);
        analogWrite(PWMB, directionMSG.speed_left_wheel);

        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        //
        // // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        endTime = (int64_t)esp_timer_get_time() / 1000 + directionMSG.time_angle;
        while ((endTime - (int64_t)esp_timer_get_time() / 1000) > 0)
        {
        };

        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        break;

    case LEFT:
        Serial.println("LEFT");

        analogWrite(PWMB, directionMSG.speed_left_wheel);
        analogWrite(PWMA, directionMSG.speed_right_wheel);

        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        // do half left turn
        // delay(600);

        // lfc = digitalRead(LF_C);
        delay(directionMSG.time_angle);

        directionMSG.direction = STOP;
        processCarMovement(directionMSG);

        break;

    case RIGHT:
        Serial.println("RIGHT");

        analogWrite(PWMB, directionMSG.speed_left_wheel);
        analogWrite(PWMA, directionMSG.speed_right_wheel);

        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // digitalWrite(LED1, HIGH);
        //  // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        // analogWrite(PWMA, 255);
        // analogWrite(PWMB, 0);
        // delay(600);

        // lfc = digitalRead(LF_C);
        // do
        // {
        //     lfc = digitalRead(LF_C);
        //     delay(40);
        // } while (lfc == 1);

        delay(directionMSG.time_angle);

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

        // processEasyCarMovement(STOP, 0, 0, 0);
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
        // processEasyCarMovement(STOP, 0, 0, 0);
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
        delay(100);

        break;
    }
}

void LineFollowerForward(MSG msg)
{
    // default values for speed.
    // changes if the line follower get indication to deviation.
    int time_angle = msg.time_angle;

    analogWrite(PWMA, msg.speed_right_wheel);
    analogWrite(PWMB, msg.speed_left_wheel);

    //  this is the motor - A
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    // // this is the motor - B
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    int64_t endTime = (int64_t)esp_timer_get_time() / 1000 + msg.time_angle;
    while ((endTime - (int64_t)esp_timer_get_time() / 1000) > 0)
    {
        // Serial.println("FORWARD");

        // Serial.print("delay = ");
        // Serial.println(min(time_angle, 50));
        // delayMicroseconds(1000 * min(time_angle, 50));
        // delay(min(time_angle, 50));
        // time_angle -= min(time_angle, 50);

        // uint16_t lfor = digitalRead(LFO_R);
        // uint16_t lfir = digitalRead(LFI_R);
        // uint16_t lfc = digitalRead(LF_C);
        // uint16_t lfil = digitalRead(LFI_L);
        // uint16_t lfol = digitalRead(LFO_L);

        // int sum = lfor + lfir + lfc + lfil + lfol;
        // Serial.print("sum = ");
        // Serial.println(sum);

        // if (sum == 5)
        // {
        //     break;
        // }
    }
}

void setupPinCarModes()
{
    // pinMode(LED1, OUTPUT);
    //  set the ENABLES pins to output type
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
