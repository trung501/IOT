
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <Servo.h>

#define TIME_SENDING 5000
#define XAC_THUC1 52836
#define XAC_THUC2 147

unsigned long _time;
RF24 radio(D4, D8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 02;   // Address of our node in Octal format ( 04,031, etc)
const uint16_t master00 = 00;    // Address of the other node in Octal format
const uint16_t node01 = 01;
struct sending{
   unsigned short xacThuc1;
   byte device;
   byte xacThuc2;
   unsigned short value;
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
   Serial.begin(115200);
  Serial.println("delay 1000");
  delay(1000);
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
      else{
         Serial.println("Du lieu gui den chua xac dinh");   
        }
  }
  
 //===== Sending data after 10s =====//
 if ( (unsigned long) (millis() - _time) > TIME_SENDING)
    {

      bool ok = sendingData(master00,1,6);//node=0,device=1,value=6      
      
      
      ok = sendingData(node01,5,17);//node=1,device=5,value=17    
       
         //Update _time var
        _time = millis();
     }
}
