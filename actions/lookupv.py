from actions.actions import AAction

class LookUpVAction(AAction):
    def __init__(self,):
        super().__init__("LookUpV")


    def action(self,databall, currentContext, memory, tts, speak):
        var_gross = 0

        if "var_"+self.p1 in databall:
            var_gross = databall["var_"+self.p1]

        stringname = currentContext[var_gross].text
        stringtemp = ""
        for i in range(0,len(stringname)):
            stringtemp=stringtemp.join(stringname[i])
            if i < len(stringname)-1:
                stringtemp=stringtemp.join("_")

        if "memory1" in databall and stringtemp in databall["memory1"]:
            databall["memory1"] = databall["memory1"][stringtemp]
        else:
            databall["memory1"] = memory["NULL"]