from beaconImplementation.beacon import beacon
from beaconImplementation.network import network

import copy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np 
import random

# problem 1:
# each beacon in the remote area are separated by 30m 
# each beacon is configured to have txPower = 0dBm, 
# hence, maximum coverage of 50m
def problemUniform(separation = 30, width=300, breadth=90):
    #numBeacons = 30
    x = np.arange(0, width, separation)  # in meter
    y = np.arange(0, breadth, separation)
    coord = []
    for i in x:
        for j in y:
            coord.append([i,j])

    numBeacons = len(coord)
    return numBeacons, coord


def problemMod(separation = 30, width=300, breadth=90, modVal = 7):
    #numBeacons = 30
    x = np.arange(0, width, separation)  # in meter
    y = np.arange(0, breadth, separation)
    coord = []
    for i in x:        
        for j in y:
            if (i+j+random.randint(0, 7))%modVal!=0:
                coord.append([i,j])

    numBeacons = len(coord)
    return numBeacons, coord







