from RF24 import RF24
from RF24Network import RF24Network

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
try:
    while True:
        network.update()
        while network.available():
            header, payload = network.read(4)            
            print("payload length ", len(payload))
            print(
                f"Received payload {list(payload)[0]} from {oct(header.from_node)}",
                f"to {oct(header.to_node)} ",
            )
            # print("payload:",payload)
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.powerDown()


