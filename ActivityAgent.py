from agentspace import Agent, space
import openai


class ActivityAgent(Agent):

    def __init__(self,nameActivity,nameInput):
        self.Activity = nameActivity
        self.Input = nameInput
        super().__init__()
        
    def init(self):
        openai.api_key = ('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')
        print('ready to answer')
        space.attach_trigger(self.Input,self)

    def senseSelectAct(self):
        Input = space[self.Input]

        prompt = "Your job is to recognize command to do some activity from user input. If there is no activity command, answer Undefined."

        messages = [ {"role": "system", "content":  prompt} ] 
        messages.append({"role": "user", "content": Input})
        if Input is not None:
            chat = openai.ChatCompletion.create( 
            model="gpt-4", messages=messages 
            )
            answer = chat.choices[0].message.content
            space(validity=5.0)[self.Activity] = answer

           
