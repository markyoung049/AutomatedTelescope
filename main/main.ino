void setup() {
  // put your setup code here, to run once:


  Serial.begin(9600);
  while (!Serial) {
      ; // Wait for the serial port to connect
  }

  Serial.println("Arduino Ready");
  float position[2];
  requestLocation(position);
  Serial.println(position[1]);

  String data = requestBodyPosition("moon", 85.5, 82);
  Serial.println(data);
}



void loop() {
  // put your main code here, to run repeatedly:

}



// returns the coordinates of the object in the sky
String requestBodyPosition(String name, float latitude, float longitude) {
  Serial.println("Body: " + name);

  // Loop until python returns a reponse
  while (Serial.available() == 0) {
    delay(100);
  }

  String incomingData = Serial.readStringUntil('\n');  // Read incoming data until newline character
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