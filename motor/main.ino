#include <math.h>
#include <string.h>
// Define pins for the stepper driver
const int stepPin = 2;  // Step pin
const int dirPin = 5;   // Direction pin
const int enabPin = 8; // Enable pin
const int stepSize = 200;



  

// Function to turn a motor a given angle at a given speed (degrees, degrees/s)
void turn(float angle, float speed) {

  // Enable the motor
  digitalWrite(enabPin, LOW);
  // Set the direciton to turn
  if (angle >= 0) {
    digitalWrite(dirPin, HIGH);
  }

  else {
    digitalWrite(dirPin, LOW);
    angle = -angle;
  }

  // Calculate the needed parameters for the turn
  int steps = round((angle / 360) * stepSize); // gives number of pulses to send
  Serial.println(steps);
  float stepSpeed = (speed / 360) * stepSize; // gives the speed in steps
  int timePerStep = round(1000000 / stepSpeed); // Gives the time delay for each pulse in ms

  for (int i = 0; i < steps; i++) {  // 400 steps for one full revolution 
    digitalWrite(stepPin, HIGH);    // Send a step pulse
    delayMicroseconds(timePerStep);        // Adjust the speed (1000 microseconds = 1ms delay)
    digitalWrite(stepPin, LOW);     // Complete the step
    delayMicroseconds(timePerStep);        // Adjust the speed
  }

  digitalWrite(enabPin, HIGH);
}




void setup() {
  Serial.begin(9600);  // Start Serial Monitor
  Serial.println("Uploaded...");
  // Set the step and direction pins as outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enabPin, OUTPUT);

  // Set the direction of the motor
  digitalWrite(dirPin, HIGH);  // Set motor direction to clockwise (change to LOW for counterclockwise)

  // Enabl the driver
  digitalWrite(enabPin, LOW);
}


void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int separatorIndex = input.indexOf(':');
    String command = input.substring(0, separatorIndex);
    String args = input.substring(separatorIndex + 1);
    int separatorIndex = input.indexOf(',');
    String arg1 = input.substring(0, separatorIndex);
    String arg2 = input.substring(separatorIndex + 1);


    if (command == "turn") {
      float angle = arg1.toFloat();
      float speed = arg2.toFloat();
      turn(angle, speed);
    } else {
      
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

