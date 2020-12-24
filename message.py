import time
import threading

class Message:
    latitude = 0
    longitude = 0
    hop = 0
    lifetime = 0
    id = ""
    destination_id = ""
    source_id = ""
    message = ""
    is_valid = True
    
    def __init__(self, latitude, longitude, lifetime, id, destination_id, source_id, message):
        self.latitude = latitude
        self.longitude = longitude
        self.lifetime = lifetime
        self.id = id
        self.destination_id = destination_id
        self.source_id = source_id
        self.message = message
        thread_timer = threading.Thread(target=self.timer)
        thread_timer.start()

    def increase_hop(self):
        self.hop = self.hop + 1

    def timer(self):
        while(self.lifetime > 0):
            time.sleep(1)
            self.decrease_lifetime()
    
    def decrease_lifetime(self):
        self.lifetime = self.lifetime - 1

    def invalidate(self):
        self.is_valid = False
    
