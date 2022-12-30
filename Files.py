# this script is for testing the .yaml and .json file types for later use. it will also
# generate a generic config.yaml and data.json with default settings and readings for the sensor system. If a file
# exists it will erase the files, and rewrite them with default values to prevent errors. Essentially this script resets
# the entire sensor system to default. Like the others in this folder, this is a POC item mostly designed for later use
# to make the overall program easier ot write. This one however has the exception to being useful to UI, and over all
# program as it give reference ot the file types and dictionaries used on the sensor side.  
# As per usual comment convention is to explain all functions and commands for later reuse, and the code is designed to
# be easy to follow and read. in other words, there is nothing fancy here by design.

# David Robinson
# Version 0.8


import yaml
import json
from os.path import exists
import os


# The following function checks if the file exists. returning a simple bool
def checkFile(file):
    if not exists(file): # If the file isn't there
        return False
    else: # The file is there
        return True


# the following will create and load, or just load default values into the config file
# load = 0 for create and load, meaning file does not exist
# load = 1 for erase all and load default
def createConfigFile(load):

    # Default configuration values
    reading = int(6)  # default number of readings for each sensor
    wait = float(0.5)  # the default break between readings
    seqOrLoop = bool(False)  # to take readings sequentially or loop around all units first, 0 for sequential, 1 for loop.
    depth = int(15)  # default depth in meters of the cenotes taken as average from https://magicblueplanet.com/en/about-cenotes-in-mexico/
    rotations = float(1 / 3)  # the default fraction to determine the depth of the unit.
    speed = float(1 / 7)  # speed in revolutions per second default is 1/7
    mass = float(2)  # Mass of the sample container in kg for use in calculating return flight default is 2kg

    # Sensor Dictionary Assembly
    sensorInfo = [{'S-reading': reading,
                   'S-Wait': wait,
                   'S-s&l': seqOrLoop}]

    # Stepper Dictionary Assembly
    stepInfo = [{'R-depth': depth,
                 'R-Rotation': rotations,
                 'R-speed': speed,
                 'R-mass': mass}]

    # Insert new configurations here

    # Complete Dictionary Assembly
    fullDict = [{'Sensor': sensorInfo,
                 'Stepper': stepInfo}] # Make sure any new config dictionaries get added to this one.

    if load == True:
        os.remove('config.yaml')  # Deletes existing file

    config = open('config.yaml', 'x')  # recreates file as empty
    config.close()  # closes new empty file

    # Writes dictionary to config file
    with open('config.yaml', 'w') as f:
        config = yaml.dump(fullDict, f, sort_keys=False, default_flow_style=False)


# The following creates a test Data file if one exists, it deletes it and recreates another.
def createDataFile(load):

    # The following will pull the number of readings from config.yaml
    with open('config.yaml', 'r') as f:
        data = yaml.safe_load(f)
    topNumber = (data[0]['Sensor'])
    number = (topNumber[0]['S-reading'])
    # Arbitrary data pulled from SenseTest.py to act as the default
    # These will just be loaded X number of times in succession by defualt
    temp = 38.16
    orp = -877.8
    pH = 13.905
    do = 0.00
    conduct = -1023.000

    # the following block defines the dictionary of values that will be used to
    # fill the default data.json file.
    readings = [temp, orp, pH, do, conduct]
    rNames = ["Temp", "ORP", "pH", "do", "conduct"]
    dataSet = {}
    for num in range(4): # number of sensors
        for secondNum in range(number): # Number of items called for in the config
            name = rNames[num] # Gets name from array
            indName = str(name + str(secondNum)) # Gives name a value
            dataSet[indName] = readings[num] # places name and value in dictionary for conversion

    if load == True:
        os.remove('data.json') # Deletes existing file
    dataTwo = open('data.json', 'x')  # recreates file as empty
    dataTwo.close()  # closes new empty file

    # Dumps the data into a file.
    with open("data.json", "w") as write_file:
        json.dump(dataSet, write_file)


def main():

    # defines the files
    config = 'config.yaml'
    data = 'data.json'

    cFile = checkFile(config) # Does config.yaml exist?
    createConfigFile(cFile) # Passes that info into default creator

    sFile = checkFile(data) # Does data.json exist?
    createDataFile(sFile) # Passes that info into file creator

main()
