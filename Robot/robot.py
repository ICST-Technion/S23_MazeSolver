from distance_calibration.pid import PIDController
import numpy as np

class Robot(object):
    def __init__(self, kp, ki, kd):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.location = (0, 0)
        self.orientation = 0.0
        self.pid_controller = PIDController(kp=kp, kd=kd, ki=ki)
        self.wheelbase = 2
        self.wheel_radius = 2
        self.l_speed = 0
        self.r_speed = 0

    def set_position(self, loc, orientation):
        self.location = loc
        self.orientation = orientation

    def get_speeds(self):
        return self.l_speed, self.r_speed

    def calc_speeds(self, err):
        pid = PIDController.calculate(err, 1)
        self.l_speed, self.r_speed = self.pid_to_speeds(pid)

    def pid_to_speeds(self, steering, max_steering_angle=45):
        """
        steering = front wheel steering angle, limited by max_steering_angle(max 90 degree)
        """
        steering = steering * (180.0 / np.pi)
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle

        if steering > 0:
            right_speed = 200
            left_speed = steering / (self.wheelbase / (2 * self.wheel_radius)) + right_speed

        else:
            left_speed = 200
            right_speed = left_speed - steering/(self.wheelbase / (2 * self.wheel_radius))

        return left_speed, right_speed

