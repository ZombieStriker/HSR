from actions.actions import AAction

class GotoAction(AAction):
    def __init__(self,):
        super().__init__("Goto")


    def action(self,databall, currentContext,actiondataball):
        """Simply sets the index that the stack of actions is set to"""
        databall["actionindex"]=int(self.params[0])