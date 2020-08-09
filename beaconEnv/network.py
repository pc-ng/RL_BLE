import random
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from beaconImplementation.beacon import beacon 
# from matplotlib import rc
# rc('text', usetex=True)
random.seed( 30 )

class network:
    def __init__(self, numBeacons=3, width = 100, breadth = 100,
                deployOption = 'random', beaconCoor = []):
        '''
        create a network object:
        >> defines the number of beacons in the environment
        >> for area defined by width and breadth
        >> get the coordinate of each deployed beacons
           >> if deployOption = 'random', generate the coordinate randomly
           >> if 'manual', used the hardcoded coordinate

        >> need a method to return the distance between each beacon on the fly
        >> so we can determine the neighboring beacons for each b in B
        >> or more properly, we should determine the neighbor 
        based on the scanning and advertising overlapping
        >> based on possible virtual links

        Beacon Network object:  Gb = ({B,R}, L)
        TODO: the mobility model for the receiver
        self.numBeacons = numBeacons
        '''        
        self.numBeacons = numBeacons
        self.width = width       # in meter
        self.breadth = breadth
        self.area = width * breadth         

        # get the location of the deployed beacons 
        # constraints to the available area
        if deployOption == 'random':
            self.beaconCoor, self.beaconDist = self.deployedCoor(numBeacons, width, breadth)
        elif deployOption == 'manual':
            self.beaconCoor = beaconCoor
            self.beaconDist = self.computeDist(np.array(beaconCoor))

        self.beaconID = np.arange(0,numBeacons)

        self.b = [self.deployedBeacons(id=self.beaconID[i]) for i in range(numBeacons)]
        
        # variables that changes during the running 
        self.t = 0        
        self.activeAdvBeacons = []
        _, _, self.advTime = self.getAdvSeq()          
        self.states = []   # a list of states observed by active scan beacons
        self.source = -1
        self.destination = -1

    ########################################
    # Methods Definition
    ########################################
    # get the beacon object
    # update the deployed coord (default is (0,0) when initiate the beacon object)
    # update the expected number of neighboring beacons for each beacons
    # self.numNeighbors = np.sum(self.beaconDist < maxCoverage, axis=1)
    def deployedBeacons(self, id):
        b = beacon(str(id))
        b.deployedCoor = self.beaconCoor[id]
        bDist = self.beaconDist[id]

        # 1. anything in cm, remember to convert it to m
        # 2. need to exclude itself
        b.expectedNeighbors = sum(bDist < b.maxCoverage)-1  
        return b

    def deployedCoor(self, numBeacons, width, breadth):
        minSpace = 10   # in cm
        x = [random.randrange(0, width*100, minSpace) for i in range(numBeacons)]   # width and breadth are in m
        y = [random.randrange(0, breadth*100, minSpace) for i in range(numBeacons)] # but the x, y in cm

        bCoor = list(zip(x, y))   
        bPoints = (np.array(bCoor)/100)  # convert anything in cm to m

        bDist = self.computeDist(bPoints)  # the distance in m
        return bCoor, bDist

    def computeDist(self, points):     
        bDist = np.sqrt(np.sum((points[None, :] - points[:, None])**2, axis = -1))  # the distance in m
        return bDist

    # visualize the deployed beacon
    def visualizeNetwork(self):
        # plt.figure(figsize=(10,10))
        pts = np.array(self.beaconCoor)
        if (self.source == -1 and self.destination == -1):
            plt.plot(pts[:,0], pts[:,1], 'bo', markersize=12, alpha=0.7, label='beacon')
        else:            
            # pts.remove(self.source.deployedCoor)
            # pts.remove(self.destination.deployedCoor)
            plt.plot(self.source.deployedCoor[0], self.source.deployedCoor[1], 'ro', markersize=12, alpha=0.7, label='source')
            if(self.destination.packet[-1] == '01'):
                plt.plot(self.destination.deployedCoor[0], self.destination.deployedCoor[1], 'rs', markersize=12, label='destination*')
            else:
                plt.plot(self.destination.deployedCoor[0], self.destination.deployedCoor[1], 'go', markersize=12, alpha=0.7, label='destination')
            
                        
            toDelete = [int(self.source.beaconId), int(self.destination.beaconId)]
            firstCur1 = True
            firstCur2 = True
            for s in self.states:
                if (len(s.receivedPacketFrom) != 0):                    
                    if(s.observedBy.beaconId != self.source.beaconId and s.observedBy.beaconId != self.destination.beaconId):
                        if firstCur1:
                            plt.plot(s.observedBy.deployedCoor[0], s.observedBy.deployedCoor[1], 'yo', markersize=12, alpha=0.7, label = 'current received beacon')
                            firstCur1 = False
                        else:
                            plt.plot(s.observedBy.deployedCoor[0], s.observedBy.deployedCoor[1], 'yo', markersize=12, alpha=0.7)
                else:
                    if(s.observedBy.beaconId != self.source.beaconId and s.observedBy.beaconId != self.destination.beaconId):
                        if firstCur2:
                            plt.plot(s.observedBy.deployedCoor[0], s.observedBy.deployedCoor[1], 
                                'yo', markeredgecolor = 'blue', markersize=12, alpha=0.3, label = 'active scanning beacon')
                            firstCur2 = False
                        else:
                            plt.plot(s.observedBy.deployedCoor[0], s.observedBy.deployedCoor[1],
                                'yo', markeredgecolor = 'blue', markersize=12, alpha=0.3)
                toDelete.append(int(s.observedBy.beaconId))
            ptsUpdated = np.delete(pts, toDelete, axis = 0)          
            
            plt.plot(ptsUpdated[:,0], ptsUpdated[:,1], 'bo', markersize=12, alpha=0.7, label='beacon')

        bStr = ['b'+str(id) for id in self.beaconID]
        for i, txt in enumerate(bStr):
            plt.annotate(txt, self.beaconCoor[i])
        
        plt.xlabel(r'$x (m)$')
        plt.ylabel(r'$y (m)$')
        plt.title(f'$Advertising Beacons: {[b.beaconId for b in self.activeAdvBeacons]}; t = {self.t} ms $')
        plt.legend()

    def visualizeAdvTimeOfAllBeacons(self):
        advI = [self.b[i].advInit for i in range(self.numBeacons)]
        plt.stem(advI, np.ones(self.numBeacons), use_line_collection=True)

        bStr = ['b'+str(id) for id in self.beaconID]
        for i, txt in enumerate(bStr):
            plt.annotate(txt, (advI[i], 1))

        plt.xlabel(r'$time (ms)$')
        plt.ylabel(r'Advertising packet')

    def visualizeAdvEventOfBeacon(self, ind):
        t = self.b[ind].advInit
        dur = self.b[ind].advDur
        Ta = self.b[ind].advInt
        plt.step([0, t, t+dur, Ta], [0, 0, 1, 0], color = 'blue')

        plt.xlabel(r'$time (ms)$')
        plt.ylabel('b' + str(self.b[ind].beaconId))

    def visualizeScanEventOfBeacon(self, ind):
        t = self.b[ind].scanInit
        dur = self.b[ind].scanDur
        Ts = self.b[ind].scanInt
        plt.step([0, t, t+dur, Ts], [0, 0, 1, 0], color = 'green')

        plt.xlabel(r'$time (ms)$')
        plt.ylabel('b' + str(self.b[ind].beaconId))

    def getAdvSeq(self):
        advI = np.array([self.b[i].advInit for i in range(self.numBeacons)])
        sortAdv = np.sort(advI)
        sortAdvInd = np.argsort(advI)

        return sortAdv, sortAdvInd, advI

    def makeOverlay(self):
        for i in range(self.numBeacons):
            self.b[i].enabledScanEvent(scanInt = 1000, scanDur = 500)
        
        self.activeScanBeacons = [] 
        _, _, self.scanTime = self.getScanSeq()


    def getScanSeq(self):
        scanI = np.array([self.b[i].scanInit for i in range(self.numBeacons)])
        sortScan = np.sort(scanI)
        sortScanInd = np.argsort(scanI)

        return sortScan, sortScanInd, scanI


    ## run the network
    def runNetwork(self):
        while(True):
            self.activeAdvBeacons = []
            advEventInd = np.where(self.advTime == self.t)[0]
            k = 0
            for ind in advEventInd:
                self.advTime[ind] += self.b[ind].advInt  #TODO: need to add some pseudo-random delay as according to BLE specs
                bDist = self.beaconDist[ind]
                temp = np.delete(advEventInd, k)
                toAdd = True
                for tInd in temp:
                    if bDist[tInd] < self.b[ind].maxCoverage:
                        toAdd = False
                        break
                if (toAdd):    
                    self.activeAdvBeacons.append(self.b[ind])
                k += 1
                
            scanEventInd = np.where(self.scanTime == self.t)[0]
            for ind in scanEventInd:
                self.b[ind].activeScan = self.b[ind].scanDur
                self.scanTime[ind] += self.b[ind].scanInt
                self.activeScanBeacons.append(self.b[ind])

            if (len(self.activeScanBeacons)!=0):
                for b in self.activeScanBeacons:
                    if (b.activeScan == 0):
                        self.activeScanBeacons.remove(b)
                    else:
                        b.activeScan -= 1    
                    
                    if (len(self.activeScanBeacons) == 0):
                        break                        
                
                # for every scanning, check if any receive packet
                # checking if any neighboring beacon is advertising the same time
                k = 0
                self.states = []
                for scanBeacon in (self.activeScanBeacons):
                    # exclude the source beacon into consideration even it is active scanning
                    if scanBeacon != self.source:
                        receivedPacketFrom = []
                        immediateNeighbor = []
                        theirNeighbors = []
                        for advBeacon in (self.activeAdvBeacons):

                            i = int(scanBeacon.beaconId)
                            j = int(advBeacon.beaconId)
                            if (i!=j and self.beaconDist[i][j] < advBeacon.maxCoverage):
                                immediateNeighbor.append(advBeacon)
                                # check the advertising packet to see if there is any forwarding request
                                forwardReq = True if (advBeacon.packet[-1] == '01') else False
                                if (forwardReq and scanBeacon.activeScan>advBeacon.advDur):
                                    receivedPacketFrom.append(advBeacon.beaconId)
                                    
                        if(len(immediateNeighbor) != 0):
                            theirNeighbors = [immediateB.expectedNeighbors for immediateB in (immediateNeighbor)]
                        k += 1

                        theState = state()
                        theState.observedBy = scanBeacon
                        theState.expectedNeighbors = scanBeacon.expectedNeighbors
                        theState.observedNeighbors = len(immediateNeighbor)
                        theState.theirNeighbors = sum(theirNeighbors)
                        theState.receivedPacketFrom = receivedPacketFrom
                        theState.updateState()
                        self.states.append(theState)

            if(sum([s.waitingDecision for s in self.states]) > 0):
                return self.observedState()
                #break
            self.t = self.t+1

    # define a problem with only one source a time
    def reset(self, sInd = -1, dInd = -1):
        if sInd == -1:
            self.source = random.choice(self.b)
            distToSource = self.beaconDist[int(self.source.beaconId)]
            self.destination = self.b[np.argmax(distToSource)]
        else:
            self.source = self.b[sInd]
            self.destination = self.b[dInd]

        self.source.packet[-1] = '01'
        observed = self.runNetwork()
        return observed

    def observedState(self):
        # observedBeacons = [s.observedBy.beaconId for s in self.states]
        # waitingDecision = [s.waitingDecision for s in self.states]
        # observedNeighbors = [s.observedNeighbors for s in self.states]
        # theirNeighbors = [s.theirNeighbors for s in self.states]
        # throughput = [s.observedNeighbors/s.expectedNeighbors for s in self.states]

        cost = []
        observedBeacons = []
        waitingDecision = []
        observedNeighbors = []
        theirNeighbors = []
        dissemination = []
        for s in self.states:
            if s.observedBy.forwardInit != 0:
                timeDiff = self.t - s.observedBy.forwardInit

                if self.destination.beaconId in s.receivedPacketFrom:
                    s.observedBy.cost -= self.numBeacons*timeDiff
                
                if self.isPacketReceivedFromPreviousBeacons(s.observedBy.requestedBy, s.receivedPacketFrom):
                    s.observedBy.cost -= len(s.receivedPacketFrom)*timeDiff
                # else:
                #     s.observedBy.cost += timeDiff

                if len(s.receivedPacketFrom) == 0:                    
                    s.observedBy.cost += timeDiff
            cost.append(s.observedBy.cost)

            observedBeacons.append(s.observedBy.beaconId)
            waitingDecision.append(s.waitingDecision)
            observedNeighbors.append(s.observedNeighbors)
            theirNeighbors.append(s.theirNeighbors)
            dissemination.append(s.observedNeighbors/s.expectedNeighbors)

        return list(zip(observedBeacons, waitingDecision, observedNeighbors, theirNeighbors, dissemination)), cost          
    
    def isPacketReceivedFromPreviousBeacons(self, previousRequested, currentReceived):
        toAdd = True
        for p in previousRequested:
            if p[0] in currentReceived:
                toAdd = False
        return toAdd

    def action(self, bId, action, stateInd):
        if self.isPacketReceivedFromPreviousBeacons(self.b[int(bId)].requestedBy, self.states[stateInd].receivedPacketFrom):
            self.b[int(bId)].requestedBy.append(self.states[stateInd].receivedPacketFrom)

        if action == 1:
            self.b[int(bId)].packet[-1] = '01'
            self.b[int(bId)].forwardInit = self.t if self.b[int(bId)].forwardInit == 0 else self.b[int(bId)].forwardInit
            self.b[int(bId)].cost = 1       
            
        elif action == 0:
            self.b[int(bId)].packet[-1] = '00'
            self.b[int(bId)].cost = 1


class state:
    def __init__(self):
        self.observedBy = beacon('-1')   # observed by which beacon?
        self.expectedNeighbors = -1   # its expected neigbhors
        self.observedNeighbors = -1   # the exact neighbors it sees during the runtime
        self.theirNeighbors = -1
        self.receivedPacketFrom = []

    def updateState(self):
        if (len(self.receivedPacketFrom) != 0):
            self.waitingDecision = 1
        else:
            self.waitingDecision = 0
