from actions.actions import AAction
from contextcontainers.wordcontextcontainer import WordContextContainer

class CompareEqualsAction(AAction):
    def __init__(self,):
        super().__init__("Equals")


    def action(self,databall, currentContext,actiondataball):
        print("Equals Called")
        if "memory1" in databall:
            if self.params[0].startswith("&"):
                self.params[0] = self.params[0][1:]
                var_gross = -1
                try:
                    if "var_"+self.params[0] in databall:
                         var_gross = databall["var_"+self.params[0]]
                except:
                     print("Failed to find "+self.params[0])
                                
                lenth = 1
                if "varlen_"+self.params[0] in databall:
                    lenth = int(databall["varlen_"+self.params[0]])
                j = 0
                stringtemp = ""
                while j < lenth:
                    if var_gross>=0:
                        stringname = currentContext[var_gross+j].text
                        stringtemp = ""
                        j+=1
                        for i in range(0,len(stringname)):
                            stringtemp=stringtemp.join(stringname[i])
                            if i < len(stringname)-1:
                                 stringtemp=stringtemp.join("_")
                    
                print("=="+stringtemp)
                print("xx"+str(databall["memory1"]))
                

                cc = WordContextContainer([stringtemp])
                cc.process(actiondataball.dictionary,actiondataball.memory)


                if("number" in databall["memory1"] and hasattr(cc,"number")):
                    if(databall["memory1"]["number"] == cc.number):
                        databall["memory1"] = actiondataball.memory["TRUE"]
                    else:
                        databall["memory1"] = actiondataball.memory["FALSE"]
            else:
                if(databall["memory1"] == int(self.params[0])):
                    databall["memory1"] = actiondataball.memory["TRUE"]
                else:
                    databall["memory1"] = actiondataball.memory["FALSE"]
        else:
            print("Databall does not contain memory1")