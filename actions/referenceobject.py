from actions.actions import AAction
class ReferenceObjectAction(AAction):
    def __init__(self,):
        super().__init__("RefObj")

    def action(self,databall, currentContext, memory, tts, speak):

        var_gross = 0

        try:
            if "var_"+self.p1 in databall:
                var_gross = databall["var_"+self.p1]
        except:
            print("Failed to find "+self.p1)


        stringname = currentContext[var_gross].text
        stringtemp = ""
        for i in range(0,len(stringname)):
            stringtemp=stringtemp.join(stringname[i])
            if i < len(stringname)-1:
                stringtemp=stringtemp.join("_")
        if stringtemp in memory:
            databall["memory1"]= memory[stringtemp]
        else:
            databall["memory1"] = memory["NULL"]