#include <vector>

typedef enum
{
    FORWARD = 1,
    BACKWARD = 2,
    RIGHT = 3,
    LEFT = 4,
    STOP = 5,
    UNDEFINED = 6
} DIRECTION;

// driver motor pins
#define EN1 14
#define EN2 12
// motor a
#define IN1 25
#define IN2 33
// motor b
#define IN3 27
#define IN4 26

void setUpPinModes();
void processCarMovement(DIRECTION inputValue);
