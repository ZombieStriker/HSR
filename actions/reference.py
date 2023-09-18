from actions.actions import AAction
class ReferenceAction(AAction):
    def __init__(self,):
        super().__init__("Ref")

    def action(self,databall, currentContext, memory, tts, speak):
        if self.p1 in memory:
            databall["memory1"]= memory[self.p1]
        else:
            databall["memory1"] = memory["NULL"]