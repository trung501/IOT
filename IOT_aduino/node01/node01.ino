
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <Servo.h>

unsigned long time;
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
  Serial.println("node01");
  Serial.println("setup finish");
  time = millis();
}

void loop() {
  network.update();
  //===== Receiving =====//
  while ( network.available() ) {     // Is there any incoming data?
    RF24NetworkHeader header;
    sending incomingData;
    network.read(header, &incomingData, sizeof(incomingData)); // Read the incoming data
    if(checkXacThuc(incomingData)){
      Serial.print("Received value ") ;
      Serial.print(incomingData.value) ;
      Serial.print(" of device ") ;
      Serial.print(incomingData.device) ;
      Serial.print(" from node ") ;
      Serial.println(header.from_node);      
      }    
  }

  //===== Sending data after 10s =====//
 if ( (unsigned long) (millis() - time) > 10000)
    {
      //Send to node0 - master
      sending data ={xacThuc1,1,xacThuc2,20};
      RF24NetworkHeader header8(master00);
      bool ok = network.write(header8, &data, sizeof(data)); // Send the data     
    } 
    
}
