import time
import config


class Distance_estimator:

    def __init__(self):
        self.cumulative_distance_m = 0.0
        self.mm_per_pixel = config.mm_per_pixel
        self.speed_mps = config.Robot_Speed_mps
        self.last_time = time.time()



    def pixel_to_mm(self, px_value):
        mm = px_value * self.mm_per_pixel
        return mm



    def update_odometry(self):
        current_time = time.time()
        dt = current_time - self.last_time        #calculate time passed
        self.cumulative_distance_m += self.speed_mps * dt         #updates distance
        self.last_time = current_time               #updates
        return self.cumulative_distance_m