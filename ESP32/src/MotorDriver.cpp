#include "MotorDriver.h"

vector<double> rightSpeedVec = {1, 2, 3, 4, 5};
vector<double> leftSpeedVec = {5, 4, 3, 2, 1};

void moveForward(MSG msg);
void processCarMovement(MSG directionMSG);

/**
 * Blinks the two leds if the car arrived to the end of the maze.
 */
void ledsBlink(double delayTime, int seconds)
{
    int numOfBlinks = seconds / (delayTime / 500);

    for (int i = 0; i < numOfBlinks; i++)
    {
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
        delay(delayTime);
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
        delay(delayTime);
    }

    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
}

/**
 * This is the main movement function.
 * The function sets the wheels to the direction that received from the rpi.
 * There are 3 parameters for movement:
 * 1. time in ms.
 * 2. right wheel speed. (pwmA)
 * 3. left wheel speed. (pwmB)
 */
void processCarMovement(MSG directionMSG)
{
    switch (directionMSG.direction)
    {
    case FINISH:
        Serial.println("FINISH");
        directionMSG.direction = STOP;
        processCarMovement(directionMSG);
        ledsBlink(50, 10);
        break;
    case FORWARD:
        Serial.println("FORWARD");

        analogWrite(PWMA, directionMSG.speed_right_wheel);
        analogWrite(PWMB, directionMSG.speed_left_wheel);

        //  this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);

        // // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        delay(directionMSG.time_angle);

        // stop the car
        // directionMSG.direction = STOP;
        // processCarMovement(directionMSG);
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

        delay(directionMSG.time_angle);

        // directionMSG.direction = STOP;
        // processCarMovement(directionMSG);
        break;

    case LEFT:
        Serial.println("LEFT");

        analogWrite(PWMB, directionMSG.speed_left_wheel);
        analogWrite(PWMA, directionMSG.speed_right_wheel);

        // this is the motor - A
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        // this is the motor - B
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);

        delay(directionMSG.time_angle);

        // directionMSG.direction = STOP;
        // processCarMovement(directionMSG);
        break;

    case RIGHT:
        Serial.println("RIGHT");

        analogWrite(PWMB, directionMSG.speed_left_wheel);
        analogWrite(PWMA, directionMSG.speed_right_wheel);

        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);

        delay(directionMSG.time_angle);

        // directionMSG.direction = STOP;
        // processCarMovement(directionMSG);
        break;

    case STOP:
        Serial.println("STOP");
        // this is the motor - A
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        analogWrite(PWMB, 0);
        analogWrite(PWMA, 0);
        //  // this is the motor - B
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;

    default:
        delay(700);
        break;
    }
}

/**
 * This is a debug function for checking easy movement with simple parameters.
 */
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

/**
 * Setup the pins that relevent to the car only.
 * The pins are the driver motors pins on the esp32 board
 */
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
