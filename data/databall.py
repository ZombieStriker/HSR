class DataBall:
    def __init__(self, memory, subprocesses, tts, speakmethod, ACTIONS, SUBPROCESSES):
        self.memory = memory
        self.subprocesses = subprocesses
        self.SUBPROCESSES = SUBPROCESSES
        self.tts = tts
        self.speakmethod = speakmethod
        self.ACTIONS = ACTIONS

    def speak(self,message):
        self.speakmethod(message,self.tts)