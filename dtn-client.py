import socket
import struct
import threading
import sys
import json
import ast
import uuid
import time

# declare imoprtant variables
# TODO: tambahkan init fake GPS
multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 3000
broadcast_queue = {}
received_msg = {}
my_id = uuid.uuid4().hex
print("your id: " + my_id)

# create receiver socket
receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receiver.bind((bind_addr, port))

# handle received message
def received_message_handler():
    while True:
        message, address = receiver.recvfrom(255)
        dict_str = message.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        if(mydata["destination_id"] == my_id and mydata["id"] not in received_msg):
            received_msg[mydata["id"]] = mydata
        elif(int(mydata["hop"]) < 3 and int(mydata["lifetime"]) > 0 and mydata["id"] not in broadcast_queue):
            #increase hop count and add to queue
            mydata["source_id"] = my_id
            mydata["hop"] = int(mydata["hop"]) + 1
            broadcast_queue[mydata["id"]] = mydata

msg_handler = threading.Thread(target=received_message_handler);
msg_handler.start()

# declare sender socket
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
# sender.sendto(message.encode(), (multicast_addr, port))

# create message broadcaster thread
def broadcast_message():
    while True:
        time.sleep(1);
        for msg in list(broadcast_queue):
            if(int(broadcast_queue[msg]["hop"]) < 3 and int(broadcast_queue[msg]["lifetime"]) > 0):
                message = json.dumps(broadcast_queue[msg], indent=2).encode('utf-8')
                sender.sendto(message, (multicast_addr, port))

msg_broadcaster = threading.Thread(target=broadcast_message)
msg_broadcaster.start()

def message_lifetime_handler():
    while True:
        time.sleep(1);
        for msg in list(broadcast_queue):
            if(int(broadcast_queue[msg]["hop"]) < 3 and int(broadcast_queue[msg]["lifetime"]) > 0):
                broadcast_queue[msg]["lifetime"] = broadcast_queue[msg]["lifetime"] - 1
            else:
                # TODO: tambahkan pesan kenapa di drop
                # TODO: tambahkan batasan GPS
                del broadcast_queue[msg]
    pass

msg_lifetime_handler = threading.Thread(target=message_lifetime_handler)
msg_lifetime_handler.start()

def add_message(dst, msg):
    # TODO: ganti id pesan menjadi my_id+"/"+urutan_pesan
    message = {"hop": 0,"lifetime": 86400, "id": uuid.uuid4().hex, "destination_id": dst, "source_id": my_id, "message": msg}
    broadcast_queue[message["id"]] = message

def print_received_messages():
    for msg in list(broadcast_queue):
        print(repr(received_msg[msg]))
        del received_msg[msg]


while True:
    try:
        opt = input("1) print received messages\n2) send a message\n(1/2): ")
        print(opt)
        # TODO: tambahkan opsi update fake GPS
        if(opt == "2"):
            # TODO: tambahkan input lifetime dan maks jarak
            dst = input("send message to: ")
            msg = input("your message is: ")
            add_message(dst, msg)
            print("added to broadcast queue")
        elif(opt == "1"):
            print("received messages:")
            print_received_messages()
    except KeyboardInterrupt:
        print('Interrupted')
        break
        sys.exit(0)