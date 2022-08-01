from itertools import count
import time
from paho.mqtt import client as mqtt_client

class MQTT_client():
    def __init__(self,host,topic = None,id_name='python_mqtt',port = 1883):
        self.host=host
        self.port = port
        self.client = mqtt_client.Client(self.host)
        self.topic = topic
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
        self.client.loop_start()
        self.topic = topic
        result = []
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic on server mqtt")
            result.append(msg.payload.decode())
            return
            # if len(result) > 1:
            #     return result[-1]
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        self.client.loop_stop()
        # self.client.loop_forever()
        if len(result) > 0:
            return result.pop()
        return 5

def run():
    client = MQTT_client('192.168.0.176')
    client.topic = 'control'
    client.connect_mqtt()
    while True:
        print(client.subscribe())

    # client = connect_mqtt()
    # subscribe(client)
    # client.loop_forever()
    # client.loop_start()
    # #client.loop_start()
    # #publish(client)


if __name__ == '__main__':
    run()
