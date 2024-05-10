import cv2 as cv 
from agentspace import Agent, space
import dlib
import json

class FaceMarksDetectorAgent(Agent):
   
    def __init__(self,nameImage,nameFace,nameImageLandmarks,nameLandmarks, nameUserName,nameSaveUser,nameDialog):
        self.nameImage = nameImage
        self.nameFace = nameFace
        self.nameImageLandmarks = nameImageLandmarks
        self.nameLandmarks = nameLandmarks
        self.userName = nameUserName
        self.saveUser = nameSaveUser
        self.dialog = nameDialog
        super().__init__()

    def init(self):
         self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
         
         space.attach_trigger(self.nameFace, self)

    def senseSelectAct(self):
        image = space[self.nameImage]
        face = space[self.nameFace]
        userNameD = space[self.userName]
        saveUser = space[self.saveUser]
        dialog = space[self.dialog]
        if image is None:
            return
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        rect = dlib.rectangle(left=face[0][0], top=face[0][1], right=face[0][2], bottom=face[0][3])
        landmarks = self.predictor(gray_image, rect)
        

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv.circle(image, (x, y), 1, (0, 255, 0), -1)
        
        
        user_data = {"landmarks": [(p.x, p.y) for p in landmarks.parts()]}

        if saveUser is True and userNameD is not None:
            if dialog is None:
                dialog = ""
            user_data["dialog"] = dialog
            with open("people/" + userNameD.strip() + ".json", "w") as file:
                json.dump(user_data, file)
            print("user saved")
            space(validity=1)[self.saveUser] = None
            

        space(validity=0.1)[self.nameImageLandmarks] = image
        space(validity=0.1)[self.nameLandmarks] = landmarks
