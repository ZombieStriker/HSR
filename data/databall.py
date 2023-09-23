class DataBall:
    def __init__(self, memory, subprocesses, tts, speakmethod, ACTIONS, SUBPROCESSES, parsemethod, wordprocessingmethod, stack=None, dictionary=None):
        self.memory = memory
        self.subprocesses = subprocesses
        self.SUBPROCESSES = SUBPROCESSES
        self.tts = tts
        self.speakmethod = speakmethod
        self.ACTIONS = ACTIONS
        self.parsemethod = parsemethod
        self.stack = stack
        self.actionindex = 0
        self.wordprocessingmethod = wordprocessingmethod
        self.dictionary = dictionary

    def speak(self,message):
        self.speakmethod(message,self.tts)