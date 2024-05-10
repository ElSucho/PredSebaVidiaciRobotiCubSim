
import cv2
import numpy as np
from agentspace import Agent, space


class AgeAgent(Agent):

    def __init__(self,nameFace,nameImage,nameAge):
        self.nameFace = nameFace
        self.nameImage = nameImage
        self.nameAge = nameAge
        super().__init__()

    def init(self): 
        print("ageDetector: loading model")
        AGE_MODEL = 'models/age/deploy_age.prototxt'
        AGE_PROTO = 'models/age/age_net.caffemodel'
        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self.AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                        '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
        self.frame_width = 1280
        self.frame_height = 720
        self.ageNet = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
        print("ageDetector: model loaded")

        space.attach_trigger(self.nameFace, self)

    def get_optimal_font_scale(text, width):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
            new_width = textSize[0][0]
            if (new_width <= width):
                return scale/10
        return 1

    # from: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):

        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation = inter)
    
    def senseSelectAct(self):
        img = space[self.nameImage]
        if img is None:
            return
        frame = img.copy()
        if frame.shape[1] > self.frame_width:
            frame = self.image_resize(frame, width=self.frame_width)
        faces = space[self.nameFace]
        for i, (start_x, start_y, end_x, end_y) in enumerate(faces):
            face_img = frame[start_y: end_y, start_x: end_x]
            blob = cv2.dnn.blobFromImage(
                image=face_img, scalefactor=1.0, size=(227, 227), 
                mean=self.MODEL_MEAN_VALUES, swapRB=False
            )

            self.ageNet.setInput(blob)
            age_preds = self.ageNet.forward()
            i = age_preds[0].argmax()
            age = self.AGE_INTERVALS[i]
            age_confidence_score = age_preds[0][i]

            label = f"Age:{age} - {age_confidence_score*100:.2f}%"

            space(validity=1)[self.nameAge] = age


    
