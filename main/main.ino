#include <math.h>
#include <Wire.h>         // Library that allows communication with I2C Device
#include <MPU9250.h>

MPU9250 mpu;

void setup() {
  Serial.begin(9600);
  
  Wire.begin();
  
  if (!mpu.setup(0x68)) {  // Address of the MPU9250
    Serial.println("MPU9250 connection failed.");
    while (1);
  }
}

void loop() {
  if (mpu.update()) {
    float accelerometer[3] = {mpu.getAccX(), mpu.getAccY(), mpu.getAccZ()}; // Grabbing the acceleration vector
    float magnometer[3] = {mpu.getMagX(), mpu.getMagY(), mpu.getMagZ()}; // Grabbing the magnometer vector
    float gyroscope[3] = {mpu.getGyroX(), mpu.getGyroY(), mpu.getGyroZ()}; // Grabbing the gyroscope vector
    Serial.print("Data: ");
    Serial.print(accelerometer[0]);
    Serial.print(' ');
    Serial.print(accelerometer[1]);
    Serial.print(' ');
    Serial.print(accelerometer[2]);
    Serial.print('\n');
    delay(10);
    // Compute where east is
    float east[3] = { accelerometer[2]*magnometer[3] - accelerometer[3]*magnometer[2],
                        accelerometer[3]*magnometer[1] - accelerometer[1]*magnometer[3],
                        accelerometer[1]*magnometer[2] - accelerometer[2]*magnometer[1]};


  }
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