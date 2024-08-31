#include <math.h>


const int north = 2; // North Pin
const int west = 8; // West Pin
const int east = 12; // East Pin
const int south = 13; // North Pin

void setup() {
  // put your setup code here, to run once:
  pinMode(north, OUTPUT);
  pinMode(south, OUTPUT);
  pinMode(east, OUTPUT);
  pinMode(west, OUTPUT);

  digitalWrite(north, HIGH);
  delay(1000);

  digitalWrite(east, HIGH);
  delay(1000);

  digitalWrite(south, HIGH);
  delay(1000);

  digitalWrite(west, HIGH);
  delay(1000);
  



  Serial.begin(9600);
  while (!Serial) {
      ; // Wait for the serial port to connect
  }

  Serial.println("Arduino Ready");
  float position[2];
  requestLocation(position);
 

  float data = requestBodyPosition("moon", 85.5, 82);
  Serial.println(data);

  float azimuthRadians = data * (PI/180);
  // Azimuth has north set a zero, so this angle needs a correction
  azimuthRadians = -(azimuthRadians + PI/2);
  
  // Show angle on circuit 
  float y = sin(azimuthRadians);
  float x = cos(azimuthRadians);

  // Square the values to make it more apparent on the display
  y = y*y;
  x = x*x;

// Display North/South
  if (y >= 0) {
    int brightness = round(y * 255 / (2*PI));
    analogWrite(north, brightness);   
  }
  else {
    int brightness = round(y * -255 / (2*PI));
    analogWrite(south, brightness);
  }

// Display East/West
  if (x >= 0) {
    int brightness = round(x * 255 / (2*PI));
    analogWrite(east, brightness);   
  }
  else {
    int brightness = round(x * -255 / (2*PI));
    analogWrite(west, brightness);
  }




  // get Azimuth of the moon and show on leds
  delay (10000);
}



void loop() {
  // put your main code here, to run repeatedly:

}



// returns the coordinates of the object in the sky
float requestBodyPosition(String name, float latitude, float longitude) {
  Serial.println("Body: " + name);

  // Loop until python returns a reponse
  while (Serial.available() == 0) {
    delay(100);
  }

  float incomingData = Serial.readStringUntil('\n').toFloat();  // Read incoming data until newline character
  return incomingData;
}



// Returns position as [latitude, longitude]
void requestLocation(float position[2]) {
  Serial.println("Position");

  // Loop until Data found
  while (Serial.available() == 0) {
    delay(100);
  }

  float latitude = Serial.readStringUntil(' ').toFloat();  // Read latitude
  float longitude = Serial.readStringUntil('\n').toFloat();  // Read longitude
  
  // Return the coords as an array
  position[0] = latitude;
  position[1] = longitude;
  return position;
}