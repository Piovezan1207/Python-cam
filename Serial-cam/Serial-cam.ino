#include <Servo.h>
String palavra;
Servo servo;
Servo servo2;
byte var = 90;
byte var2 = 90;
byte v1,v2,v3,v4;
void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo2.attach(10);
  
}

void loop()
{


}

void serialEvent() {
char letra = Serial.read();
  switch(letra)
  {
    case 'a': if(var <180) var++; break;
    case 'c': if(var > 0) var--; break;
    case 'd': if(var2 <180) var2++; break;
    case 'e': if(var2 > 0) var2--; break;
  }
  servo.write(var);
  servo2.write(var2);
 //  delay(5);
//  Serial.println("ok");

}


/* void serialEvent() {
char letra = Serial.read();
  switch(letra)
  {
    case 'a': v1++; break;
    case 'c': v2++; break;
    case 'd': v3++; break;
    case 'e': v4++; break;
  }
  if (v1 == 2)  {if(var <180) var++; v1 = 0;}
  if (v2 == 2)  {if(var > 0) var--; v2 = 0;}
  if (v3 == 2)  {if(var2 <180) var2++; v3 = 0;}
  if (v4 == 2)  {if(var2 > 0) var2--; v4 = 0;}
  servo.write(var);
  servo2.write(var2);
  Serial.println("ok");

}*/
 
