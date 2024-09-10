#include <Wire.h>

#define MPU9250_ADDRESS 0x68  // MPU-9250 I2C address
#define AK8963_ADDRESS 0x0C   // Magnetometer (AK8963) I2C address

// MPU-9250 Registers
#define ACCEL_XOUT_H 0x3B
#define GYRO_XOUT_H 0x43
#define PWR_MGMT_1 0x6B
#define CONFIG 0x1A
#define SMPLRT_DIV 0x19
#define GYRO_CONFIG 0x1B
#define ACCEL_CONFIG 0x1C
#define AK8963_CNTL1 0x0A
#define AK8963_ASAX 0x10
#define AK8963_HXL 0x03

/*
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float magX, magY, magZ;


void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  // Initialize MPU-9250 (Accel + Gyro)
  initMPU9250();
  
  // Initialize AK8963 (Magnetometer)
  initAK8963();
}


void loop() {
  // Read accelerometer data
  float accel[3];
  readAccelData(accel);
  float accelX = accel[0];
  float accelY = accel[1];
  float accelZ = accel[2];
  
  // Read gyroscope data
  float gyro[3];
  readGyroData(gyro);
  float gyroX = gyro[0];
  float gyroY = gyro[1];
  float gyroZ = gyro[2];
  
  // Read magnetometer data
  float mag[3];
  readMagData(mag);
  float magX = mag[0];
  float magY = mag[1];
  float magZ = mag[2];

  // Print out the raw data
  Serial.print("Accel: X = "); Serial.print(accelX); Serial.print(", Y = "); Serial.print(accelY); Serial.print(", Z = "); Serial.println(accelZ);
  Serial.print("Gyro: X = "); Serial.print(gyroX); Serial.print(", Y = "); Serial.print(gyroY); Serial.print(", Z = "); Serial.println(gyroZ);
  Serial.print("Mag: X = "); Serial.print(magX); Serial.print(", Y = "); Serial.print(magY); Serial.print(", Z = "); Serial.println(magZ);
  
  delay(3000);
}
*/
void initMPU9250() {
  // Wake up MPU-9250
  writeByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x00);
  
  // Set sample rate to 1 kHz
  writeByte(MPU9250_ADDRESS, SMPLRT_DIV, 0x07);
  
  // Set accelerometer configuration (+/- 2g full scale)
  writeByte(MPU9250_ADDRESS, ACCEL_CONFIG, 0x00);
  
  // Set gyroscope configuration (+/- 250 deg/s full scale)
  writeByte(MPU9250_ADDRESS, GYRO_CONFIG, 0x00);
  
  // Set DLPF (Digital Low Pass Filter) configuration
  writeByte(MPU9250_ADDRESS, CONFIG, 0x01);
}

void initAK8963() {
  // Set AK8963 to Power Down mode
  writeByte(AK8963_ADDRESS, AK8963_CNTL1, 0x00);
  delay(10);

  // Set AK8963 to Fuse ROM access mode to get sensitivity adjustment values
  writeByte(AK8963_ADDRESS, AK8963_CNTL1, 0x0F);
  delay(10);

  // Set AK8963 to Continuous measurement mode 2 (100 Hz)
  writeByte(AK8963_ADDRESS, AK8963_CNTL1, 0x16);
  delay(10);
}

void readAccelData(float *data) {
  uint8_t rawData[6];  // x/y/z accel data
  readBytes(MPU9250_ADDRESS, ACCEL_XOUT_H, 6, &rawData[0]);
  
  // Convert the data to 16-bit values
  accelX = ((int16_t)rawData[0] << 8) | rawData[1];
  accelY = ((int16_t)rawData[2] << 8) | rawData[3];
  accelZ = ((int16_t)rawData[4] << 8) | rawData[5];

  // Convert from data format (-32768, 32768) to g (-2g, 2g)
  float accelXF = float(accelX)/16384;
  float accelYF = float(accelY)/16384;
  float accelZF = float(accelZ)/16384;
  
  data[0] = accelXF;
  data[1] = accelYF;
  data[2] = accelZF;

}

void readGyroData(float *data) {
  uint8_t rawData[6];  // x/y/z gyro data
  readBytes(MPU9250_ADDRESS, GYRO_XOUT_H, 6, &rawData[0]);
  
  // Convert the data to 16-bit values
  gyroX = ((int16_t)rawData[0] << 8) | rawData[1];
  gyroY = ((int16_t)rawData[2] << 8) | rawData[3];
  gyroZ = ((int16_t)rawData[4] << 8) | rawData[5];

   // Convert from data format (-32768, 32768) to g (-250 degrees/s, 250 degrees/s)
  float gyroXF = float(gyroX * 250) / 16384;
  float gyroYF = float(gyroY * 250) / 16384;
  float gyroZF = float(gyroZ * 250) / 16384;

  data[0] = gyroXF;
  data[1] = gyroYF;
  data[2] = gyroZF;  
}

void readMagData(float *data) {
  uint8_t rawData[7];  // x/y/z mag data + status
  readBytes(AK8963_ADDRESS, AK8963_HXL, 7, &rawData[0]);
  
  // Convert the data to 16-bit values
  magX = ((int16_t)rawData[1] << 8) | rawData[0];
  magY = ((int16_t)rawData[3] << 8) | rawData[2];
  magZ = ((int16_t)rawData[5] << 8) | rawData[4];

  // Covert raw data to mircoTeslas
  float magXF = float(magX) * 0.15;
  float magYF = float(magY) * 0.15;
  float magZF = float(magZ) * 0.15;

  data[0] = magXF;
  data[1] = magYF;
  data[2] = magZF;
}

// Helper function to write a byte to a specific register
void writeByte(uint8_t address, uint8_t subAddress, uint8_t data) {
  Wire.beginTransmission(address);  // Start communication with the device
  Wire.write(subAddress);           // Send the register address
  Wire.write(data);                 // Send the data
  Wire.endTransmission();           // End transmission
}

// Helper function to read multiple bytes from a specific register
void readBytes(uint8_t address, uint8_t subAddress, uint8_t count, uint8_t * dest) {
  Wire.beginTransmission(address);  // Start communication with the device
  Wire.write(subAddress);           // Send the register address
  Wire.endTransmission(false);      // End transmission but keep the connection active
  Wire.requestFrom(address, count); // Request 'count' bytes from the device

  uint8_t i = 0;
  while (Wire.available()) {
    dest[i++] = Wire.read();  // Receive the bytes into the buffer
  }
}
