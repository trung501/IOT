
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <Servo.h>


RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 01;   // Address of our node in Octal format ( 04,031, etc)
const uint16_t master00 = 00;    // Address of the other node in Octal format
unsigned int xacThuc1=52836;
byte xacThuc2=147;
struct sending{
   unsigned int xacThuc1;
   byte device;
   byte xacThuc2;
   unsigned int value;
};

bool checkXacThuc(sending Data){
  if (Data.xacThuc1==xacThuc1 && Data.xacThuc2==xacThuc2){
    return true;
    }
    return false;
  }

void setup() {
  SPI.begin();
  radio.begin();
  network.begin(90, this_node); //(channel, node address)
  radio.setDataRate(RF24_1MBPS);
  Serial.begin(9600);
  Serial.println("delay 1000");
  delay(1000);
  Serial.println("setup finish");
}

void loop() {
  network.update();
  //===== Receiving =====//
  while ( network.available() ) {     // Is there any incoming data?
    RF24NetworkHeader header;
    sending incomingData;
    network.read(header, &incomingData, sizeof(incomingData)); // Read the incoming data
    if (header.from_node == 0) {    // If data comes from Node 0
      if (checkXacThuc(incomingData)){
        Serial.print("Master ");
        Serial.print("value ");
        Serial.println(incomingData.value);
        }
       else{
        Serial.println("Du lieu nhan duoc loi");
        }
    }
    if (header.from_node == 10) {    // If data comes from Node 012
     Serial.println("Node012");
    }    
  }

  sending data ={xacThuc1,1,xacThuc2,20};
  RF24NetworkHeader header8(master00);
  bool ok = network.write(header8, &data, sizeof(data)); // Send the data
  delay(1000);
  data.device=2;
  data.value=39;
  ok =  network.write(header8, &data, sizeof(data)); // Send the data
  delay(1000);
}
