from actions.actions import AAction
class ReferenceObjectAction(AAction):
    def __init__(self,):
        super().__init__("RefObj")

    def action(self,databall, currentContext, actiondataball):
        """Loads an object into \"memory1\""""

        var_gross = 0

        try:
            if "var_"+self.params[0] in databall:
                var_gross = databall["var_"+self.params[0]]
        except:
            print("Failed to find "+self.params[0])


        stringname = currentContext[var_gross].text
        stringtemp = ""
        for i in range(0,len(stringname)):
            stringtemp=stringtemp.join(stringname[i])
            if i < len(stringname)-1:
                stringtemp=stringtemp.join("_")
        if stringtemp in actiondataball.memory:
            databall["memory1"]= actiondataball.memory[stringtemp]
        else:
            databall["memory1"] = actiondataball.memory["NULL"]