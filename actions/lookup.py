from actions.actions import AAction

class LookUpAction(AAction):
    def __init__(self,):
        super().__init__("LookUp")


    def action(self,databall, currentContext, actiondataball):
        if "memory1" in databall and self.params[0] in databall["memory1"]:
            databall["memory1"] = databall["memory1"][self.params[0]]
        else:
            databall["memory1"] = actiondataball.memory["NULL"]