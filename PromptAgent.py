from agentspace import Agent, space


class PromptAgent(Agent):
     def __init__(self, nameFaceEmotion,nameAge,nameDialog,namePrompt,nameUserName,nameInput,nameActivity,nameResShop):
        self.nameFaceEmotion = nameFaceEmotion
        self.nameAge = nameAge
        self.nameDialog = nameDialog
        self.namePromp = namePrompt
        self.nameUserName = nameUserName
        self.Input = nameInput
        self.Activity = nameActivity
        self.ResShop = nameResShop
        super().__init__()

     def init(self):
        print('ready to create prompt')
        space.attach_trigger(self.ResShop,self)
        space.attach_trigger(self.Activity,self)

     def senseSelectAct(self):
        Input = space[self.Input]
        emotion = space[self.nameFaceEmotion]
        age = space[self.nameAge]
        dialog = space[self.nameDialog]
        userName = space[self.nameUserName]
        activity = space[self.Activity]
        resShop = space[self.ResShop]
        if Input is not None:
            if activity is None:
                return
            if emotion is None:
                emotion = "undefined"
            if age is None:
                age = "undefined"
            if dialog is None:
                dialog = "[No dialog yet]"
            if userName is None:
                userName = "undefinded"
            if resShop is None:
                return
        

            prompt = f"""You are a humanoid robot iCub. You have robot body, but for now, you cannot control him. Your job  is to maintaining a conversation with the user, taking into account the current circumstances.
            If it is not necessary, do not mention the user's mood, and in no case mention the user's age unless the user asks you. However, adapt the response to consider the user's age and mood.
            Do not exceed the maximum response length of 400 characters unless necessary. 
            You can end the response without a question.
            If you know users name and it's begin of conversation, use users name to greet him.
            Here is the current content:
            The user name is {userName}.
            The user is in the range of {age} years old.
            The user current emotion is {emotion}.
            User mentioned activity {activity}
            Recent dialogue: {dialog}.
            Activity or place that could be recomended in answer: {resShop}.
            """

            messages = [ {"role": "system", "content":  prompt} ] 
            messages.append({"role": "user", "content": Input})


            print(f"""User age: range {age}.
User emotion: {emotion}.
Dialog: {dialog}.
Activity or place that could be recomended in answer: {resShop}
""")
             
            space(validity=1.0)[self.namePromp] = messages