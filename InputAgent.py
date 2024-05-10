import cv2 as cv
from agentspace import Agent, space

class InputAgent(Agent):

    def __init__(self, nameDebugInput):
        self.debugInput = nameDebugInput
        super().__init__()
        
    def init(self):
        while True:
            DebugInput = input()
            space(validity=10)[self.debugInput] = DebugInput
 
    def senseSelectAct(self):
        pass