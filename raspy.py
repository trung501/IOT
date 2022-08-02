import this
from paho_mqtt import MQTT_client
from RF24 import RF24
from RF24Network import RF24Network,RF24NetworkHeader
import struct
import time

node1 = 0o1
node2 = 0o2
node21=0o21

class IOT_Rasp:
    def __init__(self,CE,CSN,this_node,host_mqtt='192.168.0.176'):
        self.CE=CE
        self.CSN=CSN
        self.this_node= this_node
        self.radio = RF24(self.CE, self.CSN,1000000)
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
        # client mqtt
        self.client = MQTT_client(host_mqtt)

    def checkXacThuc(self,data):
        if len(data) != 6:
            return False,0
        data= struct.unpack("HBBH",data)
        if data[0]==self.xacThuc1 and data[2]==self.xacThuc2:
            return True,{"device":data[1],"value":data[3]}
    def check_server_mqtt(self):
        try:
            self.client.connect_mqtt()
            return True
        except:
            return False
    def handleDataReceiveFromNode1(self,data):
        # data[1] = 1 - nhiet do
        # data[2] = 2 - do am
        self.client.topic = f"node1/{data['device']}"
        self.client.publish(data["value"])
    def handleDataReceiveFromNode2(self,data):
        #self.client.publish(data[3])
        pass
    def handleDataReceiveFromNode21(self,data):
        #self.client.publish(data[3])
        pass

    def receiveFromMcuAndHandle(self):
        self.network.update()
        while self.network.available():
            header, payload = self.network.read(10)  
            checkReceive,data = self.checkXacThuc(payload)
            if checkReceive==True:
                print(
                f"Received value {data['value']} of device {data['device']} from {oct(header.from_node)}",
                f"to {oct(header.to_node)} "
                )
                if header.from_node==node1:
                    self.handleDataReceiveFromNode1(data)
                elif  header.from_node==node2:
                    self.handleDataReceiveFromNode2(data)
                elif header.from_node==node21:
                    self.handleDataReceiveFromNode21(data)
                else :
                    print("Khong co xu ly tu node",header.from_node)
            else:
                print("Nhan payload",payload,"from node",oct(header.from_node))
    
    def sendToNode(self,node,device,value ):
        payload = struct.pack("HBBH", self.xacThuc1 ,device,self.xacThuc2,self.packets_sent)
        ok = self.network.write(RF24NetworkHeader(node), payload)
        print(f"Sending  {value} to device {device} of node {oct(node)}...", "ok." if ok else "failed.")

    def sendToMCU(self):
        self.network.update()
        now = int(time.monotonic_ns() / 1000000)
        

        if now - self.last_sent >= self.interval:
            self.last_sent = now
            self.packets_sent += 1
            # self.sendToNode(node1,0,self.packets_sent)  
            self.sendToNode(node2,0,self.packets_sent)  
            self.sendToNode(node21,0,self.packets_sent+15)           

    def run(self):
        if not self.check_server_mqtt():
            print("not connect server mqtt!!")
            return
        self.client.topic = 'control'
        self.client.subscribe_value = 'start'
        self.client.connect_mqtt()
        self.client.client.loop_start()
        try:
            while True:
                #self.receiveFromMcuAndHandle()
                time.sleep(1)
                value_sub = self.client.get_subscribe()
                print(value_sub)
                
                
                #self.sendToMCU()
        except KeyboardInterrupt:
            print("powering down radio and exiting.")
            self.radio.powerDown()


IOT=IOT_Rasp(22, 0,0o0,host_mqtt='localhost')
IOT.run()


        