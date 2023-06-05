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
        self.wheelbase = 11
        self.wheel_radius = 3.5
        self.l_speed = 0
        self.r_speed = 0

    def set_position(self, loc, orientation):
        self.location = loc
        self.orientation = orientation

    def get_speeds(self):
        return self.l_speed, self.r_speed

    def calc_speeds(self, err):
        pid = self.pid_controller.calculate(err, 1)
        print("pid", pid)
        self.l_speed, self.r_speed = self.pid_to_speeds(pid)

    def pid_to_speeds(self, steering, max_steering_angle=55):
        """
        steering = front wheel steering angle, limited by max_steering_angle(max 90 degree)
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        print("steering: ", steering)
        if steering > 0:
            left_speed = 255
            right_speed = min(left_speed - steering, 255)

        else:
            right_speed = 255
            left_speed = min(right_speed + steering, 255)


        return int(left_speed), int(right_speed)

