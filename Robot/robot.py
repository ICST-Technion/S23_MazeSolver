from distance_calibration.pid import PIDController
import numpy as np


class Robot(object):
    def __init__(self, kp, ki, kd, a_kp, a_ki, a_kd):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.location = (0, 0)
        self.orientation = 0.0
        self.pid_controller = PIDController(kp=kp, kd=kd, ki=ki)
        self.pid_angle = PIDController(kp=a_kp, kd=a_kd, ki=a_ki)
        self.l_speed = 0
        self.r_speed = 0
        self.max_speed = 180

    def set_position(self, loc, orientation):
        self.location = loc
        self.orientation = orientation

    def reset_angle_pid(self):
        self.pid_angle.reset()

    def reset_dir_pid(self):
        self.pid_controller.reset()

    def get_speeds(self):
        return self.l_speed, self.r_speed

    def get_rotation_length(self, err):
        return self.pid_to_rotation_speeds(self.pid_angle.calculate(err))

    def calc_speeds(self, err):
        pid = self.pid_controller.calculate(err, 1)
        print("pid", pid)
        self.l_speed, self.r_speed = self.pid_to_speeds(pid)

    def pid_to_speeds(self, steering, max_steering_angle=70):
        """
        steering = front wheel steering angle, limited by max_steering_angle(max 90 degree)
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        print("steering: ", steering)
        if steering > 0:
            left_speed = self.max_speed - 8
            right_speed = min(left_speed - steering, self.max_speed)

        else:
            right_speed = self.max_speed
            left_speed = min(right_speed + steering, self.max_speed) - 8

        return int(left_speed), int(right_speed)

    def pid_to_rotation_speeds(self, angle, max_rotation=680):
        if angle > max_rotation:
            angle = max_rotation
        if angle < -max_rotation:
            angle = -max_rotation
        return angle
