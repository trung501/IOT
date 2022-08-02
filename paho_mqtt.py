from itertools import count
import time
from paho.mqtt import client as mqtt_client

class MQTT_client():
    def __init__(self,host,topic = None,id_name='python_mqtt',port = 1883):
        self.host=host
        self.port = port
        self.client = mqtt_client.Client(self.host)
        self.topic = topic
        self.subscribe_value = None
    def set_username_password(self,username,password):
        self.client.username_pw_set(username,password)
    def connect_mqtt(self):
        def on_connect(client,userdata,flags,rc):
            if rc == 0:
                print("Connected to MQTT broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        self.client.on_connect = on_connect
        self.client.connect(self.host,self.port)
    def publish(self,msg="hello nod-red"):
        self.client.loop_start()
        result = self.client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
        self.client.loop_stop()
    def subscribe(self,topic='control'):
        self.topic = topic
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic on server mqtt")
            self.subscribe_value= (msg.payload.decode())
        #self.client.loop_start()
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
    def get_subscribe(self,topic='control'):
        old_value = self.subscribe_value
        self.subscribe(topic)
        if old_value != self.subscribe_value :
            return True,self.subscribe_value
        else:
            return False,0



def run():
    client = MQTT_client('192.168.0.176')
    client.topic = 'control'
    client.connect_mqtt()
    while True:
    #   
        # time.sleep(1)
        check,value = client.get_subscribe()
        if check:
            print(value)
            

if __name__ == '__main__':
    run()
