import serial
import pygame
import sys
import math

# Set up serial communication with the Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your port

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
            accelVector = [float(request[1]), float(request[2]), float(request[3])] # Get the accel ector
            accelMagnitude = math.sqrt(accelVector[0] * accelVector[0] + accelVector[1] * accelVector[1] + accelVector[2] * accelVector[2]) # Compute vector magnitude
            normalizedAccel = [accelVector[0] / accelMagnitude, accelVector[1] / accelMagnitude, accelVector[2] / accelMagnitude]
            # 
            magVector = [float(request[4]), float(request[5]), float(request[6])]
            magMagnitude = math.sqrt(magVector[0] * magVector[0] + magVector[1] * magVector[1] + magVector[2] * magVector[2]) # Compute vector magnitude
            normalizedMag = [magVector[0] / magMagnitude, magVector[1] / magMagnitude, magVector[2] / magMagnitude]

            # Compute east via accel x mag
            east = [(normalizedAccel[1] * normalizedMag[2]) - (normalizedAccel[2] * normalizedMag[1]),
                    (normalizedAccel[2] * normalizedMag[0]) - (normalizedAccel[0] * normalizedMag[2]),
                    (normalizedAccel[0] * normalizedMag[1]) - (normalizedAccel[1] * normalizedMag[0])]
            
            # North is east x up
            north = [(east[1] * normalizedAccel[2]) - (east[2] * normalizedAccel[1]),
                     (east[2] * normalizedAccel[0]) - (east[0] * normalizedAccel[2]),
                     (east[0] * normalizedAccel[1]) - (east[1] * normalizedAccel[0])]
            

            lineSize = screenSize // 3 # Sets the max length of the line
            normalizedVector = [int(north[0] * lineSize), 
                                int(north[1] * 255 ), # normalized for color, if confused keep reading
                                int(north[2] * lineSize)] # Vector normalization to line size

            # Compute line endpoint (uses Z because im showing this in x-z plane)
            endPoint = (origin[0] - normalizedVector[0], # transform based on nveted x axis o accelerometer
                        origin[1] - normalizedVector[2]) # subtracts because pygame's y-axis is inverted

            # Depict y axis with color. green for toward you and red for away
            color = []
            if north[1] >= 0:
                color = [0, normalizedVector[1], 0]
            else:
                color = [-normalizedVector[1], 0, 0] 
                
            
            heading = math.atan2(north[1], north[0]) * (180.0 / math.pi)
            print(heading)
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