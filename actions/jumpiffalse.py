from actions.actions import AAction

class JIFAction(AAction):
    def __init__(self,):
        super().__init__("Jif")


    def action(self,databall, currentContext,actiondataball):
        """If the space at \"memory1\" is equal to false, jump the specified amount of lines."""
        if "memory1" in databall:
            print("JUMP CHECK IF TRUE OR FALSE:  "+str(databall["memory1"]["name"]))
            if(databall["memory1"]["name"] == "FALSE" or databall["memory1"]["name"] == "false"):
                databall["actionindex"]=databall["actionindex"]+int(self.params[0])
                print("Jumping "+str(databall["actionindex"]))