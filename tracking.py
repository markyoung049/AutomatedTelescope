#########################################################################
# Automated Telescope Tracking Functions
#########################################################################
import datetime

# Function to print a log message to the console. Returns nothing.
def log(message):
    print(datetime.datetime.now(), message)
    

# Function to turn on the system. Return 0 if sucessful, -1 if not.
def enableTracking():
    log("Tracking Enabled")
    return -1


# Function to turn off the system. Return 0 if sucessful, -1 if not.
def disableTracking():
    log("Tracking Disabled")
    return 0

# Function to look up planetary data for an object. Return data if it exists, and -1 if it doesnt
def lookup():

    return datetime.datetime.now()

