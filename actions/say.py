from actions.actions import AAction

class SpeakAction(AAction):
    def __init__(self,):
        super().__init__("Say")


    def action(self,databall, currentContext, memory, tts, speak):
        if "output" in databall:
              speak(databall["output"],tts)