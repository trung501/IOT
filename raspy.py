from RF24 import RF24
from RF24Network import RF24Network,RF24NetworkHeader
import struct
import time

radio = RF24(22, 0,1000000)
network = RF24Network(radio)
this_node = 0o0

other_node1 = 0o1

if not radio.begin():
    raise RuntimeError("radio hardware not responding")

radio.channel = 90
network.begin(this_node)
radio.printPrettyDetails()
radio.startListening()  # put radio in RX mode

def checkXacThuc(data):
    if len(data) != 6:
        return False,0
    data= struct.unpack("HBBH",data)
    if data[0]==52836 and data[2]==147:
        return True,data


interval = 2000  # in milliseconds
packets_sent = 0
last_sent = 0
try:
    while True:
        # radio.startListening() 
        #Nhan goi tin
        network.update()
        while network.available():
            header, payload = network.read(10)  
            checkReceive,data = checkXacThuc(payload)
            if checkReceive==True:
                print(
                f"Received state {data[3]} of device {data[1]} from {oct(header.from_node)}",
                f"to {oct(header.to_node)} ",
            )
            else:
                print("Nhan payload",payload)
            
        time.sleep(0.1)
        #radio.stopListening() 

        # Gui goi tin
        network.update()
        now = int(time.monotonic_ns() / 1000000)
        # If it's time to send a message, send it!
        if now - last_sent >= interval:
            last_sent = now
            packets_sent += 1
            payload = struct.pack("I", packets_sent)
            ok = network.write(RF24NetworkHeader(other_node1), payload)
            print(f"Sending  {packets_sent} to {other_node1}...", "ok." if ok else "failed.")
        
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.powerDown()



