import socket
import select
import struct
import threading
import sys
import time
import pickle
from message import Message
from haversine import haversine 

class Dtn:
    # declare imoprtant variables
    multicast_addr = '224.0.0.1'
    bind_addr = '0.0.0.0'
    port = 3000
    broadcast_queue = {}
    received_msg = {}
    message_count = 0
    running = True
    
    # create receiver socket
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)
    receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver.bind((bind_addr, port))
    receiver.setblocking(0)

    # declare sender socket
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sender.setblocking(0)

    def __init__(self, user_id, latitude, longitude):
        self.my_id = user_id
        print("your id: " + self.my_id)
        self.latitude = latitude
        self.longitude = longitude
        
        self.running = True
        sys.stdout.flush()
        thread_message_receiver = threading.Thread(target=self.message_receiver)
        thread_message_timer = threading.Thread(target=self.message_timer)
        thread_message_broadcaster = threading.Thread(target=self.message_broadcaster)
        thread_message_validator = threading.Thread(target=self.message_validator)
        thread_message_receiver.start()
        thread_message_broadcaster.start()
        thread_message_timer.start()
        thread_message_validator.start()

    def __del__(self):
        if(self.running):
            print("will be terminated in 3 s")
            self.running = False
            for i in range(3):
                time.sleep(1)
                print(3-i)
            print("terminated")

    # handle received message
    def message_receiver(self):
        while self.running:
            ready = select.select([self.receiver], [], [], 1)
            if ready[0]:
                data, address = self.receiver.recvfrom(4096)
                message = pickle.loads(data)
                if(message.id not in self.received_msg and message.id not in self.broadcast_queue):
                    if(message.destination_id == self.my_id):
                        print("received a message from: " + message.source_id)
                        print("message: " + message.message)
                        self.received_msg[message.id] = message
                    else:
                        #increase hop count and add to queue
                        print("message added to broadcast queue")
                        message.sender_id = self.my_id
                        message.increase_hop()
                        self.broadcast_queue[message.id] = message
        print("message receiver terminated")

    # create message broadcaster thread
    def message_broadcaster(self):
        while self.running:
            time.sleep(1)
            for msg in list(self.broadcast_queue):
                message = self.broadcast_queue[msg]
                if(message.is_valid):
                    data = pickle.dumps(message)
                    self.sender.sendto(data, (self.multicast_addr, self.port))
        print("message broadcaster terminated")

    # create message timer thread
    def message_timer(self):
        while self.running:
            time.sleep(1)
            for msg in list(self.broadcast_queue):
                message = self.broadcast_queue[msg]
                if(message.lifetime > 0):
                    message.decrease_lifetime()
        print("message timer terminated")

    def message_validator(self):
        while self.running:
            time.sleep(1)
            for msg in list(self.broadcast_queue):
                # TODO: tambahkan batasan GPS
                message = self.broadcast_queue[msg]
                
                if(message.lifetime <= 0):
                    if(message.is_valid):
                        print("message with id: " + message.id + " will be invalidated due to lifetime")
                        message.invalidate()
                    continue
                if(message.hop > 3):
                    if(message.is_valid):
                        print("message with id: " + message.id + " will be invalidated due to hop")
                        message.invalidate()
                    continue
                if(haversine((self.latitude, self.longitude),(message.latitude, message.longitude)) > message.distance):
                    if(message.is_valid):
                        print("message with id: " + message.id + " will be invalidated due to distance")
                        message.invalidate()
                    continue
                if(haversine((self.latitude, self.longitude),(message.latitude, message.longitude)) <= message.distance):
                    if(not message.is_valid):
                        print("message with id: " + message.id + " will be validated due to distance")
                        message.validate()
                    continue
        print("message validator terminated")

    def updateGPS(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def add_message(self, dst, msg, lifetime, distance):
        message = Message(self.latitude, self.longitude, lifetime, self.my_id + "/" + str(self.message_count), dst, self.my_id, msg, distance)
        self.increase_message_count()
        self.broadcast_queue[message.id] = message
        print("added:")
        print(vars(self.broadcast_queue[message.id]))

    def print_received_messages(self):
        if(not len(self.received_msg)): return
        print("received messages:")
        for msg in list(self.received_msg):
            print(vars(self.received_msg[msg]))
            del self.received_msg[msg]

    def increase_message_count(self):
        self.message_count = self.message_count + 1