# import the necessary packages
import numpy as np
import cv2 as cv 
from agentspace import Agent, space

class EmotionAgent(Agent):

    def __init__(self,nameImage,nameFaceEmotion,nameFace):
        self.nameImage = nameImage
        self.nameFaceEmotion = nameFaceEmotion
        self.nameFace = nameFace
        super().__init__()

    def init(self): 
        print("faceDetector: loading model")
        face_architecture = 'models/face/deploy.prototxt'
        face_weights = 'models/face/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv.dnn.readNetFromCaffe(face_architecture,face_weights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        print("faceDetector: model loaded")

        print("emotionDetector: loading model")
        model_path = 'models/emotions/affectnet_emotions/'
        self.net2 = cv.dnn.readNet(model_path+'mobilenet_7.pbtxt',model_path+'mobilenet_7.pb')
        print("emotionDetector: model loaded")
        self.labels = None
        labelsFile = model_path + "labels.txt"
        with open(labelsFile, 'rt') as f:
            self.labels = f.read().rstrip('\n').split('\n')

        space.attach_trigger(self.nameImage, self)

    def senseSelectAct(self):
        image = space[self.nameImage]
        if image is None:
            return

        height = 300
        width = 300
        mean = (104.0, 177.0, 123.0)
        threshold = 0.5
        h, w = image.shape[:2] 

        rgb = cv.cvtColor(image,cv.COLOR_BGR2RGB)

        blob = cv.dnn.blobFromImage(cv.resize(image,(width,height)),1.0,(width,height),mean)

        self.net.setInput(blob)
        detections = self.net.forward()

        rects = []
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype(np.int)
                if startX < 0:
                    startX = 0
                if startY < 0:
                    startY = 0
                if endX > w:
                    endX = w
                if endY > h:
                    endY = h
                if (startY+1 < endY) and (startX+1 < endX):
                    rects.append((startX, startY, endX, endY, confidence))
                    face = np.copy(image[startY:endY,startX:endX,:])
                    faces.append(face)
        
        result = np.copy(image)

        if len(rects) > 0:
            
            best = np.argmin([rect[4] for rect in rects])

            startX, startY, endX, endY, confidence = rects[best]
            cv.rectangle(result, (startX, startY), (endX, endY), (0, 0, 255), 2)
            text = "{:.2f}%".format(confidence * 100)
            cv.putText(result, text, (startX, startY-5), 0, 1.0, (0, 0, 255), 2)
            
            blob = cv.dnn.blobFromImage(faces[best], 1.0, (224, 224), (123.68, 116.779, 103.939), True, False)
            self.net2.setInput(blob)
            scores = self.net2.forward()[0]
            emotion = np.argmax(scores) 

            label = self.labels[emotion]

            cv.putText(result, label, (10,50), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv.LINE_AA)
            space(validity=1)[self.nameFace] = [(startX, startY, endX, endY)]
            space(validity=1)[self.nameFaceEmotion] = label



