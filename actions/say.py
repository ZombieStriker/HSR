from actions.actions import AAction

class SpeakAction(AAction):
    def __init__(self,):
        super().__init__("Say")


    def action(self,databall, currentContext,actiondataball):
        if "output" in databall:
              actiondataball.speak(databall["output"])
        else:
             print("No output for speaking :(")