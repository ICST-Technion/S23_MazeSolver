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

    def calculate(self, num_travelled, num_desired, dt=1):
        # Calculate the error
        error = num_desired - num_travelled
        print(error)
        # Calculate the proportional term
        proportional = self.kp * error

        # Calculate the integral term
        self.integral = self.integral + self.ki*error

        # Calculate the derivative term
        derivative = self.kd * (error - self.last_error) / dt

        # Calculate the output
        output = proportional + self.integral + derivative

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
        self.error = 0
        self.error_diff = 0

    def to_calibrate(self, num_travelled, num_desired):
        self.num_sampled += 1
        self.error = self.controller.calculate(num_travelled, num_desired, 1)
        self.max_error = max(self.error, self.max_error)
        if self.max_error == 0:
            self.confidence = 1 - 1/self.num_sampled
        else:
            self.error_diff = self.error/self.max_error - self.error
            self.confidence = min(1 - self.error/self.max_error, 1)
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
    p = PIDController(1.5, 0.4, 0)
    c = ConfidenceCalibrator(p)
    coef = random.uniform(0, 1)
    learning_rate = 0.001
    distances = [random.uniform(200, 500) for x in range(20)]
    print(f"coef: {coef}")
    print(distances)
    i = 0
    for d in distances:
        c.to_calibrate(d*coef, d)
        i += 1
        print(f"error: {c.error} \t\t confidence: {c.confidence}\t\tcoef: {coef}")
        coef += learning_rate*c.error
        time.sleep(0.1)



