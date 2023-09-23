from actions.actions import AAction
class ReferenceAction(AAction):
    def __init__(self,):
        super().__init__("Ref")

    def action(self,databall, currentContext, actiondataball):
        """Loads directly an object into \"memory1\""""
        if self.p1 in actiondataball.memory:
            databall["memory1"]= actiondataball.memory[self.params[0]]
        else:
            databall["memory1"] = actiondataball.memory["NULL"]