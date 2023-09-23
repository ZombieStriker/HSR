from actions.actions import AAction

class LookUpVAction(AAction):
    def __init__(self,):
        super().__init__("LookUpV")


    def action(self,databall, currentContext, actiondataball):
        """Looks up a relative attribute of the object in \"memory1\". May be merged with LookUp in the future"""
        var_gross = 0

        if "var_"+self.params[0] in databall:
            var_gross = databall["var_"+self.params[0]]

        stringname = currentContext[var_gross].text
        stringtemp = ""
        for i in range(0,len(stringname)):
            stringtemp=stringtemp.join(stringname[i])
            if i < len(stringname)-1:
                stringtemp=stringtemp.join("_")

        if "memory1" in databall and stringtemp in databall["memory1"]:
            databall["memory1"] = databall["memory1"][stringtemp]
        else:
            databall["memory1"] = actiondataball.memory["NULL"]