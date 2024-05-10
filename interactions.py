from agentspace import space, Agent
import time
import os
import signal
from pyicubsim import iCubApplicationName
from CameraAgent import CameraAgent
from ViewerAgent import ViewerAgent
from HumanDetectionAgent import HumanDetectionAgent
from FollowHumanAgent import FollowHumanAgent
from EmotionAgent import EmotionAgent
from AgeAgent import AgeAgent
from ListenerAgent import ListenerAgent
from TranscriptionAgent import TranscriptionAgent
from PromptAgent import PromptAgent
from AnswerAgent import AnswerAgent
from DialogAgent import DialogAgent
from FaceMarksDetectorAgent import FaceMarksDetectorAgent
from CompareAgent import CompareAgent
from InputAgent import InputAgent
from ActivityAgent import ActivityAgent
from NameAgent import NameAgent
from RoleAgent import RoleAgent
from LipsAgent import LipsAgent

def quit():
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()

signal.signal(signal.SIGINT, signal_handler)

iCubApplicationName('/followHuman')
CameraAgent(0,'camera')
InputAgent('input')
HumanDetectionAgent('camera','features','image')
ViewerAgent('image')
ListenerAgent('audio')
FollowHumanAgent('features')
FaceMarksDetectorAgent('image','face','faceLandmarks','landmarks','userName','saveUser','dialog')
EmotionAgent('image','faceEmotion','face')
AgeAgent('face','image','age')
TranscriptionAgent('audio','input')
PromptAgent('faceEmotion','age','dialog','prompt','userName','input','activity','resShop')
AnswerAgent('prompt','answer')
ActivityAgent('activity','input')
NameAgent('userName','input','saveUser','wave')
RoleAgent('resShop','faceEmotion','age','dialog','input','activity')
DialogAgent('answer','dialog','input','userName')
CompareAgent('landmarks','userName','dialog')
LipsAgent('speaking')


