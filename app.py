#########################################################################
# Automated Telescope App
#########################################################################


# libraries Import
from tkinter import *
import customtkinter
import tracking


########################################################################
# Main Window Properties and global variables

window = Tk()
window.title("Telescope Tracking System")
window.geometry("800x500")
window.configure(bg="#FFFFFF")
currentPlanet = None

########################################################################
# Functions

# Lookup the object and if it exists, then track it and update the data appropriately. 
def objectLookup():
    
    # Grab the data
    object = objectEntry.get()
    
    # Update the current planet
    global currentPlanet
    currentPlanet = object
    az, alt, skyCoordObj, home = tracking.lookup(object)

    # Write the data
    Label_object.configure(text = object)
    Label_azimuth.configure(text = "Azimuth: "+ f'{az:.2f}' +"°")
    Label_altitude.configure(text = "Altitude: "+ f'{alt:.2f}' +"°")

    # Queue updates
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
        window.after(1000, lambda: objectUpdate(skyCoordObj, home, object))

    

########################################################################
# Elements

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
Label_id7 = customtkinter.CTkLabel(
    master=window,
    text="Label7",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id7.place(x=30, y=180)
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
Label_id8 = customtkinter.CTkLabel(
    master=window,
    text="Label8",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id8.place(x=30, y=210)
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
    command=tracking.enableTracking
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
    command=tracking.disableTracking
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