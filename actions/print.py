from actions.actions import AAction

class PrintAction(AAction):
    def __init__(self,):
        super().__init__("Print")


    def action(self,databall, currentContext,actiondataball):
        if "memory1" in databall:
              print(databall["memory1"])