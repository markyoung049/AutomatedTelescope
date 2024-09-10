#include <arduino.h>
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

// Initialize gyro and accelerometer
void initMPU9250();

// Initialize magnetometer
void initAK8963();

// Grab accelerometer data
void readAccelData(float *data);

// Grab gyro data
void readGyroData(float *data);

// Grab magnetometer data
void readMagData(float *data);

// Helper function to write a byte to a specific register
void writeByte(uint8_t address, uint8_t subAddress, uint8_t data);

// Helper function to read multiple bytes from a specific register
void readBytes(uint8_t address, uint8_t subAddress, uint8_t count, uint8_t * dest);