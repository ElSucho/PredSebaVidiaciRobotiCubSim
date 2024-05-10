from agentspace import Agent, space
import numpy as np
import cv2 as cv


class HumanDetectionAgent(Agent):

    def __init__(self, nameImage, nameFeatures, nameImageDet):
        self.nameImage = nameImage
        self.nameFeatures = nameFeatures
        self.nameImageDet = nameImageDet
        super().__init__()

    def init(self):
        self.net = cv.dnn.readNet("./Yolo/yolov3.weights", "./Yolo/yolov3.cfg")
        space.attach_trigger(self.nameImage,self)

    def senseSelectAct(self):
        image = space[self.nameImage]
        if image is None:
            return
        (height, width) = image.shape[:2]

        blob = cv.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        output_layer_name = self.net.getUnconnectedOutLayersNames()
        output_layers = self.net.forward(output_layer_name)

        people = []

        for output in output_layers:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if class_id == 0 and confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    people.append((x, y, w, h, center_x, center_y, width, height))
        space(validity=0.5)[self.nameFeatures] = people
        for (x, y, w, h, cX, cY, width, height) in people:
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        space(validity=0.1)[self.nameImageDet] = image
        
            