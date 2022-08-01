
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <Servo.h>
#include <AHT10.h>
#include <Wire.h>

#define TIME_SENDING 10000
#define XAC_THUC1 52836
#define XAC_THUC2 147
#define NHIET_DO 1
#define DO_AM 2

unsigned long _time;
RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
AHT10 myAHT10(AHT10_ADDRESS_0X38);
const uint16_t this_node = 01;   // Address of our node in Octal format ( 04,031, etc)
const uint16_t master00 = 00;    // Address of the other node in Octal format
uint8_t readStatusAHT10 = 0;


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
 void NhanVaGuiDuLieuAHT10(const uint16_t node){
  readStatusAHT10= myAHT10.readRawData(); //read 6 bytes from AHT10 over I2C
   if (readStatusAHT10 != AHT10_ERROR)
    {
      unsigned int nhietDo=( unsigned int)round(myAHT10.readTemperature());//nhiet do C
    Serial.print(F("Temperature: ")); Serial.print(nhietDo); Serial.println(F(" +-0.3C")); 
    sendingData(node,NHIET_DO,nhietDo);
    
    unsigned int doAm=( unsigned int)round(myAHT10.readHumidity());
    Serial.print(F("Humidity...: ")); Serial.print(doAm);    Serial.println(F(" +-2%"));   
    sendingData(node,DO_AM,doAm);
    }
    else
    {
      Serial.print(F("Failed to read - reset: ")); 
      Serial.println(myAHT10.softReset());         //reset 1-success, 0-failed
    } 
  }

void setup() {
  SPI.begin();
  radio.begin();
  network.begin(90, this_node); //(channel, node address)
  radio.setDataRate(RF24_1MBPS);
  Serial.begin(115200);
  Serial.println("node01");
  Serial.println("setup finish");
  _time = millis();

    while (myAHT10.begin() != true)
  {
    Serial.println(F("AHT10 not connected or fail to load calibration coefficient")); //(F()) save string to flash & keeps dynamic memory free
    delay(1000);
  }
  Serial.println(F("AHT10 OK"));
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

  //===== Sending data after TIME_SENDING =====//
 if ( (unsigned long) (millis() - _time) > TIME_SENDING)
    {    
    NhanVaGuiDuLieuAHT10(master00);
       
     //Update _time var
     _time = millis();
    } 
    
}
