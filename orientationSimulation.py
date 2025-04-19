import serial
import pygame
import sys
import math
import numpy as np

# Set up serial communication with the Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your port

# Initialize Pygame
pygame.init()

# Set up the display
screenSize = 600
screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("Pygame Initialization")

# Set the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # Check if new data is avaliable
    if arduino.in_waiting > 0:

        # Read the request from Arduino
        request = arduino.readline().decode('utf-8').strip().split(' ')

        if request[0] == "Data:":

            # Do math for accelerometer vector
            origin = (screenSize // 2, screenSize // 2) # Compute the origin
            up = np.array([float(request[1]), float(request[2]), float(request[3])]) # Get the accel ector
            up = up / np.linalg.norm(up) # Normalize the vector
            
            # Magnetometer vector
            offset = np.array([17.47, 22.05, 117.98]) # Offset for the magnetometer vector
            magVector = np.array([float(request[4]), float(request[5]), float(request[6])]) - offset
            magVector = magVector / np.linalg.norm(magVector) # Normalize the vector

            # Compute east via accel x magw
            east = np.cross(magVector, up) # Cross product of accel and mag vectors   
            east = east / np.linalg.norm(east) # Normalize the vector

            # North is east x up
            north = np.cross(up, east) # Cross product of east and accel vectors
            north = north / np.linalg.norm(north) # Normalize the vector
            
            # Now transform from the seosors coorindtas to 3d space using north, east, and up as bases
            transformInverse = np.array([east, north, up]).T
            transform = np.linalg.inv(transformInverse) # Inverse of the transformation matrix
            y = np.array([0, -1, 0]).T

            yNew = np.dot(transform, y) # This is the heading vector in 3d space
            
            lineSize = screenSize // 3 # Sets the max length of the line
            normalizedVector = [int(yNew[0] * lineSize), 
                                int(yNew[1] * 255 ), # normalized for color, if confused keep reading
                                int(yNew[2] * lineSize)] # Vector normalization to line size

            # Compute line endpoint (uses Z because im showing this in x-z plane)
            endPoint = (origin[0] - normalizedVector[0], # transform based on nveted x axis o accelerometer
                        origin[1] - normalizedVector[2]) # subtracts because pygame's y-axis is inverted

            # Depict y axis with color. green for toward you and red for away
            color = []
            if yNew[1] >= 0:
                color = [0, normalizedVector[1], 0]
            else:
                color = [-normalizedVector[1], 0, 0] 
                
            headingX = math.atan2(yNew[0], yNew[1]) * (180.0 / math.pi)
            headingY = math.atan2(yNew[2], yNew[1]) * (180.0 / math.pi)
            print("Heading X: ", headingX)
            print("Heading Y: ", headingY)

            # Draw the line
            # Fill the screen with a color (optional)
            screen.fill((255, 255, 255))  # White background
            try:
                pygame.draw.line(screen, color, origin, endPoint, 5)
            except:
                running = False
                print("Color invalid: ")
                print(color)

            # Update the display
            pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()


# NOTES: THIS IS BASICALLY A PROGRAM THAT TRANSFORMS SPACE BETWEEN MPU AND OUR SPACE.
# SO YOU APPLY THE TRANSFORM TO THE SENSORS Z AXIS AND SEE HOW IT TURNS. THIS IS EASY, ITS JUST ADDING 
# AND SUBTRACTING VECTORS WHICH WORS SINCE ITS OF LENGTH 1 ALWAYS. BASICALLY