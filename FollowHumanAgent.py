from agentspace import Agent, space
import time
from pyicubsim import iCubTorso

class FollowHumanAgent(Agent):

    def __init__(self, nameFeatures):
        self.nameFeatures = nameFeatures
        super().__init__()
        
    def init(self):
        space.attach_trigger(self.nameFeatures,self)
        self.torso = iCubTorso()
 
    def senseSelectAct(self):
        people = space[self.nameFeatures]
        if len(people) <= 0:
            return
        #choose first human
        human = people[0]

        x = ((human[4] / human[6]) * 58) - 29
        self.torso.set((x,0,0))
        time.sleep(0.2)

