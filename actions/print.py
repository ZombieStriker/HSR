from actions.actions import AAction

class PrintAction(AAction):
    def __init__(self,):
        super().__init__("Print")


    def action(self,databall, currentContext,actiondataball):
        """Simply prints the object in \"memory1\". Used for debugging"""
        if "memory1" in databall:
              print(databall["memory1"])