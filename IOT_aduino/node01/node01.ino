
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <Servo.h>

#define TIME_SENDING 10000
#define XAC_THUC1 52836
#define XAC_THUC2 147

unsigned long _time;
RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 01;   // Address of our node in Octal format ( 04,031, etc)
const uint16_t master00 = 00;    // Address of the other node in Octal format
struct sending{
   unsigned int xacThuc1;
   byte device;
   byte xacThuc2;
   unsigned int value;
};

bool checkXacThuc(sending Data){
  if (Data.xacThuc1==XAC_THUC1 && Data.xacThuc2==XAC_THUC2){
    return true;
    }
    return false;
  }
bool sendingData(const uint16_t node, byte device,unsigned int value ){
      sending data ={XAC_THUC1,device,XAC_THUC2,value};//device=1,value=20
      RF24NetworkHeader header(node);
      bool ok= network.write(header, &data, sizeof(data)); // Send the data   
      Serial.print("Send note ");  
      Serial.print(node); 
      Serial.print(" is "); 
       if (ok){
        Serial.println("OK");
       }
      else{
        Serial.println("Fail");
        }
       return ok;
  }
  

void setup() {
  SPI.begin();
  radio.begin();
  network.begin(90, this_node); //(channel, node address)
  radio.setDataRate(RF24_1MBPS);
  Serial.begin(9600);
  Serial.println("node01");
  Serial.println("setup finish");
  _time = millis();
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
 if ( (unsigned long) (millis() - _time) > TIME_SENDING)
    {
      //Send to node0 - master
      bool ok = sendingData(master00,1,20);//node=0,device=1,value=20   
       
     //Update _time var
     _time = millis();
    } 
    
}
