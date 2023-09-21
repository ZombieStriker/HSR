from actions.actions import AAction

class WriteVAction(AAction):
    def __init__(self,):
        super().__init__("WriteV")


    def action(self,databall, currentContext,actiondataball):
        var_gross = -1

        try:
            if "var_"+self.params[0] in databall:
                var_gross = databall["var_"+self.params[0]]
        except:
            print("Failed to find "+self.params[0])




        if var_gross>=0:
            lenth = 1
            if "varlen_"+self.params[0] in databall:
                lenth = int(databall["varlen_"+self.params[0]])
            else:
                print("varlen for "+self.params[0]+" was not found")
            j = 0
            while j < lenth:
                stringname = currentContext[var_gross+j].text
                stringtemp = ""
                j=j+1
                for i in range(0,len(stringname)):
                    stringtemp=stringtemp.join(stringname[i])
                    if i < len(stringname)-1:
                        stringtemp=stringtemp.join("_")
                if stringtemp in actiondataball.memory:
                    if "output" in databall:
                        databall["output"] = databall["output"]+" "+(actiondataball.memory[stringtemp])["name"]
                    else:
                        databall["output"] = actiondataball.memory[stringtemp]["name"]
                else:
                    if "output" in databall:
                        databall["output"] = databall["output"]+" "+(stringtemp)
                    else:
                        databall["output"] = stringtemp
        else:
            print("Cannot find "+str(var_gross)+" (var_"+self.params[0]+")")