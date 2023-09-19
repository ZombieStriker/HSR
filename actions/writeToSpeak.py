from actions.actions import AAction

class WriteAction(AAction):
    def __init__(self,):
        super().__init__("Write")


    def action(self,databall, currentContext, actiondataball):
        if "memory1" in databall:
            if "output" in databall:
                databall["output"] = databall["output"]+" "+(databall["memory1"])
            else:
                databall["output"] = (databall["memory1"])