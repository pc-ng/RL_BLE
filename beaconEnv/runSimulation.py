from beaconImplementation.beacon import beacon
from beaconImplementation.network import network

import copy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np 

Gb = network(numBeacons=10, width = 100, breadth = 100)
Go = copy.deepcopy(Gb)
Go.makeOverlay()

advTime, advInd = Go.getAdvSeq()
scanTime, scanInd = Go.getScanSeq()

t = 0
# 0 for advertising, 1 for scanning
activeBeacon = []
while(True):
    for i in range (len(activeBeacon)):
        activeBeacon[i].activeAdv -= 1 if activeBeacon[i].activeAdv != 0 else 0
        activeBeacon[i].activeScan -= 1 if activeBeacon[i].activeScan != 0 else 0

        if (activeBeacon[i].activeAdv == 0 and activeBeacon[i].activeScan == 0):
            del activeBeacon[i]

    advEventInd = np.where(advTime == t)[0]
    for i in range (advEventInd.shape[0]):
        ind = advInd[advEventInd[0]]
        Go.b[ind].activeAdv = Go.b[ind].advDur

        advTime[advEventInd[0]] += Go.b[ind].advInt
        activeBeacon.append(Go.b[ind])
        
    scanEventInd = np.where(scanTime == t)[0]
    for i in range (scanEventInd.shape[0]):
        ind = scanInd[scanEventInd[0]]
        Go.b[ind].activeScan = Go.b[ind].scanDur

        scanTime[scanEventInd[0]] += Go.b[ind].scanInt
        activeBeacon.append(Go.b[ind])
        
    t = t+1