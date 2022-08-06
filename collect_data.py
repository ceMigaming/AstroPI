import os
import logging
import numpy as np

from logzero import setup_logger
from sense_hat import SenseHat
import ephem

# Path, where our software is stored and our data will be saved
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Setting up formatter
FORMATTER = logging.Formatter("%(asctime)-15s - %(levelname)s:, %(message)s")

# We keep the original formatTime function
FORMATTER.formatTime_ = FORMATTER.formatTime
current_time = None


def format_time(record, datefmt=None):
    """This function is used to get the same time in both formatters."""
    global current_time
    global change
    if current_time:
        return current_time
    # We use original formatTime function to get time
    current_time = FORMATTER.formatTime_(record, datefmt)
    return current_time


# We overwrite formatTime function to get the same time in both formatters
# We need the same time in order to reference between both files during post processing
FORMATTER.formatTime = format_time

# Creating logger objects
# For logging raw data just in case of mistaken calculations
RAW_LOGGER = setup_logger(
    name="Raw data logger",
    logfile=DIR_PATH + "/data01.csv",
    level=logging.INFO,
    formatter=FORMATTER,
)
# For saving calculated data
CALCULATED_LOGGER = setup_logger(
    name="Calculated data logger",
    logfile=DIR_PATH + "/data02.csv",
    level=logging.INFO,
    formatter=FORMATTER,
)

# Declaring variables for keeping magnetometer data
current_x = None
current_y = None
current_z = None

# Declaring variables for keeping location data
current_sublat = None
current_sublong = None

# Declaring variables for keeping angles
current_horizontal_angle = None
current_vertical_angle = None
# Declaring TLE set for the ISS
NAME = "ISS (ZARYA)"
LINE1 = "1 25544U 98067A   19340.65162351 -.00000206  00000-0  44295-5 0  9994"
LINE2 = "2 25544  51.6436 226.2718 0006901   6.3372  31.6165 15.50090093202011"


def magnetometer():
    """Function for getting data from magnetometer."""
    raw_data = sense.get_compass_raw()

    # Declaring variables as global
    global current_x
    global current_y
    global current_z

    # Assigning new value to variables
    current_x = raw_data["x"]
    current_y = raw_data["y"]
    current_z = raw_data["z"]


def location():
    """Function for retrieving location of ISS"""
    iss = ephem.readtle(NAME, LINE1, LINE2)
    iss.compute()

    # Declaring variables as global
    global current_sublat
    global current_sublong

    # Assigning new value to variables
    current_sublat = iss.sublat
    current_sublong = iss.sublong


def calculate():
    """Function for calculating data to save"""
    global current_x
    global current_y
    global current_z
    global current_horizontal_angle
    global current_vertical_angle

    # We are getting horizontal angle beetween computer and geographical north
    current_horizontal_angle = sense.get_compass()

    # We are getting vertical angle based on calculations that you can find in readme.md
    current_vertical_angle = np.degrees(
        np.arccos(current_x / np.sqrt(current_x ** 2 + current_z ** 2))
    )
    if current_z < 0:
        current_vertical_angle = 360 - current_vertical_angle


def save():
    """Saving data to file"""
    RAW_LOGGER.info(
        "%s,%s,%s,%s,%s",
        current_x,
        current_y,
        current_z,
        current_sublat,
        current_sublong,
    )
    CALCULATED_LOGGER.info(
        "%s,%s,%s,%s",
        current_horizontal_angle,
        current_vertical_angle,
        current_sublat,
        current_sublong,
    )
    # We need to change current_time to None in order for our overwrite to work
    global current_time
    current_time = None
