from agentspace import Agent, space
import openai
import api_key


class RoleAgent(Agent):

    def __init__(self,nameResearch,nameFaceEmotion,nameAge,nameDialog,nameInput,nameActivity):
        self.Research = nameResearch
        self.Emotion = nameFaceEmotion
        self.Age = nameAge
        self.Dialog = nameDialog
        self.Input = nameInput
        self.Activity = nameActivity
        super().__init__()
        
    def init(self):
        print()
        openai.api_key = (api_key.API_KEY)
        print('ready to answer')
        space.attach_trigger(self.Input,self)

    def senseSelectAct(self):
        activity = space[self.Activity]
        emotion = space[self.Emotion]
        age = space[self.Age]
        dialog = space[self.Dialog]
        Input = space[self.Input]

        promptShop = f"""You are a robot salesman in shop with electronics. Your job is to decide wich product customer (user) should buy. You can recomended all basic products of electronics shops. Your answer will be always product type and nothing else. If you cant decide answer will be Undefined. Make a decision based on these parameters:
            The user is in the range of {age} years old.
            The user current emotion is {emotion}.
            User mentioned activity {activity}.
            Recent dialogue: {dialog}.
            """

        messagesShop = [ {"role": "system", "content":  promptShop} ] 
        messagesShop.append({"role": "user", "content": Input})


        promptGuide = f"""You are a robot town guide. Your job is to decide wich activity or place should user visit. Your answer will always be only recomended place or activity and nothing else. Make a decision based on these parameters:
            The user is in the range of {age} years old.
            The user current emotion is {emotion}.
            User mentioned activity {activity}.
            Recent dialogue: {dialog}.
            You can recomend more than one activity or place, but yout answer will always be only names of places or activities andn othing else. If you cant recomended place or activity based on user prompt, answer will be Undefined. 
            If user has not expressed interest in seeding a place, your answer will be "Undefined".
            """

        messagesGuide = [ {"role": "system", "content":  promptGuide} ] 
        messagesGuide.append({"role": "user", "content": Input})
            

        if messagesGuide is not None:
            chat = openai.ChatCompletion.create( 
            model="gpt-4", messages=messagesGuide 
            )
            answer = chat.choices[0].message.content 
            space(validity=5.0)[self.Research] = answer
           #speak(answer)