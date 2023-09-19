from actions.actions import AAction

class WriteVAction(AAction):
    def __init__(self,):
        super().__init__("WriteV")


    def action(self,databall, currentContext, memory, tts, speak):
        var_gross = -1

        try:
            if "var_"+self.p1 in databall:
                var_gross = databall["var_"+self.p1]
        except:
            print("Failed to find "+self.p1)




        if var_gross>=0:
            lenth = 1
            if "varlen_"+self.p1 in databall:
                lenth = int(databall["varlen_"+self.p1])
            j = 0
            while j < lenth:
                stringname = currentContext[var_gross+j].text
                stringtemp = ""
                j=j+1
                for i in range(0,len(stringname)):
                    stringtemp=stringtemp.join(stringname[i])
                    if i < len(stringname)-1:
                        stringtemp=stringtemp.join("_")
                if stringtemp in memory:
                    if "output" in databall:
                        databall["output"] = databall["output"]+" "+(memory[stringtemp])["name"]
                    else:
                        databall["output"] = memory[stringtemp]["name"]