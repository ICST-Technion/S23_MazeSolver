import threading

class Solver:

    def __init__(self, l_speed, r_speed, learning_rate=0.001):
        self.left_wheel_speed = l_speed
        self.right_wheel_speed = r_speed
        self.location = (0, 0)
        self.learning_rate = learning_rate
        self.lock = threading.Lock()

    def update_location(self, loc):
        self.location = loc

    def get_location(self):
        return self.location

    def update_speeds(self, forward_error, sideways_error):
        self.lock.acquire(blocking=True)
        # uses image dimensions to define negative and positive error
        self.left_wheel_speed -= sideways_error*self.learning_rate
        self.right_wheel_speed += sideways_error*self.learning_rate

        # forward fixing is the same for both wheels
        self.left_wheel_speed += forward_error*self.learning_rate
        self.right_wheel_speed += forward_error*self.learning_rate
        self.lock.release()

    def get_wheel_speeds(self):
        self.lock.acquire(blocking=True)
        l_speed, r_speed = self.left_wheel_speed, self.right_wheel_speed
        self.lock.release()
        return l_speed, r_speed
