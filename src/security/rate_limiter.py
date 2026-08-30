import time

class RateLimiter:

    def __init__(self):

        self.last_request = 0

        self.interval = 2

    def allow(self):

        now = time.time()

        if now - self.last_request < self.interval:

            return False

        self.last_request = now

        return True
