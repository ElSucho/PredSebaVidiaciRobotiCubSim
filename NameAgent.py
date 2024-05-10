from agentspace import Agent, space
import openai
from pyicubsim import iCubHead, iCubTorso, iCubRightArm, iCubLeftArm, iCubRightLeg, iCubLeftLeg
import time
import api_key


class NameAgent(Agent):

    def __init__(self,nameUserName,nameInput,nameUserSaved,nameWave):
        self.userName = nameUserName
        self.input = nameInput
        self.userSaved = nameUserSaved
        self.Wave = nameWave
        super().__init__()
        
    def init(self):
        openai.api_key = (api_key.API_KEY)
        print('ready to answer')
        self.head = iCubHead()
        self.right_arm = iCubRightArm()
        self.left_arm = iCubLeftArm()
        self.left_leg = iCubRightLeg()
        self.left_leg = iCubLeftLeg()

        space.attach_trigger(self.input,self)

    def senseSelectAct(self):
        Input = space[self.input]

        prompt = "Your job is to recognize if prompt include introduction of user. If user introduce himself answer will be his name, if not answer will be None."

        messages = [ {"role": "system", "content":  prompt} ] 
        messages.append({"role": "user", "content": Input})
        if Input is not None:
            chat = openai.ChatCompletion.create( 
            model="gpt-4", messages=messages 
            )
            answer = chat.choices[0].message.content 
            if answer == "None":
                return
            self.wave()
            space(validity=10.0)[self.userName] = answer
            space(validity=2.0)[self.userSaved] = True



    def wave(self):

        start = 90
        for i in range(3):
            while start > 30:
                self.right_arm.set((-80,80,0,start,0,0,0,59,20,20,20,10,10,10,10,10))
                time.sleep(0.2)
                start -= 20

            while start < 90:
                self.right_arm.set((-80,80,0,start,0,0,0,59,20,20,20,10,10,10,10,10))
                time.sleep(0.2)
                start += 20

        self.head.set((0,0,0,0,0,0))
        self.right_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))
        self.left_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))
        self.left_leg.set((0,0,0,0,0,0))
        self.left_leg.set((0,0,0,0,0,0))
            
