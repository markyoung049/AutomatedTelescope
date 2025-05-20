#########################################################################
# Automated Telescope App
#########################################################################


# libraries Import
from tkinter import *
import customtkinter
import tracking
from PIL import Image, ImageTk
import math
import serial


########################################################################
# Main Window Properties and global variables

window = Tk()
window.title("Telescope Tracking System")
window.iconbitmap("images\\moon.ico")
window.geometry("800x500")
window.configure(bg="#FFFFFF")
currentPlanet = None
track = False
lookup = False

# Load the arrow image
base_img = Image.open("images\\arrow.png")  # make sure it's pointing right by default
# Resize it (e.g. to 50x50 pixels)
resized_img = base_img.resize((100, 100), Image.LANCZOS)
arrow_img = ImageTk.PhotoImage(resized_img)



# Set up serial communication with the sensor arduino
sensor = serial.Serial('COM5', 9600, timeout=2)
motor = serial.Serial('COM4', 9600, timeout=2)

########################################################################
# Functions

# Function to turn on the system.
def enableTracking():
    
    # Set the system to tracking mode
    global track
    
    # Set the system to tracking mode
    track = True
    tracking.log("Tracking Enabled")

    # Queue the next update
    window.after(1000, headingUpdate)





# Function to turn off the system.
def disableTracking():
    
    # Set the system to tracking mode
    global track
    track = False
    tracking.log("Tracking Disabled")





# Update the telescope heading. This will be called every so-often to update the data.
def headingUpdate():

    if track:

        # if the Data is available, then read it
        if sensor.in_waiting > 0:
            # Grab the azimuth and altitude data from the sensor
            azimuth, altitude = tracking.heading(sensor)

            # Update the labels with the new data
            telescopeAltitudeLabel.configure(text = "Altitude: "+ f'{altitude:.2f}' +"°")
            telescopeAzimuthLabel.configure(text = "Azimuth: "+ f'{azimuth:.2f}' +"°")


            if lookup:
                objectAZ = float(Label_azimuth.cget("text").split(': ')[1][:-1]) % 360
                objectALT = float(Label_altitude.cget("text").split(': ')[1][:-1]) % 360

                xAngle = objectAZ - azimuth
                yAngle = objectALT - altitude

                if xAngle >= 180:
                    xAngle = xAngle - 360

                if yAngle >= 180:
                    yAngle = yAngle - 360

                tracking.turn(motor, xAngle, xAngle)








        # Queue the next update
        window.after(10, headingUpdate)



# Lookup the object and if it exists, then track it and update the data appropriately. 
def objectLookup():
    
    global lookup
    lookup = True
    # Grab the data
    object = objectEntry.get().title()
    
    # Update the current planet
    global currentPlanet
    currentPlanet = object
    az, alt, skyCoordObj, home = tracking.lookup(object)

    # Write the data
    Label_object.configure(text = object)
    Label_azimuth.configure(text = "Azimuth: "+ f'{az:.2f}' +"°")
    Label_altitude.configure(text = "Altitude: "+ f'{alt:.2f}' +"°")

    # Queue updates and tracking
    if track:
        status = tracking.autoTrack(az, alt)

        # Make sure the track was successful, and if not, then disable tracking and log the error
        if status != 0:
            tracking.log("Tracking failed, disabling tracking...")
            disableTracking()

    objectUpdate(skyCoordObj, home, object)
    




# Update the object currently in focus
def objectUpdate(skyCoordObj, home, object):

    # Check if this task should be cancelled since a new object has been chosen
    if object == currentPlanet:
        # Fetch the new info
        az, alt = tracking.update(skyCoordObj, home)


        # Grab the azimuth and add earth rotation amount
        Label_azimuth.configure(text = "Azimuth: "+ f'{az:.2f}' +"°")
        Label_altitude.configure(text = "Altitude: "+ f'{alt:.2f}' +"°")
        window.after(100, lambda: objectUpdate(skyCoordObj, home, object))

    else: 
        global lookup
        lookup = False

########################################################################
# Elements

canvas = Canvas(window, 
    width=100, 
    height=100, 
    bg="white")
canvas.place(x=300, y=300)

arrow_obj = canvas.create_image(50, 50, image=arrow_img)

Label_object = customtkinter.CTkLabel(
    master=window,
    text="None",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_object.place(x=270, y=180)
Button_id21 = customtkinter.CTkButton(
    master=window,
    text="+90",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=40,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id21.place(x=570, y=160)
Label_id9 = customtkinter.CTkLabel(
    master=window,
    text="Label9",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id9.place(x=30, y=240)
Label_id10 = customtkinter.CTkLabel(
    master=window,
    text="Tracking System",
    font=("Arial", 30),
    text_color="#000000",
    height=40,
    width=230,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id10.place(x=250, y=20)
telescopeAzimuthLabel = customtkinter.CTkLabel(
    master=window,
    text="Azimuth",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
telescopeAzimuthLabel.place(x=30, y=180)
Label_azimuth = customtkinter.CTkLabel(
    master=window,
    text="Azimuth: ",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_azimuth.place(x=270, y=210)
Label_id20 = customtkinter.CTkLabel(
    master=window,
    text="Horizontal:",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id20.place(x=570, y=130)
Button_id19 = customtkinter.CTkButton(
    master=window,
    text="Go!",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=45,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    command=lambda: objectLookup()
    )
Button_id19.place(x=400, y=140)
telescopeAltitudeLabel = customtkinter.CTkLabel(
    master=window,
    text="Altitude: ",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
telescopeAltitudeLabel.place(x=30, y=210)
objectEntry = customtkinter.CTkEntry(
    master=window,
    placeholder_text="e.g. Moon",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=130,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#f7f7f7",

    )
objectEntry.place(x=270, y=140)
Button_id22 = customtkinter.CTkButton(
    master=window,
    text="-90",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=40,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id22.place(x=620, y=160)
Button_id1 = customtkinter.CTkButton(
    master=window,
    text="On",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=45,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    command=enableTracking
    )
Button_id1.place(x=30, y=140)
Label_altitude = customtkinter.CTkLabel(
    master=window,
    text="Altitude: ",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_altitude.place(x=270, y=240)
Button_id25 = customtkinter.CTkButton(
    master=window,
    text="-90",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=40,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id25.place(x=620, y=240)
Label_id5 = customtkinter.CTkLabel(
    master=window,
    text="Tracking: OFF",
    font=("Arial", 19),
    text_color="#000000",
    height=30,
    width=130,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id5.place(x=30, y=90)
Label_id23 = customtkinter.CTkLabel(
    master=window,
    text="Vertical:",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id23.place(x=570, y=210)
Label_id18 = customtkinter.CTkLabel(
    master=window,
    text="Motor Controls",
    font=("Arial", 19),
    text_color="#000000",
    height=30,
    width=132,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id18.place(x=570, y=90)
Label_id17 = customtkinter.CTkLabel(
    master=window,
    text="Celestial Object",
    font=("Arial", 19),
    text_color="#000000",
    height=30,
    width=150,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id17.place(x=270, y=90)
Button_id2 = customtkinter.CTkButton(
    master=window,
    text="Off",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=45,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    command=disableTracking
    )
Button_id2.place(x=80, y=140)
Button_id24 = customtkinter.CTkButton(
    master=window,
    text="+90",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=40,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id24.place(x=570, y=240)



#run the main loop
window.mainloop()