#include "CytronMotorDriver.h"
#include <SoftwareSerial.h>



SoftwareSerial mySerial(2, 3); // RX, TX
CytronMD motor(PWM_DIR, 10, 9);
CytronMD motor2(PWM_DIR, 11, 6);

char data = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
  }
  Serial.println("Robot started");
  mySerial.begin(9600);

}

void loop() {
  if(mySerial.available())      
   {
      data = mySerial.read();
      delay(5);        
      Serial.print(data);          
      Serial.print("\n");
      if(data == 'F') 
        {
          motor.setSpeed(255);
          motor2.setSpeed(255);
          //delay(1000);
        }
      else if(data == 'B')        
         { 
           motor.setSpeed(-255);
           motor2.setSpeed(-255);
           //delay(1000);
         }
      else if(data == 'R')
      {
        motor.setSpeed(255);
        motor2.setSpeed(-255);

      }
      else if(data == 'L')
      {
        motor.setSpeed(-255);
        motor2.setSpeed(255);

      }
      else
      {
        motor.setSpeed(0);
        motor2.setSpeed(0);
      }
   }
}
