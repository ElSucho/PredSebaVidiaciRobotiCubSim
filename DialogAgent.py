from agentspace import Agent, space
import os
import json


class DialogAgent(Agent):

     def __init__(self, nameAnswer,nameDialog,nameText,nameUserName):
        self.nameDialog = nameDialog
        self.nameAnswer = nameAnswer
        self.nameText = nameText
        self.userName = nameUserName
        super().__init__()

     def init(self):
        space.attach_trigger(self.nameAnswer,self)

     def senseSelectAct(self):
        dialog = space[self.nameDialog]
        answer = space[self.nameAnswer]
        text = space[self.nameText]
        userName = space[self.userName]
        newDialog = ""
        if text is not None and answer is not None: 
            actualDialog = f"User:\n{text}\nGPT:\n{answer}\n"
                                
            if dialog is None:
                newDialog = actualDialog
            else:
                newDialog = dialog + actualDialog
            if userName is not None:
               f = os.path.join("people", userName + ".json")
               if os.path.isfile(f):
                  with open(f, "r") as file:
                     savedFaceFeatures = json.load(file)
                  savedFaceFeatures["dialog"] = newDialog
                  with open(f, "w") as file:
                     json.dump(savedFaceFeatures, file)
        space(validity=60.0)[self.nameDialog] = newDialog

        
