from beaconImplementation.beacon import beacon
from beaconImplementation.network import network

import copy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

Gb = network(numBeacons=10, width = 100, breadth = 100)
# b = Gb.b[0].__dict__
f = plt.figure(figsize=(15, 15))
gs = gridspec.GridSpec(ncols=2, nrows=4, figure=f)
f.add_subplot(gs[:-1,:])
Gb.visualizeNetwork()
f.add_subplot(gs[-1,:])
Gb.visualizeAdvTimeOfAllBeacons()
plt.tight_layout()

Go = copy.deepcopy(Gb)
Go.makeOverlay()
# Go.b[0].__dict__
f = plt.figure(figsize=(15, 15))
gs = gridspec.GridSpec(ncols=2, nrows=6, figure=f)
f.add_subplot(gs[:-2,:])
Go.visualizeNetwork()
f.add_subplot(gs[-2,:])
Gb.visualizeAdvEventOfBeacon(0)
f.add_subplot(gs[-2,:])
Go.visualizeScanEventOfBeacon(0)
plt.tight_layout()


# _, _, advTime = Go.getAdvSeq()
# _, _, scanTime = Go.getScanSeq()

# t = 0
# activeScanBeacons = []
# while(True):
#     activeAdvBeacons = []
#     advEventInd = np.where(advTime == t)[0]
#     for ind in advEventInd:
#         advTime[ind] += Go.b[ind].advInt
#         activeAdvBeacons.append(Go.b[ind])
        
#     scanEventInd = np.where(scanTime == t)[0]
#     for ind in scanEventInd:
#         Go.b[ind].activeScan = Go.b[ind].scanDur
#         scanTime[ind] += Go.b[ind].scanInt
#         activeScanBeacons.append(Go.b[ind])

#     if (len(activeScanBeacons)!=0):
#         for b in activeScanBeacons:
#             if (b.activeScan == 0):
#                 activeScanBeacons.remove(b)
#             else:
#                 b.activeScan -= 1    
            
#             if (len(activeScanBeacons) == 0):
#                 break                        
        
#         # for every scanning, check if any receive packet
#         # checking if any neighboring beacon is advertising the same time
#         numImmediateNeighbors = np.zeros(len(activeScanBeacons))
#         numTheirExpectedNeighbors = np.zeros(len(activeScanBeacons))
#         k = 0
#         for scanBeacon in (activeScanBeacons):
#             receivedPacketFrom = []
#             immediateNeighbor = []
#             for advBeacon in (activeAdvBeacons):
#                 i = int(scanBeacon.beaconId)
#                 j = int(advBeacon.beaconId)
#                 if (i!=j and Go.beaconDist[i][j] < advBeacon.maxCoverage):
#                     immediateNeighbor.append(advBeacon)
#                     # check the advertising packet to see if there is any forwarding request
#                     forwardReq = True if (advBeacon.packet[-1] == '01') else False
#                     if (forwardReq and scanBeacon.activeScan>advBeacon.advDur):
#                         receivedPacketFrom.append(advBeacon.beaconId)
                        

#             numImmediateNeighbors[k] = len(immediateNeighbor)
#             if(len(immediateNeighbor) != 0):
#                 theirNeighbors = [immediateB.expectedNeighbors for immediateB in (immediateNeighbor)]
#                 numTheirExpectedNeighbors[k] = sum(theirNeighbors)
#             k += 1
        
#     t = t+1



