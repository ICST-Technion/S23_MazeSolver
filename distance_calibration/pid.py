class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain, how fast system responds
        self.ki = ki  # Integral gain,
        self.kd = kd  # Derivative gain

        self.last_error = 0  # Error from the previous iteration
        self.integral = 0  # Accumulated error

    def calculate(self, error, dt=1):

        # Calculate the proportional term
        proportional = error

        # Calculate the integral term
        self.integral = self.integral + error*dt

        # Calculate the derivative term
        derivative = (error - self.last_error) / dt

        # Calculate the output
        output = self.kp*proportional + self.ki*self.integral + self.kd*derivative

        # Store the current error for the next iteration
        self.last_error = error

        return output