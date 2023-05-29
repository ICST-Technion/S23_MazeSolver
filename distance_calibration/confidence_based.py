import math
import random
import time
import numpy as np
from config import Config

def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 +
              (c1[1] - c2[1]) ** 2)

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain, how fast system responds
        self.ki = ki  # Integral gain,
        self.kd = kd  # Derivative gain

        self.last_error = 0  # Error from the previous iteration
        self.integral = 0  # Accumulated error
        self.last_point = None

    def calculate(self, desired_point, current_point, dt):
        self.last_point = current_point
        # Calculate the error
        error = dist(desired_point, current_point)

        # Calculate the proportional term
        proportional = self.kp * error

        # Calculate the integral term
        self.integral += error * dt
        integral = self.ki * self.integral

        # Calculate the derivative term
        derivative = self.kd * (error - self.last_error) / dt

        # Calculate the output
        output = proportional + integral + derivative

        # Store the current error for the next iteration
        self.last_error = error

        return output


class ConfidenceCalibrator:

    def __init__(self, controller_model):
        self.confidence = 0
        self.controller = controller_model
        self.max_error = 0
        self.init_time = time.time()
        self.num_sampled = 0
        self.last_error = 0
        self.error_diff = 0

    def to_calibrate(self, desired_point, current_point):
        self.num_sampled += 1
        error = self.controller.calculate(desired_point, current_point, self.num_sampled)
        self.max_error = max(error, self.max_error)
        if self.max_error == 0:
            self.confidence = 1 - 1/self.num_sampled
        else:
            self.error_diff = error/self.max_error - self.last_error
            self.confidence = min(1 - error/self.max_error, 1)
            self.last_error = error/self.max_error
        return self.sample(min_val=Config.lower_confidence_thresh)

    def sample(self, num_times=4, min_val=0.8, max_val=1):
        # more times the sum should converge to a normal distribution around (min + high) /2
        rand_sum = 0
        for _ in range(num_times):
            rand_sum += random.uniform(min_val, max_val)

        print("rand val:", rand_sum/num_times)
        if rand_sum/num_times > self.confidence:
            return True
        return False


if __name__ == "__main__":
    p = PIDController(1, 0.1, 0)
    c = ConfidenceCalibrator(p)

    for i in range(int(input())):
        w_x, w_y = input().split()
        x, y = input().split()
        print(f"to calibrate: {c.to_calibrate((float(w_x), float(w_y)), (float(x), float(y)))}")
        print(f"confidence: {c.confidence}")
        print(f"error: {c.last_error}")
        print("\n")



