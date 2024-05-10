from agentspace import Agent, space
import speech_recognition as sr

class TranscriptionAgent(Agent):

    def __init__(self, nameAudio, nameInput):
        self.nameAudio = nameAudio
        self.nameImput = nameInput
        super().__init__()
        
    def init(self):
        self.recognizer = sr.Recognizer()
        print('ready to transcript')
        space.attach_trigger(self.nameAudio,self)
 
    def senseSelectAct(self):
        audio_data = space[self.nameAudio]
        if audio_data is not None:
            print('transcripting...')
            try:
                result = self.recognizer.recognize_google(audio_data)
                space(validity=10.0)[self.nameImput] = result
            except sr.UnknownValueError:
                print("Rozpoznávanie nebolo úspešné.")
            except sr.RequestError as e:
                print("Chyba pri komunikácii s Google API: {0}".format(e))
