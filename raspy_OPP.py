import this
from RF24 import RF24
from RF24Network import RF24Network,RF24NetworkHeader
import struct
import time

node1 = 0o1

class IOT_Rasp:
    def __init__(self,CE,CSN,this_node):
        self.CE=CE
        self.CSN=CSN
        self.this_node= this_node
        self.radio = RF24(CE, CSN,1000000)
        self.network=RF24Network(self.radio)
        if not self.radio.begin():
            raise RuntimeError("radio hardware not responding")       
        self.radio.channel = 90
        self.network.begin(self.this_node)
        self.radio.printPrettyDetails()
        self.radio.startListening()

        self.xacThuc1=52836
        self.xacThuc2=147

        self.interval=2000
        self.last_sent = 0
        self.packets_sent = 0

    def checkXacThuc(self,data):
        if len(data) != 6:
            return False,0
        data= struct.unpack("HBBH",data)
        if data[0]==self.xacThuc1 and data[2]==self.xacThuc2:
            return True,data
    
    def receiveFromMCU(self):
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
    
    def sendToNode(self,node,device,value ):
        payload = struct.pack("HBBH", self.xacThuc1 ,device,self.xacThuc2,self.packets_sent)
        ok = self.network.write(RF24NetworkHeader(node), payload)
        print(f"Sending  {value} to device {device} of node {node}...", "ok." if ok else "failed.")

    def sendToMCU(self):
        self.network.update()
        now = int(time.monotonic_ns() / 1000000)
        # If it's time to send a message, send it!
        if now - self.last_sent >= self.interval:
            self.last_sent = now
            self.packets_sent += 1
            self.sendToNode(node1,0,self.packets_sent)            

    def run(self):
        try:
            while True:
                self.receiveFromMCU()    
                time.sleep(0.1)
                self.sendToMCU()                
        except KeyboardInterrupt:
            print("powering down radio and exiting.")
            self.radio.powerDown()


IOT=IOT_Rasp(22, 0,0o0)
IOT.run()


        