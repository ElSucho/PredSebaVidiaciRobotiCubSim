from agentspace import Agent, space
import openai
from speak import speak

class AnswerAgent(Agent):

    def __init__(self, namePrompt,nameAnswer):
        self.namePrompt = namePrompt
        self.nameAnswer = nameAnswer
        super().__init__()
        
    def init(self):
        openai.api_key = ('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')
        space.attach_trigger(self.namePrompt,self)
 
    def senseSelectAct(self):
        prompt = space[self.namePrompt]

        if prompt is not None:
           chat = openai.ChatCompletion.create( 
            model="gpt-4", messages=prompt 
            )
           answer = chat.choices[0].message.content 
           space(validity=10.0)[self.nameAnswer] = answer
           speak(answer)
           print()
           
