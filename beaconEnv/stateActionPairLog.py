import numpy as np 

class stateActionLog:
    def __init__(self, sn, sm, st, action):
        self.sn = sn  #neighboring neighbors observed by the receiving beacons
        self.sm = sm  #sum of expected neighbors by the neighboring neighbors
        self.st = st  #the dissemination rate

        self.action = action  #action taken by the beacon



class costLog:
    def __init__(self, cost, state, action, contributedBy):
        self.contributedBy = [contributedBy]
        self.state = state
        self.action = [action]        
        self.cost = [cost]
        self.totalCost = [0, 0]
        self.update()


    def update(self):
        self.totalCost = [0, 0]
        for i, a in enumerate(self.action):
            if a == 0:
                self.totalCost[0] += self.cost[i]
            elif a == 1:
                self.totalCost[1] += self.cost[i]
