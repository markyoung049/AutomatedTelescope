import serial
import requests
import base64

# Set up serial communication with the Arduino
arduino = serial.Serial('COM4', 9600)  # Replace 'COM3' with your port


userpass = "5775f5b4-8f70-4a11-8ee6-3f7ed55887fb" \
":afcc636292ef134fd9dc94eeb0d2ae5c097c2aa152ca42657e1d6d5eb5ae2dcaadd6b91819e76e2d0640706e42dfb984e52073982ebd9e2de13814a9ddb3461bf70ab6df93390918c1ff24fdcaf2a6ed15bcc949f06481d80727905f1a1b34228ed9bf3ec6f2c709aab989e006839b4e"
authString = base64.b64encode(userpass.encode()).decode()

while True:
    if arduino.in_waiting > 0:

        # Read the request from Arduino
        request = arduino.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {request}")

        print(request)
        # if getting the position
        if request == 'Position':

            longitude = "33.775867"
            latitude = "-84.39733"

            arduino.write((latitude+ ", "+ longitude + '\n').encode('utf-8'))
            


        # if getting the API call
        else:

            # Replace with your actual API endpoint
            url = 'https://api.astronomyapi.com/api/v2/bodies/positions/:mars'
            header = {"Authorization": "Basic " + authString}
            response = requests.get(url, headers = header)

            # Print the response or send it back to Arduino
            #print(f"Server response: {response.text}")