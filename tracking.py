#########################################################################
# Automated Telescope Tracking Functions
#########################################################################
import datetime
import requests
import base64
import serial
import numpy as np
import math

from astropy.coordinates import SkyCoord, AltAz
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation



# Function to print a log message to the console. Returns nothing.
def log(message):
    print('>', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  ":",  message)
    

# Function to track the given object. Basically it will prompt the motors to move with it. Return 0 if fine, -1 if failure.
def autoTrack(az, alt):



    return 0


# Function to look up planetary data for an object. Return data if it exists, and -1 if it doesnt
def lookup(object):

    log("Fetching data for " + object)
    # Use Astornomy API to get astronomical data and then process it using astropy.
    userpass = "05828125-953d-431d-9d45-e1a6aa44590a" \
    ":afcc636292ef134fd9dc94eeb0d2ae5c097c2aa152ca42657e1d6d5eb5ae2dcaadd6b91819e76e2d0640706e42dfb984e52073982ebd9e2de13814a9ddb3461b92a35b6ecdf6f98fe1e7377532256b823dc030dec463c842fa49b6394bbc9f845d8c24d5ed4b88d2f5a2ddf563cb5920"
    authString = base64.b64encode(userpass.encode()).decode()


    now = datetime.datetime.now()
    currentDate = now.strftime("%Y-%m-%d")
    currentTime = now.strftime('%H:%M:%S')
    latitude = "40.2849"
    longitude = "-75.2812"
    height = 93 # in meters

    # Make the request
    url = f'https://api.astronomyapi.com/api/v2/bodies/positions/{object}'
    headers = {"Authorization": "Basic " + authString }
    params = {
        "latitude": latitude,       
        "longitude": longitude,     
        "elevation": height,           
        "from_date": currentDate, 
        "to_date": currentDate,   
        "time": currentTime   
    }      

    # Grab data
    response = requests.get(url, headers = headers, params=params)
    data = response.json()
    
    # If the jobect does not exist
    if data == None:

        # Return the data and log the failure
        log("Data for " + object + " not found.")
        return (0, 0)

    # If it does
    else:

        # Grab the date, RA, and declination for the astronomy model
        ra = float(data.get('data').get('table')['rows'][0]['cells'][0]['position']['equatorial']['rightAscension']['hours'])
        dec = float(data.get('data').get('table')['rows'][0]['cells'][0]['position']['equatorial']['declination']['degrees'])

        # Make the astropy object to track the object
        skyCoordObj = SkyCoord(ra = ra, dec = dec, frame='icrs',
                          unit=(u.hourangle, u.deg))
        home = EarthLocation(lat=float(latitude) * u.deg, 
                             lon=float(longitude) * u.deg, 
                             height=390 * u.m)
        utcoffset = -4 * u.hour  # Eastern Daylight Time
        time = Time(now.strftime("%Y-%m-%d %H:%M:%S") ) - utcoffset

        # Get the altitude and azimuth
        altaz = skyCoordObj.transform_to(AltAz(obstime=time, location=home))

        # Return the data and log the completion
        log("Data for " + object + " obtained.")

        return (altaz.az.deg, altaz.alt.deg, skyCoordObj, home)

    


# Function to update azimuth
def update(skyCoordObj, home):

    # Set the new time (a different time, say 5 minutes later)
    new_time = Time(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Convert to altitude/azimuth for the new time
    altaz = skyCoordObj.transform_to(AltAz(obstime=new_time, location=home))
    return (altaz.az.deg, altaz.alt.deg)



# Function to give the heading of the object using arduino data. Returns the heading s in x and y
def heading(arduino):

    # Read the request from Arduino
    request = arduino.readline().decode('utf-8').strip().split(' ')

    if request[0] == "Data:":

        # Do math for accelerometer vector
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

        # Compute the heading angles in degrees
        headingX = math.atan2(yNew[0], yNew[1]) * (180.0 / math.pi)
        headingY = math.atan2(yNew[2], yNew[1]) * (180.0 / math.pi)


        return (headingX, headingY)