from sprocesses.subprocess import ASubprocess 
import time

class CountdownSubprocess(ASubprocess):

    def __init__(self):
        self.name = "Countdown"

    # Returns whether the object should be removed from the subprocesses
    def tick(self,databall) -> bool:
        if type(self.params[0]) is str:
            self.params[0]=int(self.params[0])

        if self.params[0] > 0:
            self.params[0] = self.params[0]-1

        databall.speak(self.params[0])

        return self.params[0]<=0

