#include <math.h>
#include <Wire.h>         // Library that allows communication with I2C Device
#include "mpu.h"


void setup() {
  Serial.begin(9600);
  
  Wire.begin();
  
  // Initialize MPU-9250 (Accel + Gyro)
  initMPU9250();
  
  // Initialize AK8963 (Magnetometer)
  initAK8963();
}

void loop() {
    
  float accel[3] = {0.0, 0.0, 0.0}; // Grabbing the acceleration vector
  float mag[3] = {0.0, 0.0, 0.0}; // Grabbing the magnetometer vector
  float gyro[3] = {0.0, 0.0, 0.0}; // Grabbing the gyroscope vector 

  // Avgerage the values for smoothing 
  for (int i=0; i<100; i++){

  
    float a[3]; // Grabbing the acceleration vector
    float m[3]; // Grabbing the magnetometer vector
    float g[3]; // Grabbing the gyroscope vector

    
    readAccelData(a);
    //readGyroData(g);
    

    readMagData(m);

   
    accel[0] += a[0]/100; 
    accel[1] += a[1]/100; 
    accel[2] += a[2]/100;
    
    mag[0] += m[0]/100; 
    mag[1] += m[1]/100; 
    mag[2] += m[2]/100;
    
  }

  Serial.print("Data: ");
  
  Serial.print(accel[0]);
  Serial.print(' ');
  Serial.print(accel[1]);
  Serial.print(' ');
  Serial.print(accel[2]);
  Serial.print(' '); 
  
  Serial.print(mag[0]);
  Serial.print(' ');
  Serial.print(mag[1]);
  Serial.print(' ');
  Serial.print(mag[2]);

  Serial.print('\n');
  
  
  // Compute where east is
  /*
  float east[3] = { accelerometer[2]*magnometer[3] - accelerometer[3]*magnometer[2],
                      accelerometer[3]*magnometer[1] - accelerometer[1]*magnometer[3],
                      accelerometer[1]*magnometer[2] - accelerometer[2]*magnometer[1]};
  Serial.println(magnometer[0]);
  Serial.println(magnometer[1]);
  Serial.println(magnometer[2]);
  */
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


// This funcitons caluclates the azimuth from the data in requestLocation
float getAzimuth(float data){

  float azimuthRadians = data * (PI/180);
  // Azimuth has north set a zero, so this angle needs a correction
  azimuthRadians = -(azimuthRadians + PI/2);
  return azimuthRadians;
}