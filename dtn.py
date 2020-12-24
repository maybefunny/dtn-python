import socket
import select
import struct
import threading
import sys
import uuid
import time
import pickle
from message import Message

class Dtn:
    # declare imoprtant variables
    # TODO: tambahkan init fake GPS
    multicast_addr = '224.0.0.1'
    bind_addr = '0.0.0.0'
    port = 3000
    broadcast_queue = {}
    received_msg = {}
    my_id = uuid.uuid4().hex
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

    def __init__(self):
        print("your id: " + self.my_id)

        self.running = True
        sys.stdout.flush()
        thread_message_receiver = threading.Thread(target=self.message_receiver);
        thread_message_broadcaster = threading.Thread(target=self.message_broadcaster)
        thread_message_timer = threading.Thread(target=self.message_timer)
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
                print(3-i)
                time.sleep(1)
            print("terminated")

    # handle received message
    def message_receiver(self):
        while self.running:
            ready = select.select([self.receiver], [], [], 1)
            if ready[0]:
                message, address = self.receiver.recvfrom(255)
                mydata = pickle.loads(message)
                if(mydata.destination_id == self.my_id and mydata.id not in self.received_msg):
                    self.received_msg[mydata.id] = mydata
                    print("received a message from :" + mydata.source_id)
                    print("message: " + mydata.message)
                elif(mydata.id not in self.broadcast_queue):
                    #increase hop count and add to queue
                    mydata.source_id = self.my_id
                    mydata.increase_hop()
                    self.broadcast_queue[mydata.id] = mydata
        print("message receiver terminated")

    # create message broadcaster thread
    def message_broadcaster(self):
        while self.running:
            time.sleep(1);
            for msg in list(self.broadcast_queue):
                if(self.broadcast_queue[msg].hop < 3 and self.broadcast_queue[msg].lifetime > 0):
                    message = pickle.dumps(self.broadcast_queue[msg])
                    self.sender.sendto(message, (self.multicast_addr, self.port))
        print("message broadcaster terminated")

    def message_timer(self):
        while self.running:
            time.sleep(1);
            for msg in list(self.broadcast_queue):
                if(self.broadcast_queue[msg].lifetime > 0):
                    self.broadcast_queue[msg].decrease_lifetime()
        print("message timer terminated")

    def message_validator(self):
        while self.running:
            time.sleep(1);
            for msg in list(self.broadcast_queue):
                delete = False
                # TODO: tambahkan batasan GPS
                if(self.broadcast_queue[msg].lifetime <= 0):
                    print("message with id: " + self.broadcast_queue[msg].id + " will be deleted due to lifetime")
                    delete = True
                if(self.broadcast_queue[msg].hop > 3):
                    print("message with id: " + self.broadcast_queue[msg].id + " will be deleted due to hop")
                    delete = True
                if(delete):
                    del self.broadcast_queue[msg]
        print("message validator terminated")

    def add_message(self, dst, msg):
        message = Message(0, 0, 60, self.my_id + "/" + str(self.message_count), dst, self.my_id, msg)
        self.broadcast_queue[message.id] = message
        print("added:")
        print(vars(self.broadcast_queue[message.id]))

    def print_received_messages(self):
        if(not len(self.received_msg)): return
        print("received messages:")
        for msg in list(self.received_msg):
            print(vars(self.received_msg[msg]))
            del self.received_msg[msg]
