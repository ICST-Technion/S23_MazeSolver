from distance_calibration.pid import PIDController


class Robot(object):
    def __init__(self, kp, ki, kd, a_kp, a_ki, a_kd, max_speed=200):
        """
        Creates robot and initializes PID controllers for rotation/forward motion
        """
        self.location = (0, 0)
        self.orientation = 0.0
        self.pid_controller = PIDController(kp=kp, kd=kd, ki=ki)
        self.pid_angle = PIDController(kp=a_kp, kd=a_kd, ki=a_ki)
        self.l_speed = 0
        self.r_speed = 0
        self.max_speed = max_speed

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
        """
        gets the amount to rotate for given current error from wanted direction
        :param err: error from wanted direction
        :return: duration to rotate for
        """
        return self.pid_to_rotation_speeds(self.pid_angle.calculate(err))

    def calc_speeds(self, err):
        """
        calculates the left and right wheel speeds to account for steer and updates inner variables
        :param err: observed error
        :return: None
        """
        pid = self.pid_controller.calculate(err, 1)
        self.l_speed, self.r_speed = self.pid_to_speeds(pid)

    def pid_to_speeds(self, steering, max_steering_angle=70):
        """
        takes in PID value and gets the left and right wheel speeds to account for steer
        :return left speed, right speed
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if steering > 0:
            left_speed = self.max_speed - 10
            right_speed = min(left_speed - steering, self.max_speed)
        else:
            right_speed = self.max_speed
            left_speed = min(right_speed + steering, self.max_speed) - 10

        return int(left_speed), int(right_speed)

    def pid_to_rotation_speeds(self, angle, max_rotation=680, coef=2.5):
        """
        translates PID value to rotation length
        :param angle: angle provided from PID
        :param max_rotation: maximum rotation to allow
        :param coef: coefficient that allows to calibrate duration from angle
        :return:
        """
        if angle > max_rotation:
            angle = max_rotation
        if angle < -max_rotation:
            angle = -max_rotation
        return angle*coef
