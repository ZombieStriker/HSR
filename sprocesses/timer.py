from sprocesses.subprocess import ASubprocess 
import time

class TimerSubprocess(ASubprocess):

    timelast = -1


    def __init__(self):
        self.name = "Timer"

    # Returns whether the object should be removed from the subprocesses
    def tick(self,databall) -> bool:
        if type(self.params[0]) is str:
            self.params[0]=int(self.params[0])

        delta = 1
        if(timelast == -1):
            timelast = time.time()

        delta = time.time()-timelast

        if self.params[0] <= delta:
            if(len(self.params)>1):
                databall.speak(self.params[1])
            else:
                databall.speak("done")

        return self.params[0]<=delta

