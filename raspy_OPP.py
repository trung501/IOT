import this
from RF24 import RF24
from RF24Network import RF24Network,RF24NetworkHeader
import struct
import time
radio=RF24(22, 0,1000000)
node1 = 0o1
packets_sent = 0
last_sent = 0
class IOT_Rasp:
    def __init__(self,CE,CSN,this_node):
        self.CE=CE
        self.CSN=CSN
        self.this_node= this_node
        self.radio = radio
        self.network=RF24Network(self.radio)
        self.xacThuc1=52836
        self.xacThuc2=147
        self.interval=2000
        self.radio.channel = 90
        self.network.begin(self.this_node)
        self.radio.printPrettyDetails()
        self.radio.startListening()


    def checkXacThuc(self,data):
        if len(data) != 6:
            return False,0
        data= struct.unpack("HBBH",data)
        if data[0]==self.xacThuc1 and data[2]==self.xacThuc2:
            return True,data
    
    def run(self):
        try:
            while True:
                #Nhan goi tin
                self.network.update()
                while self.network.available():
                    header, payload = self.network.read(10)  
                    checkReceive,data = self.checkXacThuc(payload)
                    if checkReceive==True:
                        print(
                        f"Received value {data[3]} of device {data[1]} from {oct(header.from_node)}",
                        f"to {oct(header.to_node)} "
                        )
                    else:
                        print("Nhan payload",payload)
                    
                time.sleep(0.1)

                # Gui goi tin
                self.network.update()
                now = int(time.monotonic_ns() / 1000000)
                # If it's time to send a message, send it!
                if now - last_sent >= interval:
                    last_sent = now
                    packets_sent += 1
                    payload = struct.pack("HBBH", self.xacThuc1 ,0,self.xacThuc2,packets_sent)
                    ok = self.network.write(RF24NetworkHeader(node1), payload)
                    print(f"Sending  {packets_sent} to {node1}...", "ok." if ok else "failed.")
                
        except KeyboardInterrupt:
            print("powering down radio and exiting.")
            self.radio.powerDown()


IOT=IOT_Rasp(22, 0,0o0)
IOT.run()


        