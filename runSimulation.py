from beaconImplementation.beacon import beacon
from beaconImplementation.network import network

import copy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np 

Gb = network(numBeacons=20, width = 100, breadth = 100)
Go = copy.deepcopy(Gb)
Go.makeOverlay()
plt.figure(figsize=(7,7))
Go.visualizeNetwork()

# Go.runNetwork()
# observedBeacons, observedNeighbors, theirNeighbors, throughput = 
ret = Go.reset()
plt.figure(figsize=(7,7))
Go.visualizeNetwork()

ret = Go.runNetwork()
plt.figure(figsize=(7,7))
Go.visualizeNetwork()
