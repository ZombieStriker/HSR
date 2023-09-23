from actions.actions import AAction

class SpeakAction(AAction):
    def __init__(self,):
        super().__init__("Say")


    def action(self,databall, currentContext,actiondataball):
        """Says the message set in \"output\""""
        if "output" in databall:
              actiondataball.speak(databall["output"])
        else:
             print("No output for speaking :(")