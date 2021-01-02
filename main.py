import sys
from dtn import Dtn
user_id = input('input username : ')
latitude = float(input("input latitude : "))
longitude = float(input("input longitude : "))
myDtn = Dtn(user_id, latitude, longitude)
while True:
    try:
        opt = input("1) print received messages\n2) send a message\n3) update GPS\n(1/2/3): ")
        # TODO: tambahkan opsi update fake GPS
        if(opt == "1"):
            myDtn.print_received_messages()
        elif(opt == "2"):
            # TODO: tambahkan input lifetime dan maks jarak
            dst = input("send message to: ")
            msg = input("your message is: ")
            lifetime = int(input("input lifetime : "))
            distance = int(input("input max distance : "))
            myDtn.add_message(dst, msg, lifetime, distance)
        elif(opt == "3"):
            latitude = float(input("input latitude : "))
            longitude = float(input("input longitude : "))
            myDtn.updateGPS(latitude, longitude)
    except KeyboardInterrupt:
        myDtn.__del__()
        del myDtn
        sys.exit(0)
        break