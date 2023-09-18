from actions.actions import AAction

class WriteTAction(AAction):
    def __init__(self,):
        super().__init__("WriteT")


    def action(self,databall, currentContext, memory, tts, speak):
        if self.p1 in memory:
            if "output" in databall:
                databall["output"] = databall["output"]+" "+memory[self.p1]["name"]
            else:
              databall["output"] =memory[self.p1]["name"]