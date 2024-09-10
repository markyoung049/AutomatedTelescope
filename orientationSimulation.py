import serial
import pygame
import sys
import math

# Set up serial communication with the Arduino
arduino = serial.Serial('COM4', 9600)  # Replace 'COM3' with your port

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

            # Draw the vector
            origin = (screenSize // 2, screenSize // 2) # Compute the origin
            vector = [float(request[1]), float(request[2]), float(request[3])] # Get the vector
            magnitude = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2]) # Compute vector magnitude
            lineSize = screenSize // 3 # Sets the max length of the line
            normalizedVector = [int(vector[0] * lineSize / magnitude), 
                                int(vector[1] * 255 / magnitude), # normalized for color, if confused keep reading
                                int(vector[2] * lineSize / magnitude)] # Vector normalization to line size
            
            # Sompute line endpoint (uses Z because im showing this in x-z plane)
            endPoint = (origin[0] - normalizedVector[0], # transform based on nveted x axis o accelerometer
                        origin[1] - normalizedVector[2]) # subtracts because pygame's y-axis is inverted

            # Depict y axis with color. green for toward you and red for away
            color = []
            if vector[1] >= 0:
                color = [0, normalizedVector[1], 0]
            else:
                color = [-normalizedVector[1], 0, 0] 
                

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