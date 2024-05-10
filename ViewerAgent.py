from agentspace import Agent, space
import cv2 as cv
import time

class ViewerAgent(Agent):

    def __init__(self, nameImageDet):
        self.nameImageDet = nameImageDet
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameImageDet,self)
            
    def senseSelectAct(self):
        image = space[self.nameImageDet]
        if image is None:
            return

        cv.imshow("camera",image)
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite(str(time.time())+'.png',image)