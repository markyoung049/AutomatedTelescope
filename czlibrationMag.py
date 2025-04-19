import serial
import numpy as np
import matplotlib.pyplot as plt
import time



offX = 22.05
offY = 17.47
offZ = -117.98


# Set up serial communication with the Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your port



# Collect data for 30 seconds
time_data = []
mag_x_data = []
mag_y_data = []
mag_z_data = []

start_time = time.time()


while time.time() - start_time < 60:  # Run for 30 seconds


    if arduino.in_waiting > 0:

        # Read the request from Arduino
        request = arduino.readline().decode('utf-8').strip().split(' ')

        if request[0] == "Data:":

            mag_x, mag_y, mag_z = float(request[4]) - offX, float(request[5]) - offY, float(request[6]) - offZ  # Replace with actual sensor data read
            mag_x_data.append(mag_x)
            mag_y_data.append(mag_y)
            mag_z_data.append(mag_z)

# After collecting the data, create a 3D scatter plot
# Create subplots for XY, XZ, and YZ planes
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# XY Plane: Plot Mag X vs Mag Y
axs[0].scatter(mag_x_data, mag_y_data, c='b', marker='o')
axs[0].set_xlabel('Mag X (µT)')
axs[0].set_ylabel('Mag Y (µT)')
axs[0].set_title('XY Plane')

# XZ Plane: Plot Mag X vs Mag Z
axs[1].scatter(mag_x_data, mag_z_data, c='r', marker='o')
axs[1].set_xlabel('Mag X (µT)')
axs[1].set_ylabel('Mag Z (µT)')
axs[1].set_title('XZ Plane')

# YZ Plane: Plot Mag Y vs Mag Z
axs[2].scatter(mag_y_data, mag_z_data, c='g', marker='o')
axs[2].set_xlabel('Mag Y (µT)')
axs[2].set_ylabel('Mag Z (µT)')
axs[2].set_title('YZ Plane')

# Show the plots
plt.tight_layout()
plt.show()



















"""
# Set up serial communication with the Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your port

running = True

while running:

    

            """