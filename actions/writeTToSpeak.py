from actions.actions import AAction

class WriteTAction(AAction):
    def __init__(self,):
        super().__init__("WriteT")


    def action(self,databall, currentContext,actiondataball):
        """writes the text directly to \"output\""""
        if self.params[0] in actiondataball.memory:
            if "output" in databall:
                    databall["output"] = databall["output"]+" "+actiondataball.memory[self.params[0]]["name"]
            else:
                    databall["output"] = actiondataball.memory[self.params[0]]["name"]
        else:
            if "output" in databall:
                    databall["output"] = databall["output"]+" "+self.params[0]
            else:
                    databall["output"] = self.params[0]