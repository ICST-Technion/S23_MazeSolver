"""
PID controller interface
"""

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain,
        self.kd = kd  # Derivative gain
        self.first_calculation = 0
        self.last_error = 0  # Error from the previous iteration
        self.integral = 0  # Accumulated error

    def reset(self):
        """
        resets the controller
        :return: None
        """
        self.last_error = 0
        self.integral = 0
        self.first_calculation = 0

    def calculate(self, error, dt=1):
        """
        calculates the PID value given an error

        :param error: the observed error
        :param dt: time unit for derivative and integral, defaults to 1
        :return: the PID value
        """
        # Calculate the proportional term
        proportional = error

        # Calculate the integral term
        self.integral = self.integral + error*dt

        # Calculate the derivative term
        derivative = (error - self.last_error) / dt

        # Calculate the output
        output = self.kp*proportional + self.ki*self.integral + self.kd*derivative
        output *= self.first_calculation
        # Store the current error for the next iteration
        self.last_error = error
        self.first_calculation = 1
        return output