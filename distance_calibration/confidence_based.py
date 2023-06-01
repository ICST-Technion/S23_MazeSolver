import math
import random
import time
import numpy as np
from config import Config


class ConfidenceCalibrator:

    def __init__(self, lower_confidence_thresh=0.8):
        self.confidence = 0
        self.lower_confidence_thresh = lower_confidence_thresh

    def update(self, expected, travelled):

        self.confidence = max(1 - abs(expected - travelled)/travelled, 0)

    def to_update(self, stochastic=False):
        if stochastic:
            return self.sample(min_val=self.lower_confidence_thresh)
        else:
            return self.confidence < self.lower_confidence_thresh

    def sample(self, num_times=5, min_val=0.98, max_val=1):
        # more times the sum should converge to a normal distribution around (min + high) /2
        rand_sum = 0
        for _ in range(num_times):
            rand_sum += random.uniform(min_val, max_val)

        if rand_sum/num_times > self.confidence:
            return True
        return False



