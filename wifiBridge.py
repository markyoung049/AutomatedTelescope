import serial
import requests
import base64
import datetime

# Set up serial communication with the Arduino
arduino = serial.Serial('COM4', 9600)  # Replace 'COM3' with your port

latitude = "33.7758"
longitude = "-84.3973"




userpass = "05828125-953d-431d-9d45-e1a6aa44590a" \
":afcc636292ef134fd9dc94eeb0d2ae5c097c2aa152ca42657e1d6d5eb5ae2dcaadd6b91819e76e2d0640706e42dfb984e52073982ebd9e2de13814a9ddb3461b92a35b6ecdf6f98fe1e7377532256b823dc030dec463c842fa49b6394bbc9f845d8c24d5ed4b88d2f5a2ddf563cb5920"
authString = base64.b64encode(userpass.encode()).decode()

while True:
    if arduino.in_waiting > 0:

        # Read the request from Arduino
        request = arduino.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {request}")
        # if getting the position

        if request == 'Position':
            # Send the daa to the arduino
            arduino.write((latitude+ ", "+ longitude + '\n').encode('utf-8'))
            


        # If getting the API call
        elif request[:4] == "Body":
            name = request[6:]

            # Get the current date
            currentDate = datetime.date.today()
            currentTime = datetime.datetime.now().strftime('%H:%M:%S')


            # Make the request
            url = f'https://api.astronomyapi.com/api/v2/bodies/positions/{name}'

            headers = {"Authorization": "Basic " + authString }

            params = {
                "latitude": latitude,       
                "longitude": longitude,     
                "elevation": 10,           
                "from_date": currentDate, 
                "to_date": currentDate,   
                "time": currentTime   
            }      

            # Grab azimuth and send to arduino
            response = requests.get(url, headers = headers, params=params)
            data = response.json()
            azimuth = data.get('data').get('table')['rows'][0]['cells'][0]['position']['horizontal']['azimuth']['degrees']
            arduino.write(azimuth.encode('utf-8'))
            # Print the response or send it back to Arduino

            #print(f"Server response: {response.text}")





