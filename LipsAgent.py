from agentspace import Agent, space
from noyarpicub import iCub_emotions 
import time
import random

class LipsAgent(Agent):

    def __init__(self,nameSpeaking):
        self.Speaking = nameSpeaking
        super().__init__()
        
    def init(self):
        self.emotions = iCub_emotions()
        self.openmouth = False
        self.attach_timer(0.25)
 
    def senseSelectAct(self):
        speaking = space[self.Speaking]
        if speaking:
            if random.random() < 0.7:
                self.emotions.set('neu')
            else:
                self.emotions.set('sur')
                self.openmouth = True
        else:
            if self.openmouth:
                self.emotions.set('neu')
                self.openmouth = False
 

