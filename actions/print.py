from actions.actions import AAction

class PrintAction(AAction):
    def __init__(self,):
        super().__init__("Print")


    def action(self,databall, currentContext, memory, tts, speak):
        if "memory1" in databall:
              print(databall["memory1"])
        else:
            databall["memory1"] = memory["NULL"]