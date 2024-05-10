from agentspace import Agent, space
import os
import json
import math

class CompareAgent(Agent):

    def __init__(self,nameLandmarks,nameUserName,nameDialog):
        self.nameLandmarks = nameLandmarks
        self.nameUserName = nameUserName
        self.dialog = nameDialog
        super().__init__()

    def init(self):
        self.directory = 'people'
        space.attach_trigger(self.nameLandmarks, self)


    def euklidDistance(self, landmark1, landmark2):
        return math.sqrt((landmark1[0] - landmark2[0])**2 + (landmark1[1] - landmark2[1])**2)

    def compareFaces(self, faceLandmarks1, faceLandmarks2):
        if len(faceLandmarks1) != len(faceLandmarks2):
            raise ValueError("Sady bodov musia mať rovnaký počet bodov pre porovnanie.")

        distanes = [self.euklidDistance(landmark1, landmark2) for landmark1, landmark2 in zip(faceLandmarks1, faceLandmarks2)]

        avarageDistance = sum(distanes) / len(distanes)
        return avarageDistance

    def senseSelectAct(self):
        landmarks = space[self.nameLandmarks]
        dialog = space[self.dialog]

        if landmarks is None:
            return
        name = None
        faceFeatures = [(p.x, p.y) for p in landmarks.parts()]
        for filename in os.listdir(self.directory):
            f = os.path.join(self.directory, filename)
            if os.path.isfile(f):
                with open(f, "r") as file:
                    savedFaceFeatures = json.load(file)
                    avarageDistance = self.compareFaces(savedFaceFeatures["landmarks"], faceFeatures)
                    if avarageDistance < 50:
                        name = filename.split('.')[0]
                        if dialog is None:
                            space(validity=20)[self.dialog] = savedFaceFeatures["dialog"]
        
        if name is not None:
            space(validity=5)[self.nameUserName] = name
                    

