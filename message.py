class Message:
    # TODO: ganti id pesan menjadi self.my_id+"/"+urutan_pesan
    latitude = 0
    longitude = 0
    hop = 0
    lifetime = 0
    id = ""
    destination_id = ""
    source_id = ""
    message = ""
    
    def __init__(self, latitude, longitude, lifetime, id, destination_id, source_id, message):
        self.latitude = latitude
        self.longitude = longitude
        self.lifetime = lifetime
        self.id = id
        self.destination_id = destination_id
        self.source_id = source_id
        self.message = message

    def increase_hop(self):
        self.hop = self.hop + 1
    
    def decrease_lifetime(self):
        self.lifetime = self.lifetime - 1
    
