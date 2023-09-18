from actions.actions import AAction

class LookUpAction(AAction):
    def __init__(self,):
        super().__init__("LookUp")


    def action(self,databall, currentContext, memory, tts, speak):
        if "memory1" in databall and self.p1 in databall["memory1"]:
            databall["memory1"] = databall["memory1"][self.p1]
        else:
            databall["memory1"] = memory["NULL"]