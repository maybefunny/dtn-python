class Message:
    latitude = 0
    longitude = 0
    hop = 0
    lifetime = 0
    id = ""
    destination_id = ""
    source_id = ""
    message = ""
    distance = 0
    sender_id = ""
    is_valid = True
    
    def __init__(self, latitude, longitude, lifetime, id, destination_id, source_id, message, distance):
        self.latitude = latitude
        self.longitude = longitude
        self.lifetime = lifetime
        self.id = id
        self.destination_id = destination_id
        self.source_id = source_id
        self.sender_id = source_id
        self.message = message
        self.distance = distance

    def increase_hop(self):
        self.hop = self.hop + 1
    
    def decrease_lifetime(self):
        self.lifetime = self.lifetime - 1

    def invalidate(self):
        self.is_valid = False
    
    def validate(self):
        self.is_valid = True
